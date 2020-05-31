import unittest

target = __import__("thinfiles")

generateFilesPerDayForHalvingPattern = target.generateFilesPerDayForHalvingPattern
#print(generateFilesPerDayForHalvingPattern)

class TestGenFilesPerDayForHalvingPattern(unittest.TestCase):
    def test_gen(self):
        """
        Test that we generate expected files per day specs
        """

        self.assertEqual(generateFilesPerDayForHalvingPattern(9), [9, 4, 2, 1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(8), [8, 4, 2, 1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(7), [7, 3, 1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(2), [2, 1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(1), [1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(0), [])

        self.assertEqual(generateFilesPerDayForHalvingPattern(9, extend=True), [9,   4, 4,   2, 2, 2, 2,   1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(8, extend=True), [8,   4, 4,   2, 2, 2, 2,   1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(7, extend=True), [7,   3, 3,   1, 1, 1, 1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(2, extend=True), [2,   1, 1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(1, extend=True), [1])
        self.assertEqual(generateFilesPerDayForHalvingPattern(0, extend=True), [])

        print("IN TEST")
if __name__ == '__main__':
    unittest.main()
    print("IN TEST 2")


