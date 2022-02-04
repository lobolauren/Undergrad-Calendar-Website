import unittest

# individual test classes
import test_scraper
import test_makegraph
import test_constants

suite_list = []
suite_list.append(unittest.TestLoader().loadTestsFromTestCase(test_scraper.TestScraper))
suite_list.append(unittest.TestLoader().loadTestsFromTestCase(test_makegraph.TestMakeGraph))

if __name__ == '__main__':
    comboSuite = unittest.TestSuite(suite_list)
    unittest.TextTestRunner(verbosity=0).run(comboSuite)