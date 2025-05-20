import tkinter as tk
from tkinter import messagebox, ttk
import os
import csv
import re

def tela_fornecedores(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Fornecedores 🏢", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    formas_pagamento = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Transferência", "Boleto", "Cheque", "Pix"]
    prazos_entrega = ["1 dia", "2 dias", "3 dias", "4 dias", "5 dias", "6 dias", "7 dias"]
    estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
               "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

    campos = {
        "Nome da Empresa": tk.Entry(campos_frame, width=30),
        "CNPJ": tk.Entry(campos_frame, width=30),
        "Telefone": tk.Entry(campos_frame, width=30),
        "Email": tk.Entry(campos_frame, width=30),
        "Responsável": tk.Entry(campos_frame, width=30),
        "Produto Fornecido": tk.Entry(campos_frame, width=30),
        "Prazo de Entrega": ttk.Combobox(campos_frame, width=30, values=prazos_entrega, state="readonly"),
        "Forma de Pagamento": ttk.Combobox(campos_frame, width=30, values=formas_pagamento, state="readonly"),
        "Endereço": tk.Entry(campos_frame, width=30),
        "Cidade": tk.Entry(campos_frame, width=30),
        "Estado (UF)": ttk.Combobox(campos_frame, width=30, values=estados, state="readonly"),
        "CEP": tk.Entry(campos_frame, width=30),
        "Número de Registro": tk.Entry(campos_frame, width=30),
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12),
                 bg="#e6f2ff", fg="#003d66").grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    def salvar_fornecedor():
        dados = [entrada.get().strip() for entrada in campos.values()]
        if all(dados):
            # Validação de CNPJ
            cnpj = dados[1]
            if not re.fullmatch(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", cnpj):
                messagebox.showerror("Erro", "CNPJ inválido. Ex: 00.000.000/0000-00")
                return
            
            os.makedirs("dados", exist_ok=True)
            with open("dados/fornecedores.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Fornecedor salvo com sucesso.")
            for entrada in campos.values():
                if isinstance(entrada, ttk.Combobox):
                    entrada.set("")
                else:
                    entrada.delete(0, tk.END)
            carregar_fornecedores()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def exportar_csv():
        try:
            with open("dados/fornecedores.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/fornecedores.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/fornecedores.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    def carregar_fornecedores():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/fornecedores.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [valor.strip() for valor in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    def carregar_para_edicao(event):
        item = tabela.selection()
        if item:
            valores = tabela.item(item[0])["values"]
            for i, entrada in enumerate(campos.values()):
                if isinstance(entrada, ttk.Combobox):
                    entrada.set(valores[i])
                else:
                    entrada.delete(0, tk.END)
                    entrada.insert(0, valores[i])

            salvar_btn.pack_forget()
            atualizar_btn.pack(side="left", padx=10)

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    salvar_btn = tk.Button(botoes_frame, text="💾 Salvar Fornecedor", bg="#339966", fg="white",
                           font=("Helvetica", 12, "bold"), width=20, command=salvar_fornecedor)
    salvar_btn.pack(side="left", padx=10)

    atualizar_btn = tk.Button(botoes_frame, text="🔄 Atualizar Fornecedor", bg="#ff9933", fg="white",
                              font=("Helvetica", 12, "bold"), width=20)

    tk.Button(botoes_frame, text="📁 Exportar dados", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_csv).pack(side="left", padx=10)

    tabela_frame = tk.LabelFrame(frame, text="📋 Fornecedores Cadastrados", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = tuple(campos.keys())
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=150, anchor="center")

    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)

    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    tabela.bind("<Double-1>", carregar_para_edicao)

    carregar_fornecedores()
