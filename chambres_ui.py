import tkinter as tk
from tkinter import ttk, messagebox
from chambres import (
    ajouter_chambre,
    modifier_chambre,
    supprimer_chambre,
    afficher_chambres_libres,
    afficher_chambres_occupees
)

BG = "#f4f6f8"
PRIMARY = "#1f4e79"

def open_chambres_window(parent):
    window = tk.Toplevel(parent)
    window.title("Gestion des chambres")
    window.geometry("820x560")
    window.configure(bg=BG)
    window.resizable(False, False)

    # ================= TITLE =================
    tk.Label(
        window,
        text="Gestion des chambres",
        font=("Segoe UI", 16, "bold"),
        bg=BG,
        fg=PRIMARY
    ).pack(pady=10)

    # ================= FORM =================
    form = tk.LabelFrame(
        window,
        text=" Informations chambre ",
        font=("Segoe UI", 11, "bold"),
        bg=BG,
        fg=PRIMARY,
        padx=20,
        pady=15
    )
    form.pack(padx=20, pady=10, fill="x")

    tk.Label(form, text="Numéro :", bg=BG).grid(row=0, column=0, sticky="w", pady=6)
    tk.Label(form, text="Type :", bg=BG).grid(row=1, column=0, sticky="w", pady=6)
    tk.Label(form, text="Prix / nuit :", bg=BG).grid(row=2, column=0, sticky="w", pady=6)
    tk.Label(form, text="Statut :", bg=BG).grid(row=3, column=0, sticky="w", pady=6)

    num_entry = tk.Entry(form, width=30)
    type_entry = ttk.Combobox(form, values=["simple", "double", "suite"], state="readonly", width=27)
    prix_entry = tk.Entry(form, width=30)
    statut_entry = ttk.Combobox(form, values=["libre", "occupée"], state="readonly", width=27)

    num_entry.grid(row=0, column=1, pady=6, padx=10)
    type_entry.grid(row=1, column=1, pady=6, padx=10)
    prix_entry.grid(row=2, column=1, pady=6, padx=10)
    statut_entry.grid(row=3, column=1, pady=6, padx=10)

    # ================= BUTTONS =================
    btn_frame = tk.Frame(form, bg=BG)
    btn_frame.grid(row=4, column=1, pady=12)

    def clear_inputs():
        num_entry.delete(0, tk.END)
        prix_entry.delete(0, tk.END)
        type_entry.set("")
        statut_entry.set("")

    def add_room():
        try:
            ajouter_chambre(
                int(num_entry.get()),
                type_entry.get(),
                float(prix_entry.get()),
                statut_entry.get() or "libre"
            )
            refresh_all()
            clear_inputs()
            messagebox.showinfo("Succès", "Chambre ajoutée")
        except:
            messagebox.showerror("Erreur", "Données invalides")

    def update_room():
        if not num_entry.get():
            messagebox.showwarning("Attention", "Sélectionnez une chambre")
            return
        modifier_chambre(
            int(num_entry.get()),
            type_chambre=type_entry.get(),
            prix_nuit=float(prix_entry.get()),
            statut=statut_entry.get()
        )
        refresh_all()
        messagebox.showinfo("Succès", "Chambre modifiée")

    def delete_room():
        if not num_entry.get():
            messagebox.showwarning("Attention", "Sélectionnez une chambre")
            return
        if messagebox.askyesno("Confirmation", "Supprimer cette chambre ?"):
            supprimer_chambre(int(num_entry.get()))
            refresh_all()
            clear_inputs()

    ttk.Button(btn_frame, text="Ajouter", width=12, command=add_room).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Modifier", width=12, command=update_room).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Supprimer", width=12, command=delete_room).pack(side="left", padx=5)

    # ================= FILTERS =================
    filter_frame = tk.Frame(window, bg=BG)
    filter_frame.pack(pady=5)

    ttk.Button(filter_frame, text="Toutes", width=15, command=lambda: refresh_all()).pack(side="left", padx=5)
    ttk.Button(filter_frame, text="Libres", width=15, command=lambda: refresh_libres()).pack(side="left", padx=5)
    ttk.Button(filter_frame, text="Occupées", width=15, command=lambda: refresh_occupees()).pack(side="left", padx=5)

    # ================= TABLE =================
    table_frame = tk.Frame(window, bg=BG)
    table_frame.pack(padx=20, pady=10, fill="both", expand=True)

    columns = ("Num", "Type", "Prix", "Statut")
    table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor="center", width=170)

    table.pack(fill="both", expand=True)

    table.tag_configure("libre", background="#d4edda")
    table.tag_configure("occupee", background="#f8d7da")

    # ================= LOAD FUNCTIONS =================
    def clear_table():
        table.delete(*table.get_children())

    def refresh_libres():
        clear_table()
        for room in afficher_chambres_libres():
            table.insert("", "end", values=room, tags=("libre",))

    def refresh_occupees():
        clear_table()
        for room in afficher_chambres_occupees():
            table.insert("", "end", values=room, tags=("occupee",))

    def refresh_all():
        clear_table()
        for room in afficher_chambres_libres():
            table.insert("", "end", values=room, tags=("libre",))
        for room in afficher_chambres_occupees():
            table.insert("", "end", values=room, tags=("occupee",))

    # ================= TABLE SELECTION =================
    def on_select(event):
        selected = table.focus()
        if not selected:
            return
        values = table.item(selected, "values")
        num_entry.delete(0, tk.END)
        num_entry.insert(0, values[0])
        type_entry.set(values[1])
        prix_entry.delete(0, tk.END)
        prix_entry.insert(0, values[2])
        statut_entry.set(values[3])

    table.bind("<<TreeviewSelect>>", on_select)

    refresh_all()
