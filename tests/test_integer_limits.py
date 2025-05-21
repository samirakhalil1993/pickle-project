import unittest
from main import hash_pickle


class TestPickleIntegerSerialization(unittest.TestCase):

    def setUp(self):
        # Defining integer edge cases
        self.int_values = [
            (2**31 - 1, "Max 32-bit int"),
            (2**31, "Overflow 32-bit int"),
            (2**63 - 1, "Max 64-bit int"),
            (2**63, "Overflow 64-bit int"),
            (-2**31, "Min 32-bit int"),
            (-2**63, "Min 64-bit int")
        ]

    def test_pickle_integer_limits(self):
        for value, description in self.int_values:
            with self.subTest(description=description):
                try:
                    hashed = hash_pickle(value)
                    self.assertEqual(len(hashed), 64)  # SHA-256 hex digest is 64 characters
                except Exception as e:
                    self.fail(f"Unexpected error for {description}: {e}")
