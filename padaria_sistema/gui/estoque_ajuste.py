import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

def tela_ajuste_inventario(janela):
    # Limpar tela anterior
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f0fff0")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🛠️ Ajuste de Inventário", font=("Helvetica", 18, "bold"),
             bg="#f0fff0", fg="#2e8b57").pack(pady=10)

    # Campo de pesquisa
    busca_frame = tk.Frame(frame, bg="#f0fff0")
    busca_frame.pack(pady=5)

    tk.Label(busca_frame, text="🔍 Buscar Código ou Nome:", font=("Helvetica", 12),
             bg="#f0fff0").pack(side="left", padx=5)

    entrada_busca = tk.Entry(busca_frame, width=40)
    entrada_busca.pack(side="left", padx=5)

    def buscar_produto():
        termo = entrada_busca.get().lower()
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if any(termo in v.lower() for v in valores):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Arquivo de produtos não encontrado.")

    tk.Button(busca_frame, text="🔍 Buscar", bg="#2e8b57", fg="white",
              font=("Helvetica", 11, "bold"), command=buscar_produto).pack(side="left", padx=5)

    # Frame da tabela
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(pady=10)

    colunas = ["Nome", "Código", "Preço", "Quantidade", "Data de Validade", "Fornecedor", "Descrição", "Categoria"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0)
    scroll.grid(row=0, column=1, sticky="ns")

    # Campo para ajuste de quantidade
    ajuste_frame = tk.Frame(frame, bg="#f0fff0")
    ajuste_frame.pack(pady=10)

    tk.Label(ajuste_frame, text="📦 Novo Estoque (Quantidade):", font=("Helvetica", 12),
             bg="#f0fff0").pack(side="left", padx=5)

    entrada_qtd = tk.Entry(ajuste_frame, width=10)
    entrada_qtd.pack(side="left", padx=5)

    def ajustar_estoque():
        item = tabela.focus()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um item da tabela.")
            return

        nova_qtd = entrada_qtd.get()
        if not nova_qtd.isdigit():
            messagebox.showwarning("Erro", "Digite uma quantidade válida.")
            return

        dados_atuais = tabela.item(item)['values']
        dados_atuais[3] = nova_qtd  # Atualiza a quantidade

        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                linhas = f.readlines()

            with open("dados/produtos.txt", "w", encoding="utf-8") as f:
                for linha in linhas:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if valores[1] == dados_atuais[1]:  # Código do produto
                        f.write(" | ".join(dados_atuais) + "\n")
                    else:
                        f.write(linha)

            messagebox.showinfo("Sucesso", "Estoque ajustado com sucesso.")
            carregar_estoque()
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Arquivo de produtos não encontrado.")

    tk.Button(ajuste_frame, text="💾 Salvar Ajuste", bg="#228b22", fg="white",
              font=("Helvetica", 12, "bold"), command=ajustar_estoque).pack(side="left", padx=10)

    # Botões inferiores
    botoes_frame = tk.Frame(frame, bg="#f0fff0")
    botoes_frame.pack(pady=10)

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
            with open("dados/ajuste_estoque.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(colunas)
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/ajuste_estoque.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    tk.Button(botoes_frame, text="🔄 Recarregar", bg="#3cb371", fg="white",
              font=("Helvetica", 12, "bold"), command=carregar_estoque).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar CSV", bg="#2e8b57", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    carregar_estoque()
