# logout.py

from tkinter import messagebox, Tk


def handle_logout(current_root):
    """
    Ask for confirmation.
    If YES:
        - close the current dashboard window
        - open the Login window again
    """
    from login import LoginWindow   # imported INSIDE to avoid circular import

    op = messagebox.askyesno("Logout", "Do you really want to logout?",
                             parent=current_root)
    if op:
        # close dashboard
        current_root.destroy()

        # reopen Login window
        root = Tk()
        LoginWindow(root)
        root.mainloop()
