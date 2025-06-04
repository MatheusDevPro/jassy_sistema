import tkinter as tk
from tkinter import ttk

def tela_relatorios_personalizados(janela):
    # Limpar tela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    # Cabeçalho
    tk.Label(frame, text="🧾 Relatórios Personalizados", font=("Helvetica", 18, "bold"), bg="#f8f8ff", fg="#993399").pack(pady=10)

    # Instruções
    tk.Label(frame, text="Selecione os filtros desejados para gerar um relatório personalizado.", bg="#f8f8ff", font=("Helvetica", 11)).pack(pady=5)

    # Filtros
    filtros_frame = tk.Frame(frame, bg="#f8f8ff")
    filtros_frame.pack(pady=10)

    tk.Label(filtros_frame, text="Data Início:", bg="#f8f8ff").grid(row=0, column=0, padx=5)
    tk.Entry(filtros_frame, width=15).grid(row=0, column=1, padx=5)

    tk.Label(filtros_frame, text="Data Fim:", bg="#f8f8ff").grid(row=0, column=2, padx=5)
    tk.Entry(filtros_frame, width=15).grid(row=0, column=3, padx=5)

    ttk.Button(filtros_frame, text="Gerar Relatório").grid(row=0, column=4, padx=10)

    # Tabela de Relatório
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(padx=10, pady=10, fill="both", expand=True)

    tabela = ttk.Treeview(tabela_frame, columns=("Coluna 1", "Coluna 2", "Coluna 3"), show="headings")
    for col in ("Coluna 1", "Coluna 2", "Coluna 3"):
        tabela.heading(col, text=col)
        tabela.column(col, anchor="center")

    tabela.pack(fill="both", expand=True)
