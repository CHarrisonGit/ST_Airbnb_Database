import unittest
import sys
import pandas as pd
import tkinter as tk
import main
import keyword_records
sys.path.insert(1, "./src/")  # to import running in the test path


class TestSwarm(unittest.TestCase):

    def test_correct_date(self):
        root = tk.Tk()
        test = main.DBmenu(root)
        keyword = "test"
        start = pd.DataFrame({'year': [2019], 'month': [2], 'day': [4]})
        end = pd.DataFrame({'year': [2019], 'month': [2], 'day': [3]})
        with self.assertRaises(ValueError):
            keyword_records.keyword_search(keyword, start, end)

    def test_keyword_search(self):
        root = tk.Tk()
        test = main.DBmenu(root)
        keyword = ""
        start = pd.DataFrame({'year': [2019], 'month': [2], 'day': [4]})
        end = pd.DataFrame({'year': [2019], 'month': [2], 'day': [5]})
        with self.assertRaises(ValueError):
            keyword_records.keyword_search(keyword, start, end)



if __name__ == "__main__":
    unittest.main()
