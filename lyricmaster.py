# Created on 27/6/2011 by Craig McL <mistercouk@gmail.com>

import random

class LyricMaster(object):
    # Class variable
    ARTISTS = {"S CLUB 7" : "SClub7.txt"}
    def __init__(self, *args, **kwargs):
        """Takes a dictionary as an argument.

        Dictionary has keys of artists and values of the file lyrics
        are to be found.

        Files should have a standard structure for each song:
        [Number of songs in file]
        >>Name of Song
        ... lyrics....

        Followed by an empty line and zero or more songs.
        """
        if kwargs:
            self.artists = kwargs
        else:
            self.artists = LyricMaster.ARTISTS

    def has_artist(self, artist):
        if self.artists.get(artist, None):
            return True
        else:
            return False

    def get_artist_iter(self, artist):
        if not self.artists.get(artist, None):
            return None

        songs = []
        # Open file
        with open("SClub7.txt", "r") as f:
            line = f.readline()
            num = int(line[1])
            while num > 0:
                title = ""
                lyrics = []
                line = f.readline().strip()
                while line != "":
                    if line.startswith(">>"):
                        title = line[2:]
                    else:
                        lyrics.append(line)
                    line = f.readline().strip()
                songs.append((title, lyrics))
                num = num - 1

        # Create lyric generator
        def next_song(bot, data):
            song = random.randint(0, len(songs) - 1)
            songTitle = songs[song][0]
            lyrics = songs[song][1]
            bot.send("\"{}\" by {}:".format(songTitle, artist), data["to"])
            for line in lyrics:
                bot.send("{}".format(line), data["to"])

        return next_song
                            
