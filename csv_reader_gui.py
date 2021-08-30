# -*- coding: utf-8 -*-

from tkinter import ttk
import tkinter as tk
import csv
from csv2strings import sync as csv_sync


class CSVReaderGUI(tk.Frame):
    def __init__(self, master=None):
        self.csv_path = 'localization.csv'
        self.master = master
        self.setup_config()
        self.loadData()
        self.create_widgets()

    def setup_config(self):
        s = ttk.Style()
        s.configure('Treeview', rowheight=40)

    def create_widgets(self):
        columns = self.csv_rows[0]

        top_frame = ttk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.BOTH)

        add_button = ttk.Button(top_frame, text='Add', command=self.add_action)
        add_button.pack(side=tk.LEFT)

        sync_button = ttk.Button(top_frame, text='Gen', command=self._sync_action)
        sync_button.pack(side=tk.LEFT, expand=1)

        self.find_entry = ttk.Entry(top_frame)
        self.find_entry.bind('<Return>', self.find_action)
        self.find_entry.pack(side=tk.RIGHT)

        find_label = ttk.Label(top_frame, text='Find:')
        find_label.pack(side=tk.RIGHT)

        self.treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)
        self.treeview.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.treeview.bind('<Double-1>', self.set_cell_value)  # Double-click the left button to enter the edit

        for col in columns:  # bind function to make the header sortable
            self.treeview.heading(col, text=col)

        for column in columns:
            self.treeview.column(column, width=int(w / 7), anchor='center')  # indicates column, not displayed

        for idx, row in enumerate(self.csv_rows):
            if idx == 0:
                continue
            self.treeview.insert('', idx, values=tuple(row))

    def loadData(self):
        self.csv_rows = []
        with open(self.csv_path, 'r', encoding='utf_8_sig') as f:
            reader = csv.reader(f)
            for row in reader:
                self.csv_rows.append(row)

    # find entry return action
    def find_action(self, event):
        find_entry_value = self.find_entry.get()
        print(find_entry_value)
        children = self.treeview.get_children()
        selections = []
        for child in children:
            values = self.treeview.item(child)['values']
            if find_entry_value in values:
                selections.append(child)
        self.treeview.selection_set(selections)

    # add a new row action
    def add_action(self):
        new_row = ['', '', '', '', '', '', '']
        self.csv_rows.append(new_row)
        self.treeview.insert('', len(self.csv_rows)-1, values=tuple(new_row))
        self.treeview.update()

    # cell double click action
    # double click a cell to modify its value.
    def set_cell_value(self, event):  # Double click to enter the edit state
        # double-click will trigger twice sometimes
        # unbind to solve this
        self.treeview.unbind('<Double-1>')
        for item in self.treeview.selection():
            column = self.treeview.identify_column(event.x)  # column
            row = self.treeview.identify_row(event.y)  # row

        # cn = column number, rn = row number
        # both of them are hexadecimal
        cn = int(str(column).replace('#', ''), 16)
        rn = int(str(row).replace('I', ''), 16)
        print('cn = %s, rn = %s', (cn, rn))

        def saveedit(event):
            self.treeview.set(item, column=column, value=entryedit.get())
            # update csv
            self.csv_rows[rn][cn-1] = entryedit.get()
            with open(self.csv_path, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(self.csv_rows)
            # clean
            entryedit.destroy()
            # bind double-click action
            self.treeview.bind('<Double-1>', self.set_cell_value)  # Double-click the left button to enter the edit

        def select_all(event):
            entryedit.select_range(0, 'end')
            entryedit.icursor('end')

        def paste_and_commit(event):
            root.after(50, saveedit, event)

        # add an entry for user to modify cell values.
        entryedit = ttk.Entry(root)
        entryedit.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        entryedit.bind('<Return>', saveedit)
        entryedit.focus()
        item_value = self.treeview.item(item)['values'][cn-1]
        entryedit.insert(0, item_value)

        entryedit.select_range(0, 'end')
        entryedit.icursor('end')

        entryedit.bind('<Command-a>', select_all)
        entryedit.bind('<Command-v>', paste_and_commit)
        print(self.treeview.item(item))

    def _sync_action(self):
        csv_sync()


root = tk.Tk()  # initial box declaration
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.geometry("%dx%d" % (w, h))
csv_gui = CSVReaderGUI(root)
root.mainloop()  # enter the message loop
