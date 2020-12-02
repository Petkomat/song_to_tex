from html.parser import HTMLParser
import grip
import re
import urllib.request
import urllib.error
# noinspection PyUnresolvedReferences
from chord import Chord, ALLOWED_TONES, get_tone_index
from time import sleep
from random import random


GRIP_LIBRARY_FILE = "grips.txt"  # contains dictionary {repr(chord): [repr(grip1), ... }

MINOR = ("m",)
SEVEN = ("7",)
MINOR_SEVEN = ("m", "7")
MAJ_SEVEN = ("M7",)
POWER = ("5",)
SIX = ("6",)
SUS2 = ("sus2",)
SUS4 = ("sus4",)

ALLOWED_FRACTIONS = {2, 4, 7, 10, 11}  # e.g., C/D is ok, but not C/C# ...
ALLOWED_DECORATIONS = {MINOR: "m",
                       SEVEN: "7",
                       MINOR_SEVEN: "m7",
                       MAJ_SEVEN: "maj7",
                       POWER: "5",
                       SIX: "6",
                       SUS2: "sus2",
                       SUS4: "sus4"}
for allowed_tone in ALLOWED_TONES:
    ALLOWED_DECORATIONS["/{}".format(allowed_tone)] = "_{}-bass".format(ALLOWED_TONES[allowed_tone][1])


def load_grip_library():
    with open(GRIP_LIBRARY_FILE) as f:
        return eval(f.readline())


GRIP_LIBRARY = load_grip_library()


def save_grip_library():
    with open(GRIP_LIBRARY_FILE, "w") as f:
        print(repr(GRIP_LIBRARY), file=f)


def filter_grip_library():
    new_lib = {}
    global GRIP_LIBRARY
    for key, grips in GRIP_LIBRARY.items():
        updated = []
        for g in grips:
            if g not in updated:
                updated.append(g)
        new_lib[key] = updated
    GRIP_LIBRARY = new_lib


class ChordHTMLParser(HTMLParser):
    """
    Finds and parses parts of the html
    <div class="greybox g2" ...>
        <table class="piano_table">
            <tr> ... </tr>
            ...
            <tr> ... </tr>
        </table>
    </div>
    There seems to be exactly 6 <tr> parts. They consist of
     8 (first), 7 (second) and 6 (third to sixth) <td> ... </td> parts:
    - first:
        - 1: useless
        - 8: useless
        - 2-7: contain <img> tag; x, o or blank figure: src is either "closed2(b).gif",
                "open2(b).gif" or "blank2(b).gif", and the names are "top1", "top2", ... , "top6"
    - second:
        - 1: may contain the fret number, e.g., <td ...>Fret: 4</td>
        - 2-7: fingers' positions description
    - third to fifth:
        - 1-6: fingers' positions description
    - sixth:
        - 1-6: tones which the strings give: either <td>-</td> (when string is closed) or, e. g. D or Db or D#.

    The fingers' description lines are given as follows:
        <img vstring="x", src="y">, where 1 <= x <= 6 and y is either suare.gif or suare2_2f<finger number>.gif.
    """

    # {tag name:  [level, (property1, value1), (property2, value2), ...], ... }
    HTML_TREE = {"div": [0, ("class", "greybox g2")], "table": [1, ("class", "piano_table")], "tr": [2], "td": [3]}
    MAX_LEVEL = max([y[0] for y in HTML_TREE.values()])

    def __init__(self, chord):
        super().__init__()
        self.grips = []
        self.current_grip = [[]]
        self.grip_start = None
        self.grip_end = None
        self.tree_level = -1
        self.text = None
        self.chord = chord

    def getpos(self):
        line, offset = super().getpos()
        return [line - 1, offset]

    def feed(self, data):
        self.text = data.split("\n")
        super().feed(data)

    def handle_starttag(self, tag, attrs):
        if tag in ChordHTMLParser.HTML_TREE and ChordHTMLParser.HTML_TREE[tag][0] == self.tree_level + 1:
            is_ok = True
            properties = ChordHTMLParser.HTML_TREE[tag][1:]
            for tag_property in properties:
                has_property = False
                for attr in attrs:
                    if attr == tag_property:
                        has_property = True
                        break
                if not has_property:
                    is_ok = False
                    break
            if is_ok:
                self.tree_level += 1
                if self.tree_level == ChordHTMLParser.MAX_LEVEL:
                    self.grip_start = self.getpos()

    def handle_endtag(self, tag):
        if tag in ChordHTMLParser.HTML_TREE and ChordHTMLParser.HTML_TREE[tag][0] == self.tree_level:
            if self.tree_level == ChordHTMLParser.MAX_LEVEL:
                self.grip_end = self.getpos()
                self.grip_end[1] += len(tag) + 2
                self.current_grip[-1].append(self.joined_text())
            elif self.tree_level == ChordHTMLParser.MAX_LEVEL - 1:
                self.current_grip.append([])
            elif self.tree_level == ChordHTMLParser.MAX_LEVEL - 2:
                self.current_grip = self.current_grip[:-1]  # remove the empty element
                self.parse_chord()
                self.current_grip = [[]]
            self.tree_level -= 1

    def joined_text(self):
        answer = self.text[self.grip_start[0]:self.grip_end[0] + 1]
        answer[0] = answer[0][self.grip_start[1]:]
        answer[-1] = answer[-1][:self.grip_end[1]]
        return "".join(answer)

    def parse_chord(self):
        """
        Parses the current grip table into a Grip object.
        :return:
        """
        def get_img_tag(description):
            return re.search('<img(.+?)>', description).group(1).strip()

        def get_open_closed_pressed_strings(description):
            allowed_types = {"closed2.gif": grip.Grip.CLOSED_STRING,
                             "closed2b.gif": grip.Grip.CLOSED_STRING,
                             "open2.gif": grip.Grip.OPEN_STRING,
                             "open2b.gif": grip.Grip.OPEN_STRING,
                             "blank2.gif": grip.Grip.PRESSED_STRING,
                             "blank2b.gif": grip.Grip.PRESSED_STRING}
            for string in range(6):
                img_tag = get_img_tag(description[string])
                name_pattern = 'name=top{}'.format(string + 1)
                string_name = re.search(name_pattern, img_tag)
                assert string_name is not None
                type_pattern = 'src=([^ ]+)?'
                string_type = re.search(type_pattern, img_tag).group(1)
                open_closed_pressed[string + 1] = allowed_types[string_type]

        def get_fingers(description):
            """
            Six element list of <td><img ... src="<our interest:)>"  ... ></td> strings.
            :param description:
            :return: {string number: finger number, ...} dictionary
            """
            answer = {}
            for string in range(6):
                # print("    ", string + 1)
                img_tag = get_img_tag(description[string])
                # sanity check
                string_pattern = 'vstring="({})"'.format(string + 1)
                string_found = re.search(string_pattern, img_tag)
                if string_found is None:
                    return False, None
                else:
                    string_found = int(string_found.group(1))
                    assert string_found == string + 1
                    # fingers
                    blank_pattern = 'src=suare.gif'
                    if re.search(blank_pattern, img_tag) is None:
                        finger_pattern = 'suare2_2f([1-4]).gif'
                        answer[string + 1] = int(re.search(finger_pattern, img_tag).group(1))
            return True, answer

        is_ok = True
        open_closed_pressed = {string: None for string in range(1, 7)}
        positions_dict = {}
        assert len(self.current_grip) == 6
        # first row: opened, closed and pressed strings
        get_open_closed_pressed_strings(self.current_grip[0][1:-1])
        # 1st row: maybe fret number
        fret = re.search('<td .+>Fret: ([0-9]+)</td>', self.current_grip[1][0])
        fret = 1 if fret is None else int(fret.group(1))
        self.current_grip[1] = self.current_grip[1][1:]
        # 2nd-5th row: fingers positions
        for relative_fret in range(4):
            # print("  ", relative_fret)
            success, positions = get_fingers(self.current_grip[1 + relative_fret])
            if success:
                positions_dict[1 + relative_fret] = positions
            else:
                is_ok = False
                break
        # 6th row: tones: we do not care for them:)
        if is_ok:
            self.grips.append(grip.Grip(fret, open_closed_pressed, positions_dict, self.chord))
        else:
            print("This grip description is not valid.")


def transform_decoration(my_chord):
    decoration = sorted(my_chord.decoration)
    if len(decoration) == 0:
        return True, ""
    elif len(decoration) == 1 and decoration[0].startswith("/"):
        tone_index = get_tone_index(my_chord.tone)
        bass_index = get_tone_index(decoration[0][1:])
        difference = (bass_index - tone_index) % 12
        return difference in ALLOWED_FRACTIONS, ALLOWED_DECORATIONS[decoration[0]]
    else:
        for allowed_decoration in ALLOWED_DECORATIONS:
            if sorted(allowed_decoration) == decoration:
                return True, ALLOWED_DECORATIONS[allowed_decoration]
    return False, None


def chord_url(my_chord):
    tone_str = ALLOWED_TONES[my_chord.tone][1]
    is_ok, decoration_str = transform_decoration(my_chord)
    if is_ok:
        return "https://www.8notes.com/guitar_chord_chart/{0}{1}.asp".format(tone_str, decoration_str)
    else:
        print("Probably, the chord {} cannot be found on the internet:)".format(my_chord))
        return None


def load_test_html():
    a = []
    with open("html_am.txt") as f:
        for x in f:
            a.append(x)
    return "".join(a)


def get_finger_positions(my_chord, debug=False):
    if repr(my_chord) not in GRIP_LIBRARY:
        print("Obtaing grips from the chord {}".format(my_chord))
        url = chord_url(my_chord)
        if url is not None:
            print("    from url", url)
            my_parser = ChordHTMLParser(my_chord)
            if not debug:
                try:
                    html_description = urllib.request.urlopen(url).read().decode("utf8")
                    a = int(15 + 20 * random())
                    print("Sleeping for", a, "seconds")
                    sleep(a)
                    my_parser.feed(html_description)
                    GRIP_LIBRARY[repr(my_chord)] = my_parser.grips
                except urllib.error.HTTPError:
                    print("Wrong url for {}?".format(my_chord), url)
                    return None
                except:
                    print("Something went wrong")
                    return None
            else:
                html_description = load_test_html()
                my_parser.feed(html_description)
                return None
        else:
            return None
    return GRIP_LIBRARY[repr(my_chord)]


