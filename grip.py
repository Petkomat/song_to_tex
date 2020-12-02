class Grip:
    OPEN_STRING = "o"
    CLOSED_STRING = "x"
    PRESSED_STRING = ""

    def __init__(self, fret, open_closed_pressed, positions_dict, chord):
        """
        Constructor for description how to play a chord.
        :param fret: the "base" fret or how to call this, a number
        :param open_closed_pressed: {1: type, ..., 6: type}, where type is one of the OPEN_STRING, CLOSED_STRING or
        PRESSED_STRING.
        :param positions_dict: {fretNumber: {stringNumber: fingerNumber, ...}, ...},
            - where fretNumber is 1, 2, 3 and 4 (it is relative to the fret)
            - 1 <= stringNumber <= 6 and 1 <= fingerNumber <= 4, and there can be less than 6 key-value pairs
        :param chord: a chord object which the grip belongs to
        :return:
        """
        self.fret = fret
        self.open_closed_pressed = open_closed_pressed
        self.positions = positions_dict
        self.chord = chord

    def __repr__(self):
        return "grip.Grip({}, {}, {}, {})".format(self.fret, self.open_closed_pressed, self.positions, repr(self.chord))

    def __eq__(self, other):
        same_frets = self.fret == other.fret
        same_ocp = self.open_closed_pressed == other.open_closed_pressed
        same_pos = self.positions == other.positions
        return same_frets and same_ocp and same_pos

    def __hash__(self):
        return hash(repr(self))

    def latex_string(self):
        fret_representation = self.fret if self.fret != 1 else ""
        strings_where = [None] * 6
        fingers_where = ["0"] * 6
        for string in range(1, 7):
            if self.open_closed_pressed[string] in [Grip.OPEN_STRING, Grip.CLOSED_STRING]:
                strings_where[string - 1] = self.open_closed_pressed[string].upper()
        for fret_number in self.positions:
            for string_number, finger_number in self.positions[fret_number].items():
                assert strings_where[string_number - 1] is None
                strings_where[string_number - 1] = str(fret_number)
                assert fingers_where[string_number - 1] == "0"
                fingers_where[string_number - 1] = str(finger_number)
        strings_where = "".join(strings_where)
        fingers_where = "".join(fingers_where)
        # chord_representation = self.chord.latex_string()[2:-1]
        return "\\gtab{{}}{{{0}:{1}:{2}}}".format(fret_representation,
                                                  strings_where,
                                                  fingers_where)


class Grips:
    def __init__(self, grips):
        self.grips = []
        for grip in grips:
            if grip not in self.grips:
                self.grips.append(grip)

    def latex_string(self):
        header = ["\\begin{table}",
                  "    \\centering",
                  "    \\begin{{tabular}}{{*{{{0}}}{{r}}}}",
                  "        \\multicolumn{{{0}}}{{c}}{{\\printchordtable{{{1}}}}}  \\\\"]
        body_offset = 8 * " "
        body = []
        footer = ["    \\end{tabular}",
                  "\\end{table}"]
        allowed_per_line = 4
        n = len(self.grips)
        per_line = min(n, allowed_per_line)
        chord_string = self.grips[0].chord.latex_string_grip()

        header[2] = header[2].format(per_line)
        header[3] = header[3].format(per_line, chord_string)

        number_lines = n // allowed_per_line
        if n % allowed_per_line:
            number_lines += 1
        current = 0
        for line in range(number_lines):
            body.append([])
            for column in range(per_line):
                if current < n:
                    body[-1].append("{" + self.grips[current].latex_string() + "}")
                else:
                    body[-1].append(" ")
                current += 1
            body[-1] = body_offset + " & ".join(body[-1])
            if line < number_lines - 1:
                body[-1] += "\\\\"
        return "\n".join([line for lines in [header, body, footer] for line in lines])
