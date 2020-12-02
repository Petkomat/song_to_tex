# README #

This repository contains some songs together with chords.

### How to create a song book? ###

First, you need to

#### Create a song

Create a text file that contains

- the title of the song
- the author of the song
- the lyrics of the song, together with the chords.

For example, the syntax is the following:

```
We wish you a Merry Christmas
Tradidional author
We <C>wish you a Merry <F>Christmas,
we <D>wish you a Merry <G>Christmas.
We <E-7>wish you a Merry Christ<a>mas
and a <F>Happy <G>New <C>Year!
```

In essence, major chords are given in uppercase (e.g., `C`) letter, and minor chords in lowercase (e.g., `a`).
For any additional stuff (e.g., `7` etc.), use `-` and add the stuff afterwards, e.g., `E-7`.
Every chord is surrounded  by `<` and `>`.

Do this for as many songs as you want and put the files in the same folder.
It is advisable that the file names follow some pattern, which makes them easy to filter by name, e.g., 
`[artist].[title].txt` (see the `songs` directory).


#### Create a Songbook

We follow the example in `main.py`. The series of commands

```
directory = "songs/"
input_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.startswith("slon_in_sadez")]

the_songbook = "songbooks/theSongbook/the_songbook.sgbk"
the_songbook_tex = "songbooks/theSongbook/the_songbook.tex"
book = songbook.create_songbook_from_text_files(input_files, the_songbook)  # songbook.SongBook(the_songbook)  #
# book = songbook.SongBook(the_songbook)
book.write_to_tex_file(the_songbook_tex)
```
creates a song-book file (from which in the future runs, the songbook will be directly loaded) and the tex file,
that you can further edit manually and compile (with LaTeX). The tex file contains:

- placeholders on the title page,
- lyrics and chords,
- fingerings for all the chords that appear in any of the songs (sorted alphabetically).



### Dependencies

- The code is written in Python3. Nothing except for the standard library is needed.
- For compiling the `.tex` file, the LaTeX package `songs` is needed
(available [here](https://www.ctan.org/pkg/songs), the instructions for manual installation can be found
[here](https://tex.stackexchange.com/a/2066/77685)).
