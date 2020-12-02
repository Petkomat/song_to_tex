import unittest
import song
import stanza
import verse
import misc


class SongTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = [["<C>Kuža pazi, <G>z repkom miga, <C>vstane, <G>leže, <C>tačko da.",
                         "<C>Hišo čuva, <G>jezno laja, <C>če ni<G>kogar <C>ni doma."],
                        ["<C>Ko pa Jurček <G>cicibanček <C>truden <G>se od<C>pravi spat,",
                         "<C>kuža naš <G>pred vrata leže, <C>da ne <G>vzame <C>Jurčka tat."]]
        cls.transposed = [["<A#>Kuža pazi, <F>z repkom miga, <A#>vstane, <F>leže, <A#>tačko da.",
                           "<A#>Hišo čuva, <F>jezno laja, <A#>če ni<F>kogar <A#>ni doma."],
                          ["<A#>Ko pa Jurček <F>cicibanček <A#>truden <F>se od<A#>pravi spat,",
                           "<A#>kuža naš <F>pred vrata leže, <A#>da ne <F>vzame <A#>Jurčka tat."]]
        cls.verses_orig = [[verse.parse_verse(vrs) for vrs in sta] for sta in cls.original]
        cls.stanzas_orig = [stanza.Stanza(stnza) for stnza in cls.verses_orig]
        cls.title_orig = "Kuža pazi"
        cls.song_orig = song.Song(song.LJUDSKA, cls.title_orig, cls.stanzas_orig)

        cls.songs_folder = misc.create_temp_folder(".")
        cls.song_file1 = cls.songs_folder + "/song1.txt"
        song.create_text_song(cls.song_file1, song.LJUDSKA, cls.title_orig, cls.original)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        misc.remove_temp_folder(cls.songs_folder)

    def test_equality(self):
        stolen = song.Song("Janez Kradljivec", "Kuža pazi", self.stanzas_orig)
        wrongly_titled = song.Song(song.LJUDSKA, "Kuza pazi", self.stanzas_orig)
        first_stanza = song.Song(song.LJUDSKA, "Kuža pazi", self.stanzas_orig[:1])
        same = song.Song(song.LJUDSKA, "Kuža pazi", self.stanzas_orig)

        self.assertNotEqual(stolen, self.song_orig)
        self.assertNotEqual(wrongly_titled, self.song_orig)
        self.assertNotEqual(first_stanza, self.song_orig)
        self.assertEqual(same, self.song_orig)

    def test_transpose(self):
        verses_tran = [[verse.parse_verse(vrs) for vrs in sta] for sta in self.transposed]
        stanzas_tran = [stanza.Stanza(stnza) for stnza in verses_tran]
        song_tran = song.Song(song.LJUDSKA, "Kuža pazi", stanzas_tran)

        self.assertEqual(self.song_orig.transpose(-2), song_tran)

    def test_parse_song(self):
        parsed = song.parse_song(self.song_file1)
        self.assertEqual(self.song_orig, parsed)

    def test_latex_string(self):
        answer = "\\beginsong{Kuža pazi}[by={ljudska}]\n" \
                 "\n" \
                 "\\beginverse\\singlespace\n" \
                 "    \\[C]Kuža pazi, \\[G]z repkom miga, \\[C]vstane, \\[G]leže, \\[C]tačko da.\n" \
                 "    \\[C]Hišo čuva, \\[G]jezno laja, \\[C]če ni\\[G]kogar \\[C]ni doma.\n" \
                 "\\endverse\n" \
                 "\n" \
                 "\\beginverse\\singlespace\n" \
                 "    \\[C]Ko pa Jurček \\[G]cicibanček \\[C]truden \\[G]se od\\[C]pravi spat,\n" \
                 "    \\[C]kuža naš \\[G]pred vrata leže, \\[C]da ne \\[G]vzame \\[C]Jurčka tat.\n" \
                 "\\endverse\n" \
                 "\n" \
                 "\\endsong"
        self.assertEqual(answer, self.song_orig.latex_string())

