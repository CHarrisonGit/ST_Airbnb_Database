from openpyxl import load_workbook
import statistics
import numpy as np
import csv
import datetime
import pandas as pd
from tkinter import messagebox as msg


def review_search(start,end):

    if start > end:
        raise ValueError(msg.showerror(title="Date Error", message="You can not have end date before start date."))
        pass

    # Load csv files
    date_cols2 = ["host_since"]
    pd_listings = pd.read_csv('DB Files/listings_dec18.csv', parse_dates=date_cols2)

    # Convert dates to same format
    np_start = np.datetime64(start)
    np_end = np.datetime64(end)

    returns = []
    np_listings = np.array

    listing_date = pd_listings[pd_listings.host_since > np_start].fillna(0)
    listing_final = listing_date.sort_values(by=['review_scores_rating'], ascending=False)

    np_listings = listing_final[["id","name","neighbourhood","room_type","review_scores_rating"]].to_numpy()

    if len(returns) == 0:
        raise LookupError(msg.showerror(title="Search Error", message="No search results found"))
    else:
        return returns


if __name__ == "__main__":
 pass
