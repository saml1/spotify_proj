import requests
import sqlite3
import sqlitedb
from sqlite3 import Error
import json
import os

# given spotify playlist_id and database file, this populates db_file with songs from playlist_id
def get_playlist_db(playlist_id, playlist_name):
    config = json.load(open('config.json'))

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': config['spotify']['client_id'],
        'client_secret': config['spotify']['client_secret'],
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'

    # create a database connection
    conn = sqlitedb.create_connection(os.getcwd() + '/libraries.db')

    database = (0, playlist_name)

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

    response = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', headers=headers, params=get_params(None))
    response = response.json()
    results = response['items']
    while len(results) < response["total"]:
        response = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', headers=headers,
                                params=get_params(len(results)))
        results.extend(response.json()['items'])
        response = response.json()
    for t in results:
        if t['track'] is None:
            continue
        track = (t['track']['name'], t['track']['artists'][0]['name'], t['track']['album']['name'],
                 round(int(t['track']['duration_ms'])/1000), database_id)
        sqlitedb.create_song(conn, track)


def get_params(results):
    if results is None:
        params = {
            "limit": 100
        }
    else:
        params = {
            "limit": 100,
            "offset": results
        }
    return params
