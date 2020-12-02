from verse import parse_verse
import stanza


LJUDSKA = "ljudska"
NEZNANI_AVTOR = "neznano"


class Song:
    def __init__(self, artist, title, stanzas):
        self.artist = artist  # comma separated string of values (for Latex purposes)
        self.title = title
        self.stanzas = stanzas

    def __repr__(self):
        return "Song('{}', '{}', {})".format(self.artist, self.title, self.stanzas)

    def __str__(self):
        lines = [self.title]
        for stnza in self.stanzas:
            lines.append("")
            lines.append(str(stnza))
        return "\n".join(lines)

    def __eq__(self, other):
        same_artist = self.artist == other.artist
        same_titles = self.title == other.title
        same_lengths = len(self.stanzas) == len(other.stanzas)
        same_stanzas = all([st1 == st2 for st1, st2 in zip(self.stanzas, other.stanzas)])
        return same_artist and same_titles and same_lengths and same_stanzas

    def transpose(self, half_tones):
        return Song(self.artist, self.title, [stnza.transpose(half_tones) for stnza in self.stanzas])

    def difficulty(self):
        """
        Finds the difficulty of the chords in the song.
        :return: Maximal difficulty of chords in the song.
        """
        max_difficulty = -float("inf")
        for stnza in self.stanzas:
            for verse in stnza.verses:
                for chord in verse.chords:
                    max_difficulty = max(max_difficulty, chord.difficulty)
        return max_difficulty

    def most_user_friendly_version(self):
        """
        Finds the number of half-tones for which the song should be transposed
        for its chords to be as simple as possible. If there is more than one option,
        the version that is the nearest to the original wins. If still, there are two
        options, the positive wins.
        :return:
        """
        optimal_score = float("inf")
        optimal_version = None
        for halftones in range(7):  # +- 6 option is computed twice, no biggie
            for direction in [1, -1]:
                transposed = self.transpose(direction * halftones)
                score = transposed.difficulty()
                if score < optimal_score:
                    optimal_score = score
                    optimal_version = transposed
        return optimal_version

    def latex_string(self):
        header = "\\beginsong{{{}}}[by={{{}}}]".format(self.title, self.artist)
        footer = "\\endsong"
        parts = [header] + [stnz.latex_string() for stnz in self.stanzas] + [footer]
        return "\n\n".join(parts)


def create_text_song(song_file, artist, title, list_of_text_stanzas):
    """
    Writes a song to a text file. This is the inverse of parse_song.
    :param song_file: destination file
    :param artist:
    :param title:
    :param list_of_text_stanzas: [stanza1, ...], where stanza1 = [verse1, ...], where verse1
    must follow the syntax used in the verse.parse_verse method.
    :return:
    """
    with open(song_file, "w", encoding="utf-8") as f:
        print(artist, file=f)
        print(title, file=f)
        for text_stanza in list_of_text_stanzas:
            for text_verse in text_stanza:
                print(text_verse, file=f)
            print("", file=f)


def parse_song(text_file):
    """
    Reads the contents of the text file with the songs which are given in the following form.
    <artist>
    <title of the song>
    <first stanza, first verse>
    ...
    <first stanza, last verse>
    <empty line>
    <second stanza, first verse>
    ...
    ...
    <last stanza, last verse>

    Each verse must follow the syntax used in the verse.parse_verse method. The last verse of the last stanza
    can be followed by an empty line.
    :param text_file: the name of the input file with the songs
    :return: the corresponding Song object
    """
    stanzas = []
    with open(text_file, encoding="utf-8") as f:
        artist = f.readline().strip()
        title = f.readline().strip()
        current_stanza = []
        for line in f:
            stripped = line.strip()
            if stripped:
                current_stanza.append(parse_verse(stripped))
            else:
                stanzas.append(stanza.Stanza(current_stanza[::]))
                current_stanza = []
        if current_stanza:
            stanzas.append(stanza.Stanza(current_stanza[::]))
    return Song(artist, title, stanzas)
