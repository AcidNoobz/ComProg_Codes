import tkinter as tk
from tkinter import ttk, messagebox
from crud import *
from report import *
from db import setup_database

# setup database
setup_database()

# main window
root = tk.Tk()
root.title("Luis Bakery Sales Recording System")
root.geometry("1200x700")
root.config(bg="white")

# title
title = tk.Label(
    root,
    text="LUIS BAKERY SALES RECORDING SYSTEM",
    font=("Arial", 24, "bold"),
    bg="white",
    fg="red"
)

title.pack(pady=15)

# =========================
# FORM FRAME
# =========================

form_frame = tk.Frame(root, bg="white")
form_frame.pack(pady=10)

# product
tk.Label(
    form_frame,
    text="Product Name",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="red"
).grid(row=0, column=0, padx=10, pady=5)

product_entry = tk.Entry(form_frame, width=25)
product_entry.grid(row=0, column=1)

# category
tk.Label(
    form_frame,
    text="Category",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="red"
).grid(row=1, column=0, padx=10, pady=5)

category_entry = tk.Entry(form_frame, width=25)
category_entry.grid(row=1, column=1)

# quantity
tk.Label(
    form_frame,
    text="Quantity",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="red"
).grid(row=2, column=0, padx=10, pady=5)

quantity_entry = tk.Entry(form_frame, width=25)
quantity_entry.grid(row=2, column=1)

# price
tk.Label(
    form_frame,
    text="Price",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="red"
).grid(row=0, column=2, padx=10, pady=5)

price_entry = tk.Entry(form_frame, width=25)
price_entry.grid(row=0, column=3)

# date
tk.Label(
    form_frame,
    text="Date",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="red"
).grid(row=1, column=2, padx=10, pady=5)

date_entry = tk.Entry(form_frame, width=25)
date_entry.grid(row=1, column=3)

# =========================
# TABLE STYLE
# =========================

style = ttk.Style()

style.theme_use("default")

style.configure(
    "Treeview",
    background="white",
    foreground="black",
    rowheight=28,
    fieldbackground="white",
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background="red",
    foreground="white",
    font=("Arial", 11, "bold")
)

# =========================
# TABLE
# =========================

tree = ttk.Treeview(root)

tree["columns"] = (
    "ID",
    "Product",
    "Category",
    "Quantity",
    "Price",
    "Total",
    "Date"
)

tree.column("#0", width=0, stretch=tk.NO)

tree.column("ID", width=60, anchor=tk.CENTER)
tree.column("Product", width=180, anchor=tk.CENTER)
tree.column("Category", width=150, anchor=tk.CENTER)
tree.column("Quantity", width=100, anchor=tk.CENTER)
tree.column("Price", width=100, anchor=tk.CENTER)
tree.column("Total", width=120, anchor=tk.CENTER)
tree.column("Date", width=120, anchor=tk.CENTER)

for col in tree["columns"]:
    tree.heading(col, text=col)

tree.pack(pady=20)

editing_id = None

# =========================
# FUNCTIONS
# =========================

# refresh table
def refresh_table():

    for item in tree.get_children():
        tree.delete(item)

    for row in get_sales():
        tree.insert("", tk.END, values=row)

# add data
def add_data():

    try:

        add_sale(
            product_entry.get(),
            category_entry.get(),
            int(quantity_entry.get()),
            float(price_entry.get()),
            date_entry.get()
        )

        messagebox.showinfo(
            "Success",
            "Record Added Successfully"
        )

        refresh_table()

    except:

        messagebox.showerror(
            "Error",
            "Invalid Input"
        )

# delete data
def delete_data():

    selected = tree.focus()

    if not selected:
        messagebox.showerror(
            "Delete Sale",
            "Please select a record to delete."
        )
        return

    values = tree.item(selected, "values")

    delete_sale(values[0])

    refresh_table()

# edit data

def edit_data():

    global editing_id

    selected = tree.focus()

    if not selected:
        messagebox.showerror(
            "Edit Sale",
            "Please select a record to edit."
        )
        return

    values = tree.item(selected, "values")

    editing_id = values[0]

    product_entry.delete(0, tk.END)
    product_entry.insert(0, values[1])

    category_entry.delete(0, tk.END)
    category_entry.insert(0, values[2])

    quantity_entry.delete(0, tk.END)
    quantity_entry.insert(0, values[3])

    price_entry.delete(0, tk.END)
    price_entry.insert(0, values[4])

    date_entry.delete(0, tk.END)
    date_entry.insert(0, values[6])

    messagebox.showinfo(
        "Edit Sale",
        "Modify the fields and press SAVE to update the record."
    )

# save edit

def save_edit():

    global editing_id

    if editing_id is None:
        messagebox.showerror(
            "Save Edit",
            "No record is currently selected for editing."
        )
        return

    try:
        update_sale(
            editing_id,
            product_entry.get(),
            category_entry.get(),
            int(quantity_entry.get()),
            float(price_entry.get()),
            date_entry.get()
        )

        messagebox.showinfo(
            "Success",
            "Record updated successfully."
        )

        editing_id = None
        refresh_table()

    except Exception:
        messagebox.showerror(
            "Error",
            "Invalid input or update failed. Please check the values."
        )

# search
def search_data():

    keyword = product_entry.get()

    data = search_sale(keyword)

    for item in tree.get_children():
        tree.delete(item)

    for row in data:
        tree.insert("", tk.END, values=row)

# overall report
def overall_report():

    total = total_sales()

    messagebox.showinfo(
        "Overall Sales",
        f"Overall Sales: PHP {total}"
    )

# daily report
def daily_report():

    total = daily_sales()

    messagebox.showinfo(
        "Daily Sales",
        f"Daily Sales: PHP {total}"
    )

# monthly report
def monthly_report():

    total = monthly_sales()

    messagebox.showinfo(
        "Monthly Sales",
        f"Monthly Sales: PHP {total}"
    )

# yearly report
def yearly_report():

    total = yearly_sales()

    messagebox.showinfo(
        "Yearly Sales",
        f"Yearly Sales: PHP {total}"
    )

# export csv
def export_csv():

    try:
        import csv

        rows = get_sales()

        with open("sales_export.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Product", "Category", "Quantity", "Price", "Total", "Date"])
            writer.writerows(rows)

        messagebox.showinfo(
            "Export CSV",
            "CSV exported to sales_export.csv"
        )
    except Exception as e:
        messagebox.showerror(
            "Export CSV",
            f"Could not export CSV: {e}"
        )

# sort data
def sort_data():

    choice = sort_option.get()

    if choice == "Category":
        rows = sort_by_category()
    elif choice == "Date":
        rows = sort_by_date()
    elif choice == "Total":
        rows = sort_by_total()
    else:
        messagebox.showerror(
            "Sort Records",
            "Please choose Category, Date, or Total from the sort dropdown."
        )
        return

    for item in tree.get_children():
        tree.delete(item)

    for row in rows:
        tree.insert("", tk.END, values=row)

# export excel
def export_excel():

    try:
        from openpyxl import Workbook

        rows = get_sales()

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Sales"

        headers = ["ID", "Product", "Category", "Quantity", "Price", "Total", "Date"]
        sheet.append(headers)

        for row in rows:
            sheet.append(row)

        workbook.save("sales_export.xlsx")

        messagebox.showinfo(
            "Export Excel",
            "Excel exported to sales_export.xlsx"
        )
    except ImportError:
        messagebox.showerror(
            "Export Excel",
            "openpyxl is required for Excel export. Install it with:\npython -m pip install openpyxl"
        )
    except Exception as e:
        messagebox.showerror(
            "Export Excel",
            f"Could not export Excel: {e}"
        )

# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=20)

# add button
tk.Button(
    button_frame,
    text="ADD",
    command=add_data,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=0, column=0, padx=5)

# delete button
tk.Button(
    button_frame,
    text="DELETE",
    command=delete_data,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=0, column=1, padx=5)

# search button
tk.Button(
    button_frame,
    text="SEARCH",
    command=search_data,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=0, column=2, padx=5)

# overall
tk.Button(
    button_frame,
    text="OVERALL",
    command=overall_report,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=0, column=3, padx=5)

# daily
tk.Button(
    button_frame,
    text="DAILY",
    command=daily_report,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=1, column=0, padx=5, pady=5)

# monthly
tk.Button(
    button_frame,
    text="MONTHLY",
    command=monthly_report,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=1, column=1, padx=5, pady=5)

# yearly
tk.Button(
    button_frame,
    text="YEARLY",
    command=yearly_report,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=1, column=2, padx=5, pady=5)

# chart
tk.Button(
    button_frame,
    text="CHART",
    command=sales_chart,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=1, column=3, padx=5, pady=5)

# csv
tk.Button(
    button_frame,
    text="CSV",
    command=export_csv,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=2, column=0, padx=5, pady=5)

# excel
tk.Button(
    button_frame,
    text="EXCEL",
    command=export_excel,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=2, column=1, padx=5, pady=5)

# edit
tk.Button(
    button_frame,
    text="EDIT",
    command=edit_data,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=2, column=2, padx=5, pady=5)

# save edit
tk.Button(
    button_frame,
    text="SAVE",
    command=save_edit,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=2, column=3, padx=5, pady=5)

# sort label
sort_option = tk.StringVar()

tk.Label(
    button_frame,
    text="Sort by:",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="red"
).grid(row=3, column=0, padx=5, pady=5)

sort_dropdown = ttk.Combobox(
    button_frame,
    textvariable=sort_option,
    values=["Category", "Date", "Total"],
    state="readonly",
    width=10
)
sort_dropdown.grid(row=3, column=1, padx=5, pady=5)

# sort button
tk.Button(
    button_frame,
    text="SORT",
    command=sort_data,
    bg="red",
    fg="white",
    font=("Arial", 10, "bold"),
    width=12
).grid(row=3, column=2, padx=5, pady=5)

# load records
refresh_table()

# run system
root.mainloop()