import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from clients import (
    ajouter_client,
    modifier_client,
    supprimer_client
)

BG = "#f4f6f9"
PRIMARY = "#1e3a8a"

# ---------- DB helpers ----------
def get_connection():
    return sqlite3.connect("hotel.db")

def get_clients():
    conn = get_connection()
    cursor = conn.cursor()
    data = cursor.execute(
        "SELECT id_client, nom, prenom, telephone FROM clients"
    ).fetchall()
    conn.close()
    return data


def open_clients_window():
    win = tk.Toplevel()
    win.title("Gestion des Clients")
    win.geometry("850x520")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="Gestion des Clients",
        bg=PRIMARY,
        fg="white",
        font=("Segoe UI", 18, "bold"),
        pady=15
    ).pack(fill="x")

    # ---------- Form ----------
    form = tk.Frame(win, bg=BG)
    form.pack(pady=15)

    fields = ["Nom", "Prénom", "Téléphone"]
    entries = {}

    for i, field in enumerate(fields):
        tk.Label(form, text=field, bg=BG).grid(row=i, column=0, pady=6, sticky="w")
        e = ttk.Entry(form, width=30)
        e.grid(row=i, column=1, pady=6, padx=10)
        entries[field] = e

    # ---------- Table ----------
    table = ttk.Treeview(
        win,
        columns=("ID", "Nom", "Prénom", "Téléphone"),
        show="headings",
        height=10
    )

    for col in table["columns"]:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=150)

    table.pack(padx=20, pady=10, fill="both", expand=True)

    def load_table():
        table.delete(*table.get_children())
        for row in get_clients():
            table.insert("", "end", values=row)

    load_table()

    # ---------- Selection ----------
    def on_select(event):
        selected = table.selection()
        if not selected:
            return
        values = table.item(selected[0], "values")

        entries["Nom"].delete(0, tk.END)
        entries["Prénom"].delete(0, tk.END)
        entries["Téléphone"].delete(0, tk.END)

        entries["Nom"].insert(0, values[1])
        entries["Prénom"].insert(0, values[2])
        entries["Téléphone"].insert(0, values[3])

    table.bind("<<TreeviewSelect>>", on_select)

    # ---------- Utils ----------
    def clear_inputs():
        for e in entries.values():
            e.delete(0, tk.END)

    # ---------- Actions ----------
    def add():
        nom = entries["Nom"].get().strip()
        prenom = entries["Prénom"].get().strip()
        tel = entries["Téléphone"].get().strip()

        if not nom or not prenom or not tel:
            messagebox.showwarning("Attention", "Tous les champs sont obligatoires")
            return

        ajouter_client(nom, prenom, tel)
        load_table()
        clear_inputs()
        messagebox.showinfo("Succès", "Client ajouté")

    def update():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionnez un client")
            return

        id_client = table.item(selected[0], "values")[0]

        modifier_client(
            id_client,
            nom=entries["Nom"].get().strip() or None,
            prenom=entries["Prénom"].get().strip() or None,
            telephone=entries["Téléphone"].get().strip() or None
        )

        load_table()
        messagebox.showinfo("Succès", "Client modifié")

    def delete():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionnez un client")
            return

        if not messagebox.askyesno("Confirmation", "Supprimer ce client ?"):
            return

        id_client = table.item(selected[0], "values")[0]
        supprimer_client(id_client)
        load_table()
        clear_inputs()
        messagebox.showinfo("Succès", "Client supprimé")

    # ---------- Buttons ----------
    btns = tk.Frame(win, bg=BG)
    btns.pack(pady=10)

    ttk.Button(btns, text="Ajouter", width=15, command=add).pack(side="left", padx=5)
    ttk.Button(btns, text="Modifier", width=15, command=update).pack(side="left", padx=5)
    ttk.Button(btns, text="Supprimer", width=15, command=delete).pack(side="left", padx=5)
