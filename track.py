class Track:
    def __init__(self, name, album, artist, length):
        self.name = name
        self.album = album
        self.artist = artist
        # length is in milliseconds
        self.length = length
        # self.year = year - removed this bc data isn't in spotify track object and it doesnt matter
