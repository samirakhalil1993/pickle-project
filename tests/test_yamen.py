import hashlib
import pickle
import pprint
import unittest

from models import Color, Person, Point


def hash_pickle(data):
    """Serialize the data using pickle and generate a SHA256 hash."""
    serialized = pickle.dumps(data)
    return hashlib.sha256(serialized).hexdigest()


def format_obj_for_display(obj):
    """Format object for display in a readable way."""
    try:
        if isinstance(obj, (dict, list, tuple, set, frozenset)):
            return pprint.pformat(obj, indent=2)
        elif isinstance(obj, (int, float, str, bool, type(None))):
            if isinstance(obj, str) and len(obj) > 100:
                return f"{obj[:100]}... (length: {len(obj)})"
            return str(obj)
        elif hasattr(obj, '__dict__'):
            return f"{type(obj).__name__}: {pprint.pformat(obj.__dict__, indent=2)}"
        else:
            return f"{type(obj).__name__}: {str(obj)}"
    except Exception as e:
        return f"<Unable to format object: {e}>"


def is_nan(value):
    """Check if a value is NaN."""
    return isinstance(value, float) and value != value


class TestPickleIntegrity(unittest.TestCase):
    """
    Tests three main aspects:
    - TC01: Round-trip Integrity
    - TC05: Function and Lambda Handling
    - TC06: Nested and Recursive Structures
    """
    
    def setUp(self):
        """Set up the test case."""
        self.test_count = 0
        self.successful_tests = 0
        self.failed_tests = []
        print("\n" + "="*80)
        print(f"RUNNING: {self._testMethodName}")
        print("="*80)
    
    def tearDown(self):
        """Print test summary."""
        if self.failed_tests:
            print(f"\nFAILED: {len(self.failed_tests)} of {self.test_count} tests failed:")
            for failure in self.failed_tests:
                print(f"  - {failure}")
        else:
            print(f"\nPASSED: All {self.test_count} tests passed")
    
    def test_tc01_round_trip_integrity(self):
        """
        TC01: Verify object remains unchanged after pickle and unpickle.
        Tests various edge cases based on pickle documentation.
        """
        print("\nTC01: Testing Round-Trip Integrity")
        print("This test verifies that objects remain unchanged after "
              "serialization and deserialization")
        
        # Organize tests by type category for better reporting
        test_categories = {
            "None and Boolean Types": [
                None,
                True,
                False
            ],
            
            "Integer Types": [
                0,
                1,
                -1,
                42,
                2**31 - 1,     # Max 32-bit int
                -2**31,        # Min 32-bit int
                2**63 - 1,     # Max 64-bit int
                -2**63,        # Min 64-bit int
                2**100         # Very large int
            ],
            
            "Float Types": [
                0.0,
                1.0,
                -1.0,
                3.14159,
                float('inf'),     # Infinity
                float('-inf'),    # Negative infinity
                float('nan'),     # Not a number
                1e308,            # Near max float
                -1e308,           # Near min float
                0.1 + 0.2         # 0.30000000000000004 (precision issue)
            ],
            
            "Complex Numbers": [
                complex(0, 0),
                complex(3.14, -2.71),
                complex(float('inf'), 2),
                complex(3, float('nan'))
            ],
            
            "String Types": [
                "",                # Empty string
                "Hello, world",
                "a" * 10000,       # Long string
                "åäö",             # Non-ASCII
                "\n\t\r",          # Control characters
                "\\",              # Backslash
                "\"",              # Quote
                "\b\f\n\r\t",      # Various control chars
                "😀"               # Emoji
            ],
            
            "Bytes and Bytearray": [
                b"",
                b'binary data',
                b'\x00\x01\x02hello',
                bytearray(b''),
                bytearray(b'12345'),
                bytearray([0, 1, 255])
            ],
            
            "Collections": [
                [],                 # Empty list
                [1, 2, 3, 4, 5],
                ["mixed", 1, 3.14, True],
                (),                 # Empty tuple
                (6, 7, 8, 9),
                ("mixed", 2, 3.14, False),
                set(),              # Empty set
                {10, 11, 12},
                frozenset(),        # Empty frozenset
                frozenset([1, 2, 3]),
                {},                 # Empty dict
                {"a": 1, "b": 2, "c": 3},
                {1: "one", "two": 2, (3, 4): "tuple_key"}
            ],
            
            "Custom Types": [
                Person("Alice", 30),
                Person("", -999),    # Edge case attributes
                Point(3, 4),
                Point(float('inf'), float('nan')),
                Color.RED,
                Color.GREEN,
                Color.BLUE
            ]
        }
        
        # Track test results by category
        category_results = {}
        
        # Process all categories
        for category, test_objects in test_categories.items():
            category_count = 0
            category_failed = 0
            
            for obj in test_objects:
                self.test_count += 1
                category_count += 1
                
                try:
                    # Perform pickle round-trip
                    serialized = pickle.dumps(obj)
                    deserialized = pickle.loads(serialized)
                    
                    # Special handling for Point with NaN values
                    if isinstance(obj, Point) and (is_nan(obj.x) or is_nan(obj.y)):
                        # For Point with NaN, check both coordinates separately
                        x_same_nan = is_nan(obj.x) and is_nan(deserialized.x)
                        y_same_nan = is_nan(obj.y) and is_nan(deserialized.y)
                        x_equal = obj.x == deserialized.x if not is_nan(obj.x) else x_same_nan
                        y_equal = obj.y == deserialized.y if not is_nan(obj.y) else y_same_nan
                        
                        if not (x_equal and y_equal):
                            error_msg = (f"Point with special values not preserved in {category}\n"
                                         f"  Original: Point(x={obj.x}, y={obj.y})\n"
                                         f"  Deserialized: Point(x={deserialized.x}, y={deserialized.y})")
                            self.failed_tests.append(error_msg)
                            category_failed += 1
                            
                            # Print detailed failure info
                            print(f"\nFAILURE DETAILS - Point in {category}:")
                            print(f"  Original Point: {obj}")
                            print(f"  Deserialized Point: {deserialized}")
                            print(f"  Original x: {obj.x} (is NaN: {is_nan(obj.x)})")
                            print(f"  Deserialized x: {deserialized.x} (is NaN: {is_nan(deserialized.x)})")
                            print(f"  Original y: {obj.y} (is NaN: {is_nan(obj.y)})")
                            print(f"  Deserialized y: {deserialized.y} (is NaN: {is_nan(deserialized.y)})")
                            print(f"  X values match: {x_equal}")
                            print(f"  Y values match: {y_equal}")
                            continue
                            
                    # Special handling for NaN values (can't use equality)
                    elif isinstance(obj, float) and is_nan(obj):  # NaN check
                        if not is_nan(deserialized):  # If result is not NaN
                            error_msg = (f"NaN value not preserved for float "
                                         f"in {category}")
                            self.failed_tests.append(error_msg)
                            category_failed += 1
                            
                            print(f"\nFAILURE DETAILS - Float in {category}:")
                            print(f"  Original: {obj} (is NaN: {is_nan(obj)})")
                            print(f"  Deserialized: {deserialized} (is NaN: {is_nan(deserialized)})")
                            continue
                            
                    # Complex with NaN
                    elif (isinstance(obj, complex) and 
                          (is_nan(obj.real) or is_nan(obj.imag))):
                        real_ok = (is_nan(obj.real) and is_nan(deserialized.real)) or obj.real == deserialized.real
                        imag_ok = (is_nan(obj.imag) and is_nan(deserialized.imag)) or obj.imag == deserialized.imag
                        
                        if not (real_ok and imag_ok):
                            error_msg = (f"NaN component not preserved for complex "
                                         f"in {category}")
                            self.failed_tests.append(error_msg)
                            category_failed += 1
                            
                            print(f"\nFAILURE DETAILS - Complex in {category}:")
                            print(f"  Original: {obj}")
                            print(f"  Deserialized: {deserialized}")
                            print(f"  Original real: {obj.real} (is NaN: {is_nan(obj.real)})")
                            print(f"  Deserialized real: {deserialized.real} (is NaN: {is_nan(deserialized.real)})")
                            print(f"  Original imag: {obj.imag} (is NaN: {is_nan(obj.imag)})")
                            print(f"  Deserialized imag: {deserialized.imag} (is NaN: {is_nan(deserialized.imag)})")
                            continue
                            
                    # Regular equality check
                    elif deserialized != obj:
                        error_msg = (f"Value not preserved for {type(obj).__name__} "
                                     f"in {category}")
                        self.failed_tests.append(error_msg)
                        category_failed += 1
                        
                        print(f"\nFAILURE DETAILS - {type(obj).__name__} in {category}:")
                        print(f"  Original: {format_obj_for_display(obj)}")
                        print(f"  Deserialized: {format_obj_for_display(deserialized)}")
                        continue
                    
                    # Type check
                    if not isinstance(deserialized, type(obj)):
                        error_msg = (f"Type changed for {type(obj).__name__} "
                                     f"in {category}")
                        self.failed_tests.append(error_msg)
                        category_failed += 1
                        
                        print(f"\nFAILURE DETAILS - Type mismatch in {category}:")
                        print(f"  Original type: {type(obj).__name__}")
                        print(f"  Deserialized type: {type(deserialized).__name__}")
                        continue
                    
                    # Hash consistency check
                    hash_before = hash_pickle(obj)
                    hash_after = hash_pickle(deserialized)
                    if hash_before != hash_after:
                        error_msg = (f"Hash mismatch for {type(obj).__name__} "
                                     f"in {category}")
                        self.failed_tests.append(error_msg)
                        category_failed += 1
                        
                        print(f"\nFAILURE DETAILS - Hash mismatch in {category}:")
                        print(f"  Original hash: {hash_before}")
                        print(f"  Deserialized hash: {hash_after}")
                        continue
                    
                    # If we get here, test passed
                    self.successful_tests += 1
                    
                except Exception as e:
                    error_msg = (f"Exception with {type(obj).__name__} in {category}: "
                                 f"{type(e).__name__}: {str(e)}")
                    self.failed_tests.append(error_msg)
                    category_failed += 1
                    
                    print(f"\nFAILURE DETAILS - Exception in {category}:")
                    print(f"  Object type: {type(obj).__name__}")
                    print(f"  Exception: {type(e).__name__}: {str(e)}")
            
            # Store category results
            category_results[category] = (category_count, category_failed)
            
            # Print category summary
            if category_failed > 0:
                print(f"  FAILED: {category}: {category_failed} of {category_count} "
                      f"tests failed")
            else:
                print(f"  PASSED: {category}: All {category_count} tests passed")
    
    def test_tc05_function_and_lambda_handling(self):
        """
        TC05: Try serializing functions and lambdas.
        """
        print("\nTC05: Testing Function and Lambda Handling")
        print("This test examines how Python's pickle module handles "
              "different types of functions")
        
        # Method from a class (should work)
        person = Person("Bob", 25)
        method = person.greet
        
        # Built-in function (should work)
        builtin_function = len
        
        # Global function (should work)
        global_function = hash_pickle
        
        # Test expected successful cases
        picklable_functions = [
            (method, "Instance method"),
            (builtin_function, "Built-in function"),
            (global_function, "Global function")
        ]
        
        # Test the functions that should be picklable
        function_results = []
        
        for func, description in picklable_functions:
            self.test_count += 1
            
            try:
                # Attempt to pickle the function
                serialized = pickle.dumps(func)
                deserialized = pickle.loads(serialized)
                
                # If we get here, serialization succeeded
                # Verify functionality for specific function types
                if description == "Instance method":
                    result = deserialized()
                    if "Bob" not in result:
                        error_msg = (f"{description}: Method lost context, "
                                     f"'Bob' not in result")
                        self.failed_tests.append(error_msg)
                        function_results.append(f"FAILED: {description}")
                        
                        print(f"\nFAILURE DETAILS - {description}:")
                        print(f"  Expected: 'Bob' to be in the result")
                        print(f"  Actual result: '{result}'")
                        continue
                elif description == "Built-in function":
                    result = deserialized("test")
                    if result != 4:
                        error_msg = (f"{description}: Function returned "
                                     f"incorrect value")
                        self.failed_tests.append(error_msg)
                        function_results.append(f"FAILED: {description}")
                        
                        print(f"\nFAILURE DETAILS - {description}:")
                        print(f"  Expected result: 4")
                        print(f"  Actual result: {result}")
                        continue
                
                # If we reached here, test passed
                self.successful_tests += 1
                function_results.append(f"PASSED: {description}")
                
            except Exception as e:
                error_msg = f"{description}: {type(e).__name__}: {str(e)}"
                self.failed_tests.append(error_msg)
                function_results.append(f"FAILED: {description}")
                
                print(f"\nFAILURE DETAILS - {description}:")
                print(f"  Exception: {type(e).__name__}: {str(e)}")
        
        # Print picklable function results
        for result in function_results:
            print(f"  {result}")
        
        # Test functions that should fail
        print("\n  Expected failures (these should not be picklable):")
        
        # Local function (should fail)
        def local_function(x):
            return x * 2
            
        # Lambda (should fail)
        lambda_function = lambda x: x * 3
        
        unpicklable_functions = [
            (local_function, "Local function"),
            (lambda_function, "Lambda function")
        ]
        
        for func, description in unpicklable_functions:
            self.test_count += 1
            
            try:
                pickle.dumps(func)
                # If we get here, it didn't fail as expected
                error_msg = (f"{description} was incorrectly pickled when "
                             f"it should fail")
                self.failed_tests.append(error_msg)
                print(f"  FAILED: {description}: Incorrectly succeeded")
                
                print(f"\nFAILURE DETAILS - {description}:")
                print(f"  Expected: Pickling to fail")
                print(f"  Actual: Pickling succeeded")
            except (pickle.PicklingError, AttributeError, TypeError):
                # This is expected - test passed
                self.successful_tests += 1
                print(f"  PASSED: {description}: Correctly failed")
    
    def test_tc06_nested_and_recursive_structures(self):
        """
        TC06: Verify correct handling of recursive or nested objects.
        """
        print("\nTC06: Testing Nested and Recursive Structures")
        print("This test verifies that pickle correctly handles deeply "
              "nested and recursive structures")
        
        # Test structure definitions
        nested_structures = {
            "Deeply nested list": [1, [2, [3, [4, [5, [6, [7, [8, [9, [10]]]]]]]]]], 
            
            "Deeply nested dictionary": {
                "a": {"b": {"c": {"d": {"e": {"f": "deep value"}}}}}
            },
            
            "Deeply nested mixed": {"a": [1, {"b": (2, [3, {"c": 4}])}, 5]},
            
            "Mixed data structure": {
                "points": [Point(1, 2), Point(3, 4)],
                "people": [Person("Alice", 30), Person("Bob", 25)],
                "data": {
                    "colors": [Color.RED, Color.GREEN],
                    "values": [1, 2, 3]
                }
            }
        }
        
        # Create recursive structures
        recursive_list = [1, 2, 3]
        recursive_list.append(recursive_list)  # List now contains itself
        
        recursive_dict = {"name": "recursive"}
        recursive_dict["self"] = recursive_dict  # Dict now contains itself
        
        # Create circular references in custom objects
        alice = Person("Alice", 30)
        bob = Person("Bob", 25)
        alice.__dict__["friend"] = bob
        bob.__dict__["friend"] = alice
        
        # Add recursive structures to test cases
        recursive_structures = {
            "Recursive list": recursive_list,
            "Recursive dictionary": recursive_dict,
            "Circular reference in custom objects": alice
        }
        
        # Test regular nested structures
        print("\n  Testing regular nested structures:")
        for name, obj in nested_structures.items():
            self.test_count += 1
            
            try:
                # Perform pickle round-trip
                serialized = pickle.dumps(obj)
                deserialized = pickle.loads(serialized)
                
                # Check structure via equality
                if deserialized != obj:
                    error_msg = f"{name}: Structure not preserved correctly"
                    self.failed_tests.append(error_msg)
                    print(f"  FAILED: {name}")
                    
                    print(f"\nFAILURE DETAILS - {name}:")
                    print(f"  Original structure and deserialized structure are not equal.")
                    continue
                
                # If we reached here, test passed
                self.successful_tests += 1
                print(f"  PASSED: {name}")
                
            except Exception as e:
                error_msg = f"{name}: {type(e).__name__}: {str(e)}"
                self.failed_tests.append(error_msg)
                print(f"  FAILED: {name}")
                
                print(f"\nFAILURE DETAILS - {name}:")
                print(f"  Exception: {type(e).__name__}: {str(e)}")
        
        # Test recursive structures 
        print("\n  Testing recursive structures:")
        for name, obj in recursive_structures.items():
            self.test_count += 1
            
            try:
                # Perform pickle round-trip
                serialized = pickle.dumps(obj)
                deserialized = pickle.loads(serialized)
                
                # Check recursive references are preserved
                if name == "Recursive list":
                    if deserialized[3] is not deserialized:
                        error_msg = f"{name}: Recursion not preserved"
                        self.failed_tests.append(error_msg)
                        print(f"  FAILED: {name}")
                        
                        print(f"\nFAILURE DETAILS - {name}:")
                        print(f"  Expected: deserialized[3] is deserialized")
                        print(f"  Actual: deserialized[3] is not deserialized")
                        continue
                        
                elif name == "Recursive dictionary":
                    if deserialized["self"] is not deserialized:
                        error_msg = f"{name}: Recursion not preserved"
                        self.failed_tests.append(error_msg)
                        print(f"  FAILED: {name}")
                        
                        print(f"\nFAILURE DETAILS - {name}:")
                        print(f"  Expected: deserialized['self'] is deserialized")
                        print(f"  Actual: deserialized['self'] is not deserialized")
                        continue
                        
                elif name == "Circular reference in custom objects":
                    if (deserialized.name != "Alice" or 
                        deserialized.friend.name != "Bob"):
                        error_msg = f"{name}: Object attributes not preserved"
                        self.failed_tests.append(error_msg)
                        print(f"  FAILED: {name}")
                        
                        print(f"\nFAILURE DETAILS - {name}:")
                        print(f"  Original: Alice->Bob->Alice")
                        print(f"  Deserialized: {deserialized.name}->{deserialized.friend.name}")
                        continue
                    
                    if deserialized.friend.friend is not deserialized:
                        error_msg = f"{name}: Circular reference not preserved"
                        self.failed_tests.append(error_msg)
                        print(f"  FAILED: {name}")
                        
                        print(f"\nFAILURE DETAILS - {name}:")
                        print(f"  Expected: deserialized.friend.friend is deserialized")
                        print(f"  Actual: deserialized.friend.friend is not deserialized")
                        continue
                
                # If we reached here, test passed
                self.successful_tests += 1
                print(f"  PASSED: {name}")
                
            except Exception as e:
                error_msg = f"{name}: {type(e).__name__}: {str(e)}"
                self.failed_tests.append(error_msg)
                print(f"  FAILED: {name}")
                
                print(f"\nFAILURE DETAILS - {name}:")
                print(f"  Exception: {type(e).__name__}: {str(e)}")


if __name__ == "__main__":
    unittest.main()