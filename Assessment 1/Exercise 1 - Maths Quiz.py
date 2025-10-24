import random # For random number generator and operator
import time # For delay
from tkinter import *


# Variables
difficulty = 0
marks = 0
questions = 1 # This is 1 and not 0 so to display "Question 1/10" instead of "Question 0/10" at the start of the quiz.
attempts = 0


# Personal functions
def buttonDif(dif):
    global difficulty
    global num1, num2
    difficulty = dif

    # Generate random numbers based on difficulty
    if difficulty == 1: # Easy (1-9)
        num1 = randomInt(1, 9)
        num2 = randomInt(1, 9)
    elif difficulty == 2: # Moderate (10-99)
        num1 = randomInt(10, 99)
        num2 = randomInt(10, 99)
    elif difficulty == 3: # Advanced (1000-9999)
        num1 = randomInt(1000, 9999)
        num2 = randomInt(1000, 9999)

    easy.destroy()
    moderate.destroy()
    hard.destroy()
    displayProblem()

def resetGame():
    global marks, questions, attempts, difficulty
    
    # Reset all variables
    marks = 0
    questions = 1
    attempts = 0
    difficulty = 0
    
    # Destroy all widgets in frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Go back to difficulty selection
    displayMenu()


# Required functions
def displayMenu():
    global easy, moderate, hard
    global label
    start.destroy()
    quit.destroy()

    # Difficulty
    label = Label(frame, text="Select a Difficulty", font=("Helvetica", 20, "bold"), bg = '#1E1E1E', fg="#FFFFFF")
    label.place(relx=0.5, rely=0.2, anchor=CENTER)

    # Easy button
    easy = Button(frame, text="Easy", font=("Helvetica", 10, "bold"), width=10, height=1, bg="#00FF00", fg="Black", bd = 2, relief=RAISED, activebackground="#117F00", activeforeground='white', command = lambda: buttonDif(1))
    easy.place(relx=0.5, rely=0.4, anchor=CENTER)

    # Moderate button
    moderate = Button(frame, text="Moderate", font=("Helvetica", 10, "bold"), width=10, height=1, bg="#FFFF00", fg="Black", bd = 2, relief=RAISED, activebackground="#767600", activeforeground='white', command = lambda: buttonDif(2))
    moderate.place(relx=0.5, rely=0.6, anchor=CENTER)

    # Hard button
    hard = Button(frame, text="Hard", font=("Helvetica", 10, "bold"), width=10, height=1, bg="#FF0000", fg="Black", bd = 2, relief=RAISED, activebackground="#720000", activeforeground='white', command = lambda: buttonDif(3))
    hard.place(relx=0.5, rely=0.8, anchor=CENTER)

def randomInt(min, max):
    return random.randint(min, max)

def decideOperation():
    operators = ['+', '-']
    return random.choice(operators)

def displayProblem():
    global ans, num1, num2
    global userAns, cow, que, submit
    
    # Destroy old widgets if they exist (to prevent overlap)
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Update question counter
    questionLabel = Label(frame, text=f"{questions}/10", font=("Helvetica", 20, "bold"), bg='#1E1E1E', fg="#FFFFFF")
    questionLabel.place(relx=0.5, rely=0.2, anchor=CENTER)
    
    # Question display
    que = Label(frame, text="", font=("Helvetica", 24, "bold"), bg='#1E1E1E', fg="#FFFFFF")
    que.place(relx=0.5, rely=0.4, anchor=CENTER)
    
    # Feedback label (correct/wrong)
    cow = Label(frame, text="", font=("Helvetica", 16, "bold"), bg='#1E1E1E')
    cow.place(relx=0.5, rely=0.1, anchor=CENTER)
    
    # Marks display
    mark = Label(frame, text=f"Marks: {marks}/100", font=("Helvetica", 12, "bold"), bg='#1E1E1E', fg="#FFFFFF")
    mark.place(relx=0.85, rely=0.9, anchor=CENTER)
    
    # User input entry
    userAns = Entry(frame, font=("Helvetica", 24, "bold"), bg='#1E1E1E', fg="#FFFFFF", width=5, justify=CENTER)
    userAns.place(relx=0.5, rely=0.6, anchor=CENTER)
    
    # Submit button
    submit = Button(frame, text="Submit", font=("Helvetica", 16, "bold"), bg='white', fg='black', relief=RAISED, command=isCorrect)
    submit.place(relx=0.5, rely=0.8, anchor=CENTER)
    
    # Generate new problem
    operation = decideOperation()
    
    if difficulty == 1:
        num1 = randomInt(1, 9)
        num2 = randomInt(1, 9)
    elif difficulty == 2:
        num1 = randomInt(10, 99)
        num2 = randomInt(10, 99)
    elif difficulty == 3:
        num1 = randomInt(1000, 9999)
        num2 = randomInt(1000, 9999)
    
    if operation == '+':
        ans = num1 + num2
    elif operation == '-':
        ans = num1 - num2
    
    que.config(text=f"{num1} {operation} {num2} = ?")
    

def isCorrect():
    global marks, questions, attempts
    
    try:
        answer = int(userAns.get())
        
        if answer == ans:
            if attempts == 0:
                cow.config(fg="#00ff00", text="Correct! +10 marks")
                marks += 10
            else:
                cow.config(fg="#00ff00", text="Correct! +5 marks")
                marks += 5
            
            questions += 1
            attempts = 0
            
            if questions <= 10:
                window.after(1000, displayProblem)  # Wait 1 second before next question
            else:
                window.after(1000, displayResult)  # Wait 1 second before showing results
        else:
            attempts += 1
            if attempts == 1:
                cow.config(fg="#ff0000", text="Wrong! One more chance")
                userAns.delete(0, END)
            else:
                cow.config(fg="#ff0000", text=f"Wrong! Answer was {ans}. No marks")
                questions += 1
                attempts = 0
                
                if questions <= 10:
                    window.after(1500, displayProblem)  # Wait 1.5 seconds
                else:
                    window.after(1500, displayResult)
                    
    except ValueError:
        cow.config(fg="#ff0000", text="Please enter a valid number!")
        

def displayResult():
    global marks, questions, attempts, difficulty
    
    # Destroy ALL widgets in the frame
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Display final score title
    resultTitle = Label(frame, text="Quiz Complete!", font=("Helvetica", 24, "bold"), bg='#1E1E1E', fg="#FFAA00")
    resultTitle.place(relx=0.5, rely=0.15, anchor=CENTER)
    
    # Display score
    scoreLabel = Label(frame, text=f"Final Score: {marks}/100", font=("Helvetica", 20, "bold"), bg='#1E1E1E', fg="#FFFFFF")
    scoreLabel.place(relx=0.5, rely=0.35, anchor=CENTER)
    
    # Determine grade and color
    if marks >= 90:
        grade = "A+"
        color = "#00FF00"
    elif marks >= 80:
        grade = "A"
        color = "#00FF00"
    elif marks >= 70:
        grade = "B"
        color = "#90EE90"
    elif marks >= 60:
        grade = "C"
        color = "#FFFF00"
    elif marks >= 50:
        grade = "D"
        color = "#FFA500"
    else:
        grade = "F"
        color = "#FF0000"
    
    # Display grade
    gradeLabel = Label(frame, text=f"Grade: {grade}", font=("Helvetica", 28, "bold"), bg='#1E1E1E', fg=color)
    gradeLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    # Play Again button
    playAgain = Button(frame, text="Play Again", font=("Helvetica", 14, "bold"), bg="#00FF00", fg='black', bd=2, relief=RAISED, command=resetGame)
    playAgain.place(relx=0.5, rely=0.7, anchor=CENTER)
    
    # Quit button
    quitBtn = Button(frame, text="Quit", font=("Helvetica", 14, "bold"), bg="#FF0000", fg='black', bd=2, relief=RAISED, command=exit)
    quitBtn.place(relx=0.5, rely=0.9, anchor=CENTER)


# Tkinter Window
window = Tk()
window.title("Math Quiz")
window.geometry('500x500')
window.resizable(0, 0)
window.config(bg='#282828')

title = Label(window, text="MATH QUIZ", font=("Helvetica", 24, "bold"), fg="#FFAA00", bg='#282828')
title.pack(pady=5)

frame = Frame(window, width = 450, height = 400, bg = "#1E1E1E", bd = 10, relief=RIDGE)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

start = Button(frame, text="Start", font=("Helvetica", 24, "bold"), bg="#BEBEBE", fg='black', bd = 1, command=displayMenu)
start.place(relx=0.5, rely=0.4, anchor=CENTER)

quit = Button(frame, text="Quit", font=("Helvetica", 16, "bold"), bg="#4F4F4F", fg='black', bd = 1, command=exit)
quit.place(relx=0.5, rely=0.6, anchor=CENTER)


window.mainloop()