import unittest
import test_constants
import os
# imports the scraper directory in the directory above the tests
import sys
sys.path.insert(0, "../")
import makegraph

class TestMakeGraph(unittest.TestCase):
    def test_saveGraphToPDF(self):
        fileName = "MyGraph"
        myGraph = makegraph.createCourseGraph(fileName)
        self.assertIsNotNone(myGraph)
        self.assertEqual(myGraph.filename, fileName + ".gv")

    def testGraphCreation(self):
        # try:
        myGraph = makegraph.createCourseGraph("MyGraph")
        makegraph.saveGraphToPDF(myGraph)
        sys.path.insert(0, "../docttest-output")
        # sys.path.insert(0, "./docttest-output")
        print(os.getcwd())
        print(sys.path)
        self.assertTrue(os.path.isdir("./MyGraph.gv.pdf"))
        # finally:
        #     os.remove("./MyGraph.gv.pdf") # delete JSON once done

if __name__ == '__main__':
    unittest.main() # allows you to run by doing python3 test_makegraph.py