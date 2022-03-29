from tkinter import *
from tkinter import messagebox
from functools import partial
from tkinter import ttk
from tkinter import scrolledtext
import random
import time
import sqlite3
import os

f = ('Times', 14)

####### SETUP OF DATABASE ##########
con = sqlite3.connect('userdata.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS record(
                    name text, 
                    email text,
                    username text,
                    contact number, 
                    gender text, 
                    country text,
                    password text
                )
            ''')
con.commit()

            
######## MAIN WINDOW SETUP ############
ws = Tk()
ws.title('Login')
ws.geometry('940x500')
ws.config(bg='#EDD94C')

############### SETUP OF DATABASE RECORDS ###############
def insert_record():
    check_counter=0
    warn = ""
    if register_name.get() == "":
       warn = "Name can't be empty"
    else:
        check_counter += 1
        
    if register_email.get() == "":
        warn = "Email can't be empty"
    else:
        check_counter += 1

    if register_mobile.get() == "":
       warn = "Contact can't be empty"
    else:
        check_counter += 1
    
    if  var.get() == "":
        warn = "Select Gender"
    else:
        check_counter += 1

    if variable.get() == "":
       warn = "Select Country"
    else:
        check_counter += 1

    if register_pwd.get() == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1

    if pwd_again.get() == "":
        warn = "Re-enter password can't be empty"
    else:
        check_counter += 1

    if register_pwd.get() != pwd_again.get():
        warn = "Passwords didn't match!"
    else:
        check_counter += 1

    if check_counter == 8:        
        try:
            con = sqlite3.connect('userdata.db')
            cur = con.cursor()
            cur.execute("INSERT INTO record VALUES (:name, :email, :contact, :gender, :country, :password)", {
                            'name': register_name.get(),
                            'email': register_email.get(),
                            'contact': register_mobile.get(),
                            'gender': var.get(),
                            'country': variable.get(),
                            'password': register_pwd.get()

            })
            con.commit()
            messagebox.showinfo('confirmation', 'Record Saved')

        except Exception as ep:
            messagebox.showerror('', ep) 
    else:
        messagebox.showerror('Error', warn)
# Functions
def hide():
    ws.withdraw()

def show():
    ws.deiconify()

############### CREATING NEW WINDOW ##########################
def openNewWindow():
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(ws)
    
    # sets the title of the
    # Toplevel widget
    newWindow.title("____")
 
    # sets the geometry of toplevel
    newWindow.geometry("800x510")

    #configures the colour
    newWindow.configure(bg='darkgrey')

    ############ STOCK DATABASE ####################
    con = sqlite3.connect('stockdatabase.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS record(
                    superdude number,
                    lizardman number,
                    waterwoman number
                    )
                ''')
    con.commit()
    
    superdudevalue = 8
    lizardmanvalue = 12
    waterwomanvalue = 3
    
    cur.execute('INSERT INTO record VALUES(8, 12, 3)')
    con.commit()

    ########## PURCHASE TRACKER DATABASE #############
    con = sqlite3.connect('purchasetracker.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS record(
                    name text,
                    email text,
                    contact number,
                    book purchased text,
                    date number,
                    purchasesmade number
                    )
                ''')

    class contact_info:
        counter = 0

        if name.get() == "":
            warn = "Please enter your name."
        else:
            counter += 1

        if counter == 1:
            try:
                con = sqlite3.connect('purchasetracker.db')
                cur = con.cursor()
                cur.execute("INSERT INTO record VALUES (:name)", {
                    'name': name.get()
                })
                con.commit()

            except Exception as ep:
                messagebox.showerror('', ep)

        else: 
            messagebox.showerror('Error', warn)
    ########## newWindow FUNCTIONS #################
    class Account:
        def __init__(self, name, stock):
            self.name = name
            self.stock = float(stock)
            account_list.append(self)

        def deposit(self, amount):
            if amount > 0:
                self.stock += amount
                return True
            else:
                return False

        def withdraw(self, amount):
            if amount <= self.stock and amount > 0:
                self.stock -= amount
                return True
            else:
                return False

        def get_progress(self):
            progress = self.stock * 100
            return progress
        
    def get_data():
        account_file = open("accounts.txt", "r")
        line_list = account_file.readlines()

        for line in line_list:
            account_data = line.strip().split(",")
            Account(*account_data)

        account_file.close()
    
    
    def create_name_list():
        name_list = []
        for account in account_list:
            name_list.append(account.name)
        return name_list

    def update_balance():
        total_stock = 0
        balance_string = ""
        account_file = open("accounts.txt", "w")

        for account in account_list:
            progress = account.get_progress()
            balance_string += "{}: {}".format(account.name, account.stock)
            total_stock += account.stock
            account_file.write("{},{}\n".format(account.name, account.stock))

        balance_string += "\nTotal stock: {}".format(total_stock)
        account_details.set(balance_string)
        account_file.close()

    def deposit_money(account):
        if account.deposit(amount.get()):
            message = random.choice(deposit_messages)
            message_text.set(message)
            messagebox.showinfo("Information", "Success! Total of {} {} books returned!".format(amount.get(), account.name))
            
        else:
            messagebox.showerror("Error", "Please try again")
            update()
            

    def withdraw_money(account):
        if account.withdraw(amount.get()):
            message = random.choice(withdraw_messages)
            message_text.set(message)
            messagebox.showinfo("Information", "Success! Total of {} {} books purchased!.".format(amount.get(), account.name))
            
        else:
            messagebox.showerror("Error", "Not enough of this book in stock!")
            update()
            

    def transaction():
        pass
    
    def logout():
        question = messagebox.askquestion("Logout?", "Are you sure you want to logout?")
        if question == 'yes':
            newWindow.destroy()
            show()
            messagebox.showinfo("Success", "You have been successfully logged out.")
            pwd_tf = ""
    
    def manage_action():
        try:
            for account in account_list:
                if chosen_account.get() == account.name:
                    if chosen_action.get() == "Return":
                        deposit_money(account)
                    else:
                        withdraw_money(account)

            update_balance()
            amount.set("")

        except ValueError:
            action_feedback.set("Please enter a valid number")

    # Lists and account setup
    account_list = []
    deposit_messages = ["Item returned successfully!"]
    withdraw_messages = ["Item purchased successfully"]
    deposit_messages_fail = ["Return Failed!"]
    withdraw_messages_fail = ["Purchase Failed!"]

    superdude = Account("SuperDude", 8)
    waterwoman = Account("WaterWoman", 3)
    lizardman = Account("LizardMan", 12)
    account_names = create_name_list()

    ########### newWindow STRUCTURE ####################

    # Frames
    top_frame = Frame(newWindow, bd=2, bg='#EDD94C', relief=SOLID, padx=10, pady=10)
    top_frame.grid(row=0, column=0, padx=15, pady=15, sticky="NSEW")

    bottom_frame = Frame(newWindow, bd=2, bg='#EDD94C', relief=SOLID, padx=10, pady=10)
    bottom_frame.grid(row=1, column=0, padx=15, pady=15, sticky="NSEW")

    right_frame = Frame(newWindow, bd=2, bg='#EDD94C', relief=SOLID, padx=10, pady=10)
    right_frame.grid(row=1, column=3, padx=15, pady=15, sticky="NSEW")

    # Create and set the message text variable
    message_text = StringVar()
    message_text.set("Welcome to the book store! Purchase or return a book using the form on the left!")

    # Create an pack image label
    message_label = Label(top_frame, textvariable=message_text, wraplength=250, bg='#EDD94C')
    message_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Creating image labels
    success_image = PhotoImage(file="G:/My Drive/13DGT - 2022/Python GUI - 3.7/small-check-mark-icon-0.jpg")
    failed_image = PhotoImage(file="G:/My Drive/13DGT - 2022/Python GUI - 3.7/x-small-256x256.png")

    # Welcome message
    image_label = Label(top_frame, text="WELCOME!", font='Helvetica 18 bold', bg='#EDD94C')
    image_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # contact info
    contact_name = Label(bottom_frame, text="Name:", bg='#EDD94C')
    contact_name.grid(row = 6, column = 0, padx=10, pady=3)
    name = DoubleVar()
    name.set("")
    name_entry = ttk.Entry(bottom_frame, textvariable=name)
    name_entry.grid(row=6, column=1, padx=10, pady=3, sticky="WE")
    
    # account details
    account_details = StringVar()

    details_label = Label(top_frame, textvariable=account_details, bg='#EDD94C')
    details_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    
    account_label = Label(bottom_frame, text="Account: ", bg='#EDD94C')
    account_label.grid(row=3, column=0, padx=10, pady=3)

    chosen_account = StringVar()
    chosen_account.set(account_names[0])

    account_box = ttk.Combobox(bottom_frame, textvariable=chosen_account, state="readonly")
    account_box['values'] = account_names
    account_box.grid(row=3, column=1, padx=10, pady=3, sticky="WE")

    # Selected action the user is wanting to make
    action_label = Label(bottom_frame, text="Action:", bg='#EDD94C')
    action_label.grid(row=4, column=0)

    action_list = ["Return", "Purchase"]
    chosen_action = StringVar()
    chosen_action.set(action_list[0])

    action_box = ttk.Combobox(bottom_frame, textvariable=chosen_action, state="readonly")
    action_box['values'] = action_list
    action_box.grid(row=4, column=1, padx=10, pady=3)

    amount_label = Label(bottom_frame, text="Amount:", bg='#EDD94C')
    amount_label.grid(row=5, column=0, padx=10, pady=3)

    amount = DoubleVar()
    amount.set("")

    amount_entry = ttk.Entry(bottom_frame, textvariable=amount)
    amount_entry.grid(row=5, column=1, padx=10, pady=3, sticky="WE")

    ########################## BUTTONS #####################################

    # logout button
    logout_button = Button(bottom_frame, text="Logout", command=logout, bg='white')
    logout_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    # submit button
    submit_button = Button(bottom_frame, text="Submit", command=manage_action, bg='white')
    submit_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    # updating the balance
    action_feedback = StringVar()
    action_feedback_label = ttk.Label(bottom_frame, textvariable=action_feedback)
    action_feedback_label.grid(row=1, column=0, columnspan=2)

    update_balance()

####### RESPONSE TO LOGIN ##########  
def login_response():
    try:
        con = sqlite3.connect('userdata.db') # attaching login to database
        c = con.cursor()
        for row in c.execute("Select * from record"):
            username = row[1]
            pwd = row[5]
        
    except Exception as ep:
        messagebox.showerror('', ep)

    uname = email_tf.get()
    upwd = pwd_tf.get()
    check_counter=0
    if uname == "":
       warn = "Username can't be empty"
    else:
        check_counter += 1
    if upwd == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1
    if check_counter == 2:
        if (uname == username and upwd == pwd):
            openNewWindow()
            hide()
            
        else:
            messagebox.showerror('Login Status', 'invalid username or password')
    else:
        messagebox.showerror('', warn)

    
var = StringVar()
var.set('male')

countries = []
variable = StringVar()
world = open('countries.txt', 'r')
for country in world:
    country = country.rstrip('\n')
    countries.append(country)

# widgets
left_frame = Frame(
    ws, 
    bd=2, 
    bg='lightgrey',   
    relief=SOLID, 
    padx=10, 
    pady=10
    )

Label(
    left_frame, 
    text="Enter Email", 
    bg='lightgrey',
    font=f).grid(row=0, column=0, sticky=W, pady=10)

Label(
    left_frame, 
    text="Enter Password", 
    bg='lightgrey',
    font=f
    ).grid(row=1, column=0, pady=10)

email_tf = Entry(
    left_frame, 
    font=f
    )
pwd_tf = Entry(
    left_frame, 
    font=f,
    show='*'
    )
login_btn = Button(
    left_frame, 
    width=15, 
    text='Login', 
    font=f, 
    relief=SOLID,
    cursor='hand2',
    command=login_response
    )

right_frame = Frame(
    ws, 
    bd=2, 
    bg='lightgrey',
    relief=SOLID, 
    padx=10, 
    pady=10
    )

Label(
    right_frame, 
    text="Enter Name", 
    bg='lightgrey',
    font=f
    ).grid(row=0, column=0, sticky=W, pady=10)

Label(
    right_frame, 
    text="Enter Email", 
    bg='lightgrey',
    font=f
    ).grid(row=1, column=0, sticky=W, pady=10)

Label(
    right_frame, 
    text="Contact Number", 
    bg='lightgrey',
    font=f
    ).grid(row=3, column=0, sticky=W, pady=10)

Label(
    right_frame, 
    text="Select Gender", 
    bg='lightgrey',
    font=f
    ).grid(row=4, column=0, sticky=W, pady=10)

Label(
    right_frame, 
    text="Select Country", 
    bg='lightgrey',
    font=f
    ).grid(row=5, column=0, sticky=W, pady=10)

Label(
    right_frame, 
    text="Enter Password", 
    bg='lightgrey',
    font=f
    ).grid(row=6, column=0, sticky=W, pady=10)

Label(
    right_frame, 
    text="Re-Enter Password", 
    bg='lightgrey',
    font=f
    ).grid(row=7, column=0, sticky=W, pady=10)

gender_frame = LabelFrame(
    right_frame,
    bg='lightgrey',
    padx=10, 
    pady=10,
    )


register_name = Entry(
    right_frame, 
    font=f
    )

register_email = Entry(
    right_frame, 
    font=f
    )

register_mobile = Entry(
    right_frame, 
    font=f
    )


male_rb = Radiobutton(
    gender_frame, 
    text='Male',
    bg='lightgrey',
    variable=var,
    value='male',
    font=('Times', 10),
    
)

female_rb = Radiobutton(
    gender_frame,
    text='Female',
    bg='lightgrey',
    variable=var,
    value='female',
    font=('Times', 10),
  
)

others_rb = Radiobutton(
    gender_frame,
    text='Others',
    bg='lightgrey',
    variable=var,
    value='others',
    font=('Times', 10)
   
)

register_country = ttk.Combobox(
    right_frame,
    textvariable = variable,
    state='readonly',
    values=countries
)
register_country.config(
    width=20,
    font=('Times', 12)
)
register_pwd = Entry(
    right_frame, 
    font=f,
    show='*'
)

pwd_again = Entry(
    right_frame, 
    font=f,
    show='*'
)

register_btn = Button(
    right_frame, 
    width=15, 
    text='Register', 
    font=f, 
    relief=SOLID,
    cursor='hand2',
    command=insert_record
)


# widgets placement
email_tf.grid(row=0, column=1, pady=10, padx=20)
pwd_tf.grid(row=1, column=1, pady=10, padx=20)
login_btn.grid(row=2, column=1, pady=10, padx=20)
left_frame.place(x=50, y=150)

register_name.grid(row=0, column=1, pady=10, padx=20)
register_email.grid(row=1, column=1, pady=10, padx=20) 
register_mobile.grid(row=3, column=1, pady=10, padx=20)
register_country.grid(row=5, column=1, pady=10, padx=20)
register_pwd.grid(row=6, column=1, pady=10, padx=20)
pwd_again.grid(row=7, column=1, pady=10, padx=20)
register_btn.grid(row=8, column=1, pady=10, padx=20)
right_frame.place(x=500, y=50)

gender_frame.grid(row=4, column=1, pady=10, padx=20)
male_rb.pack(expand=True, side=LEFT)
female_rb.pack(expand=True, side=LEFT)
others_rb.pack(expand=True, side=LEFT)

# infinite loop
ws.mainloop()
