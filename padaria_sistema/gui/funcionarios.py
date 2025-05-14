import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import csv
import os
import re

def tela_funcionarios(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Funcionários 👨‍🍳", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    entradas = {}

    def validar_entrada():
        cpf = entradas["CPF"].get()
        telefone = entradas["Telefone"].get()
        email = entradas["Email"].get()
        salario = entradas["Salário"].get()

        # Validação CPF
        if not re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
            messagebox.showerror("Erro", "CPF inválido. Formato correto: 000.000.000-00")
            return False

        # Validação Telefone
        if not re.fullmatch(r"\(\d{2}\) \d{5}-\d{4}", telefone):
            messagebox.showerror("Erro", "Telefone inválido. Formato correto: (00) 00000-0000")
            return False

        # Validação Email
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Erro", "Email inválido.")
            return False

        # Validação Salário
        try:
            float(salario)
        except ValueError:
            messagebox.showerror("Erro", "Salário deve conter apenas números.")
            return False

        return True

    campos_info = {
        "Nome": tk.Entry(campos_frame, width=30),
        "CPF": tk.Entry(campos_frame, width=30),
        "Cargo": tk.Entry(campos_frame, width=30),
        "Salário": tk.Entry(campos_frame, width=30),
        "Data de Admissão": DateEntry(campos_frame, width=27, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy'),
        "Telefone": tk.Entry(campos_frame, width=30),
        "Email": tk.Entry(campos_frame, width=30),
        "Endereço": tk.Entry(campos_frame, width=30)
    }

    for i, (rotulo, entrada) in enumerate(campos_info.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")
        entradas[rotulo] = entrada

    def salvar_funcionario():
        dados = [entrada.get().strip() for entrada in entradas.values()]
        if all(dados):
            if not validar_entrada():
                return
            os.makedirs("dados", exist_ok=True)
            with open("dados/funcionarios.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Funcionário salvo com sucesso.")
            for entrada in entradas.values():
                entrada.delete(0, tk.END)
            entradas["Data de Admissão"].set_date("")
            carregar_funcionarios()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def exportar_csv():
        try:
            with open("dados/funcionarios.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/funcionarios.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(entradas.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/funcionarios.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="💾 Salvar Funcionário", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=salvar_funcionario).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar dados", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_csv).pack(side="left", padx=10)

    tabela_frame = tk.LabelFrame(frame, text="📋 Funcionários Cadastrados", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = tuple(entradas.keys())
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

    def carregar_funcionarios():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/funcionarios.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [valor.strip() for valor in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    carregar_funcionarios()
