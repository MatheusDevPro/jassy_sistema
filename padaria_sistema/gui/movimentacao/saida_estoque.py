import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import os
import csv

def tela_saida_estoque(janela):
    # Limpar tela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("Controle de Estoque - Saída de Produtos")

    # Estilo base
    bg_color = "#f5f7fa"
    destaque = "#003366"
    fonte_padrao = ("Segoe UI", 10)
    fonte_titulo = ("Segoe UI", 16, "bold")

    # Frame principal
    frame = tk.Frame(janela, bg=bg_color)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🚚 Saída de Estoque", bg=bg_color, fg=destaque, font=fonte_titulo).pack(pady=10)

    # Frame geral dos campos
    campos_frame = tk.Frame(frame, bg=bg_color)
    campos_frame.pack(padx=10, pady=5, fill="x")

    # =================== IDENTIFICAÇÃO ===================
    identificacao = tk.LabelFrame(campos_frame, text="Identificação da Saída", bg=bg_color, font=fonte_padrao, fg=destaque)
    identificacao.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    campo_data = DateEntry(identificacao, width=18, background="gray", foreground="white", date_pattern="dd/mm/yyyy")
    campo_numero_nf = tk.Entry(identificacao, width=20)
    campo_lote = tk.Entry(identificacao, width=20)

    tk.Label(identificacao, text="Data:", bg=bg_color, font=fonte_padrao).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    campo_data.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(identificacao, text="Nota Fiscal:", bg=bg_color, font=fonte_padrao).grid(row=0, column=2, padx=5, pady=5, sticky="e")
    campo_numero_nf.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(identificacao, text="Lote:", bg=bg_color, font=fonte_padrao).grid(row=0, column=4, padx=5, pady=5, sticky="e")
    campo_lote.grid(row=0, column=5, padx=5, pady=5)

    # =================== PRODUTO ===================
    produto = tk.LabelFrame(campos_frame, text="Informações do Produto", bg=bg_color, font=fonte_padrao, fg=destaque)
    produto.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    campo_cod_produto = tk.Entry(produto, width=20)
    campo_nome_produto = tk.Entry(produto, width=40)
    campo_qtd = tk.Entry(produto, width=10)
    campo_unidade = ttk.Combobox(produto, values=["UN", "KG", "LT", "CX"], width=8, state="readonly")

    tk.Label(produto, text="Código:", bg=bg_color, font=fonte_padrao).grid(row=0, column=0, padx=5, pady=5)
    campo_cod_produto.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(produto, text="Nome do Produto:", bg=bg_color, font=fonte_padrao).grid(row=0, column=2, padx=5, pady=5)
    campo_nome_produto.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(produto, text="Quantidade:", bg=bg_color, font=fonte_padrao).grid(row=0, column=4, padx=5, pady=5)
    campo_qtd.grid(row=0, column=5, padx=5, pady=5)

    tk.Label(produto, text="Unidade:", bg=bg_color, font=fonte_padrao).grid(row=0, column=6, padx=5, pady=5)
    campo_unidade.grid(row=0, column=7, padx=5, pady=5)

    # =================== DESTINO ===================
    destino = tk.LabelFrame(campos_frame, text="Destino / Logística", bg=bg_color, font=fonte_padrao, fg=destaque)
    destino.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    campo_destino = tk.Entry(destino, width=40)
    campo_local_estoque = tk.Entry(destino, width=25)

    tk.Label(destino, text="Destino:", bg=bg_color, font=fonte_padrao).grid(row=0, column=0, padx=5, pady=5)
    campo_destino.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(destino, text="Local de Estoque:", bg=bg_color, font=fonte_padrao).grid(row=0, column=2, padx=5, pady=5)
    campo_local_estoque.grid(row=0, column=3, padx=5, pady=5)

    # =================== RESPONSÁVEL ===================
    responsavel = tk.LabelFrame(campos_frame, text="Responsável e Justificativa", bg=bg_color, font=fonte_padrao, fg=destaque)
    responsavel.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    campo_responsavel = tk.Entry(responsavel, width=30)
    campo_motivo = ttk.Combobox(responsavel, values=["Venda", "Amostra", "Descarte", "Troca", "Doação", "Quebra", "Outros"], width=30, state="readonly")

    tk.Label(responsavel, text="Responsável:", bg=bg_color, font=fonte_padrao).grid(row=0, column=0, padx=5, pady=5)
    campo_responsavel.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(responsavel, text="Motivo:", bg=bg_color, font=fonte_padrao).grid(row=0, column=2, padx=5, pady=5)
    campo_motivo.grid(row=0, column=3, padx=5, pady=5)

    # =================== OBSERVAÇÃO ===================
    campo_observacoes = tk.Entry(frame, width=110)
    tk.Label(frame, text="Observações:", bg=bg_color, font=fonte_padrao).pack(pady=(10, 2))
    campo_observacoes.pack(pady=2)

    # =================== BOTÕES ===================
    def salvar_saida():
        dados = [
            campo_data.get(), campo_numero_nf.get(), campo_lote.get(),
            campo_cod_produto.get(), campo_nome_produto.get(), campo_qtd.get(), campo_unidade.get(),
            campo_destino.get(), campo_local_estoque.get(),
            campo_responsavel.get(), campo_motivo.get(), campo_observacoes.get()
        ]
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/saida_estoque.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Saída registrada.")
            carregar_saidas()
        else:
            messagebox.showwarning("Erro", "Todos os campos devem ser preenchidos.")

    def exportar_csv():
        try:
            with open("dados/saida_estoque.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split(" | ") for linha in f if linha.strip()]
            with open("dados/saida_estoque.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow([
                    "Data", "Nota Fiscal", "Lote", "Código", "Produto", "Qtd", "Unidade",
                    "Destino", "Local", "Responsável", "Motivo", "Obs"
                ])
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Exportado para CSV com sucesso.")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo não encontrado.")

    botoes = tk.Frame(frame, bg=bg_color)
    botoes.pack(pady=10)

    tk.Button(botoes, text="💾 Salvar Saída", font=fonte_padrao, bg=destaque, fg="white", width=18, command=salvar_saida).pack(side="left", padx=10)
    tk.Button(botoes, text="📁 Exportar CSV", font=fonte_padrao, bg="#006699", fg="white", width=18, command=exportar_csv).pack(side="left", padx=10)

    # =================== TABELA ===================
    tabela_frame = tk.Frame(frame, bg=bg_color)
    tabela_frame.pack(pady=10, padx=10, fill="both", expand=True)

    colunas = ["Data", "Nota Fiscal", "Lote", "Código", "Produto", "Qtd", "Un", "Destino", "Local", "Responsável", "Motivo", "Obs"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=12)

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=100, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll.grid(row=0, column=1, sticky="ns")

    tabela_frame.rowconfigure(0, weight=1)
    tabela_frame.columnconfigure(0, weight=1)

    def carregar_saidas():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/saida_estoque.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    dados = [d.strip() for d in linha.split("|")]
                    if len(dados) == len(colunas):
                        tabela.insert("", "end", values=dados)
        except FileNotFoundError:
            pass

    carregar_saidas()
