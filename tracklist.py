class Tracklist:
    def __init__(self, data):
        self.data = data

    # t is a Track
    # tries to add t to self.data (dictionary <Track.name><deque of Tracks with that name>
    # returns True if Track was added, False if Track already exists
    def add(self, t):
        # if there already is a song with t's name
        if t.name in self.data:
            # if this song exists
            if t in self.data.at(t.name):
                return False
            else:
                self.data.at(t.name).append(t)
                return True
        else:
            self.data.at(t.name).append(t)
            return True
