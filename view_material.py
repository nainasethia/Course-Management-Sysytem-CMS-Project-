# view_material.py

from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import shutil
import sys
import subprocess


class viewMaterialClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Course Management System")
        self.root.geometry("1000x480+150+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # ===== variables =====
        self.var_id = StringVar()
        self.var_course = StringVar()
        self.var_teacher = StringVar()
        self.var_file = StringVar()
        self.var_search = StringVar()
        self.var_search_by = StringVar(value="course")

        # ===== title =====
        title = Label(self.root, text="View Course Material", font=(
            "times new roman", 20, "bold"), bg="#005470", fg="white")
        title.place(x=10, y=15, width=1517, height=35)

        # ========= search area ==========
        lbl_search_by = Label(self.root, text="Search By", font=(
            "goudy old style", 15, "bold"), bg="white")
        lbl_search_by.place(x=10, y=65)

        self.cmb_search_by = ttk.Combobox(self.root, textvariable=self.var_search_by,
                                          values=("course", "teacher"), state="readonly",
                                          font=("goudy old style", 13, "bold"), justify=CENTER)
        self.cmb_search_by.place(x=110, y=65, width=130)
        self.cmb_search_by.current(0)

        txt_search = Entry(self.root, textvariable=self.var_search, font=(
            "goudy old style", 15, "bold"), bg="lightyellow")
        txt_search.place(x=260, y=65, width=200)

        btn_search = Button(self.root, text="Search", font=(
            "goudy old style", 13, "bold"), bg="#03a9f4", fg="white",
            cursor="hand2", command=self.search)
        btn_search.place(x=470, y=63, width=100, height=30)

        btn_show_all = Button(self.root, text="Show All", font=(
            "goudy old style", 13, "bold"), bg="#607d8b", fg="white",
            cursor="hand2", command=self.show)
        btn_show_all.place(x=580, y=63, width=100, height=30)

        # ========== table ===============
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=10, y=110, width=650, height=350)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.MaterialTable = ttk.Treeview(
            self.C_Frame,
            columns=("id", "course", "teacher", "file"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.MaterialTable.xview)
        scrolly.config(command=self.MaterialTable.yview)

        self.MaterialTable.heading("id", text="ID")
        self.MaterialTable.heading("course", text="Course")
        self.MaterialTable.heading("teacher", text="Teacher")
        self.MaterialTable.heading("file", text="File Name")

        self.MaterialTable["show"] = "headings"
        self.MaterialTable.column("id", width=40)
        self.MaterialTable.column("course", width=150)
        self.MaterialTable.column("teacher", width=150)
        self.MaterialTable.column("file", width=250)

        self.MaterialTable.pack(fill=BOTH, expand=1)
        self.MaterialTable.bind("<ButtonRelease-1>", self.get_data)

        # ========== right side details / buttons ==========
        details_frame = LabelFrame(self.root, text="Details", font=(
            "times new roman", 15, "bold"), bg="white", bd=2, relief=RIDGE)
        details_frame.place(x=680, y=110, width=300, height=250)

        lbl_id = Label(details_frame, text="ID:", font=(
            "goudy old style", 13, "bold"), bg="white")
        lbl_id.place(x=10, y=10)
        lbl_course = Label(details_frame, text="Course:", font=(
            "goudy old style", 13, "bold"), bg="white")
        lbl_course.place(x=10, y=45)
        lbl_teacher = Label(details_frame, text="Teacher:", font=(
            "goudy old style", 13, "bold"), bg="white")
        lbl_teacher.place(x=10, y=80)
        lbl_file = Label(details_frame, text="File:", font=(
            "goudy old style", 13, "bold"), bg="white")
        lbl_file.place(x=10, y=115)

        self.lbl_id_val = Label(details_frame, textvariable=self.var_id, font=(
            "goudy old style", 13), bg="white")
        self.lbl_id_val.place(x=100, y=10)
        self.lbl_course_val = Label(details_frame, textvariable=self.var_course, font=(
            "goudy old style", 13), bg="white")
        self.lbl_course_val.place(x=100, y=45)
        self.lbl_teacher_val = Label(details_frame, textvariable=self.var_teacher, font=(
            "goudy old style", 13), bg="white")
        self.lbl_teacher_val.place(x=100, y=80)
        self.lbl_file_val = Label(details_frame, textvariable=self.var_file, font=(
            "goudy old style", 13), bg="white", wraplength=180, justify="left")
        self.lbl_file_val.place(x=100, y=115)

        # buttons
        btn_open = Button(self.root, text="Open / View", font=(
            "goudy old style", 15, "bold"), bg="#187898", fg="white",
            cursor="hand2", command=self.open_file)
        btn_open.place(x=700, y=380, width=120, height=40)

        btn_download = Button(self.root, text="Download", font=(
            "goudy old style", 15, "bold"), bg="#D8B537", fg="white",
            cursor="hand2", command=self.download_file)
        btn_download.place(x=830, y=380, width=120, height=40)

        btn_clear = Button(self.root, text="Clear", font=(
            "goudy old style", 13, "bold"), bg="#607d8b", fg="white",
            cursor="hand2", command=self.clear)
        btn_clear.place(x=760, y=430, width=120, height=35)

        self.show()

    # ======================= DB & table helpers =======================

    def show(self):
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course_material")
            rows = cur.fetchall()
            self.MaterialTable.delete(*self.MaterialTable.get_children())
            for row in rows:
                file_name = os.path.basename(row[3])
                self.MaterialTable.insert("", END, values=(
                    row[0], row[1], row[2], file_name))
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search(self):
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        try:
            field = self.var_search_by.get()  # 'course' or 'teacher'
            value = self.var_search.get()
            if value == "":
                self.show()
                return

            if field == "course":
                cur.execute(
                    "SELECT * FROM course_material WHERE course LIKE ?", ('%' + value + '%',))
            else:
                cur.execute(
                    "SELECT * FROM course_material WHERE teacher LIKE ?", ('%' + value + '%',))

            rows = cur.fetchall()
            self.MaterialTable.delete(*self.MaterialTable.get_children())
            if rows:
                for row in rows:
                    file_name = os.path.basename(row[3])
                    self.MaterialTable.insert("", END, values=(
                        row[0], row[1], row[2], file_name))
            else:
                messagebox.showerror(
                    "Error", "No record found", parent=self.root)
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_full_path(self, record_id):
        con = sqlite3.connect("cms.db")
        cur = con.cursor()
        cur.execute(
            "SELECT file_path FROM course_material WHERE id=?", (record_id,))
        row = cur.fetchone()
        con.close()
        return row[0] if row else None

    def get_data(self, ev):
        r = self.MaterialTable.focus()
        content = self.MaterialTable.item(r)
        row = content["values"]
        if not row:
            return
        self.var_id.set(row[0])
        self.var_course.set(row[1])
        self.var_teacher.set(row[2])
        self.var_file.set(row[3])

    def clear(self):
        self.var_id.set("")
        self.var_course.set("")
        self.var_teacher.set("")
        self.var_file.set("")
        self.var_search.set("")
        self.var_search_by.set("course")
        self.cmb_search_by.current(0)

    # ===================== open & download ============================

    def open_file(self):
        """Open selected PDF with default viewer."""
        if self.var_id.get() == "":
            messagebox.showerror(
                "Error", "Please select a material first.", parent=self.root)
            return

        file_path = self.get_full_path(self.var_id.get())
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror(
                "Error", "File not found on disk.", parent=self.root)
            return

        try:
            if sys.platform.startswith('win'):
                os.startfile(file_path)      # Windows
            elif sys.platform == "darwin":
                subprocess.call(["open", file_path])  # macOS
            else:
                subprocess.call(["xdg-open", file_path])  # Linux
        except Exception as ex:
            messagebox.showerror(
                "Error", f"Cannot open file.\n{str(ex)}", parent=self.root)

    def download_file(self):
        """Let user choose where to save a copy of the PDF."""
        if self.var_id.get() == "":
            messagebox.showerror(
                "Error", "Please select a material first.", parent=self.root)
            return

        src_path = self.get_full_path(self.var_id.get())
        if not src_path or not os.path.exists(src_path):
            messagebox.showerror(
                "Error", "File not found on disk.", parent=self.root)
            return

        initial_name = os.path.basename(src_path)

        dest = filedialog.asksaveasfilename(
            title="Save PDF As",
            initialfile=initial_name,
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if dest:
            try:
                shutil.copy(src_path, dest)
                messagebox.showinfo(
                    "Downloaded", "File downloaded successfully.", parent=self.root)
            except Exception as ex:
                messagebox.showerror(
                    "Error", f"Could not download file.\n{str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = viewMaterialClass(root)
    root.mainloop()
