import json
import os
import acoustid
import discogs_client
import requests
import sqlitedb
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

config = json.load(open('config.json'))
api_key = config['acoustid']['api_key']
lookup_url = 'https://api.acoustid.org/v2/lookup'

usertoken = config['discogs']['token']

# instantiate our discogs_client object.
discogsclient = discogs_client.Client('spotify_proj/0.1', user_token=usertoken)

# returns true if no error occurs, returns false if error occurs
def get_local_db_correct_metadata(directory, db_file, database_name):
    # create a database connection
    conn = sqlitedb.create_connection(db_file)

    database = (0, database_name)

    sql_create_databases_table = """ CREATE TABLE IF NOT EXISTS databases (
                                                    id integer PRIMARY KEY,
                                                    local integer NOT NULL,
                                                    name text NOT NULL
                                                ); """

    sql_create_songs_table = """CREATE TABLE IF NOT EXISTS songs (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                artist text NOT NULL,
                                                album textNOT NULL,
                                                duration integer NOT NULL,
                                                database_id text NOT NULL,
                                                FOREIGN KEY (database_id) REFERENCES databases (id)
                                            );"""

    # create songs and databases tables
    sqlitedb.create_table(conn, sql_create_databases_table)
    sqlitedb.create_table(conn, sql_create_songs_table)

    # create tables
    if conn is not None:
        # create new database
        database_id = sqlitedb.create_db(conn, database)
    else:
        print("Error! cannot create the database connection.")
        return False
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith('.mp3'):
                audio = EasyID3(filepath)
                track = (audio['title'][0], audio['artist'][0], audio['album'][0], int(MP3(filepath).info.length), database_id)
                sqlitedb.create_song(conn, track)
    return True


def get_local_db(directory, db_file, database_name):
    # create a database connection
    conn = sqlitedb.create_connection(db_file)

    database = (0, database_name)

    sql_create_databases_table = """ CREATE TABLE IF NOT EXISTS databases (
                                                id integer PRIMARY KEY,
                                                local integer NOT NULL,
                                                name text NOT NULL
                                            ); """

    sql_create_songs_table = """CREATE TABLE IF NOT EXISTS songs (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            artist text NOT NULL,
                                            album textNOT NULL,
                                            duration integer NOT NULL,
                                            database_id text NOT NULL,
                                            FOREIGN KEY (database_id) REFERENCES databases (id)
                                        );"""

    # create songs and databases tables
    sqlitedb.create_table(conn, sql_create_databases_table)
    sqlitedb.create_table(conn, sql_create_songs_table)

    # create tables
    if conn is not None:
        # create new database
        database_id = sqlitedb.create_db(conn, database)
    else:
        print("Error! cannot create the database connection.")
        return
    keyerror = 0
    indexerror = 0
    total = 0
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith('.mp3'):
                fingerprint = acoustid.fingerprint_file(filepath)
                params = {
                    "client": api_key,
                    "duration": int(MP3(filepath).info.length),
                    "fingerprint": fingerprint[1],
                    "meta": 'recordings'
                }
                response = requests.get(
                    lookup_url,
                    params=params,
                )
                try:
                    title = response.json()['results'][0]['recordings'][0]['title']
                    artist = response.json()['results'][0]['recordings'][0]['artists'][0]['name']
                except KeyError:
                    keyerror += 1
                    if has_correct_metadata(filepath):
                        audio = EasyID3(filepath)
                        track = (audio['title'][0], audio['artist'][0], audio['album'][0], int(MP3(filepath).info.length), database_id)
                        print("added despite keyerror bc correct metadata: " + filepath)
                        total += 1
                        print("total so far: " + str(total))
                        sqlitedb.create_song(conn, track)
                        continue
                    master = valid_master(filepath)
                    if master is not None:
                        print("good master: " + filepath)
                        album_with_durations = get_album_with_durations(master)
                        audio = EasyID3(filepath)
                        title = guess_correct_title(album_with_durations, audio, int(MP3(filepath).info.length))
                        if title is not None:
                            track = (title, audio['artist'][0], audio['album'][0], int(MP3(filepath).info.length), database_id)
                            total += 1
                            print("total so far: " + str(total))
                            sqlitedb.create_song(conn, track)
                            continue
                        else:
                            print("Error: inconsistent track duration: " + filepath)
                            continue
                    print("key error: " + filepath)
                    print(has_correct_metadata(filepath))
                    continue
                except IndexError:
                    indexerror += 1
                    print("index error: " + filepath)
                    print(has_correct_metadata(filepath))
                    continue
                track = (title, artist, artist, int(MP3(filepath).info.length), database_id)
                sqlitedb.create_song(conn, track)
                total += 1
                print("total so far: " + str(total))
    print("keyerror:" + str(keyerror))
    print("indexerror: " + str(indexerror))


# returns true if file has correct album + artist + title
def has_correct_metadata(filepath):
    audio = EasyID3(filepath)

    # search for master using song title, album, artist
    try:
        masters = discogsclient.search(track=audio['title'], title=audio['album'], artist=audio['artist'],
                                       type='master')
        # if this gives an IndexError then the search came up empty
        test = masters[0]

        # Looking through each master's tracklist, trying to find one with a matching title (when found,
        # compare durations)
        for x in range(0, masters.count):
            try:
                track = next(t for t in masters[x].tracklist if t.title == audio['title'][0])
                # sometimes duration is missing, look for version of master with durations (might be wrong)
                if track.duration == "":
                    version_with_durations = next(t for t in masters[x].versions if t.tracklist[0] != '')
                    track = next(t for t in version_with_durations if t.title == audio['title'][0])
                m, s = track.duration.split(':')
                duration = 60 * int(m) + int(s)
                # check if song we found with matching metadata has matching duration (+- 5 seconds)
                if abs(duration - int(MP3(filepath).info.length)) <= 5:  # giving 5 second leeway
                    return True
                else:
                    return False
            except StopIteration:  # sometimes the metadata slightly differs so check all for match
                continue
        return False
    except IndexError:
        return False


# returns None if album/artist are incorrect, else returns master release with correct album/artist
def valid_master(filepath):
    audio = EasyID3(filepath)
    results = discogsclient.search(title=audio['artist'][0], type='artist')
    for artist in results:
        for album in artist.releases:
            if album.title == audio['album'][0]:
                return album
    if "The" in audio['artist'][0]:  # redo search without "the"
        results = discogsclient.search(title=audio['artist'][0].replace('The', ''), type='artist')
        for artist in results:
            for album in artist.releases:
                if album.title == audio['album'][0]:
                    return album
    return None


# returns a version of a given master that contains track durations or None if no version with durations exists
def get_album_with_durations(master):
    for version in master.versions:
        if version.tracklist[0].duration == '':
            continue
        else:
            return version
    return None


# given album release containing song lengths, audio from EasyID3, and local duration
# returns guess for correct song title
def guess_correct_title(album, audio, local_duration):
    # track_number is from the local song and is -1 if local song doesn't contain track number
    try:
        track_number = int(audio['tracknumber'][0].split('/')[0])
    except KeyError:
        track_number = -1
    if track_number != -1:
        m, s = album.tracklist[track_number - 1].duration.split(':')
        duration = 60 * int(m) + int(s)
        if abs(local_duration - duration) <= 5:
            return album.tracklist[track_number - 1].title
        else:
            return None
    # tracks = {}  # empty dict
    #for track in album.tracklist:
     #   tracks[track.position] = track.title
    return track_number
