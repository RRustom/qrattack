import unittest
from main import *
from qrcodegen import *

class Test_Order_Codes_By_Ratio(unittest.TestCase):
    def setup(self, m1, m2):
        return


class Test5_Symmetric_Difference(unittest.TestCase):
    # Lindsey's exploratory code; don't delete yet
    # segs = QrSegment.make_segments("a")
    # qr1segs = []
    # qr1 = QrCode.encode_segments(segs, QrCode.Ecc.HIGH, 5, 5, 2, False)
    # for y in range(qr1.get_size()):
    #     for x in range(qr1.get_size()):
    #         qr1segs.append(qr1.get_module(x, y))
    # segs2 = QrSegment.make_segments("b")
    # qr2segs = []
    # qr2 = QrCode.encode_segments(segs2, QrCode.Ecc.HIGH, 5, 5, 2, False)
    # for y in range(qr2.get_size()):
    #     for x in range(qr2.get_size()):
    #         qr2segs.append(qr2.get_module(x, y))
    # diffs = [[],[]]
    # for i in range(len(qr2segs)):
    #     if qr1segs[i] != qr2segs[i]:
    #         diffs[qr1segs[i]].append(i) # QR1: 0/F for white; 1/T for black
    # print(diffs)
    # print([len(diff) for diff in diffs])

    def setup(self, m1, m2):
        segs = QrSegment.make_segments(m1)
        qr1 = QrCode.encode_segments(segs, QrCode.Ecc.HIGH, 5, 5, 2, False)
        segs2 = QrSegment.make_segments(m2)
        qr2 = QrCode.encode_segments(segs2, QrCode.Ecc.HIGH, 5, 5, 2, False)
        return qr1, qr2
    # no white to black
    def test_no_white_to_black(self):
        qr1, qr2 = self.setup("1", "2")
        sd = symmetric_diff(qr1, qr2)
        # TODO: L not sure how to test this
        # self.assertEqual(0, len(sd[0]))
    # no black to white
    def test_no_black_to_white(self):
        qr1, qr2 = self.setup("1", "2")
        sd = symmetric_diff(qr1, qr2)
        # TODO: L not sure how to test this
        # self.assertEqual(0, len(sd[1]))
    # no differences
    def test_no_diffs(self):
        qr1, qr2 = self.setup("1", "1")
        sd = symmetric_diff(qr1, qr2)
        self.assertEqual(0, len(sd[0]))
        self.assertEqual(0, len(sd[1]))
    # non-zero of each kind of difference
    def test_both_diff_kinds(self):
        qr1, qr2 = self.setup("a", "b")
        sd = symmetric_diff(qr1, qr2)
        self.assertEqual(54, len(sd[0]))
        self.assertEqual(40, len(sd[1]))



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
