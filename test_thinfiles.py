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

    def test_raise_on_multiple_mode_configurations(self):
    	# params 3 onwards: halving_start_count, extended_halving_start_count, max_file_counts, filepattern
    	# self.assertRaises(click.UsageError, target.validateOptions, None, None, "x4,2,1", "*.txt")

    	# options which try to configure 0 or > 1 modes
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, "9", "10", None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, "2", None, "4,2,1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, "1", "4,2,1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, "2", "1", "4,2,1", "*.txt")

    def test_raise_on_badly_formatted_configurations(self):
    	# bad file counts per day
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "0", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "-1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "-9999991", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "1,0", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "6,-2,1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "x4,2,1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "4x,2,1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "y,2,1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "8,hello,1", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "8,1,bye_", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, ",", "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, ",,,,", "*.txt")

    	# halving config
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, "", None, None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, "0", None, None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, "-1", None, None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, "2,1", None, None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, "10,2,1", None, None, "*.txt")

    	# extended halving config
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, "", None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, "0", None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, "-1", None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, "2,1", None, "*.txt")
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, "10,2,1", None, "*.txt")

    def test_raise_on_bad_file_pattern(self):
    	self.assertRaises(click.UsageError, target.validateAndParseOptions, None, None, "8,4", "hello.txt")


    def test_doesnt_raise(self):
    	target.validateAndParseOptions(None, None, "1", "*.txt")
    	target.validateAndParseOptions(None, None, "1 ", "*.txt")
    	target.validateAndParseOptions(None, None, " 1 ", "*.txt")
    	target.validateAndParseOptions(None, None, " 1", "*.txt")
    	target.validateAndParseOptions(None, None, " 1, 4,   10 ", "*.txt")
    	target.validateAndParseOptions(None, None, "4,2", "*.txt")
    	target.validateAndParseOptions(None, None, "4,2,1", "*.txt")
    	target.validateAndParseOptions(None, None, "4,2,1", "*.txt")
    	target.validateAndParseOptions(None, None, "4,2,1", "**/*.txt")
    	target.validateAndParseOptions(None, None, "4,2,1", "someDir/**/*.txt")

    	target.validateAndParseOptions("16", None, None, "*.txt")
    	target.validateAndParseOptions("16", None, None, "*.txt")

if __name__ == '__main__':
    unittest.main()


