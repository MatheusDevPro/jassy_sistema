import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from tkcalendar import DateEntry

def tela_devolucoes(janela):
    # Limpar tela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Frame principal
    frame = tk.Frame(janela, bg="#f0fff0")
    frame.pack(fill="both", expand=True)

    # Título
    tk.Label(frame, text="↩️ Devoluções de Produtos", font=("Helvetica", 18, "bold"),
             bg="#f0fff0", fg="#006633").pack(pady=10)

    # Campos
    campos_frame = tk.Frame(frame, bg="#f0fff0")
    campos_frame.pack(pady=10)

    campos = {
        "Produto": tk.Entry(campos_frame, width=30),
        "Código do Produto": tk.Entry(campos_frame, width=30),
        "Quantidade Devolvida": tk.Entry(campos_frame, width=30),
        "Data da Devolução": DateEntry(campos_frame, width=30, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy'),
        "Motivo da Devolução": tk.Entry(campos_frame, width=30),
        "Cliente ou Destinatário": tk.Entry(campos_frame, width=30),
        "Responsável pelo Registro": tk.Entry(campos_frame, width=30)
    }

    # Para distribuir os campos em duas colunas (como na entrada de estoque)
    for i, (rotulo, entrada) in enumerate(campos.items()):
        row = i // 2  # Divide as linhas em dois
        col = i % 2   # Alterna entre as duas colunas (0 ou 1)

        # Criação do rótulo
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#f0fff0").grid(row=row, column=col * 2, sticky="e", padx=5, pady=5)
        
        # Criação do campo de entrada
        entrada.grid(row=row, column=col * 2 + 1, sticky="w", padx=5, pady=5)

    # Salvar devolução
    def salvar_devolucao():
        dados = [entrada.get() for entrada in campos.values()]
        if all(dados):
            # Verifica se o diretório existe e cria caso não exista
            os.makedirs("dados", exist_ok=True)
            with open("dados/devolucoes.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Devolução registrada com sucesso.")
            # Limpa os campos após salvar
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            carregar_devolucoes()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    # Exportar para CSV
    def exportar_csv():
        try:
            with open("dados/devolucoes.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/devolucoes.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/devolucoes.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Botões
    botoes_frame = tk.Frame(frame, bg="#f0fff0")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar Devolução 💾", bg="#2e8b57", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_devolucao).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Exportar CSV 📁", bg="#1e6633", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    # Tabela
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

    # Carregar dados
    def carregar_devolucoes():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/devolucoes.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    # Inicializar a exibição
    carregar_devolucoes()
