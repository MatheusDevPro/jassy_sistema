import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def tela_baixa_estoque(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#fff8f0")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🛠️ Baixa de Estoque", font=("Helvetica", 18, "bold"), bg="#fff8f0", fg="#aa4400").pack(pady=10)

    form_frame = tk.Frame(frame, bg="#fff8f0")
    form_frame.pack(pady=20)

    campos = {
        "Código do Produto": tk.Entry(form_frame, width=30),
        "Nome do Produto": tk.Entry(form_frame, width=30),
        "Quantidade a Dar Baixa": tk.Entry(form_frame, width=30),
        "Motivo": tk.Entry(form_frame, width=30)
    }

    for i, (label, entry) in enumerate(campos.items()):
        tk.Label(form_frame, text=label + ":", font=("Helvetica", 12), bg="#fff8f0", fg="#663300").grid(row=i, column=0, padx=10, pady=8, sticky="e")
        entry.grid(row=i, column=1, padx=10, pady=8, sticky="w")

    def registrar_baixa():
        dados = [e.get().strip() for e in campos.values()]
        if all(dados):
            with open("dados/baixa_estoque.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + f" | {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            messagebox.showinfo("Sucesso", "Baixa registrada com sucesso.")
            for e in campos.values():
                e.delete(0, tk.END)
            carregar_registros()
        else:
            messagebox.showwarning("Campos incompletos", "Preencha todos os campos.")

    tk.Button(frame, text="Registrar Baixa", bg="#cc3300", fg="white", font=("Helvetica", 12, "bold"), command=registrar_baixa).pack(pady=10)

    tabela_frame = tk.Frame(frame, bg="#fff8f0")
    tabela_frame.pack(fill="both", expand=True)

    colunas = ["Código", "Produto", "Quantidade", "Motivo", "Data/Hora"]

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=150, anchor="center")
    tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def carregar_registros():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/baixa_estoque.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    tabela.insert("", "end", values=linha.strip().split(" | "))
        except FileNotFoundError:
            pass

    carregar_registros()
