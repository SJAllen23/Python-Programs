import csv
import tkinter as tk
from tkinter import messagebox

# Callback for adding expense to the CSV
def add_expense():
    date = date_entry.get()
    description = description_entry.get()
    amount = amount_entry.get()

    # Splitting and validating date format
    date_parts = date.split('-')
    if len(date_parts) != 3:
        messagebox.showerror("Error", "Invalid date format!")
        return

    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])

    if not (1 <= month <= 12 and 1 <= day <= 31):
        messagebox.showerror("Error", "Invalid date!")
        return

    # Validating amount format
    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount format!")
        return

    # Writing to the CSV
    with open("expenses.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, description, amount])

    messagebox.showinfo("Info", "Expense added successfully!")

# Callback for displaying the summary
def show_summary():
    total_amount = 0.0
    largest_expense = ('', 0.0)
    try:
        with open("expenses.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # skipping header
            for row in reader:
                date, description, amount = row
                total_amount += float(amount)
                if float(amount) > largest_expense[1]:
                    largest_expense = (description, float(amount))
    except Exception as e:
        messagebox.showerror("Error", f"Error reading data: {e}")
        return

    summary = f"Total Expenses: ${total_amount:.2f}\n"
    summary += f"Largest Expense: {largest_expense[0]} - ${largest_expense[1]:.2f}"
    messagebox.showinfo("Summary", summary)

# Setting up the GUI
root = tk.Tk()
root.title("Expense Tracker")

# Labels and Entry Widgets
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1)

tk.Label(root, text="Description:").grid(row=1, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=1, column=1)

tk.Label(root, text="Amount:").grid(row=2, column=0)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1)

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).grid(row=3, column=0, columnspan=2)
tk.Button(root, text="Show Summary", command=show_summary).grid(row=4, column=0, columnspan=2)

# Initializing the CSV file with header if doesn't exist
try:
    with open("expenses.csv", "x", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Description", "Amount"])
except FileExistsError:
    pass

root.mainloop()
