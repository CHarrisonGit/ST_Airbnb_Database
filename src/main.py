import keyword_records
import price_dist
import review_sort
import suburb_listing

import tkinter as tk


class Menu:

    def __init__(self, root):

        self.canvas1 = tk.Canvas(root, width=800, height=600)
        self.canvas1.pack()

        self.label1 = tk.Label(root, text='Airbnb Database Viewer')
        self.label1.config(font=('Arial', 20))
        self.canvas1.create_window(400, 50, window=self.label1)

        self.select_db = tk.Button(root, text='Select Database ', command=select_db, bg='palegreen2', font=('Arial', 11, 'bold'))
        self.canvas1.create_window(400, 200, window=self.select_db)

        self.close_p = tk.Button(root, text='Close Program ', command=root.destroy, bg='palegreen2', font=('Arial', 11, 'bold'))
        self.canvas1.create_window(400, 500, window=self.close_p)

        root.mainloop()


class DBmenu:

    def __init__(self, root):

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
        select_clen = tk.Button(root, text='Sort by: Cleanliness', command=None, bg='palegreen2',
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