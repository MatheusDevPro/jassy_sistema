import tkinter as tk
from tkinter import ttk

def tela_relatorio_vendas(janela):
    # Limpar tela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    # Cabeçalho
    tk.Label(frame, text="📈 Relatório de Vendas", font=("Helvetica", 18, "bold"), bg="#f8f8ff", fg="#004d66").pack(pady=10)

    # Filtro de pesquisa
    filtro_frame = tk.Frame(frame, bg="#f8f8ff")
    filtro_frame.pack(pady=10)

    tk.Label(filtro_frame, text="Data Início:", bg="#f8f8ff").grid(row=0, column=0, padx=5)
    tk.Entry(filtro_frame, width=15).grid(row=0, column=1, padx=5)

    tk.Label(filtro_frame, text="Data Fim:", bg="#f8f8ff").grid(row=0, column=2, padx=5)
    tk.Entry(filtro_frame, width=15).grid(row=0, column=3, padx=5)

    ttk.Button(filtro_frame, text="Filtrar").grid(row=0, column=4, padx=10)

    # Tabela de Relatório
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(padx=10, pady=10, fill="both", expand=True)

    colunas = ("ID", "Data", "Cliente", "Valor", "Forma de Pagamento")
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, anchor="center")

    tabela.pack(fill="both", expand=True)
