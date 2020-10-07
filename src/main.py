from openpyxl import load_workbook
import statistics
import numpy as np
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import *

import keyword_records
import price_dist
import review_sort
import suburb_listing
import pandas as pd


class Menu:

    def __init__(self, root):
        canvas1 = tk.Canvas(root, width=800, height=600)
        canvas1.pack()

        label1 = tk.Label(root, text='Airbnb Database Viewer')
        label1.config(font=('Arial', 20))
        canvas1.create_window(400, 50, window=label1)

        select_db = tk.Button(root, text='Select Database ', command=select_dbs, bg='palegreen2',
                              font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 200, window=select_db)

        close_p = tk.Button(root, text='Close Program ', command=root.destroy, bg='palegreen2',
                            font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 500, window=close_p)

        root.mainloop()


class DBmenu:

    def __init__(self, root):
        canvas1 = tk.Canvas(root, width=800, height=600)
        canvas1.pack()
        self.df1 = pd.read_csv('DB Files/listings_dec18.csv')

        label1 = tk.Label(root, text='Airbnb Database Viewer')
        label1.config(font=('Arial', 20))
        canvas1.create_window(400, 50, window=label1)

        # Price
        select_clen = tk.Button(root, text='Sort by: Price', command=self.sort_cleanliness, bg='palegreen2',
                                font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 200, window=select_clen)
        # Suburb
        select_clen = tk.Button(root, text='Sort by: Suburb', command=self.sort_cleanliness, bg='palegreen2',
                                font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 250, window=select_clen)
        # Cleanliness
        select_clen = tk.Button(root, text='Sort by: Cleanliness', command=self.sort_cleanliness, bg='palegreen2',
                                font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 300, window=select_clen)
        # Highest Review Score
        select_hr = tk.Button(root, text='Sort by: Review score', command=None, bg='palegreen2',
                              font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 350, window=select_hr)
        # Back to main
        close_p = tk.Button(root, text='Back to main menu', command=back_to_menu, bg='palegreen2',
                            font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 500, window=close_p)

        # Keyword Search
        search_key = tk.Entry(root)
        canvas1.create_window(100, 100, window=search_key)

        def search_keyword():
            keywords = str(search_key.get())
            returns = keyword_records.keyword_search(keywords)
            select_listings(returns)

        search_key_button = tk.Button(root, text='Search keyowords', command=search_keyword, bg='palegreen2',
                                      font=('Arial', 11, 'bold'))
        canvas1.create_window(100, 140, window=search_key_button)

    # Cleanliness search function
    def sort_cleanliness(self):
        # New window
        clean = tk.Tk()
        clean.title("Cleanliness Search")
        # Start date frame
        start_frame = tk.LabelFrame(clean, text="Enter Start Date", padx=5, pady=5)
        start_frame.pack(side='top', padx=10, pady=10)

        self.start_date = tk.StringVar()
        e1 = tk.Entry(start_frame, textvariable=self.start_date)
        e1.pack()

        # End date frame
        end_frame = tk.LabelFrame(clean, text="Enter End Date", padx=5, pady=5)
        end_frame.pack(side='top', padx=10, pady=10)

        self.end_date = tk.StringVar()
        e2 = tk.Entry(end_frame, textvariable=self.end_date)
        e2.pack()

        def deploydf():
            # Change type to datetime
            self.df3['last_review'] = pd.to_datetime(self.df3['last_review'])
            # Get user input dates
            mask = (self.df3['last_review'] > e1.get()) & (self.df3['last_review'] <= e2.get())
            self.df3 = self.df3.loc[mask]

            # Group by id, search for comments containing cleanliness keywords, count to new column 'count'
            self.df3['count'] = self.df3.groupby(['id_x'])['comments'].transform(
                lambda x: x[x.str.contains('clean|tidy|neat|washed', case=False, na=False, regex=True)].count())
            # Group by neighbourhood, sort by count
            self.df4 = self.df3[['neighbourhood_cleansed', 'count']].groupby(
                ['neighbourhood_cleansed']).sum().sort_values('count', ascending=False)

            # Show dataframe in a frame
            frame = tk.LabelFrame(clean,
                                  text="Cleanliness Search - Cities with most customer mentioned cleanliness",
                                  padx=5, pady=5)
            frame.pack(side='bottom', padx=10, pady=10)

            text = tk.Text(frame)
            text.insert(tk.END, str(self.df4))
            text.pack(side='left')
            # Scrollbar
            vsb = tk.Scrollbar(frame, orient="vertical")
            text.configure(yscrollcommand=vsb.set)
            vsb.configure(command=text.yview)
            vsb.pack(side='right', fill='y')

        # File dialog df2 = pd.read_csv(fd.askopenfilename(title = "Select a database",filetypes = (("CSV Files","*.csv"),)), low_memory=False)
        self.df2 = pd.read_csv('DB Files/reviews_dec18.csv')
        self.df3 = pd.merge(self.df1, self.df2, how='left', left_on=['id'], right_on=['listing_id'])
        # Search button
        tk.Button(clean, text='Search', command=deploydf).pack(side='top')










def key_search(root, returns):
    # Title
    label = tk.Label(root, text="Listings", font=("Arial", 30)).grid(row=0, columnspan=3)

    # Bottom navigation
    price_button = tk.Button(root, text="price chart", width=15).grid(row=4, column=1)
    close_button = tk.Button(root, text="Close window", width=15, command=root.destroy).grid(row=4, column=1,
                                                                                             sticky="e")

    # create listings table
    col_names = ('Listing ID', 'Name', 'Location', 'Room type', 'Price per night')
    listBox = ttk.Treeview(root, columns=col_names, show='headings')

    for col in col_names:
        listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)

    # Add data to table
    for i in returns:
        listBox.insert("", "end", values=(i[0], i[1], i[5], i[8], i[9]))


def select_dbs():
    for widget in root.winfo_children():
        widget.pack_forget()

    db_menu = DBmenu(root)


def select_listings(returns):
    listings_root = tk.Tk()
    key_search(listings_root, returns)


def back_to_menu():
    for widget in root.winfo_children():
        widget.pack_forget()

    main_ = Menu(root)


if __name__ == "__main__":
    root = tk.Tk()
    main_ = Menu(root)
