import tkinter as tk
from tkinter import ttk, messagebox
from .setup import MissionSetupWindow

# Simple in-memory user store for demo (replace with DB for production)
_USERS = {"admin": "admin"}

class LoginWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Space Debris — Login")
        self.root.geometry("420x260")
        self._build()

    def _build(self):
        frm = ttk.Frame(self.root, padding=16)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Space Debris Simulation", font=("Segoe UI", 14, "bold")).pack(pady=8)

        # username/password
        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()

        grid = ttk.Frame(frm)
        grid.pack(fill="x", pady=6)
        ttk.Label(grid, text="Username:").grid(row=0, column=0, sticky="w")
        ttk.Entry(grid, textvariable=self.user_var).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Label(grid, text="Password:").grid(row=1, column=0, sticky="w", pady=(8,0))
        ttk.Entry(grid, textvariable=self.pass_var, show="*").grid(row=1, column=1, sticky="ew", padx=8, pady=(8,0))
        grid.columnconfigure(1, weight=1)

        btns = ttk.Frame(frm)
        btns.pack(fill="x", pady=(12,0))
        ttk.Button(btns, text="Login", command=self._login).pack(side="left", expand=True, fill="x")
        ttk.Button(btns, text="Register", command=self._register_popup).pack(side="left", expand=True, fill="x")

        self.root.bind("<Return>", lambda e: self._login())

    def _login(self):
        u = self.user_var.get().strip()
        p = self.pass_var.get().strip()
        if not u or not p:
            messagebox.showerror("Error", "Enter username and password.")
            return
        if _USERS.get(u) != p:
            messagebox.showerror("Error", "Invalid credentials.")
            return
        # open mission setup window in same root (destroying widgets)
        for w in self.root.winfo_children():
            w.destroy()
        MissionSetupWindow(self.root, commander=u)

    def _register_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Register")
        popup.geometry("360x160")
        frm = ttk.Frame(popup, padding=12)
        frm.pack(fill="both", expand=True)
        user = tk.StringVar()
        pwd = tk.StringVar()
        ttk.Label(frm, text="New username:").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=user).grid(row=0, column=1, sticky="ew", padx=8)
        ttk.Label(frm, text="New password:").grid(row=1, column=0, sticky="w", pady=(8,0))
        ttk.Entry(frm, textvariable=pwd, show="*").grid(row=1, column=1, sticky="ew", padx=8, pady=(8,0))
        frm.columnconfigure(1, weight=1)
        def register():
            nu, npw = user.get().strip(), pwd.get().strip()
            if not nu or not npw:
                messagebox.showerror("Error", "Fields cannot be empty.", parent=popup)
                return
            if nu in _USERS:
                messagebox.showerror("Error", "User exists.", parent=popup)
                return
            _USERS[nu] = npw
            messagebox.showinfo("Success", "User registered.", parent=popup)
            popup.destroy()
        ttk.Button(frm, text="Register", command=register).grid(row=2, column=0, columnspan=2, pady=12, sticky="ew")
