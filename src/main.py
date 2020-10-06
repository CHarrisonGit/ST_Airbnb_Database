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

        label1 = tk.Label(root, text='Airbnb Database Viewer')
        label1.config(font=('Arial', 20))
        canvas1.create_window(400, 50, window=label1)

        # Start Date
        select_sd = tk.Button(root, text='Choose start date', command=None, bg='palegreen2',
                              font=('Arial', 11, 'bold'))
        canvas1.create_window(350, 200, window=select_sd)
        # End Date
        select_ed = tk.Button(root, text='Choose end date', command=None, bg='palegreen2',
                              font=('Arial', 11, 'bold'))
        canvas1.create_window(500, 200, window=select_ed)
        # Cleanliness
        select_clen = tk.Button(root, text='Sort by: Cleanliness', command=None, bg='palegreen2',
                                font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 300, window=select_clen)
        # Highest Review Score
        select_hr = tk.Button(root, text='Sort by: Highest review', command=None, bg='palegreen2',
                              font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 400, window=select_hr)
        # Back to main
        close_p = tk.Button(root, text='Back to main menu', command=back_to_menu, bg='palegreen2',
                            font=('Arial', 11, 'bold'))
        canvas1.create_window(400, 500, window=close_p)

        listbox_sd = tk.Listbox(root)
        canvas1.create_window(100, 400, window=listbox_sd)

        listbox_ed = tk.Listbox(root)
        canvas1.create_window(700, 400, window=listbox_ed)

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


class Listings:
    def __init__(self, root, returns):
        label = tk.Label(root, text="Listings", font=("Arial", 30)).grid(row=0, columnspan=3)

        # create listings table
        col_names = ('Listing ID', 'Name', 'Location', 'Room type', 'Price per night')
        listBox = ttk.Treeview(root, columns=col_names, show='headings')
        for col in col_names:
            listBox.heading(col, text=col)
        listBox.grid(row=1, column=0, columnspan=2)

        # Bottom navigation
        showScores = tk.Button(root, text="price chart", width=15).grid(row=4, column=1)
        closeButton = tk.Button(root, text="Back to main", width=15, command=exit).grid(row=4, column=1,sticky="e")

        for i in returns:
            listBox.insert("", "end", values=(i[0], i[1], i[5], i[8], i[9]))

def select_dbs():
    for widget in root.winfo_children():
        widget.pack_forget()

    db_menu = DBmenu(root)


def select_listings(returns):
    for widget in root.winfo_children():
        widget.pack_forget()

    listings_menu = Listings(root,returns)


def back_to_menu():
    for widget in root.winfo_children():
        widget.pack_forget()

    main_ = Menu(root)


if __name__ == "__main__":
    root = tk.Tk()
    main_ = Menu(root)
