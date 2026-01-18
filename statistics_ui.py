import tkinter as tk
from tkinter import ttk
from statistics import (
    total_chambres,
    chambres_libres,
    chambres_occupees,
    taux_occupation
)

BG = "#f4f6f9"
PRIMARY = "#1e3a8a"

def open_statistics_window():
    win = tk.Toplevel()
    win.title("Statistiques de l'hôtel")
    win.geometry("420x320")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="📊 Statistiques de l'hôtel",
        bg=PRIMARY,
        fg="white",
        font=("Segoe UI", 16, "bold"),
        pady=12
    ).pack(fill="x")

    frame = tk.Frame(win, bg=BG)
    frame.pack(pady=25)

    stats = [
        ("Nombre total de chambres", total_chambres()),
        ("Chambres libres", chambres_libres()),
        ("Chambres occupées", chambres_occupees()),
        ("Taux d’occupation", f"{taux_occupation()} %")
    ]

    for i, (label, value) in enumerate(stats):
        tk.Label(
            frame,
            text=label,
            bg=BG,
            font=("Segoe UI", 11)
        ).grid(row=i, column=0, sticky="w", pady=6, padx=10)

        tk.Label(
            frame,
            text=value,
            bg=BG,
            font=("Segoe UI", 11, "bold"),
            fg=PRIMARY
        ).grid(row=i, column=1, sticky="e", pady=6, padx=10)
