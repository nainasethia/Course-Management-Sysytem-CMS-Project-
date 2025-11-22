# student_dashboard.py

from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import os
import sys
import subprocess
import shutil

DB_NAME = "cms.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ======================================================================
#                           STUDENT DASHBOARD
# ======================================================================

class StudentDashboard:
    def __init__(self, root, user_data=None):
        self.root = root
        self.root.title("Course Management System - Student")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        self.user_data = user_data or {}
        self.username = self.user_data.get("username", "Student")

        # ========= top title ==========
        self.logo_dash = None
        if os.path.exists("images/logo_p.png"):
            self.logo_dash = ImageTk.PhotoImage(file="images/logo_p.png")

        title = Label(
            self.root,
            text="Course Management System - Student",
            padx=10,
            compound=LEFT,
            image=self.logo_dash,
            font=("times new roman", 32, "bold"),
            bg="#005470",
            fg="white",
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        welcome_text = f"Welcome, {self.username} (Student)"
        Label(
            self.root,
            text=welcome_text,
            font=("goudy old style", 12, "bold"),
            bg="#005470",
            fg="white",
            anchor="e",
        ).place(x=950, y=0, width=380, height=15)

        # =================== MENU BAR ==========================
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

        btn_course_detail = Button(
            M_Frame,
            text="Course Detail",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.open_course_detail,
        )
        btn_course_detail.place(x=100, y=5, width=200, height=40)

        btn_course_syllabus = Button(
            M_Frame,
            text="Course Syllabus",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.open_course_syllabus,
        )
        btn_course_syllabus.place(x=320, y=5, width=220, height=40)

        btn_profile = Button(
            M_Frame,
            text="Profile",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.open_profile,
        )
        btn_profile.place(x=560, y=5, width=200, height=40)

        btn_logout = Button(
            M_Frame,
            text="Logout",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.logout,
        )
        btn_logout.place(x=780, y=5, width=200, height=40)

        # ============== background image ===================
        self.bg_img = None
        if os.path.exists("images/bg.png"):
            img = Image.open("images/bg.png")
            img = img.resize((920, 500), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(img)
            Label(self.root, image=self.bg_img).place(
                x=290, y=160, width=920, height=500
            )

        # ===== summary labels ========================
        self.lbl_courses = Label(
            self.root,
            text="Total Courses\n[0]",
            font=("goudy old style", 18),
            bd=6,
            relief=RIDGE,
            bg="#D8B537",
            fg="white",
        )
        self.lbl_courses.place(x=335, y=665, width=225, height=70)

        self.lbl_materials = Label(
            self.root,
            text="Total Course Syllabus\n[0]",
            font=("goudy old style", 18),
            bd=6,
            relief=RIDGE,
            bg="#005470",
            fg="white",
        )
        self.lbl_materials.place(x=645, y=665, width=225, height=70)

        # footer
        footer = Label(
            self.root,
            text="CMS - Student Dashboard",
            font=("times new roman", 15),
            bg="#0E1115",
            fg="white",
        )
        footer.pack(side=BOTTOM, fill=X)

        self.update_counts()

    # ==================================================================
    #                           MENU HANDLERS
    # ==================================================================

    def update_counts(self):
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM course")
            total_course = cur.fetchone()[0]
        except Exception:
            total_course = 0

        try:
            cur.execute("SELECT COUNT(*) FROM course_material")
            total_mat = cur.fetchone()[0]
        except Exception:
            total_mat = 0

        con.close()

        self.lbl_courses.config(text=f"Total Courses\n[{total_course}]")
        self.lbl_materials.config(text=f"Total Course Syllabus\n[{total_mat}]")

    def open_course_detail(self):
        win = Toplevel(self.root)
        CourseDetailWindow(win)

    def open_course_syllabus(self):
        win = Toplevel(self.root)
        CourseSyllabusWindow(win)

    def open_profile(self):
        win = Toplevel(self.root)
        StudentProfileWindow(win, self.user_data)

    def logout(self):
        ans = messagebox.askyesno(
            "Logout", "Do you really want to logout?", parent=self.root
        )
        if ans:
            self.root.destroy()
            # return to login window
            from login import LoginWindow  # local import to avoid circular import

            new_root = Tk()
            LoginWindow(new_root)
            new_root.mainloop()


# ======================================================================
#                       COURSE DETAIL WINDOW
# ======================================================================

class CourseDetailWindow:
    """
    Read-only view of available courses for students:
    columns: ID, Course Name, Teacher, Duration
    (Price removed because current course table has no price column)
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Course Detail")
        self.root.geometry("900x400+200+200")
        self.root.config(bg="white")

        Label(
            self.root,
            text="Available Courses",
            font=("times new roman", 18, "bold"),
            bg="#005470",
            fg="white",
        ).pack(side=TOP, fill=X)

        frame = Frame(self.root, bd=2, relief=RIDGE)
        frame.place(x=10, y=50, width=880, height=330)

        scrolly = Scrollbar(frame, orient=VERTICAL)
        scrollx = Scrollbar(frame, orient=HORIZONTAL)

        self.CourseTable = ttk.Treeview(
            frame,
            columns=("cid", "name", "teacher", "duration"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set,
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="ID")
        self.CourseTable.heading("name", text="Course Name")
        self.CourseTable.heading("teacher", text="Teacher")
        self.CourseTable.heading("duration", text="Duration")

        self.CourseTable["show"] = "headings"
        self.CourseTable.column("cid", width=60)
        self.CourseTable.column("name", width=220)
        self.CourseTable.column("teacher", width=180)
        self.CourseTable.column("duration", width=120)

        self.CourseTable.pack(fill=BOTH, expand=1)

        self.show_courses()

    def show_courses(self):
        con = get_connection()
        cur = con.cursor()
        self.CourseTable.delete(*self.CourseTable.get_children())
        try:
            # course table: cid, name, duration, teacher, description
            cur.execute(
                "SELECT cid, name, duration, teacher FROM course"
            )
            rows = cur.fetchall()
            for row in rows:
                # row: (cid, name, duration, teacher)
                self.CourseTable.insert(
                    "", END,
                    values=(row[0], row[1], row[3], row[2])
                )
        except Exception as ex:
            print("CourseDetail error:", ex)
            messagebox.showerror(
                "Error", "Could not load course detail from database.", parent=self.root
            )
        finally:
            con.close()


# ======================================================================
#                       COURSE SYLLABUS WINDOW
# ======================================================================

class CourseSyllabusWindow:
    """
    Shows course materials uploaded by teachers:
    columns: ID, Teacher, Course, File; student can open or download PDF
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Course Syllabus")
        self.root.geometry("950x430+200+180")
        self.root.config(bg="white")

        Label(
            self.root,
            text="Course Syllabus (Materials)",
            font=("times new roman", 18, "bold"),
            bg="#005470",
            fg="white",
        ).pack(side=TOP, fill=X)

        # table frame
        frame = Frame(self.root, bd=2, relief=RIDGE)
        frame.place(x=10, y=50, width=920, height=300)

        scrolly = Scrollbar(frame, orient=VERTICAL)
        scrollx = Scrollbar(frame, orient=HORIZONTAL)

        self.MaterialTable = ttk.Treeview(
            frame,
            columns=("id", "teacher", "course", "file"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set,
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.MaterialTable.xview)
        scrolly.config(command=self.MaterialTable.yview)

        self.MaterialTable.heading("id", text="ID")
        self.MaterialTable.heading("teacher", text="Teacher")
        self.MaterialTable.heading("course", text="Course")
        self.MaterialTable.heading("file", text="File Name")

        self.MaterialTable["show"] = "headings"
        self.MaterialTable.column("id", width=50)
        self.MaterialTable.column("teacher", width=150)
        self.MaterialTable.column("course", width=220)
        self.MaterialTable.column("file", width=320)

        self.MaterialTable.pack(fill=BOTH, expand=1)
        self.MaterialTable.bind("<ButtonRelease-1>", self.get_selected)

        # buttons
        btn_open = Button(
            self.root,
            text="Open / View",
            font=("goudy old style", 14, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.open_file,
        )
        btn_open.place(x=260, y=365, width=150, height=35)

        btn_download = Button(
            self.root,
            text="Download",
            font=("goudy old style", 14, "bold"),
            bg="#D8B537",
            fg="white",
            cursor="hand2",
            command=self.download_file,
        )
        btn_download.place(x=430, y=365, width=150, height=35)

        btn_close = Button(
            self.root,
            text="Close",
            font=("goudy old style", 13, "bold"),
            bg="#607d8b",
            fg="white",
            cursor="hand2",
            command=self.root.destroy,
        )
        btn_close.place(x=600, y=365, width=120, height=35)

        self.selected_id = None
        self.show_materials()

    def show_materials(self):
        con = get_connection()
        cur = con.cursor()
        self.MaterialTable.delete(*self.MaterialTable.get_children())
        try:
            # table from coursematerial.py:
            # id, course, teacher, file_path
            cur.execute(
                "SELECT id, teacher, course, file_path FROM course_material"
            )
            rows = cur.fetchall()
            for row in rows:
                file_name = os.path.basename(row[3])
                self.MaterialTable.insert(
                    "", END, values=(row[0], row[1], row[2], file_name)
                )
        except Exception as ex:
            print("CourseSyllabus error:", ex)
            messagebox.showerror(
                "Error", "Could not load course syllabus from database.", parent=self.root
            )
        finally:
            con.close()

    def get_selected(self, ev):
        r = self.MaterialTable.focus()
        content = self.MaterialTable.item(r)
        row = content["values"]
        if not row:
            self.selected_id = None
        else:
            self.selected_id = row[0]

    def get_file_path(self):
        if self.selected_id is None:
            return None

        con = get_connection()
        cur = con.cursor()
        cur.execute(
            "SELECT file_path FROM course_material WHERE id=?",
            (self.selected_id,),
        )
        row = cur.fetchone()
        con.close()
        return row[0] if row else None

    def open_file(self):
        file_path = self.get_file_path()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror(
                "Error", "Please select a material or file not found.", parent=self.root
            )
            return

        try:
            if sys.platform.startswith("win"):
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", file_path])
            else:
                subprocess.call(["xdg-open", file_path])
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Cannot open file.\n{str(ex)}", parent=self.root
            )

    def download_file(self):
        file_path = self.get_file_path()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror(
                "Error", "Please select a material or file not found.", parent=self.root
            )
            return

        initial = os.path.basename(file_path)
        dest = filedialog.asksaveasfilename(
            title="Save PDF As",
            initialfile=initial,
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if dest:
            try:
                shutil.copy(file_path, dest)
                messagebox.showinfo(
                    "Saved", "File downloaded successfully.", parent=self.root
                )
            except Exception as ex:
                messagebox.showerror(
                    "Error", f"Could not download file.\n{str(ex)}", parent=self.root
                )


# ======================================================================
#                       SIMPLE STUDENT PROFILE
# ======================================================================

class StudentProfileWindow:
    def __init__(self, root, user_data):
        self.root = root
        self.root.title("Student Profile")
        self.root.geometry("500x300+300+220")
        self.root.config(bg="white")

        username = user_data.get("username", "")
        role = user_data.get("role", "Student")

        Label(
            self.root,
            text="My Profile",
            font=("times new roman", 18, "bold"),
            bg="#005470",
            fg="white",
        ).pack(side=TOP, fill=X)

        frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        frame.place(x=20, y=60, width=460, height=200)

        Label(frame, text="Username:", font=("goudy old style", 14, "bold"),
              bg="white").place(x=20, y=20)
        Label(frame, text=username, font=("goudy old style", 14),
              bg="white").place(x=160, y=20)

        Label(frame, text="Role:", font=("goudy old style", 14, "bold"),
              bg="white").place(x=20, y=60)
        Label(frame, text=role, font=("goudy old style", 14),
              bg="white").place(x=160, y=60)


# For direct testing:
if __name__ == "__main__":
    root = Tk()
    dummy_user = {"username": "test_student", "role": "Student"}
    StudentDashboard(root, user_data=dummy_user)
    root.mainloop()
