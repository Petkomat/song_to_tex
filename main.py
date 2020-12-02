import songbook
import os
# noinspection PyUnresolvedReferences
from chord import Chord
# noinspection PyUnresolvedReferences
from verse import Verse
# noinspection PyUnresolvedReferences
from stanza import Stanza
# noinspection PyUnresolvedReferences
from song import Song
#
#
directory = "songs/"
input_files = [directory + f for f in os.listdir(directory) if f.startswith("slon_in_sadez")]

the_songbook = "songbooks/theSongbook/the_songbook2.sgbk"
the_songbook_tex = "songbooks/theSongbook/the_songbook2.tex"
book = songbook.create_songbook_from_text_files(input_files, the_songbook)  # songbook.SongBook(the_songbook)  #
# book = songbook.SongBook(the_songbook)
book.write_to_tex_file(the_songbook_tex)
