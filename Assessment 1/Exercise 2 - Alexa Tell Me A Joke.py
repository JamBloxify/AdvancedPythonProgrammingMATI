import random
import time
from tkinter import *

window = Tk()

def tellJoke(): # Joke function
    global punchline
    with open('Assessment 1/randomJokes.txt', 'r') as jokeFile: # Opens the text file with jokes, and assigns it to 'jokeFile' variable
        jokes = jokeFile.readlines() # Reads all the lines in the text file and puts them in the variable 'jokes'
        ranJoke = random.choice(jokes).strip() # Chooses a random joke, and removes any extra spaces or new lines
        setup, punchline = ranJoke.split('?') # Splits the joke into two variables, setup and punchline, using the '?' as the separator
        punchlinelabel.config(text='') # Resets punchline label to blank
        alexa.config(text=setup) # Turns the label into the setup
        okbtn.config(text='Punchline', command=pline) # Replaces the text of the button and function

def pline(): # Function that says the punchline
    global punchline
    punchlinelabel.config(text=punchline) # Sets punchline
    okbtn.config(text='Next', command=tellJoke) # Sets text to next, and loops back to the tell joke function


def quit(): # Quit for quit button
    exit()


# Tkinter stuff
title = Label(window, text = "ALEXA", fg='white', bg='#282828', font=("Helvetica", 20, "bold"))
title.pack(pady=5)

frame = Frame(window, width = 650, height = 650, bg = "#1E1E1E", bd = 10, relief=RIDGE)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

alexa = Label(frame, text="Hello, would you like to hear a joke?", bg = "#1E1E1E", font=("Helvetica", 15, "bold"), fg='white')
alexa.place(relx=0.5, rely=0.2, anchor=CENTER)

punchlinelabel = Label(frame, text="", bg = "#1E1E1E", font=("Helvetica", 15, "bold"), fg='white')
punchlinelabel.place(relx=0.5, rely=0.4, anchor=CENTER)

okbtn = Button(frame, text='OK', font=("Helvetica", 16, "bold"), bg = 'white', fg = 'black', relief=RAISED, command=tellJoke)
okbtn.place(relx=0.5, rely=0.6, anchor=CENTER)

quit = Button(frame, text='X', font=("Helvetica", 15, "bold"), bg = 'white', fg = 'black', relief=RAISED, command=quit)
quit.place(relx=1, rely=0, anchor=NE)

window.geometry('750x750')
window.resizable(0, 0)
window.config(bg='#282828')
window.mainloop()
    
