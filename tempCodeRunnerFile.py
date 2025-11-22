# admin_dashboard.py

from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

DB_NAME = "cms.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


class AdminDashboard:
    def __init__(self, root, user_data=None):
        self.root = root
        self.root.title("Course Management System - Admin")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        self.user_data = user_data or {}
        self.username = self.user_data.get("username", "admin")

        # ---------- Top title ----------
        self.logo_dash = None
        if os.path.exists("images/logo_p.png"):
            self.logo_dash = ImageTk.PhotoImage(file="images/logo_p.png")

        title = Label(
            self.root,
            text="Course Management System - Admin",
            padx=10,
            compound=LEFT,
            image=self.logo_dash,
            font=("times new roman", 32, "bold"),
            bg="#005470",
            fg="white",
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        welcome_text = f"Welcome, {self.username} (Admin)"
        Label(
            self.root,
            text=welcome_text,
            font=("goudy old style", 12, "bold"),
            bg="#005470",
            fg="white",
            anchor="e",
        ).place(x=950, y=0, width=380, height=15)

        # ---------- Menu bar ----------
        M_Frame = LabelFrame(
            self.root,
            text="Menu",
            font=("times new roman", 15, "bold"),
            bg="#014359",
            fg="white",
            bd=5,
            relief=RIDGE,
        )
        M_Frame.place(x=10, y=70, width=1516, height=80)

        btn_manage_teachers = Button(
            M_Frame,
            text="Manage Teachers",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.focus_teacher_tab,
        )
        btn_manage_teachers.place(x=100, y=5, width=230, height=40)

        btn_manage_students = Button(
            M_Frame,
            text="Manage Students",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.focus_student_tab,
        )
        btn_manage_students.place(x=350, y=5, width=230, height=40)

        btn_logout = Button(
            M_Frame,
            text="Logout",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.logout,
        )
        btn_logout.place(x=600, y=5, width=200, height=40)

        # ---------- Center notebook (tabs) ----------
        self.notebook = ttk.Notebook(self.root)
        self.notebook.place(x=40, y=170, width=1270, height=480)

        self.tab_teacher = Frame(self.notebook, bg="white")
        self.tab_student = Frame(self.notebook, bg="white")

        self.notebook.add(self.tab_teacher, text="Teacher Accounts")
        self.notebook.add(self.tab_student, text="Student Accounts")

        self.build_teacher_tab()
        self.build_student_tab()

        # footer
        footer = Label(
            self.root,
            text="CMS - Admin Dashboard",
            font=("times new roman", 15),
            bg="#0E1115",
            fg="white",
        )
        footer.pack(side=BOTTOM, fill=X)

    # ==========================================================
    #                           TABS
    # ==========================================================

    def build_teacher_tab(self):
        # ---------- variables ----------
        self.t_name = StringVar()
        self.t_email = StringVar()
        self.t_phone = StringVar()
        self.t_username = StringVar()
        self.t_password = StringVar()
        self.t_search = StringVar()
        self.t_selected_user_id = None
        self.t_selected_teacher_id = None

        # ---------- left form ----------
        form = LabelFrame(
            self.tab_teacher,
            text="Add / Edit Teacher Account",
            font=("times new roman", 14, "bold"),
            bg="white",
        )
        form.place(x=10, y=10, width=450, height=430)

        Label(form, text="Name", font=("goudy old style", 13, "bold"),
              bg="white").place(x=20, y=30)
        Entry(form, textvariable=self.t_name, font=("goudy old style", 13),
              bg="lightyellow").place(x=150, y=30, width=250)

        Label(form, text="Email", font=("goudy old style", 13, "bold"),
              bg="white").place(x=20, y=70)
        Entry(form, textvariable=self.t_email, font=("goudy old style", 13),
              bg="lightyellow").place(x=150, y=70, width=250)

        Label(form, text="Phone", font=("goudy old style", 13, "bold"),
              bg="white").place(x=20, y=110)
        Entry(form, textvariable=self.t_phone, font=("goudy old style", 13),
              bg="lightyellow").place(x=150, y=110, width=250)

        Label(form, text="Username", font=("goudy old style", 13, "bold"),
              bg="white").place(x=20, y=150)
        Entry(form, textvariable=self.t_username, font=("goudy old style", 13),
              bg="lightyellow").place(x=150, y=150, width=250)

        Label(form, text="Password", font=("goudy old style", 13, "bold"),
              bg="white").place(x=20, y=190)
        Entry(form, textvariable=self.t_password, font=("goudy old style", 13),
              bg="lightyellow", show="*").place(x=150, y=190, width=250)

        btn_add = Button(
            form,
            text="Add",
            font=("goudy old style", 13, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.teacher_add,
        )
        btn_add.place(x=20, y=250, width=90, height=35)

        btn_update = Button(
            form,
            text="Update",
            font=("goudy old style", 13, "bold"),
            bg="#D8B537",
            fg="white",
            cursor="hand2",
            command=self.teacher_update,
        )
        btn_update.place(x=120, y=250, width=90, height=35)

        btn_delete = Button(
            form,
            text="Delete",
            font=("goudy old style", 13, "bold"),
            bg="#5F3F9E",
            fg="white",
            cursor="hand2",
            command=self.teacher_delete,
        )
        btn_delete.place(x=220, y=250, width=90, height=35)

        btn_clear = Button(
            form,
            text="Clear",
            font=("goudy old style", 13, "bold"),
            bg="#607d8b",
            fg="white",
            cursor="hand2",
            command=self.teacher_clear,
        )
        btn_clear.place(x=320, y=250, width=90, height=35)

        Label(
            form,
            text="(Teacher will login with this username & password.)",
            font=("goudy old style", 10),
            bg="white",
            fg="#444444",
        ).place(x=20, y=310)

        # ---------- right list ----------
        list_frame = LabelFrame(
            self.tab_teacher,
            text="Teacher Accounts",
            font=("times new roman", 14, "bold"),
            bg="white",
        )
        list_frame.place(x=480, y=10, width=770, height=430)

        Label(list_frame, text="Search (username or name)", font=(
            "goudy old style", 12, "bold"), bg="white").place(x=10, y=10)
        Entry(list_frame, textvariable=self.t_search, font=(
            "goudy old style", 12), bg="lightyellow").place(x=250, y=10, width=200)
        Button(
            list_frame,
            text="Search",
            font=("goudy old style", 11, "bold"),
            bg="#03a9f4",
            fg="white",
            cursor="hand2",
            command=self.teacher_search,
        ).place(x=470, y=8, width=90, height=28)
        Button(
            list_frame,
            text="Show All",
            font=("goudy old style", 11, "bold"),
            bg="#607d8b",
            fg="white",
            cursor="hand2",
            command=self.teacher_show,
        ).place(x=570, y=8, width=90, height=28)

        frame = Frame(list_frame, bd=2, relief=RIDGE)
        frame.place(x=10, y=45, width=740, height=340)

        scrolly = Scrollbar(frame, orient=VERTICAL)
        scrollx = Scrollbar(frame, orient=HORIZONTAL)

        self.TeacherTable = ttk.Treeview(
            frame,
            columns=("uid", "tid", "username", "name", "email", "phone"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set,
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.TeacherTable.xview)
        scrolly.config(command=self.TeacherTable.yview)

        self.TeacherTable.heading("uid", text="User ID")
        self.TeacherTable.heading("tid", text="Teacher ID")
        self.TeacherTable.heading("username", text="Username")
        self.TeacherTable.heading("name", text="Name")
        self.TeacherTable.heading("email", text="Email")
        self.TeacherTable.heading("phone", text="Phone")

        self.TeacherTable["show"] = "headings"
        self.TeacherTable.column("uid", width=60)
        self.TeacherTable.column("tid", width=80)
        self.TeacherTable.column("username", width=120)
        self.TeacherTable.column("name", width=150)
        self.TeacherTable.column("email", width=180)
        self.TeacherTable.column("phone", width=120)

        self.TeacherTable.pack(fill=BOTH, expand=1)
        self.TeacherTable.bind("<ButtonRelease-1>", self.teacher_get_data)

        self.teacher_show()

    # ----------------------------------------------------------

    def build_student_tab(self):
        self.s_username = StringVar()
        self.s_password = StringVar()
        self.s_search = StringVar()
        self.s_selected_user_id = None

        form = LabelFrame(
            self.tab_student,
            text="Add / Edit Student Account",
            font=("times new roman", 14, "bold"),
            bg="white",
        )
        form.place(x=10, y=10, width=450, height=250)

        Label(form, text="Username", font=("goudy old style", 13, "bold"),
              bg="white").place(x=20, y=40)
        Entry(form, textvariable=self.s_username, font=("goudy old style", 13),
              bg="lightyellow").place(x=150, y=40, width=250)

        Label(form, text="Password", font=("goudy old style", 13, "bold"),
              bg="white").place(x=20, y=90)
        Entry(form, textvariable=self.s_password, font=("goudy old style", 13),
              bg="lightyellow", show="*").place(x=150, y=90, width=250)

        btn_add = Button(
            form,
            text="Add",
            font=("goudy old style", 13, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.student_add,
        )
        btn_add.place(x=20, y=150, width=90, height=35)

        btn_update = Button(
            form,
            text="Update",
            font=("goudy old style", 13, "bold"),
            bg="#D8B537",
            fg="white",
            cursor="hand2",
            command=self.student_update,
        )
        btn_update.place(x=120, y=150, width=90, height=35)

        btn_delete = Button(
            form,
            text="Delete",
            font=("goudy old style", 13, "bold"),
            bg="#5F3F9E",
            fg="white",
            cursor="hand2",
            command=self.student_delete,
        )
        btn_delete.place(x=220, y=150, width=90, height=35)

        btn_clear = Button(
            form,
            text="Clear",
            font=("goudy old style", 13, "bold"),
            bg="#607d8b",
            fg="white",
            cursor="hand2",
            command=self.student_clear,
        )
        btn_clear.place(x=320, y=150, width=90, height=35)

        Label(
            form,
            text="(Student will login with this username & password.)",
            font=("goudy old style", 10),
            bg="white",
            fg="#444444",
        ).place(x=20, y=200)

        # ---- list ----
        list_frame = LabelFrame(
            self.tab_student,
            text="Student Accounts",
            font=("times new roman", 14, "bold"),
            bg="white",
        )
        list_frame.place(x=480, y=10, width=770, height=430)

        Label(list_frame, text="Search username", font=(
            "goudy old style", 12, "bold"), bg="white").place(x=10, y=10)
        Entry(list_frame, textvariable=self.s_search, font=(
            "goudy old style", 12), bg="lightyellow").place(x=180, y=10, width=220)
        Button(
            list_frame,
            text="Search",
            font=("goudy old style", 11, "bold"),
            bg="#03a9f4",
            fg="white",
            cursor="hand2",
            command=self.student_search,
        ).place(x=410, y=8, width=90, height=28)
        Button(
            list_frame,
            text="Show All",
            font=("goudy old style", 11, "bold"),
            bg="#607d8b",
            fg="white",
            cursor="hand2",
            command=self.student_show,
        ).place(x=510, y=8, width=90, height=28)

        frame = Frame(list_frame, bd=2, relief=RIDGE)
        frame.place(x=10, y=45, width=740, height=340)

        scrolly = Scrollbar(frame, orient=VERTICAL)
        scrollx = Scrollbar(frame, orient=HORIZONTAL)

        self.StudentTable = ttk.Treeview(
            frame,
            columns=("uid", "username", "role"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set,
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)

        self.StudentTable.heading("uid", text="User ID")
        self.StudentTable.heading("username", text="Username")
        self.StudentTable.heading("role", text="Role")

        self.StudentTable["show"] = "headings"
        self.StudentTable.column("uid", width=80)
        self.StudentTable.column("username", width=180)
        self.StudentTable.column("role", width=100)

        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.student_get_data)

        self.student_show()

    # ==========================================================
    #                      TEACHER HANDLERS
    # ==========================================================

    def teacher_clear(self):
        self.t_name.set("")
        self.t_email.set("")
        self.t_phone.set("")
        self.t_username.set("")
        self.t_password.set("")
        self.t_selected_user_id = None
        self.t_selected_teacher_id = None

    def teacher_show(self):
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute(
                """
                SELECT u.id, t.id, u.username, t.name, t.email, t.phone
                FROM users u
                LEFT JOIN teacher t ON u.teacher_id = t.id
                WHERE u.role='Teacher'
                """
            )
            rows = cur.fetchall()
            self.TeacherTable.delete(*self.TeacherTable.get_children())
            for row in rows:
                self.TeacherTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error loading teachers: {ex}", parent=self.root)
        finally:
            con.close()

    def teacher_search(self):
        val = f"%{self.t_search.get()}%"
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute(
                """
                SELECT u.id, t.id, u.username, t.name, t.email, t.phone
                FROM users u
                LEFT JOIN teacher t ON u.teacher_id = t.id
                WHERE u.role='Teacher' AND (u.username LIKE ? OR t.name LIKE ?)
                """,
                (val, val),
            )
            rows = cur.fetchall()
            self.TeacherTable.delete(*self.TeacherTable.get_children())
            for row in rows:
                self.TeacherTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error searching teachers: {ex}", parent=self.root)
        finally:
            con.close()

    def teacher_get_data(self, ev):
        r = self.TeacherTable.focus()
        content = self.TeacherTable.item(r)
        row = content["values"]
        if not row:
            return
        self.t_selected_user_id = row[0]
        self.t_selected_teacher_id = row[1]
        self.t_username.set(row[2])
        self.t_name.set(row[3])
        self.t_email.set(row[4])
        self.t_phone.set(row[5])

    def teacher_add(self):
        if (self.t_name.get().strip() == "" or
                self.t_username.get().strip() == "" or
                self.t_password.get().strip() == ""):
            messagebox.showerror(
                "Error", "Name, Username and Password are required.", parent=self.root)
            return

        con = get_connection()
        cur = con.cursor()
        try:
            # check username
            cur.execute("SELECT id FROM users WHERE username=?",
                        (self.t_username.get().strip(),))
            if cur.fetchone():
                messagebox.showerror(
                    "Error", "Username already exists.", parent=self.root)
                return

            # create teacher row
            cur.execute(
                "INSERT INTO teacher(name, email, phone) VALUES(?,?,?)",
                (self.t_name.get().strip(), self.t_email.get(
                ).strip(), self.t_phone.get().strip()),
            )
            teacher_id = cur.lastrowid

            # create user row
            cur.execute(
                "INSERT INTO users(username, password, role, teacher_id, student_id) VALUES(?,?,?,?,?)",
                (self.t_username.get().strip(),
                 self.t_password.get().strip(), "Teacher", teacher_id, None),
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Teacher account created.", parent=self.root)
            self.teacher_clear()
            self.teacher_show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error adding teacher: {ex}", parent=self.root)
        finally:
            con.close()

    def teacher_update(self):
        if not self.t_selected_user_id:
            messagebox.showerror(
                "Error", "Select a teacher from the list first.", parent=self.root)
            return
        con = get_connection()
        cur = con.cursor()
        try:
            # check username uniqueness (except own)
            cur.execute(
                "SELECT id FROM users WHERE username=? AND id<>?",
                (self.t_username.get().strip(), self.t_selected_user_id),
            )
            if cur.fetchone():
                messagebox.showerror(
                    "Error", "Username already exists.", parent=self.root)
                return

            cur.execute(
                "UPDATE teacher SET name=?, email=?, phone=? WHERE id=?",
                (
                    self.t_name.get().strip(),
                    self.t_email.get().strip(),
                    self.t_phone.get().strip(),
                    self.t_selected_teacher_id,
                ),
            )
            cur.execute(
                "UPDATE users SET username=?, password=? WHERE id=?",
                (
                    self.t_username.get().strip(),
                    self.t_password.get().strip(),
                    self.t_selected_user_id,
                ),
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Teacher account updated.", parent=self.root)
            self.teacher_show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error updating teacher: {ex}", parent=self.root)
        finally:
            con.close()

    def teacher_delete(self):
        if not self.t_selected_user_id:
            messagebox.showerror(
                "Error", "Select a teacher from the list first.", parent=self.root)
            return
        if not messagebox.askyesno("Confirm", "Delete selected teacher account?", parent=self.root):
            return

        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM users WHERE id=?",
                        (self.t_selected_user_id,))
            if self.t_selected_teacher_id:
                cur.execute("DELETE FROM teacher WHERE id=?",
                            (self.t_selected_teacher_id,))
            con.commit()
            messagebox.showinfo(
                "Deleted", "Teacher account deleted.", parent=self.root)
            self.teacher_clear()
            self.teacher_show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error deleting teacher: {ex}", parent=self.root)
        finally:
            con.close()

    # ==========================================================
    #                      STUDENT HANDLERS
    # ==========================================================

    def student_clear(self):
        self.s_username.set("")
        self.s_password.set("")
        self.s_selected_user_id = None

    def student_show(self):
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT id, username, role FROM users WHERE role='Student'")
            rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error loading students: {ex}", parent=self.root)
        finally:
            con.close()

    def student_search(self):
        val = f"%{self.s_search.get()}%"
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT id, username, role FROM users WHERE role='Student' AND username LIKE ?",
                (val,),
            )
            rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error searching students: {ex}", parent=self.root)
        finally:
            con.close()

    def student_get_data(self, ev):
        r = self.StudentTable.focus()
        content = self.StudentTable.item(r)
        row = content["values"]
        if not row:
            return
        self.s_selected_user_id = row[0]
        self.s_username.set(row[1])

    def student_add(self):
        if self.s_username.get().strip() == "" or self.s_password.get().strip() == "":
            messagebox.showerror(
                "Error", "Username and Password are required.", parent=self.root)
            return

        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT id FROM users WHERE username=?",
                        (self.s_username.get().strip(),))
            if cur.fetchone():
                messagebox.showerror(
                    "Error", "Username already exists.", parent=self.root)
                return

            cur.execute(
                "INSERT INTO users(username, password, role, teacher_id, student_id) VALUES(?,?,?,?,?)",
                (self.s_username.get().strip(),
                 self.s_password.get().strip(), "Student", None, None),
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Student account created.", parent=self.root)
            self.student_clear()
            self.student_show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error adding student: {ex}", parent=self.root)
        finally:
            con.close()

    def student_update(self):
        if not self.s_selected_user_id:
            messagebox.showerror(
                "Error", "Select a student from the list first.", parent=self.root)
            return

        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT id FROM users WHERE username=? AND id<>?",
                (self.s_username.get().strip(), self.s_selected_user_id),
            )
            if cur.fetchone():
                messagebox.showerror(
                    "Error", "Username already exists.", parent=self.root)
                return

            cur.execute(
                "UPDATE users SET username=?, password=? WHERE id=?",
                (self.s_username.get().strip(),
                 self.s_password.get().strip(), self.s_selected_user_id),
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Student account updated.", parent=self.root)
            self.student_show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error updating student: {ex}", parent=self.root)
        finally:
            con.close()

    def student_delete(self):
        if not self.s_selected_user_id:
            messagebox.showerror(
                "Error", "Select a student from the list first.", parent=self.root)
            return
        if not messagebox.askyesno("Confirm", "Delete selected student account?", parent=self.root):
            return

        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("DELETE FROM users WHERE id=?",
                        (self.s_selected_user_id,))
            con.commit()
            messagebox.showinfo(
                "Deleted", "Student account deleted.", parent=self.root)
            self.student_clear()
            self.student_show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error deleting student: {ex}", parent=self.root)
        finally:
            con.close()

    # ==========================================================
    #                        MISC
    # ==========================================================

    def focus_teacher_tab(self):
        self.notebook.select(self.tab_teacher)

    def focus_student_tab(self):
        self.notebook.select(self.tab_student)

    def logout(self):
        if not messagebox.askyesno("Logout", "Do you really want to logout?", parent=self.root):
            return
        self.root.destroy()
        from login import LoginWindow  # local import to avoid circular
        new_root = Tk()
        LoginWindow(new_root)
        new_root.mainloop()


if __name__ == "__main__":
    root = Tk()
    AdminDashboard(root, user_data={"username": "admin"})
    root.mainloop()
