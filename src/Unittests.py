import unittest
import sys
import pandas as pd
import tkinter as tk
import main
import keyword_records
import datetime
sys.path.insert(1, "./src/")  # to import running in the test path


class TestSwarm(unittest.TestCase):

    def test_correct_date(self):
        keyword = "test"
        start = datetime.datetime(2018, 6, 3)
        end = datetime.datetime(2018, 6, 1)
        with self.assertRaises(ValueError):
            keyword_records.keyword_search(keyword, start, end)

    def test_keyword_search(self):
        keyword = ""
        start = datetime.datetime(2018, 6, 1)
        end = datetime.datetime(2018, 6, 3)
        with self.assertRaises(ValueError):
            keyword_records.keyword_search(keyword, start, end)

    def test_no_search_results(self):
        keyword = "awdawdawdw"
        start = datetime.datetime(2018, 6, 1)
        end = datetime.datetime(2018, 6, 3)
        with self.assertRaises(LookupError):
            keyword_records.keyword_search(keyword, start, end)



if __name__ == "__main__":
    unittest.main()
