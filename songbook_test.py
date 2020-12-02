import unittest
import random
import misc
import songbook
import song
from unittest import mock


class SongbookTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        random.seed(1234)
        cls.songbook_folder = misc.create_temp_folder(".")
        cls.songs_folder = misc.create_temp_folder(".")
        cls.song_file1 = cls.songs_folder + "/song1.txt"
        cls.song_file2 = cls.songs_folder + "/song2.txt"
        cls.song_file3 = cls.songs_folder + "/song3.txt"
        cls.song_file4 = cls.songs_folder + "/song4.txt"
        cls.song_file5 = cls.songs_folder + "/song5.txt"
        cls.song_files = [cls.song_file1, cls.song_file2, cls.song_file3, cls.song_file4, cls.song_file5]
        artists = ["c", "A", "b", "B", "b"]
        titles = ["cc", "A", "z", "x", "y"]
        stanzass = [[["Tum <C> bum", "Pam <d> bam"], ["<c-7>Rom <g> pom"]],
                    [["<E>Bird is the word", "<E>Bird is the word"]],
                    [],
                    [["One verse, <a> <A> one stanza"]],
                    [["Pure"], ["Lyrics"], ["The end."]]]
        for song_file, artist, title, stanzas in zip(cls.song_files, artists, titles, stanzass):
            song.create_text_song(song_file, artist, title, stanzas)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        misc.remove_temp_folder(cls.songbook_folder)
        misc.remove_temp_folder(cls.songs_folder)

    def test_create_from_text_files_and_sort(self):
        with mock.patch('builtins.input', return_value='yes'):
            book = songbook.create_songbook_from_text_files(self.song_files, self.songbook_folder + "/book.sgbk")
        true_order = sorted(zip([4, 0, 3, 1, 2], self.song_files))
        songs = [song.parse_song(song_file) for _, song_file in true_order]
        book.sort_songs()
        self.assertListEqual(book.songs, songs)

    def test_write_to_file_and_create_existing_songbook(self):
        book_file = self.songbook_folder + "/book.sgbk"
        with mock.patch('builtins.input', return_value='yes'):
            book = songbook.create_songbook_from_text_files(self.song_files, book_file)
        book.write_to_file()
        book2 = songbook.SongBook(book_file)

        self.assertEqual(book, book2)


