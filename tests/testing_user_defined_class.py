# tests/test_user_defined_class_pickle.py
import unittest
import pickle
import hashlib
from models import Person

def hash_pickle(obj):
    return hashlib.sha256(pickle.dumps(obj)).hexdigest()

class TestPickleUserDefinedClass(unittest.TestCase):
    def test_pickle_roundtrip(self):
        person = Person("Alice", 30)
        dumped = pickle.dumps(person)
        loaded = pickle.loads(dumped)

        self.assertEqual(person, loaded)
        self.assertIsInstance(loaded, Person)
        self.assertEqual(hash_pickle(person), hash_pickle(loaded))
