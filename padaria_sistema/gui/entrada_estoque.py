import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

def tela_entrada_estoque(janela):
    # Limpar a tela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Frame principal
    frame = tk.Frame(janela, bg="#f0f5f5")
    frame.pack(fill="both", expand=True)

    # Título
    tk.Label(frame, text="📦 Entrada de Estoque", font=("Helvetica", 18, "bold"),
             bg="#f0f5f5", fg="#003366").pack(pady=10)

    # Frame dos campos
    campos_frame = tk.Frame(frame, bg="#f0f5f5")
    campos_frame.pack(pady=10)

    campos = {
        "Produto": tk.Entry(campos_frame, width=30),
        "Código do Produto": tk.Entry(campos_frame, width=30),
        "Quantidade Entrada": tk.Entry(campos_frame, width=30),
        "Data de Entrada": tk.Entry(campos_frame, width=30),
        "Fornecedor": tk.Entry(campos_frame, width=30),
        "Lote": tk.Entry(campos_frame, width=30),
        "Validade": tk.Entry(campos_frame, width=30),
        "Responsável": tk.Entry(campos_frame, width=30)
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12),
                 bg="#f0f5f5").grid(row=i, column=0, sticky="e", padx=5, pady=5)
        entrada.grid(row=i, column=1, sticky="w", padx=5, pady=5)

    # Salvar Entrada
    def salvar_entrada():
        dados = [entrada.get() for entrada in campos.values()]
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/entrada_estoque.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Entrada registrada com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            carregar_entradas()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    # Exportar CSV
    def exportar_csv():
        try:
            with open("dados/entrada_estoque.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/entrada_estoque.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/entrada_estoque.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Botões
    botoes_frame = tk.Frame(frame, bg="#f0f5f5")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar Entrada 💾", bg="#007399", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_entrada).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Exportar CSV 📁", bg="#00334d", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    # Tabela com Scroll
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(pady=10)

    colunas = tuple(campos.keys())
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0)
    scroll.grid(row=0, column=1, sticky="ns")

    # Carregar dados
    def carregar_entradas():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/entrada_estoque.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    carregar_entradas()
