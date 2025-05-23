import unittest
import pickle
import os
from pathlib import Path
from main import hash_pickle
#samir

class TestPathSerialization(unittest.TestCase):
    """
    This test suite verifies that file path representations, both as strings and pathlib.Path objects,
    can be correctly serialized, deserialized, and maintain hash consistency using Python's pickle module.
    """

    def test_string_path_unix_or_windows(self):
        path = "/home/user/documents/test.txt" if os.name != 'nt' else "C:\\Users\\User\\Documents\\test.txt"
        hash_before = hash_pickle(path)
        serialized = pickle.dumps(path)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for string path")
        self.assertEqual(deserialized, path)

    def test_pathlib_object_serialization(self):
        path_obj = Path("data") / "results.pkl"
        hash_before = hash_pickle(path_obj)
        serialized = pickle.dumps(path_obj)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for pathlib object")
        self.assertEqual(deserialized, path_obj)
        self.assertIsInstance(deserialized, Path)

    def test_absolute_path_roundtrip(self):
        abs_path = Path.cwd() / "output" / "logfile.log"
        hash_before = hash_pickle(abs_path)
        serialized = pickle.dumps(abs_path)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for absolute path")
        self.assertEqual(str(deserialized), str(abs_path))
        self.assertEqual(type(deserialized), type(abs_path))

    def test_path_hashes(self):
        """
        Computes SHA256 hashes for different path representations to evaluate pickle stability.
        """
        samples = {
            "StringPath": "/home/user/test.txt" if os.name != 'nt' else "C:\\Users\\User\\test.txt",
            "RelativePath": Path("data") / "results.pkl",
            "AbsolutePath": Path.cwd() / "output" / "logfile.log"
        }

        for name, obj in samples.items():
            with self.subTest(name=name):
                hash1 = hash_pickle(obj)
                hash2 = hash_pickle(obj)
                self.assertEqual(hash1, hash2, f"Hash mismatch for {name}")

if __name__ == "__main__":
    unittest.main()
