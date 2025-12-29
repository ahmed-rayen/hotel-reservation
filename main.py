import tkinter as tk
from tkinter import ttk
from chambres_ui import open_chambres_window
from reservation_ui import reservation_ui
from clients_ui import open_clients_window   # ✅ ADD THIS

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
    padding=12
)

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
    width=30,
    command=open_clients_window    # ✅ FIXED
).pack(pady=12)

ttk.Button(
    root,
    text="Gestion des réservations",
    style="Main.TButton",
    width=30,
    command=reservation_ui
).pack(pady=12)

root.mainloop()
