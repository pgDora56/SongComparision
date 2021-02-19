import csv
import Levenshtein
# import sqlite3


class SongData:
    def __init__(self, lis):
        if lis[1] == "" or lis[2] == "":
            raise ValueError(f"Invalid data: Not found title or artist: {lis}")
        self.program = lis[0]
        self.title = lis[1]
        self.artist = lis[2]
        self.lyricist = lis[3]
        self.composer = lis[4]
        self.arranger = lis[5]
        self.genre = lis[6]
        try:
            self.year = int(lis[7])
        except ValueError:
            self.year = None

    def __str__(self):
        return f"{self.program} {self.title} {self.artist}"


def compare(data1, data2):
    PRG_GRAVITY = 10
    TITLE_GRAVITY = 100
    ARTIST_GRAVITY = 10
    LYRICIST_GRAVITY = 1
    COMPOSER_GRAVITY = 1
    ARRANGER_GRAVITY = 1
    GENRE_GRAVITY = 0.1
    YEAR_GRAVITY = 1

    if data1.program == "" or data2.program == "":
        PRG_GRAVITY = 0
    if data1.lyricist == "" or data2.lyricist == "":
        LYRICIST_GRAVITY = 0
    if data1.composer == "" or data2.composer == "":
        COMPOSER_GRAVITY = 0
    if data1.arranger == "" or data2.arranger == "":
        ARRANGER_GRAVITY = 0

    prgDistance = Levenshtein.ratio(data1.program, data2.program)
    titleDistance = Levenshtein.ratio(data1.title, data2.title)
    artistDistance = Levenshtein.ratio(data1.artist, data2.artist)
    lyricistDistance = Levenshtein.ratio(data1.lyricist, data2.lyricist)
    composerDistance = Levenshtein.ratio(data1.composer, data2.composer)
    arrangerDistance = Levenshtein.ratio(data1.arranger, data2.arranger)

    genreDistance = Levenshtein.distance(data1.genre, data2.genre)
    if data1.year is None or data2.year is None:
        YEAR_GRAVITY = 0
        yearDistance = 0
    else:
        yearDistance = abs(data1.year - data2.year)

    return (
        prgDistance * PRG_GRAVITY +
        titleDistance * TITLE_GRAVITY +
        artistDistance * ARTIST_GRAVITY +
        lyricistDistance * LYRICIST_GRAVITY +
        composerDistance * COMPOSER_GRAVITY +
        arrangerDistance * ARRANGER_GRAVITY +
        genreDistance * GENRE_GRAVITY +
        yearDistance * YEAR_GRAVITY
    ) / (
        PRG_GRAVITY +
        TITLE_GRAVITY +
        ARTIST_GRAVITY +
        LYRICIST_GRAVITY +
        COMPOSER_GRAVITY +
        ARRANGER_GRAVITY +
        GENRE_GRAVITY +
        YEAR_GRAVITY
    )


filename = input("Filename > ")

stacked = []
compares = []

with open(filename) as f:
    reader = csv.reader(f)
    for line in reader:
        tmp = SongData(line)
        for x in stacked:
            distance = compare(tmp, x)
            compares.append((distance, str(tmp), str(x)))
        stacked.append(tmp)
compares.sort(key=lambda x: x[0])
