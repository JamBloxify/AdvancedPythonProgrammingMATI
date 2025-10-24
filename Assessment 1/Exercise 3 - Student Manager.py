from tkinter import *  # Import core tkinter functions
from tkinter import ttk  # Import ttk for Combobox
import customtkinter  # Import customtkinter for scrollable frame and modern widgets (Glad to have found this existed)

window = Tk()  # Create main window

# Read and extract student names from file
with open('Assessment 1/studentMarks.txt', 'r') as studentfiles:
    lines = studentfiles.readlines()  # Read all lines from file

numStudents = int(lines[0].strip())  # First line is the number of students
students = lines[1:]  # Ignore the first line cus the rest of the lines contain the real data

studentData = []  # Stores student data (code, name, marks, exam)
studentNames = []  # Stores student names for Combobox

# Loop through each student line and extract data
for line in students:
    data = line.strip().split(',')  # Remove whitespace and split by comma
    if len(data) >= 2:  # Checks if the lines have more than 2, just to make sure it doesn't break when the line has 1 data.
        studentCode = data[0]  # Student code
        studentName = data[1]  # Student name
        studentMarks = list(map(int, data[2:5]))  # Convert three coursework marks to integers
        studentExam = int(data[5])  # Convert exam mark to integer
        studentData.append((studentCode, studentName, studentMarks, studentExam))  # Add to main list
        studentNames.append(studentName)  # Add name to list for Combobox

# Function to calculate grade, total marks, percentage
def gradeCalc(studentMarks, studentExam):
    marktotal = sum(studentMarks)  # Sum of coursework marks
    exam = studentExam  # Exam mark
    total = marktotal + exam  # Total marks
    percentage = (total / 160) * 100  # Overall percentage (out of 160)
    grade = ('A' if percentage >= 70 
             else 'B' if percentage >= 60 
             else 'C' if percentage >= 50 
             else 'D' if percentage >= 40 
             else 'F')  # Determine grade based on percentage
    return marktotal, exam, percentage, grade  # Return all calculated values

# Function to clear all widgets in the scrollable frame
def clearFrame():
    for widget in frame.winfo_children():  # Loop through children widgets
        widget.destroy()  # Remove each widget

# Function to display a single student (For highest and lowest scores)
def displayStudent(student):
    clearFrame()  # Clear previous content
    code, name, marks, exam = student  # Unpack student tuple
    marktotal, exam, percentage, grade = gradeCalc(marks, exam)  # Calculate marks and grade

    info = [
        f"Name: {name}",
        f"Student Number: {code}",
        f"Coursework Total: {marktotal} / 60",
        f"Exam Mark: {exam} / 100",
        f"Overall Percentage: {percentage:.2f}%",
        f"Grade: {grade}"
    ]  # List of information in string

    for line in info:  # Add each info as a label in frame
        label = customtkinter.CTkLabel(frame, text=line, font=("Helvetica", 13), fg_color='transparent')
        label.pack(pady=5, anchor=CENTER)  # Pack with padding

# Function triggered when a student is selected from Combobox, and then displayed
def studentSelect(event):
    selectedStudent = studentCombo.get()  # Get selected name
    for student in studentData:  # Loop through students
        if student[1] == selectedStudent:  # Match by name
            displayStudent(student)  # Display the student's info
            break

# Function to display a list of students. Helps to not copy paste the same code over and over for sorting the displays.
def displayStudentsList(studentList):
    clearFrame()  # Clear previous content
    totalPercentage = 0
    for student in studentList:
        code, name, marks, exam = student
        marktotal, exam, percentage, grade = gradeCalc(marks, exam)
        totalPercentage += percentage

        info = (f"Name: {name} | "
                f"Student No: {code} | "
                f"Coursework: {marktotal}/60 | "
                f"Exam: {exam}/100 | "
                f"Overall: {percentage:.2f}% | "
                f"Grade: {grade}")
        
        label = customtkinter.CTkLabel(frame, text=info, font=("Helvetica", 13), fg_color='transparent')
        label.pack(padx=5, pady=5, anchor='w')  # Left aligns info

    totalAverage = totalPercentage / len(studentData) 

    information = (f"\nTotal Students: {numStudents} | " f"Class Average: {totalAverage:.2f}%")

    label2 = customtkinter.CTkLabel(frame, text=information, font=("Helvetica", 13, "bold"), fg_color='transparent') 
    label2.pack(pady=10) # Shows information about how many students, and the total class average.

# Display all students
def displayAll():
    displayStudentsList(studentData)  # Call display function with full list

# Display student with highest
def displayHighest():
    top = max(studentData, key=lambda s: sum(s[2]))  # Find maximum sum in coursework
    displayStudent(top)

# Display student with lowest
def displayLowest():
    low = min(studentData, key=lambda s: sum(s[2]))  # Find minimum sum in coursework
    displayStudent(low)

# Calculate total marks (coursework + exam)
def totalMarks(student):
    marks, exam = student[2], student[3]
    return sum(marks) + exam  # Return total for sorting

# Sort highest first going down
def sortDescending():
    studentData.sort(key=totalMarks, reverse=True)  # Sort descending
    displayStudentsList(studentData)  # Display sorted list

# Sort lowest first going up
def sortAscending():
    studentData.sort(key=totalMarks)  # Sort ascending
    displayStudentsList(studentData) 

# Tkinter stuff
title = Label(window, text="Student Manager", bg='#282828', fg='white', font=("Helvetica", 20, "bold"))
title.pack(pady=5)  # Main title label

# Combobox for selecting student
studentCombo = ttk.Combobox(window, values=studentNames, state='readonly')
studentCombo.set("Select...")  # Default text
studentCombo.place(relx=0.5, rely=0.2, anchor=CENTER)
studentCombo.bind("<<ComboboxSelected>>", studentSelect)  # Bind selection event

# View all students
allStudents = Button(window, text="View All Student Records", font=("Helvetica", 10, "bold"), relief=RAISED, bd=1, command=displayAll)
allStudents.place(relx=0.5, rely=0.3, anchor=CENTER)

# View highest scoring
highest = Button(window, text="View Highest Score", font=("Helvetica", 10, "bold"), relief=RAISED, bd=1, command=displayHighest)
highest.place(relx=0.2, rely=0.3, anchor=CENTER)

# View lowest scoring
lowest = Button(window, text="View Lowest Score", font=("Helvetica", 10, "bold"), relief=RAISED, bd=1, command=displayLowest)
lowest.place(relx=0.8, rely=0.3, anchor=CENTER)

# Sort all with highest first
ascending = Button(window, text="Ascending", font=("Helvetica", 10, "bold"), relief=RAISED, bd=1, command=sortAscending)
ascending.place(relx=0.2, rely=0.2, anchor=CENTER)

# Sort all with lowest first
descending = Button(window, text="Descending", font=("Helvetica", 10, "bold"), relief=RAISED, bd=1, command=sortDescending)
descending.place(relx=0.8, rely=0.2, anchor=CENTER)

# Scrollable frame to display student info. I thank customtkinter for this.
frame = customtkinter.CTkScrollableFrame(window, width=650, height=250)
frame.place(relx=0.5, rely=0.7, anchor=CENTER)

# Window settings
window.geometry('750x500') 
window.resizable(0, 0)
window.config(bg='#282828')
window.mainloop()


"""
Use of AI has been used in this code. It mainly focused on the for loop aspect in functions, which I would reuse in the other functions.
Prompt: how can i write a python for loop that reads a text file of student data (student code, name, coursework marks, exam mark) and outputs formatted information for each student?
ChatGPT
"""



