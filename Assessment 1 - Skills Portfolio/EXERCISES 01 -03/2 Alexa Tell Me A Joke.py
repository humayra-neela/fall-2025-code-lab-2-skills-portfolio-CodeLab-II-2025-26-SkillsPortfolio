import tkinter as tk
import random
import os
from tkinter import messagebox

# Function to load jokes from the text file

def load_jokes(filename):
    jokes_list = []
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

            # loop through each line in the file
            for line in lines:
                line = line.strip() 
                if "?" in line:
                    jokes_list.append(line)

    except FileNotFoundError:
        # if the file isn't found, show an error message
        messagebox.showerror("Error", "randomjokes.txt file not found!")
    return jokes_list


# Function to show a random joke setup
def show_joke():
    global current_joke
    if len(jokes) == 0:
        messagebox.showerror("Error", "No jokes found in file!")
        return

    # pick a random joke from the list
    current_joke = random.choice(jokes)

    # split the joke into question and answer
    if "?" in current_joke:
        parts = current_joke.split("?")
        setup = parts[0] + "?"
        punchline = parts[1] if len(parts) > 1 else "Hmm... no punchline?"
    else:
        setup = current_joke
        punchline = ""

    # display setup only first
    setup_label.config(text=setup)
    punchline_label.config(text="")  # hide punchline for now
    show_button.config(state="normal")  # enable "Show Punchline"


# Function to show the punchline
def show_punchline():
    if current_joke:
        if "?" in current_joke:
            parts = current_joke.split("?")
            punchline = parts[1] if len(parts) > 1 else "Hmm... no punchline?"
            punchline_label.config(text=punchline.strip())
        else:
            punchline_label.config(text="No punchline found!")
        show_button.config(state="disabled")  # disable after showing once


# Function to go to next random joke
def next_joke():
    show_joke()


# Function to quit the program
def quit_app():
    root.destroy()

# make main window

root = tk.Tk()
root.title("Alexa Joke Assistant")
root.geometry("600x350")
root.configure(bg="#79cdee")

# find the path for the joke file
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, "randomjokes.txt")

# load jokes
jokes = load_jokes(file_path)
current_joke = None

# title the label
title_label = tk.Label(root, text="Alexa, tell me a joke!",
                       font=("Arial", 18, "bold"),
                       bg="#d4e723", fg="#000")
title_label.pack(pady=15, fill="x")

# setup label (for the first part of the joke)
setup_label = tk.Label(root, text="", font=("Arial", 14),
                       wraplength=500, bg="#0b729b", fg="#000")
setup_label.pack(pady=15)

# punchline label (for the second part)
punchline_label = tk.Label(root, text="", font=("Arial", 13, "italic"),
                           fg="white", wraplength=500, bg="#0b729b")
punchline_label.pack(pady=10)

# button area
button_frame = tk.Frame(root, bg="#79cdee")
button_frame.pack(pady=20)

# buttons
alexa_button = tk.Button(button_frame, text="Alexa, Tell Me A Joke",
                         command=show_joke, font=("Arial", 12),
                         bg="#ffcc80")
alexa_button.grid(row=0, column=0, padx=10)

show_button = tk.Button(button_frame, text="Show Punchline",
                        command=show_punchline, font=("Arial", 12),
                        bg="#ffd54f", state="disabled")
show_button.grid(row=0, column=1, padx=10)

next_button = tk.Button(button_frame, text="Next Joke",
                        command=next_joke, font=("Arial", 12),
                        bg="#ffb74d")
next_button.grid(row=0, column=2, padx=10)

# quit button
quit_button = tk.Button(root, text="Quit",
                        command=quit_app, font=("Arial", 12),
                        bg="#ef5350", fg="white", width=10)
quit_button.pack(pady=10)
root.mainloop()
