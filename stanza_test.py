import unittest
import verse
import stanza


class StanzaTest(unittest.TestCase):
    def setUp(self):
        self.originals = ["<E>Ma nam jaz čaku, kaj si nor<D>,",
                          "<E>zaštarta Francelj svoj mo<D>tor.",
                          "<E>Tristo kubikov, krom ba<D>lanca,",
                          "<E>v koloni sred vrhnškega <D>klanca."]
        self.verses_orig = [verse.parse_verse(text) for text in self.originals]
        self.stanza_orig = stanza.Stanza(self.verses_orig)

    def tearDown(self):
        pass

    def test_transpose(self):
        transposed = ["<F>Ma nam jaz čaku, kaj si nor<D#>,",
                      "<F>zaštarta Francelj svoj mo<D#>tor.",
                      "<F>Tristo kubikov, krom ba<D#>lanca,",
                      "<F>v koloni sred vrhnškega <D#>klanca."]
        verses_transposed = [verse.parse_verse(text) for text in transposed]
        stanza_transposed = stanza.Stanza(verses_transposed)
        self.assertEqual(self.stanza_orig.transpose(1), stanza_transposed)

    def test_latex_string(self):
        answer = "\\beginverse\\singlespace\n" \
                 "    \\[E]Ma nam jaz čaku, kaj si nor\\[D],\n" \
                 "    \\[E]zaštarta Francelj svoj mo\\[D]tor.\n" \
                 "    \\[E]Tristo kubikov, krom ba\\[D]lanca,\n" \
                 "    \\[E]v koloni sred vrhnškega \\[D]klanca.\n" \
                 "\\endverse"
        self.assertEqual(answer, self.stanza_orig.latex_string())

