import collections

import requests

import track

CLIENT_ID = '421291cdff10468d98da0d3fe8424204'
CLIENT_SECRET = '44cb2d1956cc4020a06351fb498188bb'

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
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


def user_playlist_tracks_full(spotify_connection, user, playlist_id=None, fields=None, market=None):
    """ Get full details of the tracks of a playlist owned by a user.
        https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/

        Parameters:
            - user - the id of the user
            - playlist_id - the id of the playlist
            - fields - which fields to return
            - market - an ISO 3166-1 alpha-2 country code.
    """

    # first run through also retrieves total no of songs in library
    response = spotify_connection.user_playlist_tracks(user, playlist_id, fields=fields, limit=100, market=market)
    results = response['items']

    # subsequently runs until it hits the user-defined limit or has read all songs in the library
    while len(results) < response['total']:
        response = spotify_connection.user_playlist_tracks(
            user, playlist_id, fields=fields, limit=100, offset=len(results), market=market
        )
        results.extend(response['items'])
    return results


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


# given playlist_id, makes deck of Tracks
# Tracklist will call this
def get_playlist(playlist_id):
    response = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', headers=headers, params=get_params(None))
    response = response.json()
    # allTracks = user_playlist_tracks_full(r.json(), CLIENT_ID, playlist_id)
    results = response['items']
    # headers1 =
    while len(results) < response["total"]:
        response = requests.get(BASE_URL + 'playlists/' + playlist_id + '/tracks', headers=headers,
                                params=get_params(len(results)))
        # response = response.json()
        # print(str(len(allTracks)))
        # print(get_params(str(len(results))))
        # print(results[0]['track']['name'])
        # response = response.json()['items']
        results.extend(response.json()['items'])
        response = response.json()
    playlistD = collections.deque([])
    a = 0
    for t in results:
        # todo: have it contain all artists maybe
        # print(a)
        a += 1
        if t['track'] is None:
            # print("hi")
            continue
        playlistD.append(
            track.Track(t['track']['name'], t['track']['album']['name'], t['track']['artists'][0]['name'],
                        t['track']['duration_ms']))
        # print(t['track']['name'])
    return playlistD


def get_playlistAll(playlist_id):
    r = requests.get(BASE_URL + 'playlists/' + playlist_id, headers=headers)
    # results = user_playlist_tracks_full(requests, CLIENT_ID, playlist_id)
    r = r.json()
    playlistD = collections.deque([])
    for t in r['tracks']['items']:
        # todo: have it contain all artists maybe
        playlistD.append(
            track.Track(t['track']['name'], t['track']['album']['name'], t['track']['artists'][0]['name'],
                        t['track']['duration_ms']))
        # print(t['track']['name'])
    return playlistD
