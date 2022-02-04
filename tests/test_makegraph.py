from fileinput import filename
import unittest
import test_constants
import os
# imports the scraper directory in the directory above the tests
import sys
sys.path.insert(0, "../")
import makegraph
import scraper

class TestMakeGraph(unittest.TestCase):
    def test_graph_creation(self):
        # create graph and check for filename
        fileName = "MyGraph"
        myGraph = makegraph.create_course_graph(fileName)
        self.assertIsNotNone(myGraph)
        self.assertEqual(myGraph.filename, fileName + ".gv")
        
    def test_save_graph_to_PDF(self):
        fileName = "MyGraph"
        try:
            # Create graph with test edge and see if PDF file is created
            myGraph = makegraph.create_course_graph(fileName)
            myGraph.edge("nodeTest1", "nodeTest2")
            makegraph.save_graph_to_pdf(myGraph, fileName)
            sys.path.insert(0, "./graph-output/")
            self.assertTrue(os.path.isdir("./graph-output/"))
            self.assertTrue(os.path.isfile("./graph-output/" + fileName))
            self.assertTrue(os.path.isfile("./graph-output/" + fileName + ".pdf"))

            # make sure graph file isn't empty (.gv)
            sys.path.insert(0, "./graph-output/")
            with open("./graph-output/" + fileName, 'r') as testFile:
                contents = testFile.read()
                self.assertIsNotNone(contents)
                self.assertTrue("nodeTest1 -> nodeTest2" in contents)

        finally:
            # delete files after
            os.remove("./graph-output/" + fileName + ".pdf") 
            os.remove("./graph-output/" + fileName)

    def test_graph_degree_program(self):
        file_name = "MyGraph"
        degree_program = "cs"

        test_graph = makegraph.create_course_graph(file_name)

        # get all CIS courses and their pre-reqs
        course_info = scraper.get_course_info(["cis", "math", "stat", "engg", "ips", "phys"])
        data = {
            "programs": test_constants.PROGRAMS, # adds CS program as test
            "courses": course_info
        }
        makegraph.graph_degree_program(test_graph, degree_program, data)
        makegraph.save_graph_to_pdf(test_graph, file_name)

        # ensure graph contains correct data
        sys.path.insert(0, "./graph-output/")
        with open("./graph-output/" + file_name, 'r') as testFile:
            contents = testFile.read()
            self.assertIsNotNone(contents)
            self.assertTrue(f"Graph for |{degree_program}| degree program" in contents)
            self.assertTrue("\"ENGG*1410\" [color=chocolate4]" in contents)
            self.assertTrue("\"CIS*2750\" -> \"CIS*3760\" [color=green]" in contents)
            self.assertTrue("\"CIS*3750\" -> \"CIS*3760\" [color=green]" in contents)
            self.assertTrue("\"CIS*1300\"" in contents)
            self.assertTrue("\"CIS*1500\" [color=chocolate4]" in contents)

if __name__ == '__main__':
    unittest.main() # allows you to run by doing python3 test_makegraph.py