from openpyxl import load_workbook
import statistics
import numpy as np
import csv
from tkinter import ttk
from tkinter import *
import tkinter as tk
import tkcalendar
from tkinter import messagebox as msg

from datetime import datetime as dt
import datetime

import keyword_records
import price_dist
import review_sort
import suburb_listing
import pandas as pd
import matplotlib.pyplot as plt

class Menu:

    def __init__(self, root):
        canvas1 = tk.Canvas(root, width=800, height=600)
        canvas1.pack()

        label1 = tk.Label(root, text='Airbnb Database Viewer')
        label1.config(font=('Arial', 20))
        canvas1.create_window(400, 50, window=label1)

        select_db = tk.Button(root, text='Show Database ', command=select_dbs, bg='palegreen2',
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

        # Start Date
        start_lbl = tk.Label(root, text="Start Date", font=("Arial", 10))
        self.start_cal = tkcalendar.Calendar(root, font="Arial 5", selectmode='day', cursor="hand1", year=2019, month=2, day=5)
        canvas1.create_window(100, 200, window=self.start_cal)
        canvas1.create_window(100, 125, window=start_lbl)
        # End Date
        end_lbl = tk.Label(root, text="End Date", font=("Arial", 10))
        self.end_cal = tkcalendar.Calendar(root, font="Arial 5", selectmode='day', cursor="hand1", year=2019, month=2, day=7)
        canvas1.create_window(100, 400, window=self.end_cal)
        canvas1.create_window(100, 325, window=end_lbl)


        # Price
        select_clen = tk.Button(root, text='Suburb Search', command=self.sort_suburb, bg='palegreen2',
                                font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 200, window=select_clen)
        # Suburb
        select_clen = tk.Button(root, text='Price Chart', command=self.pricechart, bg='palegreen2',
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
        search_key.insert(0,"pool")
        canvas1.create_window(650, 100, window=search_key,)

        def search_keyword():
            keywords = str(search_key.get())
            start_date = self.start_cal.get_date()
            end_date = self.end_cal.get_date()
            date1 = pd.to_datetime(start_date)
            date2 = pd.to_datetime(end_date)

            returns = keyword_records.keyword_search(keywords, date1, date2)
            select_listings(returns)

        search_key_button = tk.Button(root, text='Search keyword', command=search_keyword, bg='palegreen2',
                                      font=('Arial', 11, 'bold'))
        canvas1.create_window(650, 140, window=search_key_button)

    # Cleanliness search function
    def sort_cleanliness(self):
        # New window
        clean = tk.Tk()
        clean.title("Cleanliness Search")

        # File dialog df2 = pd.read_csv(fd.askopenfilename(title = "Select a database",filetypes = (("CSV Files","*.csv"),)), low_memory=False)
        self.df2 = pd.read_csv('DB Files/reviews_dec18.csv')
        self.df3 = pd.merge(self.df1, self.df2, how='left', left_on=['id'], right_on=['listing_id'])

        # Change type to datetime
        self.df3['host_since'] = pd.to_datetime(self.df3['host_since'])
        # Get user input dates
        mask = (self.df3['host_since'] > self.start_cal.get_date()) & (self.df3['host_since'] <= self.end_cal.get_date())
        self.df3 = self.df3.loc[mask]

        # Group by id, search for comments containing cleanliness keywords, count to new column 'count'
        self.df3['count'] = self.df3.groupby(['id_x'])['comments'].transform(
            lambda x: x[x.str.contains('clean|cleanliness|tidy|tidiness|neat|washed|sanitised', case=False, na=False, regex=True)].count())
        # Group by neighbourhood, sort by count
        self.df4 = self.df3[['neighbourhood_cleansed', 'count']].groupby(
            ['neighbourhood_cleansed']).sum().sort_values('count', ascending=False)

        # Show dataframe in a frame
        frame = tk.LabelFrame(clean,
                              text="Cleanliness Search - Cities ranked by most customer mentioned cleanliness",
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

    #Price chart function
    def pricechart(self):
        # Change type to datetime
        self.df1['host_since'] = pd.to_datetime(self.df1['host_since'])
        # Get user input dates
        mask = (self.df1['host_since'] > self.start_cal.get_date()) & (self.df1['host_since'] <= self.end_cal.get_date())
        self.df1 = self.df1.loc[mask]

        self.df1['price'] = self.df1['price'].str.replace(',', '')
        self.df1['price'] = self.df1['price'].str.replace('$', '')
        self.df1['price'] = self.df1['price'].astype('float')
        prices = sorted(self.df1['price'].tolist())
        price_range = []

        count1 = 0
        for i in prices:
            if i <= 100:
                count1 += 1

        count2 = 0
        for i in prices:
            if i > 100 and i <= 200:
                count2 += 1

        count3 = 0
        for i in prices:
            if i > 200 and i <= 300:
                count3 += 1

        count4 = 0
        for i in prices:
            if i > 300 and i <= 400:
                count4 += 1

        count5 = 0
        for i in prices:
            if i > 400 and i <= 500:
                count5 += 1

        count6 = 0
        for i in prices:
            if i > 500 and i <= 600:
                count6 += 1

        count7 = 0
        for i in prices:
            if i > 600 and i <= 700:
                count7 += 1

        count8 = 0
        for i in prices:
            if i > 700 and i <= 800:
                count8 += 1

        count9 = 0
        for i in prices:
            if i > 800 and i <= 900:
                count9 += 1

        count10 = 0
        for i in prices:
            if i > 900 and i <= 1000:
                count10 += 1

        count11 = 0
        for i in prices:
            if i > 1000:
                count11 += 1

        price_range.extend((count1, count2, count3, count4, count5, count6, count7, count8, count9, count10, count11))

        #PLOT
        plt.figure(figsize=(11, 6))
        plt.plot(['0-100','100-200','200-300','300-400','400-500','500-600','600-700','700-800','800-900','900-1000','1000+'], price_range)
        plt.title('Sydney Airbnb Price Distribution')
        plt.xlabel('Price Range Per Night (AUD)')
        plt.ylabel('Number of listings')
        plt.grid()
        plt.show()

    #Suburb search function
    def sort_suburb(self):
        #New window
        suburb = tk.Tk()
        suburb.title("Suburb Search")
        pd.set_option('display.max_rows', self.df1.shape[0]+1)
        #Append neighbourhood column to list
        suburb_lst = self.df1['neighbourhood'].tolist()

        #Delete duplicates
        suburb_lst = sorted(list(map(str, dict.fromkeys(suburb_lst))))

        def deploydf():
            #Change type to datetime
            self.df1['host_since'] = pd.to_datetime(self.df1['host_since'])
            #Get user input dates
            mask = (self.df1['host_since'] > self.start_cal.get_date()) & (self.df1['host_since'] <= self.end_cal.get_date())
            self.df1 = self.df1.loc[mask]

            #Suburb dataframe
            searched_df = self.df1.loc[self.df1['neighbourhood'] == variable.get()]

            #Show dataframe in a frame
            frame = tk.LabelFrame(suburb, text="Suburb Search", padx=5, pady=5)
            frame.pack(side='bottom', padx=10, pady=10)

            text = tk.Text(frame)
            text.insert(tk.END, str(searched_df[['id', 'neighbourhood', 'price']]))
            text.pack(side='left')
            #Scrollbar
            vsb = tk.Scrollbar(frame, orient="vertical")
            text.configure(yscrollcommand=vsb.set)
            vsb.configure(command=text.yview)
            vsb.pack(side='right', fill='y')

        variable = tk.StringVar(suburb)
        variable.set(suburb_lst[0])

        #Option list
        option_frame = tk.LabelFrame(suburb, text="Click a suburb", padx=5, pady=5)
        option_frame.pack(side='top', padx=10, pady=10)
        opt = tk.OptionMenu(option_frame, variable, *suburb_lst).pack()

        #Search button
        tk.Button(suburb, text='Search', command=deploydf).pack(side='top')


def key_search(root, returns):

    if returns == 0:
        pass
    # Title
    label = tk.Label(root, text="Listings", font=("Arial", 30)).grid(row=0, columnspan=3)

    # Bottom navigation
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
        listBox.insert("", "end", values=(i[0], i[4], i[23], i[52], str(i[60])))


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
