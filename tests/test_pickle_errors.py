import unittest
import pickle
import os
import socket
from main import hash_pickle
# David


class TestPickleErrorHandling(unittest.TestCase):
    """
    Tests for error handling and unpicklable objects.
    """

    def setUp(self):
        self.filename = "test_pickle_data.pkl"

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_pickle_lambda_function_raises(self):
        print("\nTest: Trying to pickle a lambda function (should fail)")
        def obj(x): return x + 1
        with self.assertRaises((pickle.PicklingError, AttributeError, TypeError)) as context:
            pickle.dumps(obj)
        print(
            f"Caught exception: {type(context.exception).__name__} - {context.exception}")

    def test_pickle_socket_object_raises(self):
        print("\nTest: Trying to pickle a socket object (should fail)")
        s = socket.socket()
        try:
            with self.assertRaises((pickle.PicklingError, AttributeError, TypeError)) as context:
                pickle.dumps(s)
            print(
                f"Caught exception: {type(context.exception).__name__} - {context.exception}")
        finally:
            s.close()

    def test_unpickle_corrupted_file_raises(self):
        print("\nTest: Write pickle data to file and replace it with garbage")
        data = {'valid': True}
        # Save correct pickle first
        with open(self.filename, 'wb') as f:
            pickle.dump(data, f)
        # Write garbage that replaces the content
        with open(self.filename, 'wb') as f:
            f.write(b'This is not a pickle!')
        with open(self.filename, 'rb') as f:
            with self.assertRaises((pickle.UnpicklingError, EOFError, AttributeError, IndexError, ValueError, MemoryError)) as context:
                pickle.load(f)
        print(
            f"Caught exception: {type(context.exception).__name__} - {context.exception}")

    def test_pickle_and_unpickle_file_success(self):
        print("\nTest: Pickle to file and read back correctly")
        data = {'test': 123}
        hash_before = hash_pickle(data)
        with open(self.filename, 'wb') as f:
            pickle.dump(data, f)
        with open(self.filename, 'rb') as f:
            result = pickle.load(f)
        hash_after = hash_pickle(result)
        print("Hash before:", hash_before)
        print("Hash after:", hash_after)
        self.assertEqual(data, result, "Data mismatch")
        self.assertEqual(hash_before, hash_after,
                         "Hash mismatch after file roundtrip")


if __name__ == "__main__":
    unittest.main()
