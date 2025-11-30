# profile.py
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, UnidentifiedImageError
import sqlite3
import os
import shutil
from pathlib import Path


class ProfileClass:
    """
    Shows teacher profile (photo + details) with an Edit Profile button.
    Uses table: teacher(id INTEGER PK, name, email, phone, gender, dob, address, photo_path)
    """

    def __init__(self, root, teacher_id=1):
        self.root = root
        self.root.title("Course Management System")
        self.root.geometry("700x450+200+160")
        self.root.config(bg="white")
        self.root.focus_force()

        self.teacher_id = teacher_id

        # display variables
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_address = StringVar()

        # keep references to image objects so they are not garbage-collected
        self.photo_img = None

        # default avatar path (ensure this exists or set to None)
        self.default_photo_path = "images/user.png"

        # folder to store copied profile pics
        self.profile_pic_dir = Path("profile_pics")
        self.profile_pic_dir.mkdir(exist_ok=True)

        # ensure DB table exists, load profile and build UI
        self.create_table()
        self.load_profile()
        self.build_ui()
        self.refresh_view()

    # =========================== DB setup =============================

    def create_table(self):
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS teacher (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    gender TEXT,
                    dob TEXT,
                    address TEXT,
                    photo_path TEXT
                )"""
        )
        con.commit()
        con.close()

    def load_profile(self):
        """Ensure there is a row for this teacher_id and load it."""
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM teacher WHERE id=?", (self.teacher_id,))
        row = cur.fetchone()

        # if no record, create empty one with given id
        if row is None:
            cur.execute(
                "INSERT INTO teacher(id, name, email, phone, gender, dob, address, photo_path) "
                "VALUES(?,?,?,?,?,?,?,?)",
                (self.teacher_id, "", "", "", "", "", "", "")
            )
            con.commit()
            cur.execute("SELECT * FROM teacher WHERE id=?", (self.teacher_id,))
            row = cur.fetchone()

        con.close()

        # row: (id, name, email, phone, gender, dob, address, photo_path)
        self.profile_data = {
            "id": row[0],
            "name": row[1] or "",
            "email": row[2] or "",
            "phone": row[3] or "",
            "gender": row[4] or "",
            "dob": row[5] or "",
            "address": row[6] or "",
            "photo_path": row[7] or "",
        }

    # =========================== UI ==================================

    def build_ui(self):
        # title
        title = Label(self.root, text="My Profile", font=("times new roman", 20, "bold"),
                      bg="#005470", fg="white")
        title.place(x=10, y=10, width=680, height=35)

        # photo frame
        self.photo_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.photo_frame.place(x=30, y=70, width=200, height=230)

        self.lbl_photo = Label(self.photo_frame, bg="white")
        self.lbl_photo.place(x=10, y=10, width=180, height=210)

        # details frame
        details_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        details_frame.place(x=260, y=70, width=400, height=260)

        Label(details_frame, text="Name:", font=("goudy old style", 15, "bold"),
              bg="white").place(x=10, y=10)
        Label(details_frame, text="Email:", font=("goudy old style", 15, "bold"),
              bg="white").place(x=10, y=50)
        Label(details_frame, text="Phone:", font=("goudy old style", 15, "bold"),
              bg="white").place(x=10, y=90)
        Label(details_frame, text="Gender:", font=("goudy old style", 15, "bold"),
              bg="white").place(x=10, y=130)
        Label(details_frame, text="D.O.B:", font=("goudy old style", 15, "bold"),
              bg="white").place(x=10, y=170)
        Label(details_frame, text="Address:", font=("goudy old style", 15, "bold"),
              bg="white").place(x=10, y=210)

        Label(details_frame, textvariable=self.var_name, font=("goudy old style", 15),
              bg="white").place(x=120, y=10)
        Label(details_frame, textvariable=self.var_email, font=("goudy old style", 15),
              bg="white").place(x=120, y=50)
        Label(details_frame, textvariable=self.var_phone, font=("goudy old style", 15),
              bg="white").place(x=120, y=90)
        Label(details_frame, textvariable=self.var_gender, font=("goudy old style", 15),
              bg="white").place(x=120, y=130)
        Label(details_frame, textvariable=self.var_dob, font=("goudy old style", 15),
              bg="white").place(x=120, y=170)
        Label(details_frame, textvariable=self.var_address, font=("goudy old style", 15),
              bg="white", wraplength=250, justify="left").place(x=120, y=210)

        # edit button
        btn_edit = Button(self.root, text="Edit Profile", font=("goudy old style", 15, "bold"),
                          bg="#187898", fg="white", cursor="hand2", command=self.open_edit_window)
        btn_edit.place(x=270, y=360, width=150, height=40)

        btn_refresh = Button(self.root, text="Refresh", font=("goudy old style", 13, "bold"),
                             bg="#607d8b", fg="white", cursor="hand2", command=self.reload_and_refresh)
        btn_refresh.place(x=430, y=360, width=100, height=40)

    def refresh_view(self):
        """Push profile_data into StringVars and image label."""
        self.var_name.set(self.profile_data["name"])
        self.var_email.set(self.profile_data["email"])
        self.var_phone.set(self.profile_data["phone"])
        self.var_gender.set(self.profile_data["gender"])
        self.var_dob.set(self.profile_data["dob"])
        self.var_address.set(self.profile_data["address"])

        photo_path = self.profile_data["photo_path"] or self.default_photo_path
        if photo_path and not os.path.exists(photo_path):
            # fallback to default if available
            photo_path = self.default_photo_path if os.path.exists(
                self.default_photo_path) else None

        if photo_path:
            try:
                img = Image.open(photo_path)
                img = img.resize((180, 210), Image.Resampling.LANCZOS)
                # keep reference
                self.photo_img = ImageTk.PhotoImage(img)
                self.lbl_photo.config(image=self.photo_img, text="")
            except Exception:
                # if loading fails, show text instead
                self.lbl_photo.config(image="", text="No Image", font=(
                    "goudy old style", 15), bg="white")
        else:
            self.lbl_photo.config(image="", text="No Image", font=(
                "goudy old style", 15), bg="white")

    def reload_and_refresh(self):
        self.load_profile()
        self.refresh_view()

    # ======================= Edit Profile Window =====================

    def open_edit_window(self):
        # create a Toplevel and pass self to the editor
        self.edit_win = Toplevel(self.root)
        # make it modal-like
        self.edit_win.transient(self.root)
        self.edit_obj = EditProfileClass(self.edit_win, self)
        # block events to the main window until edit window is closed
        self.edit_win.grab_set()
        self.edit_win.wait_window()


class EditProfileClass:
    """
    Separate window to edit teacher profile.
    """

    def __init__(self, root, parent_profile: ProfileClass):
        self.root = root
        self.parent = parent_profile
        self.root.title("Edit Profile")
        self.root.geometry("600x430+250+180")
        self.root.config(bg="white")
        self.root.focus_force()

        # initialize variables with parent's current profile_data
        self.var_name = StringVar(value=self.parent.profile_data["name"])
        self.var_email = StringVar(value=self.parent.profile_data["email"])
        self.var_phone = StringVar(value=self.parent.profile_data["phone"])
        self.var_gender = StringVar(value=self.parent.profile_data["gender"])
        self.var_dob = StringVar(value=self.parent.profile_data["dob"])
        self.var_address = StringVar(value=self.parent.profile_data["address"])
        self.var_photo_path = StringVar(
            value=self.parent.profile_data["photo_path"])

        # keep a reference for preview image
        self.photo_preview = None

        # ========== title ===========
        title = Label(self.root, text="Edit Profile", font=("times new roman", 18, "bold"),
                      bg="#005470", fg="white")
        title.place(x=10, y=10, width=580, height=35)

        # ========== form ============
        Label(self.root, text="Name", font=("goudy old style", 15, "bold"),
              bg="white").place(x=20, y=60)
        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=160, y=60, width=250)

        Label(self.root, text="Email", font=("goudy old style", 15, "bold"),
              bg="white").place(x=20, y=100)
        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=160, y=100, width=250)

        Label(self.root, text="Phone", font=("goudy old style", 15, "bold"),
              bg="white").place(x=20, y=140)
        Entry(self.root, textvariable=self.var_phone, font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=160, y=140, width=250)

        Label(self.root, text="Gender", font=("goudy old style", 15, "bold"),
              bg="white").place(x=20, y=180)
        self.cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender,
                                       values=("Male", "Female", "Other"),
                                       state="readonly", justify=CENTER,
                                       font=("goudy old style", 13, "bold"))
        self.cmb_gender.place(x=160, y=180, width=150)
        if self.var_gender.get() not in ("Male", "Female", "Other"):
            self.cmb_gender.set("Male")

        Label(self.root, text="D.O.B", font=("goudy old style", 15, "bold"),
              bg="white").place(x=20, y=220)
        Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=160, y=220, width=250)

        Label(self.root, text="Address", font=("goudy old style", 15, "bold"),
              bg="white").place(x=20, y=260)
        Entry(self.root, textvariable=self.var_address, font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=160, y=260, width=380)

        # photo area
        Label(self.root, text="Photo", font=("goudy old style", 15, "bold"),
              bg="white").place(x=20, y=300)

        self.lbl_photo_name = Label(
            self.root,
            text=os.path.basename(self.var_photo_path.get(
            )) if self.var_photo_path.get() else "No file selected",
            font=("goudy old style", 11), bg="white", anchor="w"
        )
        self.lbl_photo_name.place(x=160, y=300, width=250)

        btn_browse = Button(self.root, text="Browse", font=("goudy old style", 12, "bold"),
                            bg="#607d8b", fg="white", cursor="hand2", command=self.browse_photo)
        btn_browse.place(x=420, y=297, width=100, height=28)

        # small preview
        self.preview_label = Label(self.root, bg="white")
        self.preview_label.place(x=420, y=60, width=150, height=150)
        # initial preview
        self.update_preview(self.var_photo_path.get())

        # buttons
        btn_save = Button(self.root, text="Save", font=("goudy old style", 15, "bold"),
                          bg="#187898", fg="white", cursor="hand2", command=self.save_profile)
        btn_save.place(x=220, y=350, width=120, height=40)

        btn_cancel = Button(self.root, text="Cancel", font=("goudy old style", 13, "bold"),
                            bg="#607d8b", fg="white", cursor="hand2", command=self.root.destroy)
        btn_cancel.place(x=360, y=350, width=100, height=40)

    # ------------- helpers for edit window -----------------

    def browse_photo(self):
        file_path = filedialog.askopenfilename(
            title="Select Profile Image",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif"),
                       ("All files", "*.*")]
        )
        if not file_path:
            return

        # Validate image first to avoid loading invalid/corrupt files
        try:
            # Using PIL verify to make sure file is actually an image
            with Image.open(file_path) as img_check:
                img_check.verify()
        except (UnidentifiedImageError, OSError) as ex:
            messagebox.showerror(
                "Invalid Image", "Selected file is not a valid image.", parent=self.root)
            return
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Could not open image: {ex}", parent=self.root)
            return

        # If validation passed, set var and update preview
        self.var_photo_path.set(file_path)
        self.lbl_photo_name.config(text=os.path.basename(file_path))
        self.update_preview(file_path)

    def update_preview(self, photo_path):
        """Safely load and show a small preview. Never let exceptions propagate to Tk callbacks."""
        if not photo_path:
            self.preview_label.config(image="", text="No Image")
            self.photo_preview = None
            return

        if not os.path.exists(photo_path):
            self.preview_label.config(image="", text="No Image")
            self.photo_preview = None
            return

        try:
            # Open image safely and resize
            with Image.open(photo_path) as img:
                img_copy = img.copy()
            img_copy.thumbnail((150, 150), Image.Resampling.LANCZOS)

            # keep reference to prevent GC
            self.photo_preview = ImageTk.PhotoImage(img_copy)
            self.preview_label.config(image=self.photo_preview, text="")

        except Exception as ex:
            # print to console for debugging and inform user
            print("Preview error:", ex)
            self.preview_label.config(image="", text="Invalid Image")
            self.photo_preview = None

    def save_profile(self):
        name = self.var_name.get().strip()
        email = self.var_email.get().strip()
        phone = self.var_phone.get().strip()

        if name == "" or email == "" or phone == "":
            messagebox.showerror(
                "Error", "Name, Email and Phone are required.", parent=self.root)
            return

        # prepare new_photo_path: start with existing path (could be empty)
        current_photo_path = self.parent.profile_data.get(
            "photo_path", "") or ""
        new_src = self.var_photo_path.get().strip()

        new_photo_path = current_photo_path  # default: unchanged

        try:
            # If user selected a new file and it's different from current, copy to profile_pics
            if new_src and os.path.exists(new_src) and os.path.abspath(new_src) != os.path.abspath(current_photo_path):
                ext = os.path.splitext(new_src)[1] or ".png"
                target = self.parent.profile_pic_dir / \
                    f"teacher_{self.parent.teacher_id}{ext}"
                # ensure a fresh copy (overwrite if existing)
                shutil.copy2(new_src, target)
                new_photo_path = str(target)

            # update DB
            con = sqlite3.connect("cms.db")
            cur = con.cursor()
            cur.execute(
                "UPDATE teacher SET name=?, email=?, phone=?, gender=?, dob=?, address=?, photo_path=? WHERE id=?",
                (name,
                 email,
                 phone,
                 self.var_gender.get(),
                 self.var_dob.get(),
                 self.var_address.get(),
                 new_photo_path,
                 self.parent.teacher_id)
            )
            con.commit()
            con.close()

            messagebox.showinfo(
                "Success", "Profile updated successfully.", parent=self.root)

            # refresh parent's profile_data and view (and keep image reference)
            self.parent.load_profile()
            self.parent.refresh_view()

            # Close edit window
            self.root.destroy()

        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error saving profile: {ex}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    app = ProfileClass(root)
    root.mainloop()
