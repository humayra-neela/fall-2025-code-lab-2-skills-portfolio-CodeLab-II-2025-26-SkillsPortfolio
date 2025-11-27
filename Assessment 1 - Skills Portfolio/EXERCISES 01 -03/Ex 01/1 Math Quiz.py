import tkinter as tk
from tkinter import messagebox, ttk
import random

def displayMenu():
    # This function shows the difficulty level options first
    clear_window()
    title = tk.Label(root, text="CHOOSE DIFFICULTY LEVEL", font=("Arial", 16, "bold"), bg="#b3e5fc")
    title.pack(pady=20)

    # Buttons for each level
    tk.Button(root, text="1. Easy", width=20, command=lambda: start_quiz("easy")).pack(pady=5)
    tk.Button(root, text="2. Moderate", width=20, command=lambda: start_quiz("moderate")).pack(pady=5)
    tk.Button(root, text="3. Advanced", width=20, command=lambda: start_quiz("advanced")).pack(pady=5)


def randomInt(level):
    # To pick random numbers depending on difficulty
    if level == "easy":
        return random.randint(1, 9), random.randint(1, 9)
    elif level == "moderate":
        return random.randint(10, 99), random.randint(10, 99)
    else:
        return random.randint(1000, 9999), random.randint(1000, 9999)


def decideOperation():
    # This function is to choose (+) or (-) randomly
    return random.choice(['+', '-'])


def displayProblem():
    # This function is to show each question to the player
    clear_window()
    global num1, num2, operation, attempt

    num1, num2 = randomInt(difficulty)
    operation = decideOperation()
    attempt = 1 

    # Question label
    tk.Label(root, text=f"Question {question_no + 1} of 10", font=("Arial", 12, "bold"), bg="#fff9c4").pack(pady=5)
    tk.Label(root, text=f"{num1} {operation} {num2} =", font=("Arial", 18, "bold"), bg="#fffde7").pack(pady=10)

    # Entry for answer
    answer_entry.delete(0, tk.END)
    answer_entry.pack(pady=5)
    submit_button.pack(pady=10)

    # Progress bar update
    progress['value'] = (question_no / 10) * 100
    progress.pack(pady=10, fill='x', padx=40)


def isCorrect(user_answer):
    # This checks if answer is right or wrong
    global score, question_no, attempt

    correct = num1 + num2 if operation == '+' else num1 - num2

    if user_answer == correct:
        # If correct on 1st try → 10 points
        if attempt == 1:
            score += 10
            messagebox.showinfo("Correct!", "Nice! You got it right (+10)")
        else:
            score += 5
            messagebox.showinfo("Correct!", "Good! You got it this time (+5)")
        question_no += 1
        next_question()
    else:
        # If wrong first time, give second try
        if attempt == 1:
            attempt += 1
            messagebox.showwarning("Try Again", "That’s not right. Try once more!")
        else:
            messagebox.showerror("Wrong", f"Oops! The right answer was {correct}")
            question_no += 1
            next_question()


def next_question():
    # Go to next question or show final score
    if question_no < 10:
        displayProblem()
    else:
        displayResults()


def displayResults():
    # This shows your final score and grade
    clear_window()

    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "F"

    tk.Label(root, text="🎉 QUIZ FINISHED 🎉", font=("Arial", 18, "bold"), bg="#c8e6c9").pack(pady=10)
    tk.Label(root, text=f"Your Score: {score}/100\nGrade: {grade}", font=("Arial", 16), bg="#c8e6c9").pack(pady=20)

    # Buttons to replay or exit
    tk.Button(root, text="Play Again", width=15, command=displayMenu).pack(pady=5)
    tk.Button(root, text="Exit", width=15, command=root.destroy).pack(pady=5)


def clear_window():
    # This removes everything from window before showing new stuff
    for widget in root.winfo_children():
        widget.pack_forget()


def submit_answer():
    # When user clicks submit, check their answer
    try:
        user_answer = int(answer_entry.get())
        isCorrect(user_answer)
    except ValueError:
        messagebox.showwarning("Error", "Please type a number!")


def start_quiz(level):
    # This sets up the quiz variables and starts the first question
    global difficulty, score, question_no, answer_entry, submit_button, progress
    difficulty = level
    score = 0
    question_no = 0

    answer_entry = tk.Entry(root, font=("Arial", 14))
    submit_button = tk.Button(root, text="Submit Answer", command=submit_answer)

    progress = ttk.Progressbar(root, orient="horizontal", length=250, mode="determinate")

    displayProblem()
    
root = tk.Tk()
root.title("Simple Arithmetic Quiz")
root.geometry("420x380")
root.configure(bg="#fff9c4")

displayMenu()

root.mainloop()