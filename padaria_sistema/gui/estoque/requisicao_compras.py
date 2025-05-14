import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def tela_requisicao_compras(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#eef9f1")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🛒 Requisição de Compras", font=("Helvetica", 18, "bold"), bg="#eef9f1", fg="#2e8b57").pack(pady=10)

    form_frame = tk.Frame(frame, bg="#eef9f1")
    form_frame.pack(pady=20)

    campos = {
        "Produto Necessário": tk.Entry(form_frame, width=30),
        "Quantidade": tk.Entry(form_frame, width=30),
        "Urgência": ttk.Combobox(form_frame, values=["Baixa", "Média", "Alta"], width=28),
        "Justificativa": tk.Entry(form_frame, width=30)
    }

    for i, (label, entry) in enumerate(campos.items()):
        tk.Label(form_frame, text=label + ":", font=("Helvetica", 12), bg="#eef9f1", fg="#004d33").grid(row=i, column=0, padx=10, pady=8, sticky="e")
        entry.grid(row=i, column=1, padx=10, pady=8, sticky="w")

    def salvar_requisicao():
        dados = [e.get().strip() for e in campos.values()]
        if all(dados):
            with open("dados/requisicoes.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + f" | {datetime.now().strftime('%d/%m/%Y')}\n")
            messagebox.showinfo("Salvo", "Requisição registrada.")
            for e in campos.values():
                e.delete(0, tk.END)
            campos["Urgência"].set("")
            carregar_tabela()
        else:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")

    tk.Button(frame, text="Salvar Requisição", bg="#2e8b57", fg="white", font=("Helvetica", 12, "bold"), command=salvar_requisicao).pack(pady=10)

    tabela = ttk.Treeview(frame, columns=["Produto", "Qtd", "Urgência", "Justificativa", "Data"], show="headings", height=10)
    for col in tabela["columns"]:
        tabela.heading(col, text=col)
        tabela.column(col, width=140, anchor="center")
    tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def carregar_tabela():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/requisicoes.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    tabela.insert("", "end", values=linha.strip().split(" | "))
        except FileNotFoundError:
            pass

    carregar_tabela()
