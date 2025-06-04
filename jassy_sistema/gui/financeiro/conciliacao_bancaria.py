import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

def tela_conciliacao_bancaria(janela):
    # Limpa a janela atual
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
          widget.destroy()

    # Criação do frame principal da tela
    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    # Título da tela
    tk.Label(frame, text="🏦 Conciliação Bancária", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    # Frame para os campos de entrada de dados
    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    # Definir os campos de entrada (data, valor, descrição, tipo de transação, status de conciliação)
    campos = {
        "Data": tk.Entry(campos_frame, width=30),
        "Valor": tk.Entry(campos_frame, width=30),
        "Descrição": tk.Entry(campos_frame, width=30),
        "Tipo de Transação": ttk.Combobox(campos_frame, values=["Depósito", "Retirada", "Transferência"], width=28),
        "Status de Conciliação": ttk.Combobox(campos_frame, values=["Conciliada", "Não Conciliada"], width=28)
    }

    # Exibir os campos e rótulos
    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    # Função para salvar transação
    def salvar_transacao():
        dados = [entrada.get().strip() for entrada in campos.values()]
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/conciliacao_bancaria.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Transação salva com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            carregar_transacoes()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    # Função para exportar os dados para um arquivo CSV
    def exportar_csv():
        try:
            with open("dados/conciliacao_bancaria.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/conciliacao_bancaria.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/conciliacao_bancaria.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Botões para salvar e exportar
    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="💾 Salvar Transação", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=salvar_transacao).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar dados", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_csv).pack(side="left", padx=10)

    # --- Tabela de Transações ---
    tabela_frame = tk.LabelFrame(frame, text="📋 Transações Bancárias", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = ("Data", "Valor", "Descrição", "Tipo de Transação", "Status de Conciliação", "Ações")

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

    # Função para carregar as transações na tabela
    def carregar_transacoes():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/conciliacao_bancaria.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas) - 1:
                        tabela.insert("", "end", values=valores + ("Conciliar",))
        except FileNotFoundError:
            pass

    # Função para conciliar a transação
    def conciliar_transacao(event):
        item = tabela.selection()[0]
        status_atual = tabela.item(item, "values")[4]
        novo_status = "Conciliada" if status_atual != "Conciliada" else "Não Conciliada"
        tabela.item(item, values=tabela.item(item, "values")[:4] + (novo_status,) + tabela.item(item, "values")[5:])
        messagebox.showinfo("Status Atualizado", f"Status alterado para {novo_status}.")
        # Atualizar a informação no arquivo
        with open("dados/conciliacao_bancaria.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
        with open("dados/conciliacao_bancaria.txt", "w", encoding="utf-8") as f:
            for i, linha in enumerate(linhas):
                if linha.strip().split("|")[0] == tabela.item(item, "values")[0]:
                    linha_atualizada = linha.replace(linha.strip().split("|")[4], novo_status)
                    f.write(linha_atualizada + "\n")
                else:
                    f.write(linha)
        carregar_transacoes()

    # Vincula a função de conciliar transação
    tabela.bind("<Double-1>", conciliar_transacao)

    carregar_transacoes()
