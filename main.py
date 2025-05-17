import unittest
import pickle
import hashlib

def hash_pickle(data):
    """
    Serialize the data using pickle and generate a SHA256 hash.
    """
    serialized = pickle.dumps(data)
    return hashlib.sha256(serialized).hexdigest()




def main():
    loader = unittest.TestLoader()
    suite = loader.discover('tests')  # Discover all test files in the ´tests' directory
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n All tests passed.")
    else:
        print(f"\n {len(result.failures)} test(s) failed.")

if __name__ == '__main__':
    main()