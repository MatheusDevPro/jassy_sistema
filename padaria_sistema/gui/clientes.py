import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import csv

def tela_clientes(janela):
    # Limpar tela anterior
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Frame principal
    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    # Título
    tk.Label(frame, text="Cadastro de Clientes 👤", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    # Sub-frame dos campos
    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    campos = {
        "Nome": tk.Entry(campos_frame, width=30),
        "CPF": tk.Entry(campos_frame, width=30),
        "Data de Nascimento": tk.Entry(campos_frame, width=30),
        "Sexo": tk.Entry(campos_frame, width=30),
        "RG": tk.Entry(campos_frame, width=30),
        "Data de Cadastro": tk.Entry(campos_frame, width=30),
        "Cidade": tk.Entry(campos_frame, width=30),
        "Estado": tk.Entry(campos_frame, width=30),
        "CEP": tk.Entry(campos_frame, width=30),
        "Bairro": tk.Entry(campos_frame, width=30),
        "Número": tk.Entry(campos_frame, width=30),
        "Complemento": tk.Entry(campos_frame, width=30),
        "Data de Validade": tk.Entry(campos_frame, width=30),
        "E-mail": tk.Entry(campos_frame, width=30),
        "Telefone": tk.Entry(campos_frame, width=30),
        "Endereço": tk.Entry(campos_frame, width=30)
    }

    # Posicionamento dos campos (2 colunas)
    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    # Função para salvar cliente
    def salvar_cliente():
        dados = [entrada.get().strip() for entrada in campos.values()]
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/clientes.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Cliente salvo com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            carregar_clientes()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    # Função para exportar para CSV
    def exportar_csv():
        try:
            with open("dados/clientes.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/clientes.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/clientes.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Botões
    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="💾 Salvar Cliente", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=salvar_cliente).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar dados", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_csv).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="🔄 Atualizar Lista", bg="#ffcc00", fg="black",
              font=("Helvetica", 12, "bold"), width=20, command=lambda: carregar_clientes()).pack(side="left", padx=10)

    # --- TABELA DE EXIBIÇÃO ---
    tabela_frame = tk.LabelFrame(frame, text="📋 Clientes Cadastrados", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = list(campos.keys())
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=12)

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=130, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    scroll.grid(row=0, column=1, sticky="ns", pady=8)

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    # Função para carregar os dados
    def carregar_clientes():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/clientes.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    carregar_clientes()
