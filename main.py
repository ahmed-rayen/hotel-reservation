import tkinter as tk
from tkinter import ttk, messagebox

from chambres_ui import open_chambres_window
from clients_ui import open_clients_window
from reservation_ui import reservation_ui
from hotel_db import create_database
from statistics_ui import open_statistics_window


# ---------- INIT DATABASE ----------
try:
    create_database()
except Exception as e:
    messagebox.showerror("Database Error", str(e))

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Hotel Management System")
root.geometry("520x420")
root.configure(bg="#f4f6f8")
root.resizable(False, False)

# ---------- STYLE ----------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Main.TButton",
    font=("Segoe UI", 12),
    padding=12
)

style.configure(
    "Title.TLabel",
    font=("Segoe UI", 18, "bold"),
    foreground="#1f4e79",
    background="#f4f6f8"
)

style.configure(
    "Footer.TLabel",
    font=("Segoe UI", 9),
    foreground="#6b7280",
    background="#f4f6f8"
)

# ---------- TITLE ----------
ttk.Label(
    root,
    text="🏨 HOTEL MANAGEMENT SYSTEM",
    style="Title.TLabel"
).pack(pady=30)

# ---------- BUTTONS ----------
btn_frame = tk.Frame(root, bg="#f4f6f8")
btn_frame.pack(pady=10)

ttk.Button(
    btn_frame,
    text="Gestion des chambres",
    style="Main.TButton",
    width=30,
    command=lambda: open_chambres_window(root)
).pack(pady=10)

ttk.Button(
    btn_frame,
    text="Gestion des clients",
    style="Main.TButton",
    width=30,
    command=open_clients_window
).pack(pady=10)

ttk.Button(
    btn_frame,
    text="Gestion des réservations",
    style="Main.TButton",
    width=30,
    command=reservation_ui
).pack(pady=10)

ttk.Button(
    btn_frame,
    text="Statistiques",
    style="Main.TButton",
    width=30,
    command=open_statistics_window
).pack(pady=10)


# ---------- FOOTER ----------
ttk.Label(
    root,
    text="Projet Python – Gestion des réservations d’hôtel",
    style="Footer.TLabel"
).pack(side="bottom", pady=10)

root.mainloop()
