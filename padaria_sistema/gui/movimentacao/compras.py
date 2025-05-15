import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from tkcalendar import DateEntry

def tela_compras(janela):
    # Limpar tela anterior
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Frame principal
    frame = tk.Frame(janela, bg="#fffaf0")
    frame.pack(fill="both", expand=True)

    # Título
    tk.Label(frame, text="Registro de Compras 🛒", font=("Helvetica", 18, "bold"),
             bg="#fffaf0", fg="#663300").pack(pady=10)

    # Frame dos campos
    campos_frame = tk.Frame(frame, bg="#fffaf0")
    campos_frame.pack(pady=10)

    Forma_de_Pagamento = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Transferência", "Boleto", "Cheque", "Pix"]

    campos = {
        "Fornecedor": tk.Entry(campos_frame, width=30),
        "Produto": tk.Entry(campos_frame, width=30),
        "Quantidade": tk.Entry(campos_frame, width=30),
        "Valor Unitário": tk.Entry(campos_frame, width=30),
        "Valor Total": tk.Entry(campos_frame, width=30),
        "Data da Compra": DateEntry(campos_frame, width=30, date_pattern='dd/mm/yyyy'),
        "Forma de Pagamento": ttk.Combobox(campos_frame, width=30, values=Forma_de_Pagamento, state="readonly"),
        "Número da Nota Fiscal": tk.Entry(campos_frame, width=30)
    }


    # Distribuir os campos em 2 colunas (4 campos por coluna)
    campos_por_coluna = 4
    for i, (rotulo, entrada) in enumerate(campos.items()):
        coluna = (i // campos_por_coluna) * 2  # coluna 0 e 2
        linha = i % campos_por_coluna

        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#fffaf0")\
            .grid(row=linha, column=coluna, sticky="e", padx=5, pady=5)
        entrada.grid(row=linha, column=coluna + 1, sticky="w", padx=5, pady=5)


    def salvar_compra():
        dados = [entrada.get() for entrada in campos.values()]
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/compras.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Compra registrada com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            carregar_compras()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def exportar_compras_csv():
        try:
            with open("dados/compras.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/compras.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/compras.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Botões
    botoes_frame = tk.Frame(frame, bg="#fffaf0")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar Compra 💾", bg="#996633", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_compra).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Exportar CSV 📁", bg="#333366", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_compras_csv).pack(side="left", padx=10)

    # Tabela com Scroll
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

    def carregar_compras():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/compras.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    carregar_compras()
