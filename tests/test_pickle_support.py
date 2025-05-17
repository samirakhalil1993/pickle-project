import unittest
import pickle
import hashlib
from models import Person, Point, Color

def hash_pickle(obj):
    return hashlib.sha256(pickle.dumps(obj)).hexdigest()

class TestPickleSupport(unittest.TestCase):
    def test_pickle_user_defined_class(self):
        person = Person("Alice", 30)
        data = pickle.dumps(person)
        loaded = pickle.loads(data)
        self.assertEqual(loaded, person)
        self.assertIsInstance(loaded, Person)
        self.assertEqual(hash_pickle(person), hash_pickle(loaded))

    def test_pickle_namedtuple(self):
        point = Point(3, 4)
        data = pickle.dumps(point)
        loaded = pickle.loads(data)
        self.assertEqual(loaded, point)
        self.assertIsInstance(loaded, Point)
        self.assertEqual(hash_pickle(point), hash_pickle(loaded))

    def test_pickle_enum(self):
        color = Color.GREEN
        data = pickle.dumps(color)
        loaded = pickle.loads(data)
        self.assertEqual(loaded, color)
        self.assertIsInstance(loaded, Color)
        self.assertEqual(hash_pickle(color), hash_pickle(loaded))

if __name__ == "__main__":
    unittest.main()
