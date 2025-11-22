# login.py

from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

from teacher_dashboard import CMS                     # Teacher dashboard
from student_dashboard import StudentDashboard   # Student dashboard
from admin_dashboard import AdminDashboard      # Admin dashboard

DB_NAME = "cms.db"


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Management System - Login")
        self.root.geometry("900x500+200+120")
        self.root.config(bg="#0E1115")
        self.root.resizable(False, False)

        # ============= left side image (optional) =================
        self.bg_img = None
        if os.path.exists("images/bg.png"):
            img = Image.open("images/bg.png")
            img = img.resize((500, 500), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(img)
            Label(self.root, image=self.bg_img, bd=0).place(
                x=0, y=0, width=500, height=500
            )

        # ============= right side login frame =====================
        login_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        login_frame.place(x=480, y=40, width=390, height=420)

        title = Label(
            login_frame,
            text="Welcome Back",
            font=("times new roman", 22, "bold"),
            bg="white",
            fg="#005470",
        )
        title.place(x=0, y=10, relwidth=1)

        subtitle = Label(
            login_frame,
            text="Course Management System",
            font=("goudy old style", 14),
            bg="white",
            fg="#187898",
        )
        subtitle.place(x=0, y=50, relwidth=1)

        # -------- variables ----------
        self.var_username = StringVar()
        self.var_password = StringVar()
        self.var_role = StringVar()

        # -------- form controls -------
        Label(
            login_frame,
            text="Login As",
            font=("goudy old style", 14, "bold"),
            bg="white",
        ).place(x=40, y=100)

        # Admin / Teacher / Student
        self.cmb_role = ttk.Combobox(
            login_frame,
            textvariable=self.var_role,
            values=("Admin", "Teacher", "Student"),
            state="readonly",
            font=("goudy old style", 12),
            justify=CENTER,
        )
        self.cmb_role.place(x=40, y=130, width=300)
        self.cmb_role.current(1)  # default "Teacher"

        Label(
            login_frame,
            text="Username",
            font=("goudy old style", 14, "bold"),
            bg="white",
        ).place(x=40, y=170)
        Entry(
            login_frame,
            textvariable=self.var_username,
            font=("goudy old style", 13),
            bg="#f0f0f0",
        ).place(x=40, y=200, width=300)

        Label(
            login_frame,
            text="Password",
            font=("goudy old style", 14, "bold"),
            bg="white",
        ).place(x=40, y=240)
        Entry(
            login_frame,
            textvariable=self.var_password,
            show="*",
            font=("goudy old style", 13),
            bg="#f0f0f0",
        ).place(x=40, y=270, width=300)

        btn_login = Button(
            login_frame,
            text="Log In",
            font=("goudy old style", 15, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.login,
        )
        btn_login.place(x=40, y=315, width=300, height=35)

        Label(
            login_frame,
            text="Not registered yet?",
            font=("goudy old style", 11),
            bg="white",
        ).place(x=40, y=360)

        btn_register = Button(
            login_frame,
            text="Create an account",
            font=("goudy old style", 11, "bold"),
            bg="white",
            fg="#187898",
            bd=0,
            cursor="hand2",
            command=self.open_register_window,
        )
        btn_register.place(x=180, y=355)

        btn_exit = Button(
            login_frame,
            text="Exit",
            font=("goudy old style", 12, "bold"),
            bg="#5F3F9E",
            fg="white",
            cursor="hand2",
            command=self.root.destroy,
        )
        btn_exit.place(x=150, y=390, width=90, height=25)

        # make sure db tables exist + default admin
        self.create_tables()

    # -----------------------------------------------------------------

    def create_tables(self):
        """Create users + teacher tables if not exist and seed an admin user."""
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()

        # User login credentials table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT UNIQUE NOT NULL,
                password   TEXT NOT NULL,
                role       TEXT NOT NULL,
                teacher_id INTEGER,
                student_id INTEGER
            )
            """
        )

        # Basic teacher table (profile details) – extended in profile.py
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS teacher (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                gender TEXT,
                dob TEXT,
                address TEXT,
                photo_path TEXT
            )
            """
        )

        # Seed a default admin if none exists
        cur.execute("SELECT id FROM users WHERE role='Admin'")
        row = cur.fetchone()
        if row is None:
            cur.execute(
                "INSERT INTO users(username, password, role, teacher_id, student_id) "
                "VALUES(?,?,?,?,?)",
                ("admin", "admin123", "Admin", None, None),
            )

        con.commit()
        con.close()

    # -----------------------------------------------------------------

    def login(self):
        username = self.var_username.get().strip()
        password = self.var_password.get().strip()
        role = self.var_role.get().strip()  # "Admin" / "Teacher" / "Student"

        if username == "" or password == "":
            messagebox.showerror(
                "Error",
                "Username and Password are required.",
                parent=self.root,
            )
            return

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT id, username, role, teacher_id, student_id "
                "FROM users WHERE username=? AND password=? AND role=?",
                (username, password, role),
            )
            row = cur.fetchone()

            if row is None:
                messagebox.showerror(
                    "Error",
                    "Invalid username / password / role.",
                    parent=self.root,
                )
                return

            # user row unpack
            user_data = {
                "id": row[0],
                "username": row[1],
                "role": row[2],
                "teacher_id": row[3],
                "student_id": row[4],
            }

            # SUCCESS MESSAGE
            messagebox.showinfo(
                "Success",
                f"Welcome {user_data['username']}!",
                parent=self.root,
            )

            # CLOSE LOGIN WINDOW
            self.root.destroy()

            # OPEN PROPER DASHBOARD
            if user_data["role"] == "Admin":
                root_dash = Tk()
                AdminDashboard(root_dash, user_data=user_data)
                root_dash.mainloop()
            elif user_data["role"] == "Teacher":
                root_dash = Tk()
                CMS(root_dash, user_data=user_data)
                root_dash.mainloop()
            else:  # Student
                root_dash = Tk()
                StudentDashboard(root_dash, user_data=user_data)
                root_dash.mainloop()

        except Exception as ex:
            messagebox.showerror(
                "Error",
                f"Error due to {str(ex)}",
                parent=self.root,
            )
        finally:
            con.close()

    # -----------------------------------------------------------------

    def open_register_window(self):
        self.new_win = Toplevel(self.root)
        RegisterWindow(self.new_win)


# =====================================================================
#                               REGISTER WINDOW
# =====================================================================

class RegisterWindow:
    """
    Self-registration for Teacher / Student.
    Admin accounts are only created via the seeded default or via AdminDashboard.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Register Account")
        self.root.geometry("600x450+260+150")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        # variables
        self.var_role = StringVar(value="Teacher")
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_username = StringVar()
        self.var_password = StringVar()
        self.var_confirm = StringVar()

        title = Label(
            self.root,
            text="Create New Account",
            font=("times new roman", 18, "bold"),
            bg="#005470",
            fg="white",
        )
        title.place(x=0, y=0, relwidth=1, height=40)

        # form
        Label(
            self.root,
            text="Register As",
            font=("goudy old style", 13, "bold"),
            bg="white",
        ).place(x=30, y=60)
        self.cmb_role = ttk.Combobox(
            self.root,
            textvariable=self.var_role,
            values=("Teacher", "Student"),
            state="readonly",
            font=("goudy old style", 12),
            justify=CENTER,
        )
        self.cmb_role.place(x=170, y=60, width=170)
        self.cmb_role.current(0)

        Label(
            self.root,
            text="Full Name",
            font=("goudy old style", 13, "bold"),
            bg="white",
        ).place(x=30, y=100)
        Entry(
            self.root,
            textvariable=self.var_name,
            font=("goudy old style", 12),
            bg="#f0f0f0",
        ).place(x=170, y=100, width=370)

        Label(
            self.root,
            text="Email",
            font=("goudy old style", 13, "bold"),
            bg="white",
        ).place(x=30, y=140)
        Entry(
            self.root,
            textvariable=self.var_email,
            font=("goudy old style", 12),
            bg="#f0f0f0",
        ).place(x=170, y=140, width=370)

        Label(
            self.root,
            text="Phone",
            font=("goudy old style", 13, "bold"),
            bg="white",
        ).place(x=30, y=180)
        Entry(
            self.root,
            textvariable=self.var_phone,
            font=("goudy old style", 12),
            bg="#f0f0f0",
        ).place(x=170, y=180, width=170)

        Label(
            self.root,
            text="Username",
            font=("goudy old style", 13, "bold"),
            bg="white",
        ).place(x=30, y=220)
        Entry(
            self.root,
            textvariable=self.var_username,
            font=("goudy old style", 12),
            bg="#f0f0f0",
        ).place(x=170, y=220, width=170)

        Label(
            self.root,
            text="Password",
            font=("goudy old style", 13, "bold"),
            bg="white",
        ).place(x=30, y=260)
        Entry(
            self.root,
            textvariable=self.var_password,
            show="*",
            font=("goudy old style", 12),
            bg="#f0f0f0",
        ).place(x=170, y=260, width=170)

        Label(
            self.root,
            text="Confirm Password",
            font=("goudy old style", 13, "bold"),
            bg="white",
        ).place(x=30, y=300)
        Entry(
            self.root,
            textvariable=self.var_confirm,
            show="*",
            font=("goudy old style", 12),
            bg="#f0f0f0",
        ).place(x=200, y=300, width=170)

        btn_register = Button(
            self.root,
            text="Register",
            font=("goudy old style", 15, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.register_user,
        )
        btn_register.place(x=200, y=350, width=200, height=40)

    # -----------------------------------------------------------------

    def register_user(self):
        role = self.var_role.get().strip()
        name = self.var_name.get().strip()
        email = self.var_email.get().strip()
        phone = self.var_phone.get().strip()
        username = self.var_username.get().strip()
        password = self.var_password.get().strip()
        confirm = self.var_confirm.get().strip()

        if name == "" or email == "" or username == "" or password == "":
            messagebox.showerror(
                "Error",
                "Name, Email, Username and Password are required.",
                parent=self.root,
            )
            return
        if password != confirm:
            messagebox.showerror(
                "Error",
                "Password and Confirm Password do not match.",
                parent=self.root,
            )
            return

        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        try:
            # check if username already exists
            cur.execute("SELECT id FROM users WHERE username=?", (username,))
            if cur.fetchone() is not None:
                messagebox.showerror(
                    "Error", "Username already exists.", parent=self.root
                )
                return

            teacher_id = None
            student_id = None

            if role == "Teacher":
                # create basic teacher profile row
                cur.execute(
                    "INSERT INTO teacher(name, email, phone) VALUES(?,?,?)",
                    (name, email, phone),
                )
                teacher_id = cur.lastrowid

            # Student registration: we only create a user record for now
            cur.execute(
                "INSERT INTO users(username, password, role, teacher_id, student_id) "
                "VALUES(?,?,?,?,?)",
                (username, password, role, teacher_id, student_id),
            )

            con.commit()
            messagebox.showinfo(
                "Success",
                "Account registered successfully.\nYou can log in now.",
                parent=self.root,
            )
            self.root.destroy()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root
            )
        finally:
            con.close()


# =====================================================================
#                               MAIN
# =====================================================================

if __name__ == "__main__":
    root = Tk()
    LoginWindow(root)
    root.mainloop()
