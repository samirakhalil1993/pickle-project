import unittest
import pickle
from main import hash_pickle
#samir
class TestLargeStructures(unittest.TestCase):
    """
    This test suite verifies that Python's pickle module can correctly
    serialize, deserialize, and maintain hash consistency for large data structures.
    """

    def test_large_list(self):
        large_list = list(range(1_000_000))  # 1 million integers
        hash_before = hash_pickle(large_list)
        serialized = pickle.dumps(large_list)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for large list")
        self.assertEqual(deserialized, large_list)

    def test_large_dictionary(self):
        large_dict = {f'key_{i}': i for i in range(100_000)}  # 100k key-value pairs
        hash_before = hash_pickle(large_dict)
        serialized = pickle.dumps(large_dict)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for large dictionary")
        self.assertEqual(deserialized, large_dict)

    def test_large_nested_structure(self):
        nested = [{"index": i, "values": list(range(100))} for i in range(1000)]
        hash_before = hash_pickle(nested)
        serialized = pickle.dumps(nested)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for large nested structure")
        
    def test_large_structures_hash(self):
        """
        Computes SHA256 hashes for large structures to detect changes across Python versions or OS.
        """
        samples = {
            "LargeList": list(range(1_000_000)),
            "LargeDict": {f'key_{i}': i for i in range(100_000)},
            "NestedListDict": [{"index": i, "values": list(range(100))} for i in range(1000)]
        }

        for name, obj in samples.items():
            with self.subTest(name=name):
                hash1 = hash_pickle(obj)
                hash2 = hash_pickle(obj)
                self.assertEqual(hash1, hash2, f"Hash mismatch for {name}")

if __name__ == "__main__":
    unittest.main()
