import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from reservation import (
    ajouter_reservation,
    modifier_reservation,
    supprimer_reservation,
    afficher_reservations
)

BG = "#f4f6f9"
PRIMARY = "#1e3a8a"


def reservation_ui():
    win = tk.Toplevel()
    win.title("Gestion des Réservations")
    win.geometry("900x550")
    win.configure(bg=BG)
    win.resizable(False, False)

    tk.Label(
        win,
        text="Gestion des Réservations",
        bg=PRIMARY,
        fg="white",
        font=("Segoe UI", 18, "bold"),
        pady=15
    ).pack(fill="x")

    # ---------- Form ----------
    form = tk.Frame(win, bg=BG)
    form.pack(pady=15)

    labels = ["ID Client", "Num Chambre", "Date Début", "Date Fin"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(form, text=label, bg=BG).grid(row=i, column=0, pady=5, sticky="w")

        if "Date" in label:
            e = DateEntry(form, width=27, date_pattern="yyyy-mm-dd")
        else:
            e = ttk.Entry(form, width=30)

        e.grid(row=i, column=1, pady=5, padx=10)
        entries[label] = e

    # ---------- Table ----------
    table = ttk.Treeview(
        win,
        columns=("ID", "Client", "Chambre", "Début", "Fin"),
        show="headings",
        height=10
    )

    for col in table["columns"]:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=150)

    table.pack(padx=20, pady=10, fill="both", expand=True)

    def load_table():
        table.delete(*table.get_children())
        for row in afficher_reservations():
            table.insert("", "end", values=row)

    load_table()

    # ---------- Selection ----------
    def on_select(event):
        selected = table.selection()
        if not selected:
            return

        values = table.item(selected[0])["values"]

        entries["ID Client"].delete(0, tk.END)
        entries["Num Chambre"].delete(0, tk.END)

        entries["ID Client"].insert(0, values[1])
        entries["Num Chambre"].insert(0, values[2])
        entries["Date Début"].set_date(values[3])
        entries["Date Fin"].set_date(values[4])

    table.bind("<<TreeviewSelect>>", on_select)

    # ---------- Actions ----------
    def add():
        success, msg = ajouter_reservation(
            int(entries["ID Client"].get()),
            int(entries["Num Chambre"].get()),
            entries["Date Début"].get(),
            entries["Date Fin"].get()
        )
        if success:
            load_table()
            messagebox.showinfo("Succès", msg)
        else:
            messagebox.showerror("Erreur", msg)

    def update():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Attention", "Sélectionnez une réservation")
            return

        id_res = table.item(selected[0])["values"][0]

        ok = modifier_reservation(
            id_res,
            int(entries["ID Client"].get()),
            int(entries["Num Chambre"].get()),
            entries["Date Début"].get(),
            entries["Date Fin"].get()
        )

        if not ok:
            messagebox.showerror("Erreur", "Modification impossible")
        else:
            load_table()
            messagebox.showinfo("Succès", "Réservation modifiée")

    def delete():
        selected = table.selection()
        if not selected:
            return

        if not messagebox.askyesno("Confirmation", "Supprimer cette réservation ?"):
            return

        id_res = table.item(selected[0])["values"][0]
        supprimer_reservation(id_res)
        load_table()
        messagebox.showinfo("Succès", "Réservation supprimée")

    # ---------- Buttons ----------
    btns = tk.Frame(win, bg=BG)
    btns.pack(pady=10)

    ttk.Button(btns, text="Ajouter", width=15, command=add).pack(side="left", padx=5)
    ttk.Button(btns, text="Modifier", width=15, command=update).pack(side="left", padx=5)
    ttk.Button(btns, text="Supprimer", width=15, command=delete).pack(side="left", padx=5)
