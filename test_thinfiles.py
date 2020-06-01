import unittest
import click

target = __import__("thinfiles")

generateFilesPerDayForHalvingPattern = target.generateFilesPerDayForHalvingPattern
#print(generateFilesPerDayForHalvingPattern)

# test script as a whole (by executing whole thing), or internals?

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

    def test_raise(self):
    	# params 3 onwards: halving_start_count, extended_halving_start_count, max_file_counts, filepattern
    	# self.assertRaises(click.UsageError, target.validateOptions, None, None, "x4,2,1", "*.txt")

    	# options which try to configuire >1 mode
    	self.assertRaises(click.UsageError, target.validateOptions, "9", "10", None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateOptions, "2", None, "4,2,1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateOptions, "2", "1", "4,2,1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateOptions, None, "1", "4,2,1", "*.txt")

    def test_doesnt_raise(self):
    	target.validateOptions(None, None, "4,2,1", "*.txt")

if __name__ == '__main__':
    unittest.main()


