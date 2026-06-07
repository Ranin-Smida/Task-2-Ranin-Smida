import customtkinter as ctk
from tkinter import messagebox
import json
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

FONT_FAMILY = "Georgia"

FILE_NAME = "expenses.json"


expenses = []
budget = 0


if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as file:
        expenses = json.load(file)


def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file)


def add_expense():
    amount = amount_entry.get()
    category = category_menu.get()

    if amount == "":
        messagebox.showerror("Error", "Enter an amount")
        return

    try:
        amount = float(amount)

        expense = {
            "amount": amount,
            "category": category
        }

        expenses.append(expense)

        save_data()

        messagebox.showinfo("Success", "Expense Added")

        amount_entry.delete(0, "end")

        update_total()
        show_history()

    except:
        messagebox.showerror("Error", "Enter a valid number")


def update_total():
    total = 0

    for expense in expenses:
        total = total + expense["amount"]

    total_label.configure(text=f"Total Spent: {total} DT")

    if budget > 0:
        remaining = budget - total

        budget_label.configure(
            text=f"Remaining Budget: {remaining} DT"
        )

        if total > budget:
            warning_label.configure(
                text=" Budget Exceeded!",
                text_color="red"
            )
        else:
            warning_label.configure(text="")


def set_budget():
    global budget

    value = budget_entry.get()

    if value == "":
        return

    try:
        budget = float(value)

        messagebox.showinfo(
            "Budget",
            f"Budget set to {budget} DT"
        )

        update_total()

    except:
        messagebox.showerror(
            "Error",
            "Enter a valid budget"
        )


def show_history():
    history_box.delete("0.0", "end")

    for i, expense in enumerate(expenses, start=1):
        text = (
            f"{i}. "
            f"{expense['category']} - "
            f"{expense['amount']} DT\n"
        )

        history_box.insert("end", text)


def clear_expenses():
    global expenses

    answer = messagebox.askyesno(
        "Confirm",
        "Delete all expenses?"
    )

    if answer:
        expenses = []

        save_data()

        update_total()
        show_history()


def reset_inputs():
    amount_entry.delete(0, "end")
    budget_entry.delete(0, "end")
    category_menu.set("Food")
    warning_label.configure(text="")


app = ctk.CTk()
app.geometry("600x1080")
app.title("Smart Expense Tracker")
app.configure(fg_color="#F7F3EE")

title_label = ctk.CTkLabel(
    app,
    text="Smart Expense Tracker",
    font=(FONT_FAMILY, 32, "bold"),
    text_color="#2E2A27"
)

title_label.pack(pady=20)


budget_entry = ctk.CTkEntry(
    app,
    placeholder_text="Set your budget",
    height=40,
    font=(FONT_FAMILY, 16),
    fg_color="#FFFFFF",
    text_color="#2E2A27",
    border_color="#C9B8A8"
)

budget_entry.pack(pady=10, padx=30, fill="x")

budget_button = ctk.CTkButton(
    app,
    text="Set Budget",
    command=set_budget,
    height=42,
    font=(FONT_FAMILY, 18, "bold"),
    fg_color="#3A6EA5",
    hover_color="#315E8D"
)

budget_button.pack(pady=(5, 10))

expense_row = ctk.CTkFrame(app, fg_color="transparent")
expense_row.pack(pady=10, fill="x", padx=30)

amount_entry = ctk.CTkEntry(
    expense_row,
    placeholder_text="Enter expense amount",
    height=40,
    font=(FONT_FAMILY, 16),
    fg_color="#FFFFFF",
    text_color="#2E2A27",
    border_color="#C9B8A8"
)

amount_entry.pack(side="left", padx=(0, 12), fill="x", expand=True)

category_menu = ctk.CTkOptionMenu(
    expense_row,
    values=[
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Entertainment",
        "Other"
    ],
    height=40,
    font=(FONT_FAMILY, 16),
    fg_color="#E6D5C6",
    button_color="#C9B8A8",
    button_hover_color="#B59E8B",
    text_color="#2E2A27"
)
category_menu.pack(side="right")

add_button = ctk.CTkButton(
    app,
    text="Add Expense",
    command=add_expense,
    height=42,
    font=(FONT_FAMILY, 18, "bold"),
    fg_color="#1E7A6E",
    hover_color="#18665C"
)
add_button.pack(pady=(5, 10))

total_label = ctk.CTkLabel(
    app,
    text="Total Spent: 0 DT",
    font=(FONT_FAMILY, 22, "bold"),
    text_color="#2E2A27"
)

total_label.pack(pady=15)


budget_label = ctk.CTkLabel(
    app,
    text="Remaining Budget: 0 DT",
    font=(FONT_FAMILY, 18),
    text_color="#2E2A27"
)

budget_label.pack()


warning_label = ctk.CTkLabel(
    app,
    text="",
    font=(FONT_FAMILY, 18, "bold"),
    text_color="#B0452D"
)

warning_label.pack(pady=5)


history_title = ctk.CTkLabel(
    app,
    text="Expense History",
    font=(FONT_FAMILY, 22, "bold"),
    text_color="#2E2A27"
)

history_title.pack(pady=10)

history_box = ctk.CTkTextbox(
    app,
    width=440,
    height=220,
    font=(FONT_FAMILY, 15),
    fg_color="#FFFFFF",
    text_color="#2E2A27",
    border_color="#C9B8A8"
)

history_box.pack(pady=10)


reset_button = ctk.CTkButton(
    app,
    text="Reset Inputs",
    fg_color="#6C7A89",
    hover_color="#5A6673",
    command=reset_inputs,
    height=40,
    font=(FONT_FAMILY, 16, "bold")
)

reset_button.pack(pady=(5, 8))


clear_button = ctk.CTkButton(
    app,
    text="Clear Expenses",
    fg_color="#C0412D",
    hover_color="#A33626",
    command=clear_expenses,
    height=40,
    font=(FONT_FAMILY, 16, "bold")
)

clear_button.pack(pady=15)


update_total()
show_history()

app.mainloop()