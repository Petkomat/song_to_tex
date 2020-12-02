import unittest
import chord
import verse


class VerseTest(unittest.TestCase):
    def setUp(self):
        self.description_1 = "<A>J's ne morem več <E>v temi živet"
        self.lyrics_1_true = "J's ne morem več v temi živet"
        self.chords_1_true = [(chord.Chord("A"), 0), (chord.Chord("E"), 17)]
        self.verse_1_true = verse.Verse(self.lyrics_1_true, self.chords_1_true)

        self.description_2 = "0<h>12<C#>34567<d-sus2>8<e>9<f>0123456789<H>"
        self.lyrics_2_true = "0123456789" * 2
        self.chords_2_true = [(chord.Chord("H", ["m"]), 1),
                              (chord.Chord("C#"), 3),
                              (chord.Chord("D", ["m", "sus2"]), 8),
                              (chord.Chord("E", ["m"]), 9),
                              (chord.Chord("F", ["m"]), 10),
                              (chord.Chord("H"), 20)]
        self.verse_2_true = verse.Verse(self.lyrics_2_true, self.chords_2_true)

        self.description_3 = "To besedilo ni pesem, zato akordov nima."
        self.lyrics_3_true = self.description_3
        self.chords_3_true = []
        self.verse_3_true = verse.Verse(self.lyrics_3_true, self.chords_3_true)

        self.description_4 = "<C> <G-7> <C> <G-7>"
        self.lyrics_4_true = "   "
        self.chords_4_true = [(chord.Chord("C"), 0), (chord.Chord("G", ["7"]), 1),
                              (chord.Chord("C"), 2), (chord.Chord("G", ["7"]), 3)]
        self.verse_4_true = verse.Verse(self.lyrics_4_true, self.chords_4_true)

        self.description_5 = "<C-sus2>Som<D-sus2>e chords <D>are <C#-sus2-sus4>just<G-sus4>tood<h>ense " \
                             "to be in the <A-sus4>same lin<E>e, but <C-m-sus4>some <D>words " \
                             "allow <F#-sus4>for <E>additional spaces."
        self.lyrics_5_true = "Some chords are justtoodense to be in the same line," \
                             " but some words allow for additional spaces."
        self.chords_5_true = [(chord.Chord("C", ["sus2"]), 0),
                              (chord.Chord("D", ["sus2"]), 3),
                              (chord.Chord("D"), 12),
                              (chord.Chord("C#", ["sus2", "sus4"]), 16),
                              (chord.Chord("G", ["sus4"]), 20),
                              (chord.Chord("H", ["m"]), 24),
                              (chord.Chord("A", ["sus4"]), 42),
                              (chord.Chord("E"), 50),
                              (chord.Chord("C", ["m", "sus4"]), 57),
                              (chord.Chord("D"), 62),
                              (chord.Chord("F#", ["sus4"]), 74),
                              (chord.Chord("E"), 78)]
        self.verse_5_true = verse.Verse(self.lyrics_5_true, self.chords_5_true)

    def tearDown(self):
        pass

    def test_parse(self):
        verse_1_parsed = verse.parse_verse(self.description_1)
        verse_2_parsed = verse.parse_verse(self.description_2)
        verse_3_parsed = verse.parse_verse(self.description_3)
        verse_4_parsed = verse.parse_verse(self.description_4)
        verse_5_parsed = verse.parse_verse(self.description_5)
        self.assertEqual(self.verse_1_true, verse_1_parsed)
        self.assertEqual(self.verse_2_true, verse_2_parsed)
        self.assertEqual(self.verse_3_true, verse_3_parsed)
        self.assertEqual(self.verse_4_true, verse_4_parsed)
        self.assertEqual(self.verse_5_true, verse_5_parsed)

    def test_str(self):
        verse_1_string_true = "A                E           \n" \
                              "|                |           \n" \
                              "J's ne morem več v temi živet"
        self.assertEqual(verse_1_string_true, str(self.verse_1_true))

        verse_2_string_true = "          f          \n" \
                              "          |          \n" \
                              "         e|          \n" \
                              "         ||          \n" \
                              " h C#   d-sus2      H\n" \
                              " | |    |||         |\n" \
                              "01234567890123456789 "
        self.assertEqual(verse_2_string_true, str(self.verse_2_true))

        verse_3_string_true = self.description_3
        self.assertEqual(verse_3_string_true, str(self.verse_3_true))

        verse_4_string_true = "C G-7 C G-7"
        self.assertEqual(verse_4_string_true, str(self.verse_4_true))

        v = "                        h                                                                             \n" \
            "                        |                                                                             \n" \
            "   D-sus2           G-sus4                                                                            \n" \
            "   |                |   |                                                                             \n" \
            "C-sus2      D   C#-sus2-sus4              A-sus4  E      c-sus4 D           F#-sus4 E                 \n" \
            "|  |        |   |   |   |                 |       |      |      |           |       |                 \n" \
            "Some chords are justtoodense to be in the same line, but some   words allow for     additional spaces."
        verse_5_string_true = v
        self.assertEqual(verse_5_string_true, str(self.verse_5_true))

    def test_transpose(self):
        half_tones = [0, 2, 10, -2]

        chords_1 = [[(chord.Chord("A"), 0), (chord.Chord("E"), 17)],
                    [(chord.Chord("H"), 0), (chord.Chord("F#"), 17)],
                    [(chord.Chord("G"), 0), (chord.Chord("D"), 17)],
                    [(chord.Chord("G"), 0), (chord.Chord("D"), 17)]]
        transposed_true_1 = [verse.Verse(self.lyrics_1_true, chords) for chords in chords_1]
        for halftones, solution in zip(half_tones, transposed_true_1):
            self.assertEqual(solution, self.verse_1_true.transpose(halftones))

        chords_4 = [[(chord.Chord("C"), 0), (chord.Chord("G", ["7"]), 1),
                    (chord.Chord("C"), 2), (chord.Chord("G", ["7"]), 3)],

                    [(chord.Chord("D"), 0), (chord.Chord("A", ["7"]), 1),
                    (chord.Chord("D"), 2), (chord.Chord("A", ["7"]), 3)],

                    [(chord.Chord("A#"), 0), (chord.Chord("F", ["7"]), 1),
                    (chord.Chord("A#"), 2), (chord.Chord("F", ["7"]), 3)],

                    [(chord.Chord("A#"), 0), (chord.Chord("F", ["7"]), 1),
                    (chord.Chord("A#"), 2), (chord.Chord("F", ["7"]), 3)]]
        transposed_true_4 = [verse.Verse(self.lyrics_4_true, chords) for chords in chords_4]
        for halftones, solution in zip(half_tones, transposed_true_4):
            self.assertEqual(solution, self.verse_4_true.transpose(halftones))

    def test_latex_string(self):
        verses = [self.verse_1_true, self.verse_2_true, self.verse_3_true, self.verse_4_true]
        answers = ["\\[A]J's ne morem več \\[E]v temi živet",
                   "0\\[h]12\\[C#]34567\\[d$^\\text{ sus2}$]8\\[e]9\\[f]0123456789\\[H]",
                   "To besedilo ni pesem, zato akordov nima.",
                   "{\\nolyrics \\[C] \\[G$^\\text{ 7}$] \\[C] \\[G$^\\text{ 7}$]}"]
        for ans, vrs in zip(answers, verses):
            self.assertEqual(ans, vrs.latex_string())


if __name__ == "__main__":
    unittest.main()
