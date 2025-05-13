import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime

def tela_boletos_emitidos(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📄 Boletos Emitidos", font=("Helvetica", 18, "bold"),
             bg="#f8f8ff", fg="#004d66").pack(pady=10)

    # Cria a árvore
    tree_frame = tk.Frame(frame, bg="#f8f8ff")
    tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

    colunas = ("arquivo", "data", "tamanho")
    tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")
    tree.heading("arquivo", text="Nome do Boleto")
    tree.heading("data", text="Data de Criação")
    tree.heading("tamanho", text="Tamanho")

    tree.column("arquivo", anchor="w", width=400)
    tree.column("data", anchor="center", width=150)
    tree.column("tamanho", anchor="center", width=100)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Pasta dos boletos
    boletos = os.path.join("dados", "boletos")
    os.makedirs(boletos, exist_ok=True)

    def carregar_boletos():
        tree.delete(*tree.get_children())
        arquivos = [f for f in os.listdir(boletos) if f.endswith(".pdf")]
        for nome in sorted(arquivos):
            caminho = os.path.join(boletos, nome)
            tamanho = os.path.getsize(caminho) / 1024  # em KB
            criado = datetime.datetime.fromtimestamp(os.path.getctime(caminho)).strftime("%d/%m/%Y %H:%M")
            tree.insert("", "end", values=(nome, criado, f"{tamanho:.1f} KB"))

    def abrir_boleto(event=None):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um boleto para abrir.")
            return
        nome = tree.item(item[0])["values"][0]
        caminho = os.path.join(boletos, nome)
        try:
            os.startfile(caminho)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o boleto:\n{e}")

    tree.bind("<Double-1>", abrir_boleto)

    # Botões
    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=10)

    ttk.Button(botoes_frame, text="🔄 Recarregar", width=20, command=carregar_boletos).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="📂 Abrir Selecionado", width=20, command=abrir_boleto).pack(side="left", padx=10)

    carregar_boletos()
