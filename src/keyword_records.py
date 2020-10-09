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
        pass
    if start > end:
        raise ValueError(msg.showerror(title="Date Error", message="You can not have end date before start date."))
        pass

    # Load csv files
    date_cols = ["date"]
    pd_calendar = pd.read_csv('DB Files/calendar_dec18.csv', parse_dates=date_cols)
    date_cols2 = ["host_since"]
    pd_listings = pd.read_csv('DB Files/listings_dec18.csv', parse_dates=date_cols2)

    # Convert dates to same format
    np_start = np.datetime64(start)
    np_end = np.datetime64(end)
    swap1 = datetime.date(2018, 12, 1)
    swap2 = np.datetime64(end)

    returns = []
    np_listings = np.array

    if start.year > 2018:
        listing_date = pd_calendar[pd_calendar.date == np_start]
        is_available = listing_date[listing_date.available == 't']
        summary_listings = pd_listings[pd_listings.id.isin(is_available["listing_id"])]
        np_listings = summary_listings.to_numpy()
    else:
        listings = pd_listings[pd_listings.host_since >= np_start]
        np_listings = listings.to_numpy()

    for row in np_listings:
        for cell in row:
            if type(cell) == str:
                if keywords.lower() in cell.lower():
                    temp = []
                    for cell in row:
                        temp.append(cell)

                    returns.append(temp)
                    continue
    if len(returns) == 0:
        raise LookupError(msg.showerror(title="Search Error", message="No search results found"))
    else:
        return returns


if __name__ == "__main__":
    date1 = datetime.date(2019, 12, 6)
    date2 = datetime.date(2018, 5, 17)
    test = keyword_search(keywords="family", start=date1, end=date2)
