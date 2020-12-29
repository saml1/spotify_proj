import collections

import spotify


class Tracklist:
    def __init__(self):
        self.data = {}

    # t is a Track
    # tries to add t to self.data (dictionary <Track.name><deque of Tracks with that name>
    # returns True if Track was added, False if Track already exists
    def add(self, t):
        # if there already is a song with t's name
        if t.name in self.data:
            # if this song exists
            if t in self.data.get(t.name):
                return False
            else:
                self.data.get(t.name).append(t)
                return True
        else:
            self.data[t.name] = collections.deque([t])
            # self.data.get(t.name).append(t)
            return True

    # returns true if t exists in self.data, false if otherwise
    def contains_track(self, t):
        if t.name in self.data:
            if t in self.data.get(t.name):
                return True
            else:
                return False
        else:
            return False

    # compares this Tracklist to other Tracklist
    # returns Tracklist of all songs in other that aren't in this
    def missing_songs(self, other):
        # e = Tracklist()  # songs that already exist
        dne = Tracklist()  # new songs
        for name in other.data:
            for t in other.data.get(name):
                if t.name == 'Beautiful Disaster':
                    print("bb")
                if not self.contains_track(t):  # if track already exists
                    dne.add(t)
        return dne


def create_from_spotify_playlist(playlist_id):
    tp = Tracklist()
    # deque = collections.deque(spotify.get_playlist(playlist_id))
    deque = spotify.get_playlist(playlist_id)
    for t in deque:
        tp.add(t)
        # print(t.name)
    return tp
