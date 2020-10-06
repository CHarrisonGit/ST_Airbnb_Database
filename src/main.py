import keyword_records
import price_dist
import review_sort
import suburb_listing

import tkinter as tk
from tkinter import filedialog as fd
import pandas as pd
import matplotlib

class Menu:

    def __init__(self, root):

        self.canvas1 = tk.Canvas(root, width=800, height=600)
        self.canvas1.pack()

        self.label1 = tk.Label(root, text='Airbnb Database Viewer')
        self.label1.config(font=('Arial', 20))
        self.canvas1.create_window(400, 50, window=self.label1)

        self.select_db = tk.Button(root, text='Select Database', command=select_db, bg='palegreen2', font=('Arial', 11, 'bold'))
        self.canvas1.create_window(400, 200, window=self.select_db)

        self.close_p = tk.Button(root, text='Close Program ', command=root.destroy, bg='palegreen2', font=('Arial', 11, 'bold'))
        self.canvas1.create_window(400, 500, window=self.close_p)

        root.mainloop()


class DBmenu:

    def __init__(self, root):

        #File dialog menu
        # self.file_name = fd.askopenfilename(title = "Select a database",filetypes = (("CSV Files","*.csv"),))
        #Load dataframes
        self.df1 = pd.read_csv('listings_dec18.csv')

        self.canvas1 = tk.Canvas(root, width=800, height=600)
        self.canvas1.pack()

        self.label1 = tk.Label(root, text='Airbnb Database Viewer')
        self.label1.config(font=('Arial', 20))
        self.canvas1.create_window(400, 50, window=self.label1)

        # Start Date
        select_sd = tk.Button(root, text='Choose start date', command=None, bg='palegreen2',
                                   font=('Arial', 11, 'bold'))
        self.canvas1.create_window(350, 200, window=select_sd)
        # End Date
        select_ed = tk.Button(root, text='Choose end date', command=None, bg='palegreen2',
                                   font=('Arial', 11, 'bold'))
        self.canvas1.create_window(500, 200, window=select_ed)
        # Cleanliness
        select_clen = tk.Button(root, text='Sort by: Cleanliness', command=self.sort_cleanliness, bg='palegreen2',
                                   font=('Arial', 11, 'bold'))
        self.canvas1.create_window(400, 300, window=select_clen)
        # Highest Review Score
        select_hr = tk.Button(root, text='Sort by: Highest review', command=None, bg='palegreen2',
                                   font=('Arial', 11, 'bold'))
        self.canvas1.create_window(400, 400, window=select_hr)
        # Back to main
        close_p = tk.Button(root, text='Back to main menu', command=back_to_menu, bg='palegreen2',
                                 font=('Arial', 11, 'bold'))
        self.canvas1.create_window(400, 500, window=close_p)

        listbox_sd = tk.Listbox(root)
        self.canvas1.create_window(100, 400, window=listbox_sd)

        listbox_ed = tk.Listbox(root)
        self.canvas1.create_window(700, 400, window=listbox_ed)

        # #Dialog location message
        # self.label2 = tk.Label(root, text="Database location:").pack()
        # self.db_location = tk.Label(root, text=self.file_name).pack()
        # #If no file selected
        # if self.file_name == "":
        #     back_to_menu()

    def sort_cleanliness(self):
        #New window
        clean = tk.Tk()
        clean.title("Cleanliness Search")
        #Start date frame
        start_frame = tk.LabelFrame(clean, text="Enter Start Date", padx=5, pady=5)
        start_frame.pack(side='top', padx=10, pady=10)

        self.start_date=tk.StringVar()
        e1 = tk.Entry(start_frame, textvariable=self.start_date)
        e1.pack()

        #End date frame
        end_frame = tk.LabelFrame(clean, text="Enter End Date", padx=5, pady=5)
        end_frame.pack(side='top', padx=10, pady=10)

        self.end_date=tk.StringVar()
        e2 = tk.Entry(end_frame, textvariable=self.end_date)
        e2.pack()

        def deploydf():
            #Change type to datetime
            self.df3['last_review'] = pd.to_datetime(self.df3['last_review'])
            #Get user input dates
            mask = (self.df3['last_review'] > e1.get()) & (self.df3['last_review'] <= e2.get())
            self.df3 = self.df3.loc[mask]

            #Group by id, search for comments containing cleanliness keywords, count to new column 'count'
            self.df3['count'] = self.df3.groupby(['id_x'])['comments'].transform(lambda x: x[x.str.contains('clean|tidy|neat|washed', case=False, na=False, regex=True)].count())
            #Group by neighbourhood, sort by count
            self.df4 = self.df3[['neighbourhood_cleansed', 'count']].groupby(['neighbourhood_cleansed']).sum().sort_values('count', ascending=False)

            #Show dataframe in a frame
            frame = tk.LabelFrame(clean, text="Cleanliness Search - Cities with most customer mentioned cleanliness", padx=5, pady=5)
            frame.pack(side='bottom', padx=10, pady=10)

            text = tk.Text(frame)
            text.insert(tk.END, str(self.df4))
            text.pack(side='left')
            #Scrollbar
            vsb = tk.Scrollbar(frame, orient="vertical")
            text.configure(yscrollcommand=vsb.set)
            vsb.configure(command=text.yview)
            vsb.pack(side='right', fill='y')


        #File dialog df2 = pd.read_csv(fd.askopenfilename(title = "Select a database",filetypes = (("CSV Files","*.csv"),)), low_memory=False)
        self.df2 = pd.read_csv('reviews_dec18.csv')
        self.df3 = pd.merge(self.df1, self.df2, how='left', left_on=['id'], right_on=['listing_id'])
        #Search button
        tk.Button(clean, text='Search', command=deploydf).pack(side='top')



def select_db():
    for widget in root.winfo_children():
        widget.pack_forget()

    db_menu = DBmenu(root)


def back_to_menu():
    for widget in root.winfo_children():
        widget.pack_forget()

    main_ = Menu(root)

if __name__ == "__main__":
    root = tk.Tk()
    main_ = Menu(root)
