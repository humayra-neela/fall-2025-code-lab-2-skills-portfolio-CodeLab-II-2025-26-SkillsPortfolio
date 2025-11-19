import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# ---------------- Helper Functions ---------------- #

def get_grade(percentage):
    """Return grade letter based on percentage."""
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"


def load_data(filename="studentMarks.txt"):
    """Load student data from file, automatically finding the correct path."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    students = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            n = int(lines[0].strip())
            for line in lines[1:n + 1]:
                parts = line.strip().split(",")
                if len(parts) == 6:
                    sid = parts[0]
                    name = parts[1]
                    c1, c2, c3, exam = map(int, parts[2:])
                    coursework = c1 + c2 + c3
                    total = coursework + exam
                    percentage = (total / 160) * 100
                    grade = get_grade(percentage)
                    students.append({
                        "id": sid,
                        "name": name,
                        "coursework": coursework,
                        "exam": exam,
                        "total": total,
                        "percentage": round(percentage, 2),
                        "grade": grade
                    })
    except FileNotFoundError:
        messagebox.showerror("Error", f"{filename} not found in:\n{base_dir}")
    return students


# ---------------- GUI Functions ---------------- #

def view_all():
    """Display all student records."""
    students = load_data()
    if not students:
        return

    text.delete(1.0, tk.END)
    total_percent = 0

    text.insert(tk.END, f"{'Name':<20}{'ID':<10}{'Coursework':<12}{'Exam':<8}{'Overall %':<12}{'Grade':<6}\n")
    text.insert(tk.END, "-" * 70 + "\n")

    for s in students:
        total_percent += s['percentage']
        text.insert(
            tk.END,
            f"{s['name']:<20}{s['id']:<10}{s['coursework']:<12}{s['exam']:<8}{s['percentage']:<12}{s['grade']:<6}\n"
        )

    avg = total_percent / len(students)
    text.insert(tk.END, "\n")
    text.insert(tk.END, f"Total Students: {len(students)}\n")
    text.insert(tk.END, f"Average Percentage: {avg:.2f}%\n")


def view_individual():
    """Display individual student record by name or ID."""
    students = load_data()
    if not students:
        return

    sid = simpledialog.askstring("Input", "Enter student ID or name:")
    if not sid:
        return

    found = None
    for s in students:
        if s['id'] == sid or s['name'].lower() == sid.lower():
            found = s
            break

    text.delete(1.0, tk.END)
    if found:
        text.insert(tk.END, f"Name: {found['name']}\n")
        text.insert(tk.END, f"ID: {found['id']}\n")
        text.insert(tk.END, f"Coursework Total: {found['coursework']}\n")
        text.insert(tk.END, f"Exam Mark: {found['exam']}\n")
        text.insert(tk.END, f"Overall %: {found['percentage']:.2f}\n")
        text.insert(tk.END, f"Grade: {found['grade']}\n")
    else:
        text.insert(tk.END, "Student not found.\n")


def show_highest():
    """Show the student with the highest overall percentage."""
    students = load_data()
    if not students:
        return

    highest = max(students, key=lambda s: s['percentage'])
    text.delete(1.0, tk.END)
    text.insert(tk.END, "Highest Scoring Student:\n\n")
    text.insert(tk.END, f"Name: {highest['name']}\n")
    text.insert(tk.END, f"ID: {highest['id']}\n")
    text.insert(tk.END, f"Coursework Total: {highest['coursework']}\n")
    text.insert(tk.END, f"Exam Mark: {highest['exam']}\n")
    text.insert(tk.END, f"Overall %: {highest['percentage']:.2f}\n")
    text.insert(tk.END, f"Grade: {highest['grade']}\n")


def show_lowest():
    """Show the student with the lowest overall percentage."""
    students = load_data()
    if not students:
        return

    lowest = min(students, key=lambda s: s['percentage'])
    text.delete(1.0, tk.END)
    text.insert(tk.END, "Lowest Scoring Student:\n\n")
    text.insert(tk.END, f"Name: {lowest['name']}\n")
    text.insert(tk.END, f"ID: {lowest['id']}\n")
    text.insert(tk.END, f"Coursework Total: {lowest['coursework']}\n")
    text.insert(tk.END, f"Exam Mark: {lowest['exam']}\n")
    text.insert(tk.END, f"Overall %: {lowest['percentage']:.2f}\n")
    text.insert(tk.END, f"Grade: {lowest['grade']}\n")


# ---------------- Tkinter GUI Setup ---------------- #

root = tk.Tk()
root.title("Student Manager")
root.geometry("720x500")
root.config(bg="#F0F0F0")

frame = tk.Frame(root, bg="#F0F0F0")
frame.pack(pady=15)

title_label = tk.Label(
    frame,
    text="Student Marks Manager",
    font=("Arial", 16, "bold"),
    bg="#F0F0F0"
)
title_label.grid(row=0, column=0, columnspan=4, pady=10)

btn_all = tk.Button(frame, text="1. View All", command=view_all, width=18, bg="#d9d9d9")
btn_all.grid(row=1, column=0, padx=5, pady=5)

btn_individual = tk.Button(frame, text="2. View Individual", command=view_individual, width=18, bg="#d9d9d9")
btn_individual.grid(row=1, column=1, padx=5, pady=5)

btn_highest = tk.Button(frame, text="3. Show Highest", command=show_highest, width=18, bg="#d9d9d9")
btn_highest.grid(row=1, column=2, padx=5, pady=5)

btn_lowest = tk.Button(frame, text="4. Show Lowest", command=show_lowest, width=18, bg="#d9d9d9")
btn_lowest.grid(row=1, column=3, padx=5, pady=5)

# Output area
text = tk.Text(root, wrap="word", width=85, height=20, bg="white", fg="black")
text.pack(padx=10, pady=10)

root.mainloop()