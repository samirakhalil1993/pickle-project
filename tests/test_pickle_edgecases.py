import unittest
import pickle
import os
from main import hash_pickle


# David
class TestPickleStringEdgeCases(unittest.TestCase):
    """
    Tests for edge cases in string serialization.
    """

    def setUp(self):
        self.filename = "test_string_pickle.pkl"

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def assert_pickle_integrity(self, original):
        display_str = repr(original[:60]) + \
            ("..." if len(original) > 60 else "")
        print(f"\n[Memory Test] \nOriginal string: \t\t{display_str}")

        hash_before = hash_pickle(original)
        serialized = pickle.dumps(original)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)

        print(
            f"Unpickled: \t\t\t{repr(deserialized[:60]) + ('...' if len(deserialized) > 60 else '')}")
        print(
            f"Hash before: \t\t\t{hash_before} \nHash after: \t\t\t{hash_after}")
        print(
            f"Pickled (bytes): {repr(serialized[:60]) + ('...' if len(serialized) > 60 else '')}")

        self.assertEqual(original, deserialized)
        self.assertEqual(hash_before, hash_after)

    def assert_file_pickle_integrity(self, original):
        display_str = repr(original[:60]) + \
            ("..." if len(original) > 60 else "")
        print(f"\n[File Test] \nWriting and reading string: \t{display_str}")

        hash_before = hash_pickle(original)
        with open(self.filename, 'wb') as f:
            pickle.dump(original, f)
        with open(self.filename, 'rb') as f:
            deserialized = pickle.load(f)
        hash_after = hash_pickle(deserialized)

        print(
            f"Read from file: \t\t{repr(deserialized[:60]) + ('...' if len(deserialized) > 60 else '')}")
        print(
            f"Hash before: \t\t\t{hash_before} \nHash after: \t\t\t{hash_after}")

        self.assertEqual(original, deserialized)
        self.assertEqual(hash_before, hash_after)

    # In-memory pickle tests
    def test_empty_string(self):
        self.assert_pickle_integrity("")

    def test_newline_string(self):
        self.assert_pickle_integrity("Line1\nLine2\nLine3")

    def test_tabbed_string(self):
        self.assert_pickle_integrity("Col1\tCol2\tCol3")

    def test_escaped_backslashes(self):
        self.assert_pickle_integrity("Path\\to\\some\\file")

    def test_unicode_characters(self):
        self.assert_pickle_integrity("Hello 👋🌍 - 中文 - العربية")

    def test_long_string(self):
        long_str = "A" * 10_000
        self.assert_pickle_integrity(long_str)

    def test_string_with_null_bytes(self):
        self.assert_pickle_integrity("null\0byte\0test")

    def test_mixed_special_chars(self):
        special = "Specials: \n tab\t backslash\\ null\0 check ✓"
        self.assert_pickle_integrity(special)

    # File-based pickle tests
    def test_file_pickle_simple_string(self):
        self.assert_file_pickle_integrity("Pickle via file!")

    def test_file_pickle_unicode_string(self):
        self.assert_file_pickle_integrity("Unicode file test - 測試")


if __name__ == "__main__":
    unittest.main()
