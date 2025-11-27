import tkinter as tk
from tkinter import simpledialog, messagebox
import json, os

def load_data():
    path = os.path.join(os.path.dirname(__file__), "studentMarks.json")
    with open(path, "r") as file:
        data = json.load(file)["students"]

    students = []
    for s in data:
        cw = sum(s["coursework"])
        total = cw + int(s["exam"])
        perc = round((total / 160) * 100, 2)
        students.append({
            "id": s["id"],
            "name": s["name"],
            "coursework": cw,
            "exam": int(s["exam"]),
            "percentage": perc,
            "grade": get_grade(perc)
        })
    return students

def save_data(students):
    path = os.path.join(os.path.dirname(__file__), "studentMarks.json")
    data = {"students": []}
    for s in students:
        data["students"].append({
            "id": s["id"],
            "name": s["name"],
            "coursework": [s["coursework"]], 
            "exam": s["exam"]
        })
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

def get_grade(p):
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"


def view_all():
    text.delete(1.0, tk.END)
    students = load_data()
    total_perc = 0

    for s in students:
        total_perc += s["percentage"]
        text.insert(tk.END,
        f"Name: {s['name']} | ID: {s['id']}\n"
        f"Coursework: {s['coursework']} | Exam: {s['exam']}\n"
        f"Percentage: {s['percentage']}% | Grade: {s['grade']}\n")
        text.insert(tk.END, "-"*55 + "\n")

    avg = round(total_perc / len(students), 2)
    text.insert(tk.END, f"\nTotal Students: {len(students)}")
    text.insert(tk.END, f"\nClass Average: {avg}%")

# view individual ID
def view_individual():
    students = load_data()
    sid = simpledialog.askstring("Search", "Enter Student ID or Name:")
    text.delete(1.0, tk.END)
    for s in students:
        if s["id"] == sid or s["name"].lower() == sid.lower():
            text.insert(tk.END,
            f"Name: {s['name']}\nID: {s['id']}\n"
            f"Coursework: {s['coursework']}\nExam: {s['exam']}\n"
            f"Percentage: {s['percentage']}% | Grade: {s['grade']}")
            return
    text.insert(tk.END, "Student not found.")

# highest Mark finder
def show_highest():
    students = load_data()
    top = max(students, key=lambda x: x["percentage"])
    display_student("Highest Scoring Student", top)

# lowest Mark finder
def show_lowest():
    students = load_data()
    low = min(students, key=lambda x: x["percentage"])
    display_student("Lowest Scoring Student", low)

def display_student(title, s):
    text.delete(1.0, tk.END)
    text.insert(tk.END, f"{title}\n\n")
    text.insert(tk.END,
    f"Name: {s['name']}\nID: {s['id']}\n"
    f"Coursework: {s['coursework']}\nExam: {s['exam']}\n"
    f"Percentage: {s['percentage']}% | Grade: {s['grade']}")

def sort_students():
    students = load_data()
    choice = simpledialog.askstring("Sort", "ASC or DESC:")
    text.delete(1.0, tk.END)

    if choice.lower() == "asc":
        students = sorted(students, key=lambda x: x["percentage"])
    else:
        students = sorted(students, key=lambda x: x["percentage"], reverse=True)

    for s in students:
        text.insert(tk.END, f"{s['name']} - {s['percentage']}% | Grade {s['grade']}\n")

def add_student():
    students = load_data()
    sid = simpledialog.askstring("Input", "ID:")
    name = simpledialog.askstring("Input", "Name:")
    cw1 = int(simpledialog.askstring("Input", "Coursework1:"))
    cw2 = int(simpledialog.askstring("Input", "Coursework2:"))
    cw3 = int(simpledialog.askstring("Input", "Coursework3:"))
    exam = int(simpledialog.askstring("Input", "Exam:"))

    cw_total = cw1 + cw2 + cw3
    perc = round(((cw_total + exam) / 160) * 100, 2)

    students.append({
        "id": sid,
        "name": name,
        "coursework": cw_total,
        "exam": exam,
        "percentage": perc,
        "grade": get_grade(perc)
    })
    save_data(students)
    messagebox.showinfo("Success", "Student added")

def delete_student():
    students = load_data()
    sid = simpledialog.askstring("Input", "Enter ID to delete:")
    new_list = [s for s in students if s["id"] != sid]

    if len(new_list) == len(students):
        messagebox.showinfo("Info", "Student not found")
    else:
        save_data(new_list)
        messagebox.showinfo("Removed", "Student deleted")

def update_student():
    students = load_data()
    sid = simpledialog.askstring("Input", "Enter ID to update:")
    for s in students:
        if s["id"] == sid:
            new_name = simpledialog.askstring("Update", "New name (or blank):")
            new_exam = simpledialog.askstring("Update", "New exam (or blank):")

            if new_name:
                s["name"] = new_name
            if new_exam:
                s["exam"] = int(new_exam)

            s["percentage"] = round((s["coursework"] + s["exam"]) / 160 * 100, 2)
            s["grade"] = get_grade(s["percentage"])

            save_data(students)
            messagebox.showinfo("Done", "Record updated")
            return
    messagebox.showinfo("Info", "Student not found")


root = tk.Tk()
root.title("Student Manager")
root.geometry("750x500")

title = tk.Label(root, text="Student Record Manager", font=("Arial", 15, "bold"))
title.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="1 View All", width=15, command=view_all).grid(row=0, column=0)
tk.Button(frame, text="2 View Individual", width=15, command=view_individual).grid(row=0, column=1)
tk.Button(frame, text="3 Highest", width=15, command=show_highest).grid(row=0, column=2)
tk.Button(frame, text="4 Lowest", width=15, command=show_lowest).grid(row=0, column=3)
tk.Button(frame, text="5 Sort", width=15, command=sort_students).grid(row=1, column=0)
tk.Button(frame, text="6 Add", width=15, command=add_student).grid(row=1, column=1)
tk.Button(frame, text="7 Delete", width=15, command=delete_student).grid(row=1, column=2)
tk.Button(frame, text="8 Update", width=15, command=update_student).grid(row=1, column=3)

text = tk.Text(root, width=85, height=20)
text.pack()

root.mainloop()