import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

def tela_consulta_estoque(janela):
    # Limpar a tela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Frame principal
    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    # Título
    tk.Label(frame, text="📋 Consulta de Estoque", font=("Helvetica", 18, "bold"),
             bg="#f8f8ff", fg="#004d66").pack(pady=10)

    # Campo de pesquisa
    pesquisa_frame = tk.Frame(frame, bg="#f8f8ff")
    pesquisa_frame.pack(pady=5)

    tk.Label(pesquisa_frame, text="🔍 Buscar por Nome ou Código:", font=("Helvetica", 12),
             bg="#f8f8ff").pack(side="left", padx=5)

    entrada_pesquisa = tk.Entry(pesquisa_frame, width=40, font=("Helvetica", 12))
    entrada_pesquisa.pack(side="left", padx=5)

    def pesquisar_estoque():
        termo = entrada_pesquisa.get().lower()
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if any(termo in v.lower() for v in valores):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Arquivo de estoque não encontrado.")

    # Botão de pesquisa
    tk.Button(pesquisa_frame, text="🔍 Pesquisar", bg="#cd853f", fg="white",
              font=("Helvetica", 11, "bold"), command=pesquisar_estoque).pack(side="left", padx=5)

    # Tabela de resultados
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(pady=10)

    colunas = ["Nome", "Código", "Preço", "Quantidade", "Data de Validade", "Fornecedor", "Descrição", "Categoria"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=12)

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0)
    scroll.grid(row=0, column=1, sticky="ns")

    def carregar_estoque():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    def exportar_csv():
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/estoque_consulta.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(colunas)
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Estoque exportado para 'dados/estoque_consulta.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Botões inferiores com novo estilo
    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="🔄 Atualizar", bg="#a0522d", fg="white",
              font=("Helvetica", 12, "bold"), command=carregar_estoque).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar CSV", bg="#8b4513", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    # Carrega dados inicialmente
    carregar_estoque()
