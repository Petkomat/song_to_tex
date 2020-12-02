import chord
import re


class Verse:
    def __init__(self, lyrics, chords):
        """
        Constructor for this class.
        :param lyrics: A verse, e.g., Somewhere over the rainbow.
        :param chords: A list of pairs (chord, position), e.g., [(C, 0), (e, 10)] tells that C is played in the
        beginning of Somewhere, and E-minor is played in the beginning of over (until the end).
        :return:
        """
        self.lyrics = lyrics
        self.chords = chords
        self.chords.sort(key=lambda c: c[1])

    def __repr__(self):
        return "Verse('{}', {})".format(re.sub("'", "\\'", self.lyrics), self.chords)

    def __str__(self):
        """
        Produces lines like
                                h
                                |
           D-sus2           G-sus4
           |                |   |
        C-sus2      D   C#-sus2-sus4              A-sus4  E      c-sus4 D           F#-sus4 E
        |  |        |   |   |   |                 |       |      |      |           |       |
        Some chords are justtoodense to be in the same line, but some   words allow for     additional spaces.
        :return:
        """
        if len(self.chords) == 0:
            return self.lyrics
        else:
            chord_positions = []    # (line, index in line)
            last_in_the_lines = {}  # line: index of the last chord in the line
            max_length = len(self.lyrics)
            additional_spaces = [0 for _ in range(len(self.chords))]  # number of spaces before the given chord
            longer_spaces = {}
            for i, (this_chord, this_position) in enumerate(self.chords):
                if i > 0:
                    additional_spaces[i] += additional_spaces[i - 1]
                for line in range(len(last_in_the_lines) + 1):
                    if line not in last_in_the_lines:
                        break
                    else:
                        last_chord, last_position = self.chords[last_in_the_lines[line]]
                        last_end = last_position + len(str(last_chord))
                        if last_end < this_position:
                            break
                        elif line == 0:
                            # try with additional spaces, but ...
                            space_between = self.lyrics.rfind(" ", last_position, this_position)
                            if space_between >= 0:      # ... do not break the words
                                assert space_between not in longer_spaces
                                longer_spaces[space_between] = 1 + last_end - this_position
                                additional_spaces[i] += longer_spaces[space_between]
                                break
                column = this_position + additional_spaces[i]
                chord_positions.append((line, column))
                last_in_the_lines[line] = i
                max_length = max(max_length, column + len(str(this_chord)))

            max_length = max(max_length, len(self.lyrics) + additional_spaces[-1])
            placeholder = " "
            any_lyrics = bool(self.lyrics.strip())
            number_lines = 2 * len(last_in_the_lines) + 1 if any_lyrics else 1
            lines = [[placeholder for _ in range(max_length)] for _ in range(number_lines)]
            for i, (line, column) in enumerate(chord_positions):
                chord_string = str(self.chords[i][0])
                real_line = 2 * (line + 1) if any_lyrics else 0
                for j in range(len(chord_string)):
                    lines[real_line][column + j] = chord_string[j]
                for lower_line in range(1, real_line):
                    if lines[lower_line][column] == placeholder:
                        lines[lower_line][column] = "|"
            if any_lyrics:
                index = 0
                for i in range(len(self.lyrics)):
                    if i in longer_spaces:
                        index += longer_spaces[i]
                    lines[0][index] = self.lyrics[i]
                    index += 1
            return "\n".join(["".join(line) for line in lines[::-1]])

    def __eq__(self, other):
        return self.lyrics == other.lyrics and self.chords == other.chords

    def transpose(self, half_tones):
        return Verse(self.lyrics, [(x[0].transpose(half_tones), x[1]) for x in self.chords])

    def latex_string(self):
        """
        Returns the string, appropriate for songs package. The additional care is taken in the case of
        - single words in brackets, e.g., (chorus) or (2x): these words will be shown in italics.
        - no lyrics in the line, i.e., when there are no lyrics except for the special words from the first case:
        :return:
        """
        parts = []
        chord_ind = 0
        has_some_lyrics = False
        i = 0
        did_something = True
        while did_something:
            did_something = False
            if chord_ind < len(self.chords) and i == self.chords[chord_ind][1]:
                parts.append(self.chords[chord_ind][0].latex_string())
                chord_ind += 1
                did_something = True
            if i < len(self.lyrics):
                if self.lyrics[i] == "(":
                    i_end = self.lyrics[i:].find(")") + i + 1
                    assert i_end >= i
                    substring = self.lyrics[i:i_end]
                    pattern = "\\S{{{0},{0}}}".format(len(substring))
                    if re.match(pattern, substring) is not None:
                        parts.append("\\textit{{{}}}".format(substring))
                    else:
                        parts.append(substring)
                    i = i_end
                else:
                    parts.append(self.lyrics[i])
                    has_some_lyrics = has_some_lyrics or self.lyrics[i].strip()
                    i += 1
                did_something = True
        usual_version = "".join(parts)
        if has_some_lyrics:
            return usual_version
        else:
            return "{{\\nolyrics {}}}".format(usual_version)


def parse_verse(description):
    """
    Parses a description of a verse (lyrics and possibly chords) to a Verse object
    :param description: a line of lyrics together with chords if necessary, e.g.,
    <A>Js ne morem več <E>v temi živet
    or
    <h>hotu vidt bi Sonce, <f#>hotu več svetlobe met
    The chords should be in the form as returned by Chord.__str__ method.
    :return: Verse object
    """
    lyrics = []
    chords = []
    in_chord = False
    index = 0
    chord_string = []
    position = None
    for char in description:
        if char == "<":
            assert not in_chord
            in_chord = True
            position = index
        elif char == ">":
            assert in_chord
            in_chord = False
            chords.append((chord.parse("".join(chord_string)), position))
            chord_string = []
        elif in_chord:
            chord_string.append(char)
        else:
            lyrics.append(char)
            index += 1
    return Verse("".join(lyrics), chords)
