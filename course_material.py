# course_material.py

import os
import shutil
import sqlite3
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class courseMaterialClass:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Course Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====== variables ======
        self.var_id = tk.StringVar()            # primary key id
        self.var_course = tk.StringVar()
        self.var_teacher = tk.StringVar()
        self.var_file_path = tk.StringVar()     # real saved path
        self.var_file_display = tk.StringVar()  # only filename for display
        self.var_search = tk.StringVar()

        # folder where pdfs will be copied
        # (relative to this script file, not where you run it from)
        base_dir = Path(__file__).resolve().parent
        self.material_dir = base_dir / "materials"
        self.material_dir.mkdir(exist_ok=True)

        # create table if not exists
        self.create_table()

        # ================= title ======================
        title = tk.Label(
            self.root,
            text="Manage Course Material",
            font=("times new roman", 20, "bold"),
            bg="#005470",
            fg="white",
        )
        title.place(x=10, y=15, width=1517, height=35)

        # =========== left side form ================
        lbl_course = tk.Label(
            self.root,
            text="Course Name",
            font=("goudy old style", 15, "bold"),
            bg="white",
        )
        lbl_course.place(x=10, y=60)

        lbl_teacher = tk.Label(
            self.root,
            text="Teacher Name",
            font=("goudy old style", 15, "bold"),
            bg="white",
        )
        lbl_teacher.place(x=10, y=110)

        lbl_file = tk.Label(
            self.root,
            text="Course Material (PDF)",
            font=("goudy old style", 15, "bold"),
            bg="white",
        )
        lbl_file.place(x=10, y=160)

        # entries
        self.course_list = []
        self.fetch_course()

        self.txt_course = ttk.Combobox(
            self.root,
            textvariable=self.var_course,
            values=self.course_list,
            state="readonly",
            font=("goudy old style", 15, "bold"),
            justify="center",
        )
        self.txt_course.place(x=200, y=60, width=250)
        self.txt_course.set("Select")

        self.txt_teacher = tk.Entry(
            self.root,
            textvariable=self.var_teacher,
            font=("goudy old style", 15, "bold"),
            bg="lightyellow",
        )
        self.txt_teacher.place(x=200, y=110, width=250)

        self.txt_file = tk.Entry(
            self.root,
            textvariable=self.var_file_display,
            font=("goudy old style", 15, "bold"),
            bg="lightyellow",
            state="readonly",
        )
        self.txt_file.place(x=200, y=160, width=250)

        btn_browse = tk.Button(
            self.root,
            text="Browse",
            font=("goudy old style", 12, "bold"),
            bg="#607d8b",
            fg="white",
            cursor="hand2",
            command=self.browse_file,
        )
        btn_browse.place(x=460, y=160, width=90, height=28)

        # ===== buttons (Save/Update/Delete/Clear) =====
        btn_save = tk.Button(
            self.root,
            text="Save",
            font=("goudy old style", 15, "bold"),
            bg="#187898",
            fg="white",
            cursor="hand2",
            command=self.add,
        )
        btn_save.place(x=200, y=220, width=110, height=40)

        btn_update = tk.Button(
            self.root,
            text="Update",
            font=("goudy old style", 15, "bold"),
            bg="#D8B537",
            fg="white",
            cursor="hand2",
            command=self.update,
        )
        btn_update.place(x=320, y=220, width=110, height=40)

        btn_delete = tk.Button(
            self.root,
            text="Delete",
            font=("goudy old style", 15, "bold"),
            bg="#5F3F9E",
            fg="white",
            cursor="hand2",
            command=self.delete,
        )
        btn_delete.place(x=440, y=220, width=110, height=40)

        btn_clear = tk.Button(
            self.root,
            text="Clear (Add Another)",
            font=("goudy old style", 12, "bold"),
            bg="#607d8b",
            fg="white",
            cursor="hand2",
            command=self.clear,
        )
        btn_clear.place(x=560, y=220, width=160, height=40)

        # ===== search panel (by course) ============
        lbl_search = tk.Label(
            self.root,
            text="Search By | Course",
            font=("goudy old style", 15, "bold"),
            bg="white",
        )
        lbl_search.place(x=760, y=60)

        txt_search = tk.Entry(
            self.root,
            textvariable=self.var_search,
            font=("goudy old style", 15, "bold"),
            bg="lightyellow",
        )
        txt_search.place(x=980, y=60, width=180)

        btn_search = tk.Button(
            self.root,
            text="Search",
            font=("goudy old style", 15, "bold"),
            bg="#03a9f4",
            fg="white",
            cursor="hand2",
            command=self.search,
        )
        btn_search.place(x=1170, y=60, width=120, height=28)

        # ====== table frame ========================
        self.C_Frame = tk.Frame(self.root, bd=2, relief="ridge")
        self.C_Frame.place(x=720, y=100, width=800, height=340)

        scrolly = tk.Scrollbar(self.C_Frame, orient="vertical")
        scrollx = tk.Scrollbar(self.C_Frame, orient="horizontal")

        self.MaterialTable = ttk.Treeview(
            self.C_Frame,
            columns=("id", "course", "teacher", "file"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set,
        )

        scrollx.pack(side="bottom", fill="x")
        scrolly.pack(side="right", fill="y")
        scrollx.config(command=self.MaterialTable.xview)
        scrolly.config(command=self.MaterialTable.yview)

        self.MaterialTable.heading("id", text="ID")
        self.MaterialTable.heading("course", text="Course")
        self.MaterialTable.heading("teacher", text="Teacher")
        self.MaterialTable.heading("file", text="File Name")

        self.MaterialTable["show"] = "headings"
        self.MaterialTable.column("id", width=50)
        self.MaterialTable.column("course", width=150)
        self.MaterialTable.column("teacher", width=150)
        self.MaterialTable.column("file", width=250)

        self.MaterialTable.pack(fill="both", expand=1)
        self.MaterialTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # =============================================================================
    # Helper DB methods
    # =============================================================================

    def create_table(self):
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS course_material (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course TEXT NOT NULL,
                teacher TEXT NOT NULL,
                file_path TEXT NOT NULL
            )
            """
        )
        con.commit()
        con.close()

    def fetch_course(self):
        """Fill combobox with course names from course table."""
        self.course_list.clear()
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        try:
            # Make sure you have created this table:
            # CREATE TABLE course(id INTEGER PRIMARY KEY, name TEXT);
            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()
            for row in rows:
                self.course_list.append(row[0])
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error fetching courses:\n{ex}", parent=self.root)
        finally:
            con.close()

    # =============================================================================
    # Button commands
    # =============================================================================

    def browse_file(self):
        try:
            file_path = filedialog.askopenfilename(
                parent=self.root,          # important if you use multiple windows
                title="Select PDF File",
                filetypes=[("PDF files", "*.pdf")],
            )
            if file_path:
                self.var_file_path.set(file_path)
                self.var_file_display.set(os.path.basename(file_path))
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error opening file dialog:\n{ex}", parent=self.root)

    def clear(self):
        self.var_id.set("")
        self.var_course.set("Select")
        self.var_teacher.set("")
        self.var_file_path.set("")
        self.var_file_display.set("")
        self.var_search.set("")
        self.txt_course.set("Select")
        self.show()

    def add(self):
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        try:
            if (
                self.var_course.get() == "Select"
                or self.var_teacher.get().strip() == ""
                or self.var_file_path.get().strip() == ""
            ):
                messagebox.showerror(
                    "Error", "All fields (Course, Teacher, PDF) are required", parent=self.root
                )
                return

            src = Path(self.var_file_path.get())
            if not src.exists():
                messagebox.showerror(
                    "Error", "Selected PDF file not found on disk.", parent=self.root
                )
                return

            # unique target filename
            target_name = f"{self.var_course.get()}_{src.name}"
            target_path = self.material_dir / target_name
            shutil.copy(src, target_path)

            cur.execute(
                "INSERT INTO course_material(course, teacher, file_path) VALUES(?,?,?)",
                (self.var_course.get(), self.var_teacher.get(), str(target_path)),
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Course material saved successfully.", parent=self.root)
            self.show()
            self.clear()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error while saving:\n{ex}", parent=self.root)
        finally:
            con.close()

    def update(self):
        if self.var_id.get() == "":
            messagebox.showerror(
                "Error", "Please select material from the list.", parent=self.root)
            return

        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT file_path FROM course_material WHERE id=?", (self.var_id.get(),))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror(
                    "Error", "Record not found.", parent=self.root)
                return
            old_path = row[0]

            new_path = old_path
            if self.var_file_path.get() and self.var_file_path.get() != old_path:
                src = Path(self.var_file_path.get())
                if src.exists():
                    target_name = f"{self.var_course.get()}_{src.name}"
                    target_path = self.material_dir / target_name
                    shutil.copy(src, target_path)
                    new_path = str(target_path)
                    # remove old file
                    try:
                        if old_path and os.path.exists(old_path):
                            os.remove(old_path)
                    except Exception:
                        pass

            cur.execute(
                "UPDATE course_material SET course=?, teacher=?, file_path=? WHERE id=?",
                (self.var_course.get(), self.var_teacher.get(),
                 new_path, self.var_id.get()),
            )
            con.commit()
            messagebox.showinfo(
                "Success", "Course material updated successfully.", parent=self.root)
            self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error while updating:\n{ex}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        if self.var_id.get() == "":
            messagebox.showerror(
                "Error", "Please select material from the list.", parent=self.root)
            return

        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        try:
            op = messagebox.askyesno(
                "Confirm", "Do you really want to delete?", parent=self.root
            )
            if not op:
                return

            cur.execute(
                "SELECT file_path FROM course_material WHERE id=?", (self.var_id.get(),))
            row = cur.fetchone()
            file_path = row[0] if row else None

            cur.execute("DELETE FROM course_material WHERE id=?",
                        (self.var_id.get(),))
            con.commit()

            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception:
                    pass

            messagebox.showinfo(
                "Delete", "Course material deleted successfully.", parent=self.root
            )
            self.clear()
            self.show()
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error while deleting:\n{ex}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course_material")
            rows = cur.fetchall()
            self.MaterialTable.delete(*self.MaterialTable.get_children())
            for row in rows:
                # row = (id, course, teacher, file_path)
                file_name = os.path.basename(row[3])
                self.MaterialTable.insert("", tk.END, values=(
                    row[0], row[1], row[2], file_name))
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error while loading data:\n{ex}", parent=self.root)
        finally:
            con.close()

    def get_data(self, event):
        r = self.MaterialTable.focus()
        content = self.MaterialTable.item(r)
        row = content.get("values", [])
        if not row:
            return

        self.var_id.set(row[0])
        self.var_course.set(row[1])
        self.txt_course.set(row[1])
        self.var_teacher.set(row[2])

        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT file_path FROM course_material WHERE id=?", (row[0],))
            full = cur.fetchone()
        finally:
            con.close()

        if full:
            self.var_file_path.set(full[0])
            self.var_file_display.set(os.path.basename(full[0]))

    def search(self):
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        try:
            cur.execute(
                "SELECT * FROM course_material WHERE course LIKE ?",
                ("%" + self.var_search.get() + "%",),
            )
            rows = cur.fetchall()
            self.MaterialTable.delete(*self.MaterialTable.get_children())
            if rows:
                for row in rows:
                    file_name = os.path.basename(row[3])
                    self.MaterialTable.insert(
                        "", tk.END, values=(row[0], row[1], row[2], file_name)
                    )
            else:
                messagebox.showerror(
                    "Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error while searching:\n{ex}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = courseMaterialClass(root)
    root.mainloop()
