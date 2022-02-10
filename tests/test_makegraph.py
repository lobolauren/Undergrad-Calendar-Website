from fileinput import filename
import unittest
import pytest
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
        assert myGraph != None
        assert myGraph.filename == fileName + ".gv"


    def test_save_graph_to_PDF(self):
        fileName = "MyGraph"
        try:
            # Create graph with test edge and see if PDF file is created
            myGraph = makegraph.create_course_graph(fileName)
            myGraph.edge("nodeTest1", "nodeTest2")
            makegraph.save_graph_to_pdf(myGraph, fileName)
            sys.path.insert(0, "./graph-output/")
            assert os.path.isdir("./graph-output/")
            assert os.path.isfile("./graph-output/" + fileName)
            assert os.path.isfile("./graph-output/" + fileName + ".pdf") 

            # make sure graph file isn't empty (.gv)
            sys.path.insert(0, "./graph-output/")
            with open("./graph-output/" + fileName, 'r') as testFile:
                contents = testFile.read()
                assert contents != None
                assert "nodeTest1 -> nodeTest2" in contents

        finally:
            # delete files after
            os.remove("./graph-output/" + fileName + ".pdf") 
            os.remove("./graph-output/" + fileName)


    # tests graphing a single course (CIS*4010) and its pre-reqs (done with parse_prereqs)
    def test_graph_course(self):
        file_name = "MyGraph"
        test_graph = makegraph.create_course_graph(file_name)

        # get all CIS courses and their pre-reqs
        course_info = scraper.get_course_info(["cis", "math", "engg", "ips", "phys"])
        data = {
            "programs": test_constants.PROGRAMS, # adds CS program as test
            "courses": course_info
        }
        makegraph.parse_prereqs(test_graph, "CIS*4010", data, "CIS")
        makegraph.save_graph_to_pdf(test_graph, file_name)

        # ensure graph contains correct data
        sys.path.insert(0, "./graph-output/")
        with open("./graph-output/" + file_name, 'r') as testFile:
            contents = testFile.read()
            assert contents != None
            assert "\"CIS*4010\"" in contents
            assert "\"PHYS*1130\" -> \"ENGG*2410\" [color=green]" in contents
            assert "\"CIS*2500\" -> \"CIS*2030\" [color=green]" in contents
            assert "\"CIS*1910\" -> \"CIS*2030\" [color=green]" in contents
            assert "\"CIS*2030\" -> \"CIS*3110\" [color=blue]" in contents

    # # tests graphing a department (done with parse_department)
    def test_graph_department(self):
        file_name = "MyGraph"
        test_graph = makegraph.create_course_graph(file_name)

        course_info = scraper.get_course_info(["cis"])
        data = {
            "programs": test_constants.PROGRAMS, # adds CS program as test
            "courses": course_info
        }
        makegraph.parse_department(test_graph, "cis", data, "cis")
        makegraph.save_graph_to_pdf(test_graph, file_name)

        # ensure graph contains correct data
        sys.path.insert(0, "./graph-output/")
        with open("./graph-output/" + file_name, 'r') as testFile:
            contents = testFile.read()
            print(contents)
            assert contents != None
            assert "\"CIS*1910\" -> \"CIS*2030\" [color=green]" in contents
            assert "\"ENGG*1500\" -> \"CIS*2910\" [color=orange]" in contents
            assert "\"CIS*2520\" -> \"CIS*2750\" [color=green]" in contents
            assert "\"CIS*4900\" -> \"CIS*4910\" [color=green]" in contents
            assert "\"CIS*2030\" -> \"CIS*3110\" [color=blue]" in contents

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
            self.assertTrue("\"ENGG*1410\" [color=chocolate4 fillcolor=lightgray shape=rect style=filled]" in contents)
            self.assertTrue("\"CIS*2750\" -> \"CIS*3760\" [color=green]" in contents)
            self.assertTrue("\"CIS*3750\" -> \"CIS*3760\" [color=green]" in contents)
            self.assertTrue("\"CIS*1300\"" in contents)
            self.assertTrue("\"CIS*1500\" -> \"ENGG*2410\" [color=blue]" in contents)


if __name__ == '__main__':
    unittest.main() # allows you to run by doing python3 test_makegraph.py