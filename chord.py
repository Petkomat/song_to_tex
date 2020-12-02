import re


TONES2 = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "H"]
ALLOWED_TONES = {"C": (0, "c"),
                 "C#": (1, "cx"), "Db": (1, "db"),
                 "D": (2, "d"),
                 "D#": (3, "dx"), "Eb": (3, "eb"),
                 "E": (4, "e"),
                 "F": (5, "f"),
                 "F#": (6, "fx"), "Gb": (6, "gb"),
                 "G": (7, "g"),
                 "G#": (8, "gx"), "Ab": (8, "ab"),
                 "A": (9, "a"),
                 "A#": (10, "ax"), "Bb": (10, "bb"),
                 "B": (11, "b"), "H": (11, "b")}
NUMBER_HALFTONES = 12


ALTERNATIVES = {"C#": ["Db"], "D#": ["Eb"], "F#": ["Gb"], "G#": ["Ab"], "A#": ["B", "Bb"], "H": ["B"]}
DECORATIONS = ["m", "5", "6", "7", "sus2", "sus4", "M7"] + ["/{}".format(tone) for tone in sorted(ALLOWED_TONES)]
MINOR = DECORATIONS[0]

SIMPLE = 0
BARRE_FROM_E = [1, 2]
BARRE_FROM_A = [3, 4]
DIFFICULTY = {}
for tone in ["C", "D", "E", "G", "A"]:
    DIFFICULTY[tone] = SIMPLE
for tone in ["F", "F#", "G#", "Gb", "Ab"]:
    DIFFICULTY[tone] = BARRE_FROM_E[0]
for tone in ["A#", "H", "C#", "Bb", "B", "Db"]:
    DIFFICULTY[tone] = BARRE_FROM_A[0]
for tone in ["D#", "Eb"]:
    DIFFICULTY[tone] = BARRE_FROM_A[1]

MAIN_DECORATION_SEPARATOR = "-"


def get_tone_index(t):
    return ALLOWED_TONES[t][0]


class Chord:
    def __init__(self, base_tone, decoration=None):
        self.tone = base_tone
        self.decoration = [] if decoration is None else decoration
        self.decoration.sort(key=lambda d: DECORATIONS.index(d))
        self.difficulty = DIFFICULTY[base_tone]

    def __repr__(self):
        return "Chord('{}', {})".format(self.tone, self.decoration)

    def __str__(self):
        main = self.tone
        decor = self.decoration
        if self.decoration and self.decoration[0] == MINOR:
            main = self.tone.lower()
            decor = decor[1:]
        appendix = MAIN_DECORATION_SEPARATOR.join(decor)
        between = MAIN_DECORATION_SEPARATOR if appendix else ""
        return "{}{}{}".format(main, between, appendix)

    def __eq__(self, other):
        return self.tone == other.tone and self.decoration == other.decoration

    def tuple_to_compare(self):
        return tuple([get_tone_index(self.tone)] + [DECORATIONS.index(decor) for decor in self.decoration])

    def __lt__(self, other):
        """
        Lexicographic ordering: first tone, then decorations ...
        :param other:
        :return:
        """
        return self.tuple_to_compare() < other.tuple_to_compare()

    def __hash__(self):
        return hash(repr(self))

    def transpose(self, half_tones):
        i = get_tone_index(self.tone)
        i_transposed = (i + half_tones) % NUMBER_HALFTONES
        candidates = [t for t in ALLOWED_TONES if get_tone_index(t) == i_transposed]
        if len(candidates) == 1:
            pass
        elif i_transposed == get_tone_index("H"):
            candidates = ["H"]
        else:
            contains_b = "b" in self.tone
            candidates = [t for t in candidates if contains_b == ("b" in t)]
            assert len(candidates) == 1
        new_tone = candidates[0]
        return Chord(new_tone, self.decoration)

    def latex_string(self):
        """
        Produces a representation of the chord compatible with the Latex songs package,
        e.g., \\[C#] or \\[C#$^\\text{ sus2}$].
        :return: the described string
        """
        chord_str = str(self)
        i = chord_str.find(MAIN_DECORATION_SEPARATOR)
        if i >= 0:
            main = chord_str[:i]
            decoration = chord_str[i + 1:]
            return "\\[{}$^\\text{{ {}}}$]".format(main, decoration)
        else:
            return "\\[{}]".format(chord_str)

    def latex_string_grip(self):
        ordinary_latex = self.latex_string()[2:-1]
        modified = re.sub("#", "\\\\shrp", ordinary_latex)
        modified = re.sub("&", "\\\\flt", modified)
        return modified


def parse(chord):
    atoms = chord.split(MAIN_DECORATION_SEPARATOR)
    decoration = atoms[1:]
    base_tone = atoms[0]
    if base_tone not in ALLOWED_TONES:
        decoration = ["m"] + decoration
        base_tone = base_tone.upper()
    if len(decoration):
        return Chord(base_tone, decoration)
    else:
        return Chord(base_tone)
