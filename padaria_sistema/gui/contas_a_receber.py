import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

def tela_contas_a_receber(janela):
    # Limpa a janela atual
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Criação do frame principal da tela
    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    # Título da tela
    tk.Label(frame, text="💵 Contas a Receber", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    # Frame para os campos de entrada de dados
    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    # Definir os campos de entrada (descrição, valor, vencimento, cliente, status, observações)
    campos = {
        "Descrição": tk.Entry(campos_frame, width=30),
        "Valor": tk.Entry(campos_frame, width=30),
        "Data de Vencimento": tk.Entry(campos_frame, width=30),
        "Cliente": tk.Entry(campos_frame, width=30),
        "Status": ttk.Combobox(campos_frame, values=["Pendente", "Pago", "Vencido"], width=28),
        "Observações": tk.Entry(campos_frame, width=30)
    }

    # Exibir os campos e rótulos
    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    # Função para salvar a conta
    def salvar_conta():
        dados = [entrada.get().strip() for entrada in campos.values()]
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/contas_a_receber.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Conta salva com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            carregar_contas()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    # Função para exportar os dados para um arquivo CSV
    def exportar_csv():
        try:
            with open("dados/contas_a_receber.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/contas_a_receber.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/contas_a_receber.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Botões para salvar e exportar
    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="💾 Salvar Conta", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=salvar_conta).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar dados", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_csv).pack(side="left", padx=10)

    # --- Tabela de Contas Cadastradas ---
    tabela_frame = tk.LabelFrame(frame, text="📋 Contas a Receber Cadastradas", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = ("Descrição", "Valor", "Data de Vencimento", "Cliente", "Status", "Observações", "Ações")

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=12)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=150, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    scroll.grid(row=0, column=1, sticky="ns", pady=8)

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    # Função para carregar as contas na tabela
    def carregar_contas():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/contas_a_receber.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas) - 1:
                        tabela.insert("", "end", values=valores + ("Atualizar",))
        except FileNotFoundError:
            pass

    # Função para atualizar o status da conta
    def atualizar_status(event):
        item = tabela.selection()[0]
        status_atual = tabela.item(item, "values")[4]
        novo_status = "Pago" if status_atual != "Pago" else "Pendente"
        tabela.item(item, values=tabela.item(item, "values")[:4] + (novo_status,) + tabela.item(item, "values")[5:])
        messagebox.showinfo("Status Atualizado", f"Status alterado para {novo_status}.")
        # Atualizar a informação no arquivo
        with open("dados/contas_a_receber.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
        with open("dados/contas_a_receber.txt", "w", encoding="utf-8") as f:
            for i, linha in enumerate(linhas):
                if linha.strip().split("|")[0] == tabela.item(item, "values")[0]:
                    linha_atualizada = linha.replace(linha.strip().split("|")[4], novo_status)
                    f.write(linha_atualizada + "\n")
                else:
                    f.write(linha)
        carregar_contas()

    # Vincula a função de atualizar status
    tabela.bind("<Double-1>", atualizar_status)

    carregar_contas()
