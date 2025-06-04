import tkinter as tk
from tkinter import ttk, messagebox

def calcular_liquido(salario_base, adicionais, descontos):
    try:
        return float(salario_base) + float(adicionais) - float(descontos)
    except ValueError:
        return 0.0

def tela_folha_pagamento(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
          widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🧾 Folha de Pagamento", font=("Arial", 20, "bold"), bg="#f8f8ff", fg="#333").pack(pady=20)

    # 🔍 Área de pesquisa
    pesquisa_frame = tk.Frame(frame, bg="#f8f8ff")
    pesquisa_frame.pack(pady=5, fill="x", padx=30)

    tk.Label(pesquisa_frame, text="Buscar por Nome/Matrícula:", font=("Arial", 12), bg="#f8f8ff").pack(side="left", padx=(0,10))
    entry_pesquisa = tk.Entry(pesquisa_frame, font=("Arial", 12), width=40)
    entry_pesquisa.pack(side="left")
    tk.Button(pesquisa_frame, text="Pesquisar", font=("Arial", 11), bg="#3f51b5", fg="white").pack(side="left", padx=10)

    # 📋 Formulário de preenchimento
    form_frame = tk.Frame(frame, bg="#f8f8ff")
    form_frame.pack(padx=30, pady=10, fill="x")

    campos = [
        ("Matrícula", 0), ("Nome", 1), ("Cargo", 2), ("Competência (MM/AAAA)", 3),
        ("Salário Base", 4), ("Adicionais", 5), ("Descontos", 6),
        ("Forma de Pagamento", 7), ("Data de Pagamento", 8)
    ]
    entradas = {}

    for texto, linha in campos:
        tk.Label(form_frame, text=texto + ":", font=("Arial", 11), bg="#f8f8ff").grid(row=linha, column=0, sticky="w", pady=2)
        entrada = tk.Entry(form_frame, font=("Arial", 11), width=35)
        entrada.grid(row=linha, column=1, pady=2, padx=10, sticky="w")
        entradas[texto] = entrada

    # Botão para calcular salário líquido
    def exibir_salario_liquido():
        base = entradas["Salário Base"].get()
        adicionais = entradas["Adicionais"].get()
        descontos = entradas["Descontos"].get()
        liquido = calcular_liquido(base, adicionais, descontos)
        lbl_liquido.config(text=f"💰 Salário Líquido: R$ {liquido:.2f}")

    lbl_liquido = tk.Label(form_frame, text="💰 Salário Líquido: R$ 0.00", font=("Arial", 11, "bold"), bg="#f8f8ff", fg="green")
    lbl_liquido.grid(row=4, column=2, padx=30, sticky="w", columnspan=2)

    tk.Button(form_frame, text="Calcular Líquido", command=exibir_salario_liquido,
              bg="#009688", fg="white", font=("Arial", 10)).grid(row=5, column=2, sticky="w", padx=30)

    # 🧾 Tabela de registros
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(padx=30, pady=10, fill="both", expand=True)

    colunas = ["Matrícula", "Nome", "Cargo", "Competência", "Base", "Adicionais", "Descontos", "Líquido", "Forma", "Data"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, anchor="center", width=130)

    scroll_y = tk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = tk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    # 📝 Observações
    obs_frame = tk.Frame(frame, bg="#f8f8ff")
    obs_frame.pack(fill="x", padx=30, pady=10)

    tk.Label(obs_frame, text="Observações:", font=("Arial", 12), bg="#f8f8ff").pack(anchor="w")
    txt_obs = tk.Text(obs_frame, height=4, font=("Arial", 11))
    txt_obs.pack(fill="x")

    # 📊 Rodapé com totalizador
    rodape_frame = tk.Frame(frame, bg="#f8f8ff")
    rodape_frame.pack(pady=5, fill="x", padx=30)

    lbl_total_folha = tk.Label(rodape_frame, text="Total da Folha: R$ 0.00", font=("Arial", 11, "bold"), fg="blue", bg="#f8f8ff")
    lbl_total_folha.pack(anchor="e")

    # 🧰 Botões de ação
    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=20)

    tk.Button(botoes_frame, text="Adicionar", font=("Arial", 11), bg="#4caf50", fg="white", width=18).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Editar", font=("Arial", 11), bg="#2196f3", fg="white", width=15).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Excluir", font=("Arial", 11), bg="#f44336", fg="white", width=15).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Gerar PDF", font=("Arial", 11), bg="#9c27b0", fg="white", width=15).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Atualizar Total", font=("Arial", 11), bg="#795548", fg="white", width=15).pack(side="left", padx=10)

