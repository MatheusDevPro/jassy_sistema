import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

def tela_funcionarios(janela):
    # Limpar tela anterior
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Frame principal
    frame = tk.Frame(janela, bg="#f0f5f5")
    frame.pack(fill="both", expand=True)

    # Título
    titulo = tk.Label(frame, text="Cadastro de Funcionários 👨‍🍳", font=("Helvetica", 18, "bold"),
                      bg="#f0f5f5", fg="#003d33")
    titulo.pack(pady=10)

    # Sub-frame dos campos
    campos_frame = tk.Frame(frame, bg="#f0f5f5")
    campos_frame.pack(pady=10)

    campos = {
        "Nome": tk.Entry(campos_frame, width=30),
        "CPF": tk.Entry(campos_frame, width=30),
        "Cargo": tk.Entry(campos_frame, width=30),
        "Salário": tk.Entry(campos_frame, width=30),
        "Data de Admissão": tk.Entry(campos_frame, width=30),
        "Telefone": tk.Entry(campos_frame, width=30),
        "Email": tk.Entry(campos_frame, width=30),
        "Endereço": tk.Entry(campos_frame, width=30)
    }

    linha = 0
    for i, (rotulo, entrada) in enumerate(campos.items()):
        coluna = i % 2
        linha = i // 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#f0f5f5") \
            .grid(row=linha, column=coluna*2, padx=5, pady=5, sticky="e")
        entrada.grid(row=linha, column=coluna*2 + 1, padx=5, pady=5, sticky="w")

    def salvar_funcionario():
        dados = [entrada.get() for entrada in campos.values()]
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/funcionarios.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Funcionário salvo com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            carregar_funcionarios()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def exportar_csv():
        try:
            with open("dados/funcionarios.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/funcionarios.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/funcionarios.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Frame dos botões
    botoes_frame = tk.Frame(frame, bg="#f0f5f5")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar Funcionário 💾", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_funcionario).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Exportar dados 📁", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    # --- Tabela com Scroll ---
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