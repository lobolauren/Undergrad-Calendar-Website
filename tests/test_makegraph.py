import unittest
import test_constants
import os
# imports the scraper directory in the directory above the tests
import sys
sys.path.insert(0, "../")
import makegraph

class TestMakeGraph(unittest.TestCase):
    def test_graphCreation(self):
        fileName = "MyGraph"
        myGraph = makegraph.createCourseGraph(fileName)
        self.assertIsNotNone(myGraph)
        self.assertEqual(myGraph.filename, fileName + ".gv")

        
    def test_saveGraphToPDF(self):
        fileName = "MyGraph"
        try:
            myGraph = makegraph.createCourseGraph(fileName)
            myGraph.edge("nodeTest1", "nodeTest2")
            makegraph.saveGraphToPDF(myGraph)
            sys.path.insert(0, "./doctest-output/")
            self.assertTrue(os.path.isdir("./doctest-output/"))
            self.assertTrue(os.path.isfile("./doctest-output/" + fileName + ".gv"))
            self.assertTrue(os.path.isfile("./doctest-output/" + fileName + ".gv.pdf"))

            # make sure graph file isn't empty (.gv)
            sys.path.insert(0, "./doctest-output/")
            with open("./doctest-output/" + fileName + ".gv", 'r') as testFile:
                contents = testFile.read()
                self.assertIsNotNone(contents)
                self.assertTrue("nodeTest1 -> nodeTest2" in contents)

        finally:
            # delete files after
            os.remove("./doctest-output/" + fileName + ".gv.pdf") 
            os.remove("./doctest-output/" + fileName + ".gv")

if __name__ == '__main__':
    unittest.main() # allows you to run by doing python3 test_makegraph.py