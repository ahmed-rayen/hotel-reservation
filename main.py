import tkinter as tk
from tkinter import ttk
from chambres_ui import open_chambres_window

root = tk.Tk()
root.title("Hotel Management System")
root.geometry("520x380")
root.configure(bg="#f4f6f8")
root.resizable(False, False)

# ---------- Style ----------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Main.TButton",
    font=("Segoe UI", 12),
    padding=12,
    background="#1f4e79",
    foreground="white"
)
style.map("Main.TButton", background=[("active", "#163a5c")])

# ---------- Title ----------
tk.Label(
    root,
    text="🏨 HOTEL MANAGEMENT SYSTEM",
    font=("Segoe UI", 18, "bold"),
    bg="#f4f6f8",
    fg="#1f4e79"
).pack(pady=30)

# ---------- Buttons ----------
ttk.Button(
    root,
    text="Gestion des chambres",
    style="Main.TButton",
    width=30,
    command=lambda: open_chambres_window(root)
).pack(pady=12)

ttk.Button(
    root,
    text="Gestion des clients",
    style="Main.TButton",
    width=30
).pack(pady=12)

ttk.Button(
    root,
    text="Gestion des réservations",
    style="Main.TButton",
    width=30
).pack(pady=12)

root.mainloop()
