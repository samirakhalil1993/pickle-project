import unittest
from main import hash_pickle


class TestPickleLineEndings(unittest.TestCase):

    def test_line_ending_differences(self):
        text_lf = "line1\nline2\nline3"
        text_crlf = "line1\r\nline2\r\nline3"

        hash_lf = hash_pickle(text_lf)
        hash_crlf = hash_pickle(text_crlf)

        # Expect the hashes to differ because pickle is precise when it comes to bytes
        self.assertNotEqual(
            hash_lf, hash_crlf,
            msg="Hashes should differ for LF vs CRLF line endings, but does not."
        )

    def test_normalized_line_endings_consistency(self):
        # Normalize both to LF before pickling
        text1 = "line1\r\nline2\r\n".replace("\r\n", "\n")
        text2 = "line1\nline2\n"

        self.assertEqual(text1, text2)

        hash1 = hash_pickle(text1)
        hash2 = hash_pickle(text2)

        self.assertEqual(
            hash1, hash2,
            msg="Hashes should match after normalizing line endings, but does not."
        )
