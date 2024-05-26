from tkinter import *
from tkinter import filedialog
import os
import pandas as pd
from algorithm import Apriori

file=""

def open_file_dialog():
    file_path = filedialog.askopenfilename()
    if file_path:
        global file
        file = file_path
        file_name = os.path.basename(file_path)
        label1.config(text=f"{file_name}")

def submit():
    percentage = float(txt1.get())
    min_support_count = float(txt2.get())
    min_confidence = float(txt3.get())
    global file
    result1, result2=Apriori(file, min_support_count, min_confidence, percentage)
    view_results(result1, result2)  

def view_results(result1, result2):
    result_frame = Frame(frame, bg="white")
    result_frame.grid(row=7, column=0, columnspan=5, sticky="nsew") 

    canvas = Canvas(result_frame, bg="white")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(result_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = Frame(canvas, bg="white")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") 

    # Labels inside scrollable frame
    label5 = Label(scrollable_frame, text="Frequent Itemsets", font=('Arial', 16, 'bold'), fg="black", bg="white")
    label5.grid(row=0, column=0) 

    label6 = Label(scrollable_frame, text=result1, font=('Arial', 16), fg="black", bg="white")
    label6.grid(row=1, column=0) 

    label7 = Label(scrollable_frame, text="Strong Association Rules", font=('Arial', 16, 'bold'), fg="black", bg="white")
    label7.grid(row=2, column=0) 

    label8 = Label(scrollable_frame, text=result2, font=('Arial', 16), fg="black", bg="white")
    label8.grid(row=3, column=0) 


# Create root window
root = Tk()
root.configure(bg="white")
root.title("Data Mining Assignment 1")

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set root window dimensions and center widgets
root.geometry(f"{screen_width}x{screen_height}")

# Create a frame to hold the widgets
frame = Frame(root, bg="white")
frame.pack()  # Expand to fill the window


# Create widgets inside the frame
title = Label(frame, text="Problem 1 Using Apriori Algorithm", font=('Arial', 16, 'bold'), fg="pink", bg="white")
title.grid(row=0, column=1)  # Add vertical padding

btn1 = Button(frame, text="Upload File", command=open_file_dialog, fg="white", bg="pink", font=('Arial', 16))
btn1.grid(row=1, column=1)
  
label1 =Label(frame, text="", font=('Arial', 16), fg="pink", bg="white")  
label1.grid(row=2, column=1)

label2 = Label(frame, text="Percentage of the file to use: ", font=('Arial', 16), fg="pink", bg="white")
label2.grid(row=3, column=0)

txt1 = Entry(frame, width=20, fg="white", bg="pink", font=('Arial', 16))
txt1.grid(row=3, column=2)

label3 = Label(frame, text="Minimum Support Count: ", font=('Arial', 16), fg="pink", bg="white")
label3.grid(row=4, column=0)

txt2 = Entry(frame, width=20,font=('Arial', 16), fg="white", bg="pink")
txt2.grid(row=4, column=2)

label4 = Label(frame, text="Minimum Confidence: ", font=('Arial', 16), fg="pink", bg="white")
label4.grid(row=5, column=0)

txt3 = Entry(frame, width=20,font=('Arial', 16), fg="white", bg="pink")
txt3.grid(row=5, column=2)

btn2 = Button(frame, text="Submit",font=('Arial', 16), fg="white", bg="pink", command=submit)
btn2.grid(row=6, column=1)

root.mainloop()
