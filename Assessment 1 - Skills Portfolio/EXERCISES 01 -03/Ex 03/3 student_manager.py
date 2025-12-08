import tkinter as tk
from tkinter import simpledialog, messagebox
import json, os

# load data from json file
def load_data():
    try:
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
    except:
        messagebox.showerror("Error", "studentMarks.json missing or broken")
        return []

# save data to json file
def save_data(students):
    path = os.path.join(os.path.dirname(__file__), "studentMarks.json")
    data = {"students": []}
    for s in students:
        data["students"].append({
            "id": s["id"],
            "name": s["name"],
            "coursework": [round(s["coursework"]/3)] * 3,
            "exam": s["exam"]
        })
    with open(path, "w") as file:
        json.dump(data, file, indent=4)

# grade logic
def get_grade(p):
    if p >= 70: return "A"
    if p >= 60: return "B"
    if p >= 50: return "C"
    if p >= 40: return "D"
    return "F"

# view all infos
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
        text.insert(tk.END, "-"*60 + "\n")

    if students:
        avg = round(total_perc / len(students), 2)
        text.insert(tk.END, f"\nTotal Students: {len(students)}")
        text.insert(tk.END, f"\nClass Average: {avg}%")

# individual infos
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

# highest result
def show_highest():
    students = load_data()
    if students:
        top = max(students, key=lambda x: x["percentage"])
        display_student("Highest Scoring Student", top)

# lowest result
def show_lowest():
    students = load_data()
    if students:
        low = min(students, key=lambda x: x["percentage"])
        display_student("Lowest Scoring Student", low)

def display_student(title, s):
    text.delete(1.0, tk.END)
    text.insert(tk.END, f"{title}\n\n")
    text.insert(tk.END,
    f"Name: {s['name']}\nID: {s['id']}\n"
    f"Coursework: {s['coursework']}\nExam: {s['exam']}\n"
    f"Percentage: {s['percentage']}% | Grade: {s['grade']}")

# sort student by percentage
def sort_students():
    students = load_data()
    if not students:
        return

    choice = simpledialog.askstring("Sort", "Type ASC (low to high) or DESC (high to low):")
    text.delete(1.0, tk.END)

    if not choice:
        text.insert(tk.END, "No sort option chosen.")
        return

    choice = choice.strip().lower()

    if choice == "asc":
        reverse_order = False
    elif choice == "desc":
        reverse_order = True
    else:
        text.insert(tk.END, "Please type ASC or DESC next time.")
        return

    students = sorted(students, key=lambda x: x["percentage"], reverse=reverse_order)

    total_perc = 0
    for s in students:
        total_perc += s["percentage"]
        text.insert(tk.END,
        f"Name: {s['name']} | ID: {s['id']}\n"
        f"Coursework: {s['coursework']} | Exam: {s['exam']}\n"
        f"Percentage: {s['percentage']}% | Grade: {s['grade']}\n")
        text.insert(tk.END, "-"*60 + "\n")

    avg = round(total_perc / len(students), 2)
    text.insert(tk.END, f"\nTotal Students: {len(students)}")
    text.insert(tk.END, f"\nClass Average: {avg}%")


# add new student infos
def add_student():
    students = load_data()

    sid = simpledialog.askstring("Input", "Enter new Student ID:")
    if not sid: 
        return

    name = simpledialog.askstring("Input", "Enter Student Name:")
    if not name: 
        return

    try:
        cw1 = int(simpledialog.askstring("Input", "Coursework 1 (0-20):") or 0)
        cw2 = int(simpledialog.askstring("Input", "Coursework 2 (0-20):") or 0)
        cw3 = int(simpledialog.askstring("Input", "Coursework 3 (0-20):") or 0)
        exam = int(simpledialog.askstring("Input", "Exam Mark (0-100):") or 0)
    except:
        messagebox.showerror("Error", "Please enter valid numbers")
        return

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
    messagebox.showinfo("Success", "Student added successfully!")


# delete student infos
def delete_student():
    students = load_data()
    sid = simpledialog.askstring("Delete", "Enter Student ID to delete:")
    if not sid:
        return

    new_list = [s for s in students if s["id"] != sid]

    if len(new_list) == len(students):
        messagebox.showinfo("Info", "Student ID not found")
    else:
        save_data(new_list)
        messagebox.showinfo("Success", "Student deleted successfully!")

# update student infos
def update_student():
    students = load_data()
    sid = simpledialog.askstring("Update", "Enter Student ID to update:")
    if not sid:
        return

    for s in students:
        if s["id"] == sid:

            choice = simpledialog.askstring("Update", "What do you want to update?\nname / exam / coursework:")
            if not choice:
                return

            if choice.lower() == "name":
                new_name = simpledialog.askstring("Update", "Enter new name:")
                if new_name:
                    s["name"] = new_name

            elif choice.lower() == "exam":
                try:
                    new_exam = int(simpledialog.askstring("Update", "Enter new exam mark:"))
                    s["exam"] = new_exam
                except:
                    messagebox.showerror("Error", "Invalid number")
                    return

            elif choice.lower() == "coursework":
                try:
                    cw1 = int(simpledialog.askstring("Input", "Coursework 1:"))
                    cw2 = int(simpledialog.askstring("Input", "Coursework 2:"))
                    cw3 = int(simpledialog.askstring("Input", "Coursework 3:"))
                    s["coursework"] = cw1 + cw2 + cw3
                except:
                    messagebox.showerror("Error", "Invalid number")
                    return

            s["percentage"] = round((s["coursework"] + s["exam"]) / 160 * 100, 2)
            s["grade"] = get_grade(s["percentage"])

            save_data(students)
            messagebox.showinfo("Success", "Record updated!")
            return

    messagebox.showinfo("Info", "Student ID not found")


root = tk.Tk()
root.title("Student Manager")
root.geometry("750x500")
root.configure(bg="#E8EEF1")  # light background

title = tk.Label(root, text="Student Record Manager", font=("Arial", 16, "bold"), bg="#E8EEF1", fg="#1F3B4D")
title.pack(pady=10)

frame = tk.Frame(root, bg="#E8EEF1")
frame.pack(pady=5)

btn_style = {"width": 15, "bg": "#D6E4F0", "fg": "black", "relief": "ridge"}

tk.Button(frame, text="1 View All", command=view_all, **btn_style).grid(row=0, column=0, padx=4, pady=4)
tk.Button(frame, text="2 View Individual", command=view_individual, **btn_style).grid(row=0, column=1, padx=4, pady=4)
tk.Button(frame, text="3 Highest", command=show_highest, **btn_style).grid(row=0, column=2, padx=4, pady=4)
tk.Button(frame, text="4 Lowest", command=show_lowest, **btn_style).grid(row=0, column=3, padx=4, pady=4)

tk.Button(frame, text="5 Sort", command=sort_students, **btn_style).grid(row=1, column=0, padx=4, pady=4)
tk.Button(frame, text="6 Add", command=add_student, **btn_style).grid(row=1, column=1, padx=4, pady=4)
tk.Button(frame, text="7 Delete", command=delete_student, **btn_style).grid(row=1, column=2, padx=4, pady=4)
tk.Button(frame, text="8 Update", command=update_student, **btn_style).grid(row=1, column=3, padx=4, pady=4)

text = tk.Text(root, width=90, height=20, bg="white", fg="black", font=("Arial", 10))
text.pack(pady=8)

root.mainloop()