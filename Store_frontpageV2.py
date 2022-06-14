####################  IMPORTS  #######################
from email.errors import MessageError
from tkinter import *
from tkinter import ttk
from functools import partial
from tkinter import messagebox
import tkinter as tk
import sqlite3
import os
import subprocess

##################  CLASS CODE  ######################
# Create the Account class
class Account:
  """The Account class stores the details of each account and has methods to deposit, withdraw and calculate progress towards the savings goal"""
  def __init__(self, name, balance):
    self.name = name
    self.balance = float(balance)
    account_list.append(self)

  # Deposit method adds money to balance
  def deposit(self, amount):
    if amount > 0:
      self.balance += amount
      return True
    else:
      return False

  # Withdraw method subtracts money from balance
  def withdraw(self, amount):
    if amount <= self.balance and amount > 0:
      self.balance -= amount
      return True
    else:
      return False

  # Get progress method calculates goal progress
  def get_progress(self):
    progress = (self.balance) * 100
    return progress


##############  FUNCTIONS AND SETUP ###############
# Create a function to read data from the file
def get_data():
  account_file = open("book2.txt","r")
  line_list = account_file.readlines()

  for line in line_list:
    account_data = line.strip().split(",")
    Account(*account_data)

  account_file.close()
    
    
# Create a function to get account names list
def create_name_list():
  name_list = []
  for account in account_list:
    name_list.append(account.name)
  return name_list

# Create a function that will update the balance.
def update_balance():
  total_balance = 0
  balance_string = ""
  account_file = open("book2.txt", "w")

  # Append each accounts balance, progress and goal to the label
  for account in account_list:
    progress = account.get_progress()
    balance_string += "{}: {:.2f}\n".format(account.name, account.balance)
    total_balance += account.balance
    account_file.write("{},{}\n".format(account.name, account.balance))
  balance_string += "\nTotal balance: {:.2f}".format(total_balance)
  account_details.set(balance_string)
  account_file.close()
# Create the deposit function
def restock_money(account):
  if account.deposit(amount.get()):
    messagebox.showinfo("Information", "Success! Total of {:.2f} {} books restocked".format(amount.get(), account.name))
  else:
    messagebox.showerror("Error", "Please enter a positive number")

# Create the withdraw function
def sell_money(account):
  if account.withdraw(amount.get()):
    messagebox.showinfo("Information", "Success! Total of {:.2f} {} books sold".format(amount.get(), account.name))
  else:
    messagebox.showerror("Error", "Not enough {} books available or not a valid amount".format(account.name))

# Create the manage action function
def manage_action():
  try:
    for account in account_list:
      if chosen_account.get() == account.name:
        if chosen_action.get() == "Restock":
          restock_money(account)
        else:
          sell_money(account)

    # Update the GUI
    update_balance()
    amount.set("")

  # Add an exception for text input
  except ValueError:
    messagebox.showerror("Error", "Please enter a valid number")

# Set up Lists
account_list = []

# Create instances of the class
get_data()
book_names = create_name_list()

##################  FRAMING  ######################
root = tk.Tk()
root.title("Book Store")
root.geometry('270x340')
root.configure(bg="#FFD966")


def logout():
  confirm_logout = messagebox.askyesno("Question", "Are you sure you want to logout?")
  if confirm_logout:
    root.destroy()
    subprocess.call(["python", "Registration_formV2.py"])
    
# Create the bottom frame
bottom_frame = Frame(root, bg="#FFF2CC", bd=2, relief=SOLID, padx=60, pady=10)
bottom_frame.place(x=5, y=160)

# Create and set the account details variable
account_details = StringVar()

# Frame for stock levels header
stock_frame = Frame(bottom_frame, bg='#FFD966', relief=SOLID, bd=2)
stock_frame.grid(row=0, column=1)

# Stock Levels Header
stock_text = Label(stock_frame, text="STOCK LEVELS", bg="#FFD966", font=('New Roman', 10, 'bold'))
stock_text.grid(row=0, column=1)

# Create the details label and pack it into the GUI
details_label = Label(bottom_frame, textvariable=account_details, bg="#FFF2CC")
details_label.grid(row=2, column=1)

# Create the top frame
top_frame = LabelFrame(root, bg="#FFF2CC", bd=2, relief=SOLID, padx=10, pady=10)
top_frame.place(x=5, y=1)


# Create a label for the account combobox
account_label = Label(top_frame, text="Book: ", bg="#FFF2CC")
account_label.grid(row=3, column=0, padx=10, pady=3)

# Set up a variable and option list for the account Combobox
chosen_account = StringVar()
chosen_account.set(book_names[0])

# Create a Combobox to select the account
account_box = ttk.Combobox(top_frame, textvariable=chosen_account, state="readonly")
account_box['values'] = book_names
account_box.grid(row=3, column=1, padx=10, pady=3, sticky="WE")

# Create a label for the action Combobox
action_label = Label(top_frame, text="Action:", bg="#FFF2CC")
action_label.grid(row=4, column=0)

# Set up a variable and option list for the action Combobox
action_list = ["Sell", "Restock"]
chosen_action = StringVar()
chosen_action.set(action_list[0])

# Create the Combobox to select the action
action_box = ttk.Combobox(top_frame, textvariable=chosen_action, state="readonly")
action_box['values'] = action_list
action_box.grid(row=4, column=1, padx=10, pady=3, sticky="WE")

# Create a label for the amount field and pack it into the GUI
amount_label = Label(top_frame, text="Amount:", bg="#FFF2CC")
amount_label.grid(row=5, column=0, padx=10, pady=3)

# Create a variable to store the amount
amount = DoubleVar()
amount.set("")

# Create an entry to type in amount
amount_entry = ttk.Entry(top_frame, textvariable=amount)
amount_entry.grid(row=5, column=1, padx=10, pady=3, sticky="WE")
  
# Creating the button frames
logout_buttonframe = tk.Frame(root, highlightbackground = "black")

# Create a submit button
submit_button = Button(top_frame, width=10, text="Submit", relief=SOLID, bg="#FFF2CC", cursor='hand2', command=manage_action)
submit_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Create a logout button
logout_button = Button(bottom_frame, width=15, text='Logout', relief=SOLID, bg="#FFF2CC", cursor='hand2',command=logout)
logout_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Create an action feedback label

# Run the mainloop
update_balance()
root.mainloop()
