import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os

def tela_clientes(janela):
    # Limpar tela anterior
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Frame principal
    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    # Título
    titulo = tk.Label(frame, text="Cadastro de Clientes 👤", font=("Helvetica", 18, "bold"),
                      bg="#e6f2ff", fg="#006699")
    titulo.pack(pady=10)

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

    # Posicionamento em duas colunas
    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha, coluna = divmod(i, 2)
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff") \
            .grid(row=linha, column=coluna * 2, padx=5, pady=5, sticky="e")
        entrada.grid(row=linha, column=coluna * 2 + 1, padx=5, pady=5, sticky="w")

    # Função para salvar cliente
    def salvar_cliente():
        dados = [entrada.get() for entrada in campos.values()]
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

    tk.Button(frame, text="Salvar Cliente 💾", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_cliente).pack(pady=15)

    # --- TABELA DE EXIBIÇÃO ---
    tabela_frame = tk.Frame(frame, bg="#e6f2ff")
    tabela_frame.pack(pady=10)

    colunas = list(campos.keys())
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0)
    scroll.grid(row=0, column=1, sticky="ns")

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
