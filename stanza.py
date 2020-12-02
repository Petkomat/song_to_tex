LATEX_OFFSET = 4 * " "


class Stanza:
    def __init__(self, verses):
        self.verses = verses

    def __repr__(self):
        return "Stanza({})".format(self.verses)

    def __str__(self):
        return "\n".join([str(verse) for verse in self.verses])

    def __eq__(self, other):
        return len(self.verses) == len(other.verses) and all([v1 == v2 for v1, v2 in zip(self.verses, other.verses)])

    def transpose(self, half_tones):
        return Stanza([verse.transpose(half_tones) for verse in self.verses])

    def latex_string(self):
        lines = ["\\beginverse\\singlespace"]
        for verse in self.verses:
            lines.append(LATEX_OFFSET + verse.latex_string())
        lines.append("\\endverse")
        return "\n".join(lines)

