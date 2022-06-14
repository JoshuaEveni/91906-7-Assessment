from tkinter import *
from tkinter import messagebox
from functools import partial
from tkinter import ttk
import tkinter as tk
from tkinter import scrolledtext
import sqlite3
import os
import subprocess

f = ('Times', 14)

####### SETUP OF DATABASE ##########
con = sqlite3.connect('profiledataV3.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS record (
                    firstname text,
                    lastname text,
                    email text,
                    contact number, 
                    gender text, 
                    password text,
                    country text
                )
            ''')
con.commit()

            
######## MAIN WINDOW SETUP ############
mainw = Tk()
mainw.title('Login')
mainw.geometry('1000x550')
mainw.config(bg='#D6B656')

############### SETUP OF DATABASE RECORDS ###############
def insert_record():
    check_counter=0
    warn = ""
    if register_firstname.get() == "":
       warn = "First name can't be empty"
    else:
        check_counter += 1

    if register_lastname.get() == "":
        warn = "Last name can't be empty"
    else:
        check_counter += 1
        
    if register_email.get() == "":
        warn = "Email can't be empty"
    else:
        check_counter += 1

    if register_mobile.get() == "":
        warn = "Contact Number cannot be left empty"
    else:
        check_counter += 1
        
    number_verify = True
    while number_verify == True:
       if register_mobile.get().isalpha():
            warn = "Contact Number cannot contain letters"
            number_verify = False
       else:
            check_counter += 1
            number_verify = False

    if  vargen.get() == "":
        warn = "Select Gender"
    else:
        check_counter += 1

    if register_country.get() == "":
       warn = "Select Country"
    else:
        check_counter += 1

    if register_password.get() == "":
        warn = "Password can't be empty"
    else:
        check_counter += 1

    if password_again.get() == "":
        warn = "Re-enter password can't be empty"
    else:
        check_counter += 1

    if register_password.get() != password_again.get():
        warn = "Passwords didn't match!"
    else:
        check_counter += 1

    if check_counter == 10:        
        try:
            con = sqlite3.connect('profiledataV3.db')
            cur = con.cursor()
            cur.execute("INSERT INTO record VALUES (:firstname, :lastname, :email, :contact, :gender, :password, :country)", {
                            'firstname': register_firstname.get(),
                            'lastname': register_lastname.get(),
                            'email': register_email.get(),
                            'contact': register_mobile.get(),
                            'gender': vargen.get(),
                            'password': register_password.get(),
                            'country': register_country.get()

            })
            con.commit()
            messagebox.showinfo('confirmation', 'Record Saved')

        except Exception as ep:
            messagebox.showerror('', ep) 
    else:
        messagebox.showerror('Error', warn)

####### RESPONSE TO LOGIN ##########

# functions
def login_response():
    try:
        con = sqlite3.connect('profiledataV3.db') # attaching login to database
        c = con.cursor()
        for row in c.execute("Select * from record"):
            firstname = row[1]
            password = row[6]
        
    except Exception as ep:
        messagebox.showerror('', ep)

    firsname = firstname_tf.get()
    userpwd = password_tf.get()
    check_counter1=0
    
    if firsname == "":
       warn = "Firstname can't be empty"
    else:
        check_counter1 += 1
        
    if userpwd == "":
        warn = "Password can't be empty"
    else:
        check_counter1 += 1
         
    if check_counter1 == 2:
        if firsname == firstname and userpwd == password:
            mainw.destroy()
            subprocess.call(["python", "Store_frontpageV2.py"])
        else:
            messagebox.showerror('Error', 'Invalid Name Or Password')
    else:
        messagebox.showerror('', warn)

def hide():
    mainw.withdraw()

def show():
    mainw.deiconify()

# Country list
vargen = StringVar()
vargen.set('male')
    
######### STRUCTURE ################

# background image
background_image = PhotoImage(file='bakground-registration.png')
background_label = Label(mainw, i=background_image)
background_label.pack()
# Frames
left_frame = Frame(mainw, bd=2, bg='#FFF2CC', relief=SOLID, padx=10, pady=10)
right_frame = Frame(mainw, bd=2, bg='#FFF2CC',relief=SOLID, padx=10, pady=10)
gender_frame = LabelFrame(right_frame,bg='#FFF2CC',padx=10, pady=10,)

# Headings for registration and login
registration_header_frame = Frame(right_frame, bd=2, bg='#FFFBBD', relief=GROOVE, padx=50, pady=1)
registration_header_frame.grid(row=1, column=0)
registration_header = Label(registration_header_frame, text="Registration", fg='black', bg='#FFFBBD', font=('Helvetica', 15, 'bold'))
registration_header.grid(row=1, column=0)
registration_header.configure(justify='center')

login_header_frame = Frame(left_frame, bd=2, bg='#FFFBBD', relief=GROOVE, padx=50, pady=1)
login_header_frame.grid(row=0, column=0)
login_header = Label(login_header_frame, text="Login", fg='black', bg='#FFFBBD', font=('Helvetica', 15, 'bold'))
login_header.grid(row=0, column=1)
login_header.configure(justify='center')

# Labels
Label(left_frame, text="Enter Firstname", bg='#FFF2CC', fg='lightgrey', font=f).grid(row=1, column=0, sticky=W, pady=10)
Label(left_frame, text="Enter Password", bg='#FFF2CC', fg='lightgrey', font=f).grid(row=2, column=0, pady=10)
Label(left_frame, text="Enter Firstname", bg='#FFF2CC', font=f).grid(row=1, column=0, sticky=W, pady=10)
Label(left_frame, text="Enter Password", bg='#FFF2CC',font=f).grid(row=2, column=0, pady=10)
Label(right_frame, text="Enter Firstname", bg='#FFF2CC',font=f).grid(row=2, column=0, sticky=W, pady=10)
Label(right_frame,text="Enter Lastname",bg='#FFF2CC',font=f).grid(row=3, column=0, sticky=W, pady=10)
Label(right_frame, text="Enter Email", bg='#FFF2CC',font=f).grid(row=4, column=0, sticky=W, pady=10)
Label(right_frame, text="Contact Number", bg='#FFF2CC',font=f).grid(row=5, column=0, sticky=W, pady=10)
Label(right_frame, text="Select Gender", bg='#FFF2CC',font=f).grid(row=6, column=0, sticky=W, pady=10)
Label(right_frame, text="Select Country", bg='#FFF2CC',font=f).grid(row=7, column=0, sticky=W, pady=10)
Label(right_frame, text="Enter Password", bg='#FFF2CC',font=f).grid(row=8, column=0, sticky=W, pady=10)
Label(right_frame, text="Re-Enter Password", bg='#FFF2CC',font=f).grid(row=9, column=0, sticky=W, pady=10)

# Entries
firstname_tf = Entry(left_frame, font=f)
password_tf = Entry(left_frame, font=f,show='*')
register_password = Entry(right_frame, font=f,show='*')
password_again = Entry(right_frame, font=f,show='*')
register_firstname = Entry(right_frame, font=f)
register_lastname = Entry(right_frame,font=f)
register_email = Entry(right_frame, font=f)
register_mobile = Entry(right_frame, font=f)

# Radio Buttons
male_rb = Radiobutton(gender_frame, text='Male',bg='#FFF2CC',variable=vargen,value='male',font=('Times', 10),)
female_rb = Radiobutton(gender_frame,text='Female',bg='#FFF2CC',variable=vargen,value='female',font=('Times', 10),)
others_rb = Radiobutton(gender_frame,text='Others',bg='#FFF2CC',variable=vargen,value='others',font=('Times', 10))

# Combobox
countries = []
with open('countries.txt') as inFile:
    countries = [line for line in inFile]
register_country = ttk.Combobox(right_frame, state="readonly")
register_country.config(width=15, font=('Times', 12))
register_country['values'] = tuple(countries)

# Buttons
register_btn = Button(right_frame, width=15, text='Register', font=f, relief=SOLID, cursor='hand2',command=insert_record)
login_btn = Button(left_frame, width=15, text='Login', font=f, relief=SOLID, cursor='hand2',command=login_response)

# Placements/grids
firstname_tf.grid(row=1, column=1, pady=10, padx=20)
password_tf.grid(row=2, column=1, pady=10, padx=20)
login_btn.grid(row=3, column=1, pady=10, padx=20)
left_frame.place(x=50, y=150)

register_firstname.grid(row=2, column=1, pady=10, padx=20)
register_lastname.grid(row=3, column=1, pady=10, padx=20)
register_email.grid(row=4, column=1, pady=10, padx=20) 
register_mobile.grid(row=5, column=1, pady=10, padx=20)
register_country.grid(row=7, column=1, pady=10, padx=20)
register_password.grid(row=8, column=1, pady=10, padx=20)
password_again.grid(row=9, column=1, pady=10, padx=20)
register_btn.grid(row=10, column=1, pady=10, padx=20)
right_frame.place(x=500, y=15)

gender_frame.grid(row=6, column=1, pady=10, padx=20)
male_rb.pack(expand=True, side=LEFT)
female_rb.pack(expand=True, side=LEFT)
others_rb.pack(expand=True, side=LEFT)
    

    


    
# infinite loop
mainw.mainloop()
