import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime

def tela_notas_emitidas(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📄 Notas Fiscais Emitidas", font=("Helvetica", 18, "bold"),
             bg="#f8f8ff", fg="#003366").pack(pady=10)

    # Área de lista
    tree_frame = tk.Frame(frame, bg="#f8f8ff")
    tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

    colunas = ("arquivo", "data", "tamanho")
    tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")
    tree.heading("arquivo", text="Nome do Arquivo")
    tree.heading("data", text="Data de Criação")
    tree.heading("tamanho", text="Tamanho")

    tree.column("arquivo", anchor="w", width=400)
    tree.column("data", anchor="center", width=150)
    tree.column("tamanho", anchor="center", width=100)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Pasta das notas
    pasta_notas = os.path.join("dados", "notas")
    os.makedirs(pasta_notas, exist_ok=True)

    def carregar_notas():
        tree.delete(*tree.get_children())
        arquivos = [f for f in os.listdir(pasta_notas) if f.endswith(".pdf")]
        for nome in sorted(arquivos):
            caminho = os.path.join(pasta_notas, nome)
            tamanho = os.path.getsize(caminho) / 1024  # em KB
            criado = datetime.datetime.fromtimestamp(os.path.getctime(caminho)).strftime("%d/%m/%Y %H:%M")
            tree.insert("", "end", values=(nome, criado, f"{tamanho:.1f} KB"))

    def abrir_nota(event=None):
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma nota para abrir.")
            return
        nome = tree.item(item[0])["values"][0]
        caminho = os.path.join(pasta_notas, nome)
        try:
            os.startfile(caminho)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a nota:\n{e}")

    tree.bind("<Double-1>", abrir_nota)

    # Botões
    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=10)

    ttk.Button(botoes_frame, text="🔄 Recarregar", width=20, command=carregar_notas).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="📂 Abrir Selecionada", width=20, command=abrir_nota).pack(side="left", padx=10)

    carregar_notas()
