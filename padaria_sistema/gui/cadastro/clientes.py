import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import re
from tkcalendar import DateEntry
from datetime import datetime

def criar_banco():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, cpf TEXT, data_nascimento TEXT, sexo TEXT, rg TEXT, data_cadastro TEXT,
            cidade TEXT, estado TEXT, cep TEXT, bairro TEXT, numero TEXT,
            complemento TEXT, data_validade TEXT, email TEXT, telefone TEXT, endereco TEXT
        )
    ''')
    conn.commit()
    conn.close()

def tela_clientes(janela):
    criar_banco()

    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Clientes 👤", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    sexos = ["Masculino", "Feminino", "Binário", "Não-binário", "Lésbica", "Gay", "Bissexual", "Outro"]

    campos = {
        "Nome": tk.Entry(campos_frame, width=30),
        "CPF": tk.Entry(campos_frame, width=30),
        "Data de Nascimento": DateEntry(campos_frame, width=27, date_pattern='dd/mm/yyyy'),
        "Sexo": ttk.Combobox(campos_frame, values=sexos, width=28, state="readonly"),
        "RG": tk.Entry(campos_frame, width=30),
        "Data de Cadastro": DateEntry(campos_frame, width=27, date_pattern='dd/mm/yyyy'),
        "Cidade": tk.Entry(campos_frame, width=30),
        "Estado": tk.Entry(campos_frame, width=30),
        "CEP": tk.Entry(campos_frame, width=30),
        "Bairro": tk.Entry(campos_frame, width=30),
        "Número": tk.Entry(campos_frame, width=30),
        "Complemento": tk.Entry(campos_frame, width=30),
        "Data de Validade": DateEntry(campos_frame, width=27, date_pattern='dd/mm/yyyy'),
        "E-mail": tk.Entry(campos_frame, width=30),
        "Telefone": tk.Entry(campos_frame, width=30),
        "Endereço": tk.Entry(campos_frame, width=30)
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    def validar_dados(dados_dict):
        if not re.fullmatch(r"\d{11}", dados_dict["CPF"]):
            messagebox.showerror("Erro", "CPF deve conter 11 dígitos numéricos.")
            return False
        if not re.fullmatch(r"\d{8}", dados_dict["CEP"]):
            messagebox.showerror("Erro", "CEP deve conter 8 dígitos.")
            return False
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", dados_dict["E-mail"]):
            messagebox.showerror("Erro", "E-mail inválido.")
            return False
        if not re.fullmatch(r"\d{10,11}", dados_dict["Telefone"]):
            messagebox.showerror("Erro", "Telefone deve conter 10 ou 11 dígitos.")
            return False
        if not dados_dict["Número"].isdigit():
            messagebox.showerror("Erro", "Número deve ser numérico.")
            return False
        if dados_dict["Sexo"] not in sexos:
            messagebox.showerror("Erro", "Selecione um sexo válido.")
            return False
        if len(dados_dict["RG"]) < 5:
            messagebox.showerror("Erro", "RG deve conter ao menos 5 caracteres.")
            return False
        return True

    def salvar_cliente():
        dados_dict = {
            rotulo: entrada.get().strip() if not isinstance(entrada, DateEntry)
            else entrada.get_date().strftime("%d/%m/%Y")
            for rotulo, entrada in campos.items()
        }

        if all(dados_dict.values()):
            if not validar_dados(dados_dict):
                return

            conn = sqlite3.connect("clientes.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (
                    nome, cpf, data_nascimento, sexo, rg, data_cadastro,
                    cidade, estado, cep, bairro, numero, complemento,
                    data_validade, email, telefone, endereco
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(dados_dict.values()))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Cliente salvo com sucesso.")
            for entrada in campos.values():
                if isinstance(entrada, ttk.Combobox):
                    entrada.set("")
                elif isinstance(entrada, DateEntry):
                    entrada.set_date(datetime.today())
                else:
                    entrada.delete(0, tk.END)
            carregar_clientes()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="💾 Salvar Cliente", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=salvar_cliente).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="🔄 Atualizar Lista", bg="#ffcc00", fg="black",
              font=("Helvetica", 12, "bold"), width=20, command=lambda: carregar_clientes()).pack(side="left", padx=10)

    tabela_frame = tk.LabelFrame(frame, text="📋 Clientes Cadastrados", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = list(campos.keys())
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=130, anchor="center")

    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    def carregar_clientes():
        tabela.delete(*tabela.get_children())
        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nome, cpf, data_nascimento, sexo, rg, data_cadastro, cidade, estado, cep, bairro, numero, complemento, data_validade, email, telefone, endereco FROM clientes")
        for row in cursor.fetchall():
            tabela.insert("", "end", values=row)
        conn.close()

    carregar_clientes()
