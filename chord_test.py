import unittest
import chord


class ChordTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equal_no_decorations(self):
        for tone in chord.ALLOWED_TONES:
            self.assertEqual(chord.Chord(tone), chord.Chord(tone))

    def test_equal_one_decorations(self):
        for tone in chord.ALLOWED_TONES:
            for decoration in chord.DECORATIONS:
                self.assertEqual(chord.Chord(tone, [decoration]), chord.Chord(tone, [decoration]))

    def test_equal_more_decorations(self):
        chord_1 = chord.Chord("A", decoration=[chord.DECORATIONS[i] for i in [0, 2, 5]])
        chord_2 = chord.Chord("A", decoration=[chord.DECORATIONS[i] for i in [2, 0, 5]])
        self.assertEqual(chord_1, chord_2)

    def test_not_equal_no_decorations(self):
        for tone_1 in chord.ALLOWED_TONES:
            for tone_2 in chord.ALLOWED_TONES:
                if tone_1 != tone_2:
                    self.assertNotEqual(chord.Chord(tone_1), chord.Chord(tone_2))

    def test_not_equal_decorations(self):
        for tone_1 in chord.ALLOWED_TONES:
            for tone_2 in chord.ALLOWED_TONES:
                for decoration_1 in [None, ["m", "7", "5"], ["5", "M7", "/A"]]:
                    for decoration_2 in [None, ["5", "M7", "/A"], ["7", "5", "m"]]:
                        if tone_1 != tone_2:
                            self.assertNotEqual(chord.Chord(tone_1, decoration_1), chord.Chord(tone_2, decoration_2))

    def test_transpose(self):
        chord_1 = chord.Chord("C")
        pluses = [0, 2, 3, 11, 12, 17]
        chord_1_plus_0 = chord.Chord("C")
        chord_1_plus_2 = chord.Chord("D")
        chord_1_plus_3 = chord.Chord("D#")
        chord_1_plus_11 = chord.Chord("H")
        chord_1_plus_12 = chord.Chord("C")
        chord_1_plus_17 = chord.Chord("F")
        transposed = [chord_1_plus_0, chord_1_plus_2, chord_1_plus_3, chord_1_plus_11, chord_1_plus_12, chord_1_plus_17]
        for i, half_tones in enumerate(pluses):
            self.assertEqual(chord_1.transpose(half_tones), transposed[i])

        chord_2 = chord.Chord("E")
        minuses = [0, -1, -12, -13]
        chord_2_minus_0 = chord.Chord("E")
        chord_2_minus_1 = chord.Chord("D#")
        chord_2_minus_12 = chord.Chord("E")
        chord_2_minus_13 = chord.Chord("D#")
        transposed = [chord_2_minus_0, chord_2_minus_1, chord_2_minus_12, chord_2_minus_13]
        for i, half_tones in enumerate(minuses):
            self.assertEqual(chord_2.transpose(half_tones), transposed[i])

    def test_parse_str(self):
        strings = ["C-M7", "D#-sus2-sus4", "E-sus4", "d-7", "f#", "G"]
        chords = [chord.Chord("C", ["M7"]),
                  chord.Chord("D#", ["sus2", "sus4"]),
                  chord.Chord("E", ["sus4"]),
                  chord.Chord("D", ["m", "7"]),
                  chord.Chord("F#", ["m"]),
                  chord.Chord("G")]

        for chord_string, chord_object in zip(strings, chords):
            self.assertEqual(chord.parse(chord_string), chord_object)
            self.assertEqual(chord_string, str(chord_object))

    def test_latex_string(self):
        chords = [chord.Chord("A"),
                  chord.Chord("D", ["m"]),
                  chord.Chord("F#"),
                  chord.Chord("G#", ["m"]),
                  chord.Chord("A#", ["sus2"]),
                  chord.Chord("D#", ["m", "sus2"]),
                  chord.Chord("D#", ["7", "sus2"])]
        answers = ["\\[A]",
                   "\\[d]",
                   "\\[F#]",
                   "\\[g#]",
                   "\\[A#$^\\text{ sus2}$]",
                   "\\[d#$^\\text{ sus2}$]",
                   "\\[D#$^\\text{ 7-sus2}$]"]
        for ans, elt in zip(answers, chords):
            self.assertEqual(ans, elt.latex_string())


if __name__ == "__main__":
    unittest.main()
