import unittest
import pickle
import hashlib
from models import Person, Point, Color


def hash_pickle(data):
    """Serialize the data using pickle and generate a SHA256 hash."""
    serialized = pickle.dumps(data)
    return hashlib.sha256(serialized).hexdigest()


class TestPickleIntegrity(unittest.TestCase):
    """    
    Tests three main aspects:
    - TC01: Round-trip Integrity
    - TC05: Function and Lambda Handling
    - TC06: Nested and Recursive Structures
    """
    
    def test_tc01_round_trip_integrity(self):
        """
        TC01: Verify object remains unchanged after pickle and unpickle.

        """
        # Test a variety of data types
        test_objects = [
            # Primitive types
            None,
            True,
            False,
            42,
            3.14159,
            "Hello, world",
            b'binary data',
            complex(3.14, -2.71),
            
            # Collection types
            [1, 2, 3, 4, 5],
            (6, 7, 8, 9),
            {10, 11, 12},
            {"a": 1, "b": 2, "c": 3},
            
            # Extended types
            bytearray(b'12345'),
            frozenset([1, 2, 3]),
            
            # Custom types
            Person("Alice", 30),
            Point(3, 4),
            Color.GREEN
        ]
        
        for obj in test_objects:
            with self.subTest(object_type=type(obj).__name__, object=obj):
                # Perform pickle round-trip
                serialized = pickle.dumps(obj)
                deserialized = pickle.loads(serialized)
                
                # Verify equality
                self.assertEqual(
                    deserialized, obj,
                    f"Round-trip failed for {type(obj).__name__}"
                )
                
                # Verify type
                self.assertIsInstance(
                    deserialized, type(obj),
                    f"Type changed during round-trip for {type(obj).__name__}"
                )
                
                # Verify hash consistency
                hash_before = hash_pickle(obj)
                hash_after = hash_pickle(deserialized)
                self.assertEqual(
                    hash_before, hash_after,
                    f"Hash mismatch for {type(obj).__name__}"
                )
    
    def test_tc05_function_and_lambda_handling(self):
        """
        TC05: Try serializing functions and lambdas.
        """
        # Method from a class (should work)
        person = Person("Bob", 25)
        method = person.greet
        
        # Built-in function (should work)
        builtin_function = len
        
        # Test expected successful cases
        picklable_functions = [
            (method, "Instance method"),
            (builtin_function, "Built-in function")
        ]
        
        # Test the functions that should be picklable
        for func, description in picklable_functions:
            with self.subTest(function_type=description):
                try:
                    # Attempt to pickle the function
                    serialized = pickle.dumps(func)
                    deserialized = pickle.loads(serialized)
                    
                    # If we get here, serialization succeeded
                    # Compare behavior rather than equality
                    if callable(deserialized):
                        if description == "Instance method":
                            self.assertIn("Bob", deserialized())
                        elif description == "Built-in function":
                            self.assertEqual(deserialized("test"), 4)
                    
                    print(f"✓ Successfully serialized {description}")
                    
                except Exception as e:
                    self.fail(
                        f"Failed to pickle {description} but it should work: {e}"
                    )
        
        # For functions expected to fail, verify they fail as expected
        print("\n-- Expected failures for unpicklable functions: --")
        
        # Local function - will fail
        def local_function(x):
            return x * 2
            
        # Lambda - will fail
        lambda_function = lambda x: x * 3
        
        # Verify that local functions fail expectedly
        try:
            pickle.dumps(local_function)
            self.fail("Local function was pickled but should have failed!")
        except (pickle.PicklingError, AttributeError) as e:
            print(f"✓ Correctly failed to pickle local function: {e}")
            
        # Verify that lambda functions fail expectedly
        try:
            pickle.dumps(lambda_function)
            self.fail("Lambda function was pickled but should have failed!")
        except (pickle.PicklingError, AttributeError) as e:
            print(f"✓ Correctly failed to pickle lambda function: {e}")
    
    def test_tc06_nested_and_recursive_structures(self):
        """
        TC06: Verify correct handling of recursive or nested objects.
        """
        # Deep nesting
        deeply_nested = [1, [2, [3, [4, [5, [6, [7, [8, [9, [10]]]]]]]]]]
        
        # Deep dictionary nesting
        nested_dict = {"a": {"b": {"c": {"d": {"e": {"f": "deep value"}}}}}}
        
        # Mixed nesting
        mixed_nested = {
            "points": [Point(1, 2), Point(3, 4)],
            "people": [Person("Alice", 30), Person("Bob", 25)],
            "data": {
                "colors": [Color.RED, Color.GREEN],
                "values": [1, 2, 3]
            }
        }
        
        # Recursive structure (list that contains itself)
        recursive_list = [1, 2, 3]
        recursive_list.append(recursive_list)  # List now contains itself
        
        # Recursive dictionary
        recursive_dict = {"name": "recursive"}
        recursive_dict["self"] = recursive_dict  # Dict now contains itself
        
        # Complex object graph with circular references
        alice = Person("Alice", 30)
        bob = Person("Bob", 25)
        # Add circular references by adding attributes
        alice.__dict__["friend"] = bob
        bob.__dict__["friend"] = alice
        
        # Test cases for nested structures
        nested_objects = [
            (deeply_nested, "Deeply nested list"),
            (nested_dict, "Deeply nested dictionary"),
            (mixed_nested, "Mixed nested structure"),
            (recursive_list, "Recursive list"),
            (recursive_dict, "Recursive dictionary"),
            (alice, "Circular reference in custom objects")
        ]
        
        for obj, description in nested_objects:
            with self.subTest(structure_type=description):
                try:
                    # Perform pickle round-trip
                    serialized = pickle.dumps(obj)
                    deserialized = pickle.loads(serialized)
                    
                    # Check structure integrity where possible
                    if description == "Deeply nested list":
                        self.assertEqual(
                            deserialized[1][1][1][1][1][1][1][1][1][0], 10
                        )
                        
                    elif description == "Deeply nested dictionary":
                        self.assertEqual(
                            deserialized["a"]["b"]["c"]["d"]["e"]["f"], "deep value"
                        )
                        
                    elif description == "Mixed nested structure":
                        self.assertEqual(len(deserialized["points"]), 2)
                        self.assertEqual(deserialized["people"][0].name, "Alice")
                        self.assertEqual(deserialized["data"]["colors"][1], Color.GREEN)
                        
                    elif description == "Recursive list":
                        # Check that recursion is preserved
                        self.assertIs(deserialized[3], deserialized)
                        
                    elif description == "Recursive dictionary":
                        # Check that recursion is preserved
                        self.assertIs(deserialized["self"], deserialized)
                        
                    elif description == "Circular reference in custom objects":
                        # Check that circular references are preserved
                        self.assertEqual(deserialized.name, "Alice")
                        self.assertEqual(deserialized.friend.name, "Bob")
                        self.assertIs(deserialized.friend.friend, deserialized)
                    
                    print(f"✓ Successfully tested {description}")
                    
                except Exception as e:
                    self.fail(f"Failed to handle {description}: {e}")


if __name__ == "__main__":
    unittest.main()