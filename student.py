import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1300x700+100+50")
        self.root.configure(bg="#f4f6f9")

        # ================= Variables =================
        self.var_course = tk.StringVar()
        self.var_dept = tk.StringVar()
        self.var_year = tk.StringVar()
        self.var_sem = tk.StringVar()
        self.var_section = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_enrollment = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_dob = tk.StringVar()
        self.var_phone = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_address = tk.StringVar()
        self.var_combo_search = tk.StringVar()
        self.var_search = tk.StringVar()

        self.init_db()
        self.setup_styles()

        # ================= Title =================
        title = tk.Label(
            self.root, text="🎓 Student Management System",
            font=("Segoe UI", 22, "bold"),
            bg="#2c3e50", fg="white", pady=10
        )
        title.pack(side=tk.TOP, fill=tk.X)

        # ================= Left Frame =================
        left_frame = tk.LabelFrame(
            self.root, text="Student Information",
            font=("Segoe UI", 14, "bold"),
            bg="white", fg="#2c3e50", bd=2, relief="groove"
        )
        left_frame.place(x=20, y=70, width=500, height=600)

        labels = ["Course:", "Department:", "Year:", "Semester:", "Section:", "Gender:", 
                  "Enrollment No.:", "Name:", "DOB:", "Phone:", "Email:", "Address:"]
        vars = [self.var_course, self.var_dept, self.var_year, self.var_sem,
                self.var_section, self.var_gender, self.var_enrollment, self.var_name,
                self.var_dob, self.var_phone, self.var_email, self.var_address]

        row = 0
        for lbl, var in zip(labels, vars):
            tk.Label(left_frame, text=lbl, font=("Segoe UI", 11), bg="white").grid(row=row, column=0, padx=10, pady=5, sticky="w")
            if lbl in ["Course:", "Department:", "Year:", "Semester:", "Section:", "Gender:"]:
                cb = ttk.Combobox(left_frame, textvariable=var, font=("Segoe UI", 10), width=20, state="readonly")
                if lbl == "Course:": cb["values"] = ("Select Course", "B.Tech", "M.Tech", "B.Sc", "M.Sc", "MBA", "BBA")
                if lbl == "Department:": cb["values"] = ("Select Department", "CSE", "IT", "ECE", "EEE", "ME", "Civil")
                if lbl == "Year:": cb["values"] = ("Select Year", "1st", "2nd", "3rd", "4th")
                if lbl == "Semester:": cb["values"] = ("Select Semester", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th")
                if lbl == "Section:": cb["values"] = ("A", "B", "C", "D")
                if lbl == "Gender:": cb["values"] = ("Male", "Female", "Other")
                cb.current(0)
                cb.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            else:
                ent = ttk.Entry(left_frame, textvariable=var, font=("Segoe UI", 10), width=23)
                ent.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            row += 1

        # Buttons
        btn_frame = tk.Frame(left_frame, bg="white")
        btn_frame.place(x=10, y=500, width=470, height=40)

        ttk.Button(btn_frame, text="Add", command=self.add_data, style="Accent.TButton").grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_data).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_data, style="Danger.TButton").grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset_data).grid(row=0, column=3, padx=5)

        # ================= Right Frame =================
        right_frame = tk.LabelFrame(
            self.root, text="Student Records",
            font=("Segoe UI", 14, "bold"),
            bg="white", fg="#2c3e50", bd=2, relief="groove"
        )
        right_frame.place(x=540, y=70, width=740, height=600)

        tk.Label(right_frame, text="Search By:", font=("Segoe UI", 11), bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        combo_search = ttk.Combobox(right_frame, textvariable=self.var_combo_search, font=("Segoe UI", 10), width=15, state="readonly")
        combo_search["values"] = ("Enrollment", "Name", "Phone")
        combo_search.current(0)
        combo_search.grid(row=0, column=1, padx=5, pady=5)

        ttk.Entry(right_frame, textvariable=self.var_search, font=("Segoe UI", 10), width=20).grid(row=0, column=2, padx=5)
        ttk.Button(right_frame, text="Search", command=self.search_data).grid(row=0, column=3, padx=5)
        ttk.Button(right_frame, text="Show All", command=self.fetch_data).grid(row=0, column=4, padx=5)

        # Table
        table_frame = tk.Frame(right_frame, bg="white")
        table_frame.place(x=10, y=50, width=710, height=520)

        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        self.student_table = ttk.Treeview(
            table_frame, columns=("Enrollment", "Name", "Course", "Department", "Year", "Semester", 
                                  "Section", "Gender", "DOB", "Phone", "Email", "Address"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        for col in self.student_table["columns"]:
            self.student_table.heading(col, text=col)
            self.student_table.column(col, width=120)

        self.student_table["show"] = "headings"
        self.student_table.pack(fill="both", expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    # ================= Styles =================
    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("TButton", font=("Segoe UI", 10), padding=6, relief="flat", background="#3498db", foreground="white")
        style.map("TButton", background=[("active", "#2980b9")])

        style.configure("Accent.TButton", background="#27ae60", foreground="white")
        style.map("Accent.TButton", background=[("active", "#1e8449")])

        style.configure("Danger.TButton", background="#e74c3c", foreground="white")
        style.map("Danger.TButton", background=[("active", "#c0392b")])

        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#34495e", foreground="white")
        style.map("Treeview.Heading", background=[("active", "#2c3e50")])

    # ================= Database =================
    def init_db(self):
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS student (
            Enrollment TEXT PRIMARY KEY,
            Name TEXT, Course TEXT, Department TEXT,
            Year TEXT, Semester TEXT, Section TEXT, Gender TEXT,
            DOB TEXT, Phone TEXT, Email TEXT, Address TEXT)""")
        conn.commit()
        conn.close()

    # ================= Functions =================
    def add_data(self):
        if self.var_enrollment.get() == "" or self.var_name.get() == "":
            messagebox.showerror("Error", "Enrollment and Name required")
            return
        try:
            conn = sqlite3.connect("student.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO student VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                self.var_enrollment.get(), self.var_name.get(), self.var_course.get(),
                self.var_dept.get(), self.var_year.get(), self.var_sem.get(),
                self.var_section.get(), self.var_gender.get(), self.var_dob.get(),
                self.var_phone.get(), self.var_email.get(), self.var_address.get()
            ))
            conn.commit()
            conn.close()
            self.fetch_data()
            self.reset_data()
            messagebox.showinfo("Success", "Student added")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Enrollment already exists")

    def fetch_data(self):
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()
        self.student_table.delete(*self.student_table.get_children())
        for row in rows:
            self.student_table.insert("", "end", values=row)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.student_table.focus()
        row = self.student_table.item(cursor_row)["values"]
        if row:
            self.var_enrollment.set(row[0]); self.var_name.set(row[1]); self.var_course.set(row[2])
            self.var_dept.set(row[3]); self.var_year.set(row[4]); self.var_sem.set(row[5])
            self.var_section.set(row[6]); self.var_gender.set(row[7]); self.var_dob.set(row[8])
            self.var_phone.set(row[9]); self.var_email.set(row[10]); self.var_address.set(row[11])

    def update_data(self):
        if self.var_enrollment.get() == "":
            messagebox.showerror("Error", "Select a student")
            return
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        cur.execute("""UPDATE student SET Name=?,Course=?,Department=?,Year=?,Semester=?,
                        Section=?,Gender=?,DOB=?,Phone=?,Email=?,Address=? WHERE Enrollment=?""",
            (self.var_name.get(), self.var_course.get(), self.var_dept.get(), self.var_year.get(),
             self.var_sem.get(), self.var_section.get(), self.var_gender.get(), self.var_dob.get(),
             self.var_phone.get(), self.var_email.get(), self.var_address.get(), self.var_enrollment.get()))
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Updated", "Record updated")

    def delete_data(self):
        if self.var_enrollment.get() == "":
            messagebox.showerror("Error", "Select a student")
            return
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM student WHERE Enrollment=?", (self.var_enrollment.get(),))
        conn.commit()
        conn.close()
        self.fetch_data()
        self.reset_data()
        messagebox.showinfo("Deleted", "Record deleted")

    def reset_data(self):
        self.var_course.set("Select Course"); self.var_dept.set("Select Department")
        self.var_year.set("Select Year"); self.var_sem.set("Select Semester")
        self.var_section.set(""); self.var_gender.set(""); self.var_enrollment.set("")
        self.var_name.set(""); self.var_dob.set(""); self.var_phone.set("")
        self.var_email.set(""); self.var_address.set("")

    def search_data(self):
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM student WHERE {self.var_combo_search.get()} LIKE ?", ('%' + self.var_search.get() + '%',))
        rows = cur.fetchall()
        self.student_table.delete(*self.student_table.get_children())
        for row in rows:
            self.student_table.insert("", "end", values=row)
        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    obj = StudentManagementSystem(root)
    root.mainloop()
