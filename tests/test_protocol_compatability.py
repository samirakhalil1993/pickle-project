import unittest
import pickle
from main import hash_pickle


class TestPickleProtocols(unittest.TestCase):

    def setUp(self):
        """
        Set up the test object to be serialized.
        """
        self.data_obj = {"apelsin": 1, "banan": 2}

    def test_pickle_protocols_produce_unique_hashes(self):
        """
        Ensure that different pickle protocols produce different serialized outputs (protocols 0-5).
        """
        hashes = set()

        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            digest = hash_pickle(self.data_obj, protocol=protocol)
            hashes.add(digest)

        expected_unique_count = pickle.HIGHEST_PROTOCOL + 1
        self.assertEqual(
            len(hashes),
            expected_unique_count,
            msg="Different protocols should produce unique serialized hashes"
        )
