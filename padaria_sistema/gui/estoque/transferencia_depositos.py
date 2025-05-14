import tkinter as tk
from tkinter import ttk, messagebox
import os
import csv

def tela_transferencia_depositos(janela):
    # Limpar tela anterior
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🔄 Transferência entre Depósitos", font=("Helvetica", 18, "bold"),
             bg="#f8f8ff", fg="#004d66").pack(pady=10)

    # Área de seleção de depósito
    deposito_frame = tk.Frame(frame, bg="#f8f8ff")
    deposito_frame.pack(pady=5)

    tk.Label(deposito_frame, text="Depósito de Origem:", font=("Helvetica", 12), bg="#f8f8ff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tk.Label(deposito_frame, text="Depósito de Destino:", font=("Helvetica", 12), bg="#f8f8ff").grid(row=0, column=2, padx=5, pady=5, sticky="e")

    deposito_origem = ttk.Combobox(deposito_frame, values=["Central", "Filial 1", "Filial 2"], width=20)
    deposito_destino = ttk.Combobox(deposito_frame, values=["Central", "Filial 1", "Filial 2"], width=20)
    deposito_origem.grid(row=0, column=1, padx=5, pady=5)
    deposito_destino.grid(row=0, column=3, padx=5, pady=5)

    # Dados do produto
    produto_frame = tk.Frame(frame, bg="#f8f8ff")
    produto_frame.pack(pady=5)

    campos = {
        "Código do Produto": tk.Entry(produto_frame, width=25),
        "Nome do Produto": tk.Entry(produto_frame, width=25),
        "Quantidade a Transferir": tk.Entry(produto_frame, width=15)
    }

    for i, (label, entry) in enumerate(campos.items()):
        tk.Label(produto_frame, text=label + ":", font=("Helvetica", 12), bg="#f8f8ff") \
            .grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry.grid(row=i, column=1, padx=5, pady=5)

    # Tabela de transferências realizadas
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(pady=10)

    colunas = ["Origem", "Destino", "Código", "Produto", "Quantidade"]

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=8)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=300, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0)
    scroll.grid(row=0, column=1, sticky="ns")

    # Funções
    def salvar_transferencia():
        origem = deposito_origem.get().strip()
        destino = deposito_destino.get().strip()
        codigo = campos["Código do Produto"].get().strip()
        nome = campos["Nome do Produto"].get().strip()
        qtd = campos["Quantidade a Transferir"].get().strip()

        if not all([origem, destino, codigo, nome, qtd]):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        if origem == destino:
            messagebox.showwarning("Erro", "Depósito de origem e destino não podem ser iguais.")
            return

        if not qtd.isdigit() or int(qtd) <= 0:
            messagebox.showwarning("Erro", "Quantidade inválida.")
            return

        dados = [origem, destino, codigo, nome, qtd]

        os.makedirs("dados", exist_ok=True)
        with open("dados/transferencias.txt", "a", encoding="utf-8") as arq:
            arq.write(" | ".join(dados) + "\n")

        tabela.insert("", "end", values=dados)

        for campo in campos.values():
            campo.delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Transferência registrada com sucesso.")

    def exportar_csv():
        try:
            with open("dados/transferencias.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/transferencias.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(colunas)
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Transferências exportadas para 'dados/transferencias.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    def carregar_transferencias():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/transferencias.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    # Botões com cores e fontes consistentes
    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="💾 Registrar Transferência", bg="#004d66", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_transferencia).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar CSV", bg="#006699", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="🔄 Recarregar", bg="#00aaff", fg="white",
              font=("Helvetica", 12, "bold"), command=carregar_transferencias).pack(side="left", padx=10)

    carregar_transferencias()
