# teacher_dashboard.py

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

from course import CourseClass
from student import studentClass
from course_material import courseMaterialClass
from view_material import viewMaterialClass
from profile import ProfileClass
from logout import handle_logout   # our helper function


class CMS:
    def __init__(self, root, user_data=None):
        self.root = root
        self.root.title("Course Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # ------------- logged-in user info -------------
        self.user_data = user_data or {}
        self.logged_role = self.user_data.get("role", "Guest")
        self.teacher_id = self.user_data.get("teacher_id")

        # ============ icons / title ============
        self.logo_dash = ImageTk.PhotoImage(file="images/logo_p.png")

        title = Label(
            self.root,
            text="Course Management System",
            padx=10,
            compound=LEFT,
            image=self.logo_dash,
            font=("times new roman", 40, "bold"),
            bg="#005470",
            fg="white",
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        # welcome text (top-right)
        welcome_text = f"Welcome, {self.user_data.get('username', 'Guest')} ({self.logged_role})"
        Label(self.root, text=welcome_text, font=("goudy old style", 12, "bold"),
              bg="#005470", fg="white").place(x=950, y=0, height=15)

        # ============ Menu Frame ============
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

        btn_courses = Button(
            M_Frame,
            text="Courses",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.add_course,
        )
        btn_courses.place(x=100, y=5, width=200, height=40)

        btn_student = Button(
            M_Frame,
            text="Students",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.add_student,
        )
        btn_student.place(x=320, y=5, width=200, height=40)

        btn_coursematerial = Button(
            M_Frame,
            text="Course Material",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.add_coursematerial,
        )
        btn_coursematerial.place(x=540, y=5, width=200, height=40)

        btn_viewmaterial = Button(
            M_Frame,
            text="View Material",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.add_viewmaterial,
        )
        btn_viewmaterial.place(x=760, y=5, width=200, height=40)

        btn_profile = Button(
            M_Frame,
            text="Profile",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.open_profile,
        )
        btn_profile.place(x=980, y=5, width=200, height=40)

        btn_logout = Button(
            M_Frame,
            text="Logout",
            font=("goudy old style", 18, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.add_logout,
        )
        btn_logout.place(x=1200, y=5, width=200, height=40)

        # ============ main background image ============
        self.bg_img = Image.open("images/bg.png")
        self.bg_img = self.bg_img.resize((920, 500), Image.Resampling.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.bg_img)

        self.lbl_bg = Label(self.root, image=self.bg_img)
        self.lbl_bg.place(x=290, y=160, width=920, height=500)

        # ============ stats labels ============
        self.lbl_course = Label(
            self.root,
            text="Total Courses\n[2]",
            font=("goudy old style", 18),
            bd=6,
            relief=RIDGE,
            bg="#D8B537",
            fg="white",
        )
        self.lbl_course.place(x=335, y=665, width=225, height=70)

        self.lbl_coursesyllabus = Label(
            self.root,
            text="Total Course Faculty\n[2]",
            font=("goudy old style", 18),
            bd=6,
            relief=RIDGE,
            bg="#005470",
            fg="white",
        )
        self.lbl_coursesyllabus.place(x=645, y=665, width=225, height=70)

        self.lbl_students = Label(
            self.root,
            text="Total Students\n[1]",
            font=("goudy old style", 18),
            bd=6,
            relief=RIDGE,
            bg="#5F3F9E",
            fg="white",
        )
        self.lbl_students.place(x=955, y=665, width=225, height=70)

        # ============ footer ============
        footer = Label(
            self.root,
            text="CMS-Course Management System\nContact Us for any Technichal Issue: 9509729380",
            font=("times new roman", 15),
            bg="#0E1115",
            fg="white",
        )
        footer.pack(side=BOTTOM, fill=X)

    # ------------------------------------------------------------------
    #   menu button handlers
    # ------------------------------------------------------------------

    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = studentClass(self.new_win)

    def add_coursematerial(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = courseMaterialClass(self.new_win)

    def add_viewmaterial(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = viewMaterialClass(self.new_win)

    def open_profile(self):
        # only teachers have profiles in our design
        if self.logged_role != "Teacher" or not self.teacher_id:
            messagebox.showerror(
                "Access Denied",
                "Profile is only available for teachers.",
                parent=self.root,
            )
            return

        self.new_win = Toplevel(self.root)
        self.new_obj = ProfileClass(self.new_win, teacher_id=self.teacher_id)

    def add_logout(self):
        # delegate to helper function in logout.py
        handle_logout(self.root)


# NOTE: do NOT start the app from here if you want the login
# Run:  python login.py
# Only if you ever want to test dashboard alone, uncomment below:
#
# if __name__ == "__main__":
#     root = Tk()
#     CMS(root)
#     root.mainloop()


# For testing dashboard alone (without login), you can run this file directly.
# Prevent dashboard from running directly.
# If someone runs dashboard.py, redirect them to login.
if __name__ == "__main__":
    from login import LoginWindow
    root = Tk()
    LoginWindow(root)
    root.mainloop()
