import tkinter as tk
from tkinter import ttk

def tela_controle_ponto(janela):
    from datetime import datetime

    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
          widget.destroy()

    janela.grid_rowconfigure(0, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    frame = tk.Frame(janela, bg="#f0f4f8")
    frame.grid(row=0, column=0, sticky="nsew")
    frame.grid_rowconfigure(3, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    tk.Label(frame, text="📅 Controle de Ponto", font=("Arial", 20, "bold"), bg="#f0f4f8", fg="#222").pack(pady=15)

    # 🔍 Pesquisa
    pesquisa_frame = tk.Frame(frame, bg="#f0f4f8")
    pesquisa_frame.pack(pady=5, fill="x", padx=20)
    tk.Label(pesquisa_frame, text="Pesquisar Funcionário:", font=("Arial", 12), bg="#f0f4f8").pack(side="left")
    entry_pesquisa = tk.Entry(pesquisa_frame, font=("Arial", 12), width=30)
    entry_pesquisa.pack(side="left", padx=10)
    tk.Button(pesquisa_frame, text="🔍 Buscar", font=("Arial", 11), bg="#2196f3", fg="white").pack(side="left", padx=10)

    # 📋 Formulário de Registro
    form_frame = tk.Frame(frame, bg="#f0f4f8")
    form_frame.pack(padx=20, pady=10, fill="x")

    campos = [("Matrícula", 0), ("Nome", 1), ("Data (dd/mm/aaaa)", 2), ("Hora Entrada", 3),
              ("Hora Pausa", 4), ("Retorno Pausa", 5), ("Hora Saída", 6), ("Turno", 7)]
    entradas = {}

    for texto, linha in campos:
        tk.Label(form_frame, text=texto + ":", font=("Arial", 11), bg="#f0f4f8").grid(row=linha, column=0, sticky="w", pady=2)
        entrada = tk.Entry(form_frame, font=("Arial", 11))
        entrada.grid(row=linha, column=1, pady=2, padx=10, sticky="we")
        entradas[texto] = entrada

    form_frame.grid_columnconfigure(1, weight=1)

    # 🧾 Tabela de Ponto
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(padx=20, pady=10, fill="both", expand=True)

    colunas = ["Matrícula", "Nome", "Data", "Entrada", "Pausa", "Retorno", "Saída", "Total Horas", "Turno"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, anchor="center", width=120)

    scroll_y = tk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = tk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    # 📝 Observações
    obs_frame = tk.Frame(frame, bg="#f0f4f8")
    obs_frame.pack(fill="both", padx=20, pady=5)
    tk.Label(obs_frame, text="Observações:", font=("Arial", 12), bg="#f0f4f8").pack(anchor="w")
    txt_obs = tk.Text(obs_frame, height=4, font=("Arial", 11), wrap="word")
    txt_obs.pack(fill="both", expand=True)

    # 📊 Rodapé
    rodape = tk.Frame(frame, bg="#f0f4f8")
    rodape.pack(fill="x", padx=20, pady=5)
    lbl_total_funcionarios = tk.Label(rodape, text="Total de Registros: 0", font=("Arial", 11, "bold"), fg="blue", bg="#f0f4f8")
    lbl_total_funcionarios.pack(anchor="e")

    # 🧰 Botões
    botoes = tk.Frame(frame, bg="#f0f4f8")
    botoes.pack(pady=10)
    tk.Button(botoes, text="Registrar Ponto", font=("Arial", 11), bg="#4caf50", fg="white", width=16).pack(side="left", padx=10)
    tk.Button(botoes, text="Editar Registro", font=("Arial", 11), bg="#2196f3", fg="white", width=14).pack(side="left", padx=10)
    tk.Button(botoes, text="Excluir", font=("Arial", 11), bg="#f44336", fg="white", width=12).pack(side="left", padx=10)
    tk.Button(botoes, text="Gerar Relatório", font=("Arial", 11), bg="#9c27b0", fg="white", width=14).pack(side="left", padx=10)
    tk.Button(botoes, text="Atualizar Tabela", font=("Arial", 11), bg="#795548", fg="white", width=14).pack(side="left", padx=10)
