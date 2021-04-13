import unittest
from main import *

class Test5_Ratios(unittest.TestCase):
    # first list empty
    def test_first_list_empty(self):
        first_list = []
        second_list = [(1,2), (3,4)]
        symmetric_diffs = [first_list, second_list]
        r = calculate_difference_ratio(symmetric_diffs)
        self.assertEqual(0, r)
    # second list empty
    def test_second_list_empty(self):
        first_list = [(1,2), (3,4), (4,1)]
        second_list = []
        symmetric_diffs = [first_list, second_list]
        r = calculate_difference_ratio(symmetric_diffs)
        self.assertEqual(1, r)
    # both lists empty
    def test_both_lists_empty(self):
        first_list = [(1,2), (3,4), (4,1)]
        second_list = []
        symmetric_diffs = [first_list, second_list]
        r = calculate_difference_ratio(symmetric_diffs)
        self.assertEqual(1, r)
    # len(first_list) > len(second_list)
    def test_longer_first_list(self):
        first_list = [(1,2), (3,4), (4,1)]
        second_list = [(3,2)]
        symmetric_diffs = [first_list, second_list]
        r = calculate_difference_ratio(symmetric_diffs)
        self.assertEqual(.75, r)
    # len(first_list) < len(second_list)
    def test_longer_second_list(self):
        first_list = [(2,1), (4,3)]
        second_list = [(1,2), (3,4), (4,1)]
        symmetric_diffs = [first_list, second_list]
        r = calculate_difference_ratio(symmetric_diffs)
        self.assertEqual(.4, r)
    # len(first_list) = len(second_list)
    def test_equal_length_lists(self):
        first_list = [(2,1), (4,3), (1,4)]
        second_list = [(1,2), (3,4), (4,1)]
        symmetric_diffs = [first_list, second_list]
        r = calculate_difference_ratio(symmetric_diffs)
        self.assertEqual(.5, r)

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
