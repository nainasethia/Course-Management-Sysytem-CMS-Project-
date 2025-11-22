# course.py

from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3


DB_NAME = "cms.db"


class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # ----- make sure table & teacher column exist -----
        self.setup_db_schema()

        # === variables ===
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_teacher = StringVar()
        self.var_search = StringVar()

        # === title ===
        title = Label(self.root, text="Manage Course Details", font=(
            "times new roman", 20, "bold"), bg="#005470", fg="white")
        title.place(x=10, y=15, width=1517, height=35)

        # === labels ===
        lbl_courseName = Label(self.root, text="Course Name", font=(
            "goudy old style", 15, 'bold'), bg='white')
        lbl_courseName.place(x=10, y=60)

        lbl_duration = Label(self.root, text="Duration", font=(
            "goudy old style", 15, 'bold'), bg='white')
        lbl_duration.place(x=10, y=100)

        lbl_teacher = Label(self.root, text="Teacher", font=(
            "goudy old style", 15, 'bold'), bg='white')
        lbl_teacher.place(x=10, y=140)

        lbl_description = Label(self.root, text="Description", font=(
            "goudy old style", 15, 'bold'), bg='white')
        lbl_description.place(x=10, y=180)

        # === entry fields ===
        self.txt_courseName = Entry(self.root, textvariable=self.var_course, font=(
            "goudy old style", 15, 'bold'), bg='lightyellow')
        self.txt_courseName.place(x=150, y=60, width=200)

        txt_duration = Entry(self.root, textvariable=self.var_duration, font=(
            "goudy old style", 15, 'bold'), bg='lightyellow')
        txt_duration.place(x=150, y=100, width=200)

        self.txt_teacher = Entry(self.root, textvariable=self.var_teacher, font=(
            "goudy old style", 15, 'bold'), bg='lightyellow')
        self.txt_teacher.place(x=150, y=140, width=200)

        self.txt_description = Text(self.root, font=(
            "goudy old style", 15, 'bold'), bg='lightyellow')
        self.txt_description.place(x=150, y=180, width=500, height=130)

        # === buttons ===
        btn_save = Button(self.root, text="Save", font=(
            "goudy old style", 15, "bold"), bg="#187898", fg="white",
            cursor="hand2", command=self.add)
        btn_save.place(x=150, y=400, width=110, height=40)

        btn_update = Button(self.root, text="Update", font=(
            "goudy old style", 15, "bold"), bg="#D8B537", fg="white",
            cursor="hand2", command=self.update)
        btn_update.place(x=270, y=400, width=110, height=40)

        btn_delete = Button(self.root, text="Delete", font=(
            "goudy old style", 15, "bold"), bg="#5F3F9E", fg="white",
            cursor="hand2", command=self.delete)
        btn_delete.place(x=390, y=400, width=110, height=40)

        btn_clear = Button(self.root, text="Clear", font=(
            "goudy old style", 15, "bold"), bg="#607d8b", fg="white",
            cursor="hand2", command=self.clear)
        btn_clear.place(x=510, y=400, width=110, height=40)

        # === search panel ===
        lbl_search_courseName = Label(self.root, text="Search By | Course Name", font=(
            "goudy old style", 15, 'bold'), bg='white')
        lbl_search_courseName.place(x=870, y=60)

        txt_search_courseName = Entry(self.root, textvariable=self.var_search, font=(
            "goudy old style", 15, 'bold'), bg='lightyellow')
        txt_search_courseName.place(x=1100, y=60, width=180)

        btn_search = Button(self.root, text="Search", font=(
            "goudy old style", 15, "bold"), bg="#03a9f4", fg="white",
            cursor="hand2", command=self.search)
        btn_search.place(x=1290, y=60, width=120, height=28)

        # === content (table) ===
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=800, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(
            self.C_Frame,
            columns=("cid", "name", "duration", "teacher", "description"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="Course Id")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("teacher", text="Teacher")
        self.CourseTable.heading("description", text="Description")

        self.CourseTable["show"] = "headings"
        self.CourseTable.column("cid", width=80)
        self.CourseTable.column("name", width=140)
        self.CourseTable.column("duration", width=120)
        self.CourseTable.column("teacher", width=140)
        self.CourseTable.column("description", width=250)

        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ------------------------------------------------------------------
    # DB SCHEMA
    # ------------------------------------------------------------------
    def setup_db_schema(self):
        """Create course table and add teacher column if it doesn't exist."""
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        try:
            # base table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS course (
                    cid INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    duration TEXT,
                    teacher TEXT,
                    description TEXT
                )
            """)

            # if table existed before without teacher column, add it
            cur.execute("PRAGMA table_info(course)")
            columns = [row[1] for row in cur.fetchall()]
            if "teacher" not in columns:
                cur.execute("ALTER TABLE course ADD COLUMN teacher TEXT")
                con.commit()
        finally:
            con.close()

    # ------------------------------------------------------------------
    # BUTTON FUNCTIONS
    # ------------------------------------------------------------------
    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_teacher.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0', END)
        self.txt_courseName.config(state='normal')

    def delete(self):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror(
                    "Error", "Course Name should be required", parent=self.root)
                return

            cur.execute("SELECT * FROM course WHERE name=?",
                        (self.var_course.get(),))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror(
                    "Error", "Please select course from list", parent=self.root)
                return

            op = messagebox.askyesno(
                "Confirm", "Do you really want to delete?", parent=self.root)
            if op:
                cur.execute("DELETE FROM course WHERE name=?",
                            (self.var_course.get(),))
                con.commit()
                messagebox.showinfo(
                    "Delete", "Course Deleted Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, ev):
        self.txt_courseName.config(state='readonly')
        r = self.CourseTable.focus()
        content = self.CourseTable.item(r)
        row = content["values"]
        if not row:
            return
        # row = (cid, name, duration, teacher, description)
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_teacher.set(row[3])
        self.txt_description.delete('1.0', END)
        self.txt_description.insert(END, row[4])

    def add(self):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror(
                    "Error", "Course Name should be required", parent=self.root)
                return

            cur.execute("SELECT * FROM course WHERE name=?",
                        (self.var_course.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror(
                    "Error", "Course Name already present", parent=self.root)
                return

            cur.execute(
                "INSERT INTO course(name, duration, teacher, description) VALUES(?,?,?,?)",
                (
                    self.var_course.get(),
                    self.var_duration.get(),
                    self.var_teacher.get(),
                    self.txt_description.get('1.0', END).strip()
                )
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Course Added Successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update(self):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror(
                    "Error", "Course Name should be required", parent=self.root)
                return

            cur.execute("SELECT * FROM course WHERE name=?",
                        (self.var_course.get(),))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror(
                    "Error", "Select Course from list", parent=self.root)
                return

            cur.execute(
                "UPDATE course SET duration=?, teacher=?, description=? WHERE name=?",
                (
                    self.var_duration.get(),
                    self.var_teacher.get(),
                    self.txt_description.get('1.0', END).strip(),
                    self.var_course.get(),
                )
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Course Updated Successfully", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT cid, name, duration, teacher, description FROM course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        try:
            search_val = f"%{self.var_search.get()}%"
            cur.execute(
                "SELECT cid, name, duration, teacher, description FROM course WHERE name LIKE ?",
                (search_val,)
            )
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()
