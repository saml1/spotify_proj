import json
import argparse
import spotify
import sqlitedb
import tracksearch
import os

# todo: add more options, for now just create config file
# todo: add try/catch blocks for possible errors
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help="Currently the only modes are "
                                     "create_config (or cc) and "
                                     "add_playlist (or ap) and "
                                     "add_directory (or ad) and"
                                     "get_dupes (or gd)")
    parser.add_argument('-s1', '--spotify_client_id',
                        help='enter Spotify client ID (relevant for create_config mode)')
    parser.add_argument('-s2', '--spotify_client_secret',
                        help='enter Spotify client secret (relevant for create_config mode)')
    parser.add_argument('-a', '--acoustid',
                        help='enter Actoustid api key (relevant for create_config mode)')
    parser.add_argument('-d', '--discogs',
                        help='enter discogs token (relevant for create_config mode)')
    parser.add_argument('-db', '--database_file', help="enter filepath of database (relevant for add_playlist and get_dupes mode)")
    parser.add_argument('-cf', '--config_filepath', help="enter where config file should be saved")
    parser.add_argument('-pid', '--playlist_id', help='enter playlist id to add to db (relevant for add_playlist mode)')
    parser.add_argument('-pn', '--playlist_name', help='enter playlist name (relevant for add_playlist mode)')
    parser.add_argument('-dir', '--directory',
                        help='enter directory to add mp3 files from (relevant for add_directory)')
    parser.add_argument('-dbn', '--database_name', help='enter database name for local files')
    parser.add_argument('-d1', '--database_1', help='enter name of first database (relevant for get_dupes)')
    parser.add_argument('-d2', '--database_2', help='enter name of second database (relevant for get_dupes)')
    args = parser.parse_args()
    if args.mode == 'create_config' or args.mode == 'cc':
        args = parser.parse_args()
        create_config(args.spotify_client_id, args.spotify_client_secret, args.acoustid,
                      args.discogs)
    elif args.mode == 'add_playlist' or args.mode == 'ap':
        spotify.get_playlist_db(args.playlist_id, args.playlist_name)
        print("added to database: " + args.playlist_name)
    elif args.mode == 'add_directory' or args.mode == 'ad':
        tp = tracksearch.get_local_db_correct_metadata(args.directory, args.database_name)
        if tp:
            print("Added db " + args.database_name + " in " + args.directory)
        else:
            print("Unable to add " + args.database_name + " to " + args.directory)
    elif args.mode == 'get_dupes' or args.mode == 'gd':
        sqlitedb.get_dupes(args.database_1, args.database_2)


# creates file config.json with clientId and Path
def create_config(spotify_client_id, spotify_client_secret, acoustid_api_key, discogs_token):
    config = {'spotify': {'client_id': spotify_client_id, 'client_secret': spotify_client_secret},
              'acoustid': {'api_key': acoustid_api_key},
              'discogs': {'token': discogs_token}}
    # json_file_path = 'config.json'
    with open(os.getcwd() + '/config.json', 'w') as jsonFile:
        jsonFile.write(json.dumps(config, indent=4))
    print("created config.json")


if __name__ == "__main__":
    main()
