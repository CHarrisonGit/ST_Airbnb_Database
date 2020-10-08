from openpyxl import load_workbook
import statistics
import numpy as np
import csv
import datetime
import pandas as pd
from tkinter import messagebox as msg


def keyword_search(keywords,start,end):
    if keywords == "":
        raise ValueError(msg.showerror(title="Search Error", message="Search field can not be empty"))
    if start > end:
        raise ValueError(msg.showerror(title="Date Error", message="You can not have end date before start date."))
    # Create workbook
    summary = open('DB Files/listings_summary_dec18.csv', mode='r', encoding='utf-8')
    csv_summary = csv.reader(summary)

    date_cols = ["date"]
    pd_calendar = pd.read_csv('DB Files/calendar_dec18.csv', parse_dates=date_cols)
    pd_summary = pd.read_csv('DB Files/listings_summary_dec18.csv')

    print(type(start))

    # Convert dates to same format
    np_start = np.datetime64(start)
    #np_end = np.datetime64(end)

    returns = []

    listing_date = pd_calendar[pd_calendar.date == np_start]
    is_available = listing_date[listing_date.available == 't']

    summary_listings = pd_summary[pd_summary.id.isin(is_available["listing_id"])]
    np_listings = summary_listings.to_numpy()

    for row in np_listings:
        for cell in row:
            if type(cell) == str:
                if keywords.lower() in cell.lower():
                    temp = []
                    for cell in row:
                        temp.append(cell)

                    returns.append(temp)
                    continue
    return returns


if __name__ == "__main__":
    date1 = datetime.date(2019, 12, 6)
    date2 = datetime.date(2018, 5, 17)
    test = keyword_search(keywords="family", start=date1, end=date2)
