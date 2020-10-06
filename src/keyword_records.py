from openpyxl import load_workbook
import statistics
import numpy as np
import csv


def keyword_search(keywords):
    # Create workbook
    summary = open('DB Files/listings_summary_dec18.csv', mode='r', encoding='utf-8')
    csv_summary = csv.reader(summary)
    returns = []

    for row in csv_summary:
        for cell in row:
            if keywords.lower() in cell.lower():
                temp = []
                for cell in row:
                    temp.append(cell)

                returns.append(temp)
                continue
    return returns


if __name__ == "__main__":
    test_search = keyword_search("north sydney")

    for i in test_search:
        print(i)