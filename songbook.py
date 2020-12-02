# noinspection PyUnresolvedReferences
from chord import Chord
# noinspection PyUnresolvedReferences
from verse import Verse
# noinspection PyUnresolvedReferences
from stanza import Stanza
# noinspection PyUnresolvedReferences
from song import Song

from song import parse_song
from os.path import exists
from os import makedirs
from misc import nicify_path
from re import sub
import collect_chords
import grip


SONGBOOK_FILE_ENDING = ".sgbk"
TEX_TEMPLATE = "latexStuff/songbook_template.txt"
TEX_TEMPLATE_SONGS_PLACEHOLDER = "SONGS_PLACEHOLDER"
TEX_TEMPLATE_SONGBOOK_TITLE_PLACEHOLDER = "TITLE_PLACEHOLDER"
TEX_TEMPLATE_CHORDS_PLACEHOLDER = "CHORDS_PLACEHOLDER"
TEX_TEMPLATE_SONGBOOK_AUTHOR_PLACEHOLDER = "AUTHOR_PLACEHOLDER"


class SongBook:
    def __init__(self, file_name):
        self.place_on_disk = file_name
        self.songs = []
        if not file_name.endswith(SONGBOOK_FILE_ENDING):
            raise Exception("Songbook file must end with {}".format(SONGBOOK_FILE_ENDING))
        message = "{} the songbook file {}".format("Reading" if exists(file_name) else "Creating", file_name)
        print(message)
        if exists(file_name):
            with open(file_name, encoding="utf-8") as f:
                for line in f:
                    self.songs.append(eval(line.strip()))
        else:
            nicer_name = nicify_path(file_name)
            if "/" in nicer_name:
                file_folder = nicer_name[:nicer_name.rfind("/")]
                if not exists(file_folder):
                    makedirs(file_folder)
            with open(nicer_name, "w", encoding="utf-8"):
                pass

    def __eq__(self, other):
        same_file = self.place_on_disk == other.place_on_disk
        same_number_of_songs = len(self.songs) == len(other.songs)
        same_songs = all([s1 == s2 for s1, s2 in zip(self.songs, other.songs)])
        return same_file and same_number_of_songs and same_songs

    def sort_songs(self):
        self.songs.sort(key=lambda song: (song.artist.upper(), song.title.upper()))

    def add_songs(self, new_songs):
        self.songs += new_songs

    def clear_songs(self):
        self.songs = []

    def set_songs(self, songs):
        self.songs = songs

    def write_to_file(self):
        self.sort_songs()
        with open(self.place_on_disk, "w", encoding="utf-8") as f:
            for song in self.songs:
                print(repr(song), file=f)

    def latex_string(self):
        with open(TEX_TEMPLATE) as content_file:
            content = content_file.read()
        # add songs
        songs = [sng.latex_string() for sng in self.songs]
        content = sub(TEX_TEMPLATE_SONGS_PLACEHOLDER, sub("\\\\", "\\\\\\\\", "\n\n".join(songs)), content)
        # add chords
        gripss = []
        used_chords = sorted(self.chords())
        should_filter = False
        for chrd in used_chords:
            gripss.append(collect_chords.get_finger_positions(chrd))
            if len(gripss[-1]) != len(set(gripss[-1])):
                print("You should filter the grip library. Duplicates of grips ...")
                should_filter = True
        if should_filter:
            collect_chords.filter_grip_library()
        collect_chords.save_grip_library()
        grips_tex = [grip.Grips(grips).latex_string() for grips in gripss]
        content = sub(TEX_TEMPLATE_CHORDS_PLACEHOLDER, sub("\\\\", "\\\\\\\\", "\n\n".join(grips_tex)), content)
        return content

    def write_to_tex_file(self, tex_file):
        if not tex_file.endswith(".tex"):
            print("Appending .tex to the file name", tex_file)
            tex_file += ".tex"
        with open(tex_file, "w", encoding="utf-8") as f:
            print(self.latex_string(), file=f)

    def chords(self):
        """
        Returns the set of chords that are in the book.
        :return:
        """
        return {chrd[0] for sng in self.songs for stz in sng.stanzas for vrs in stz.verses for chrd in vrs.chords}


def create_songbook_from_text_files(text_files, songbook_file):
    """
    Reads the contents of the text files which are appropriate song.parse_song input arguments.
    Creates a new SongBook object and saves the songs to the file songbook_file.
    :param text_files: the name of the input file with the songs
    :param songbook_file: the name of the output file
    :return:
    """
    should_proceed = True
    if exists(songbook_file):
        print("The songbook file {} already exists.".format(songbook_file))
        should_proceed = input("Do you want to overwrite it? (yes/no) ") == "yes"
    if should_proceed:
        songs = []
        for text_file in text_files:
            songs.append(parse_song(text_file))

        book = SongBook(songbook_file)
        book.clear_songs()
        book.set_songs(songs)
        book.write_to_file()
        return book
    else:
        print("Exiting ...")
        return None


if __name__ == "__main__":
    sgbk = create_songbook_from_text_files(["songs/ljudska.kuza_pazi.txt", "songs/siddharta.platina.txt"], "tempo.sgbk")
    tex_f = "songs/songbooks/test1/tempo.tex"
    sgbk.write_to_tex_file(tex_f)
