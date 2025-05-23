import unittest
import pickle
from main import hash_pickle
#samir
class TestExtendedDataTypes(unittest.TestCase):
    """
    Extended Data Types
    This test suite verifies that Python's pickle module can correctly serialize,
    deserialize, and maintain hash consistency across various data types.
    """

    def test_none_serialization(self):
        obj = None
        hash_before = hash_pickle(obj)
        serialized = pickle.dumps(obj)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for None")
        self.assertIsNone(deserialized)

    def test_boolean_serialization(self):
        for value in [True, False]:
            with self.subTest(value=value):
                hash_before = hash_pickle(value)
                serialized = pickle.dumps(value)
                deserialized = pickle.loads(serialized)
                hash_after = hash_pickle(deserialized)
                self.assertEqual(hash_before, hash_after, f"Hash mismatch for {value}")
                self.assertEqual(deserialized, value)

    def test_complex_number_serialization(self):
        obj = complex(3.14, -2.71)
        hash_before = hash_pickle(obj)
        serialized = pickle.dumps(obj)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for Complex number")
        self.assertEqual(deserialized, obj)

    def test_bytes_serialization(self):
        obj = b'\x00\x01\x02hello'
        hash_before = hash_pickle(obj)
        serialized = pickle.dumps(obj)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for Bytes")
        self.assertEqual(deserialized, obj)

    def test_bytearray_serialization(self):
        obj = bytearray(b'12345')
        hash_before = hash_pickle(obj)
        serialized = pickle.dumps(obj)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for Bytearray")
        self.assertEqual(deserialized, obj)

    def test_memoryview_as_bytes_serialization(self):
        obj = memoryview(b'abcdef')
        data = bytes(obj)
        hash_before = hash_pickle(data)
        serialized = pickle.dumps(data)
        deserialized = pickle.loads(serialized)
        hash_after = hash_pickle(deserialized)
        self.assertEqual(hash_before, hash_after, "Hash mismatch for Memoryview as bytes")
        self.assertEqual(deserialized, data)

if __name__ == "__main__":
    unittest.main()
