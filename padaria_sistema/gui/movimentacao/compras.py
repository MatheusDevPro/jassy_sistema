import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import os, csv

def tela_compras(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#fffaf0")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Registro de Compras 🛒", font=("Helvetica", 18, "bold"), bg="#fffaf0", fg="#663300").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#fffaf0")
    campos_frame.pack(pady=10, padx=10)

    categorias = ["Alimentos", "Bebidas", "Limpeza", "Eletrônicos", "Roupas", "Outros"]
    unidades = ["Un", "Kg", "g", "L", "ml", "Pacote", "Caixa"]
    formas_pagamento = ["Dinheiro", "Crédito", "Débito", "Pix", "Transferência", "Boleto", "Cheque"]
    status_compra = ["Pendente", "Pago", "Cancelado"]
    condicoes_pagamento = ["À Vista", "30 dias", "30/60", "30/60/90"]
    tipo_frete = ["CIF", "FOB"]

    campos = {
        # FORNECEDOR
        "Fornecedor": tk.Entry(campos_frame, width=30),
        "CNPJ do Fornecedor": tk.Entry(campos_frame, width=30),
        "Nome Fantasia": tk.Entry(campos_frame, width=30),
        "E-mail do Fornecedor": tk.Entry(campos_frame, width=30),
        "Telefone do Fornecedor": tk.Entry(campos_frame, width=30),

        # PRODUTO
        "Código do Produto": tk.Entry(campos_frame, width=30),
        "Nome do Produto": tk.Entry(campos_frame, width=30),
        "Categoria": ttk.Combobox(campos_frame, width=27, values=categorias, state="readonly"),
        "Unidade de Medida": ttk.Combobox(campos_frame, width=27, values=unidades, state="readonly"),
        "Quantidade": tk.Entry(campos_frame, width=30),
        "Valor Unitário": tk.Entry(campos_frame, width=30),
        "Valor Total": tk.Entry(campos_frame, width=30),

        # DOCUMENTO
        "Número da Nota Fiscal": tk.Entry(campos_frame, width=30),
        "Série da NF": tk.Entry(campos_frame, width=30),
        "Chave de Acesso": tk.Entry(campos_frame, width=30),

        # PAGAMENTO
        "Forma de Pagamento": ttk.Combobox(campos_frame, width=27, values=formas_pagamento, state="readonly"),
        "Condição de Pagamento": ttk.Combobox(campos_frame, width=27, values=condicoes_pagamento, state="readonly"),
        "Status da Compra": ttk.Combobox(campos_frame, width=27, values=status_compra, state="readonly"),
        "Data da Compra": DateEntry(campos_frame, width=30, date_pattern='dd/mm/yyyy'),
        "Data de Recebimento": DateEntry(campos_frame, width=30, date_pattern='dd/mm/yyyy'),
        "Data de Vencimento": DateEntry(campos_frame, width=30, date_pattern='dd/mm/yyyy'),

        # LOGÍSTICA
        "Transportadora": tk.Entry(campos_frame, width=30),
        "Tipo de Frete": ttk.Combobox(campos_frame, width=27, values=tipo_frete, state="readonly"),
        "Valor do Frete": tk.Entry(campos_frame, width=30),

        # OBS
        "Observações": tk.Text(campos_frame, width=62, height=4)
    }

    # Definir valores padrão
    campos["Categoria"].current(0)
    campos["Unidade de Medida"].current(0)
    campos["Forma de Pagamento"].current(0)
    campos["Condição de Pagamento"].current(0)
    campos["Status da Compra"].current(0)
    campos["Tipo de Frete"].current(0)

    # Distribuir os campos (em colunas)
    i = 0
    for rotulo, entrada in campos.items():
        if rotulo == "Observações":
            tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#fffaf0").grid(row=i, column=0, sticky="nw", padx=5, pady=5)
            entrada.grid(row=i, column=1, columnspan=3, sticky="w", padx=5, pady=5)
        else:
            linha, coluna = divmod(i, 2)
            linha *= 1
            tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#fffaf0").grid(row=linha, column=coluna*2, sticky="e", padx=5, pady=5)
            entrada.grid(row=linha, column=coluna*2 + 1, sticky="w", padx=5, pady=5)
            i += 1

    def salvar_compra():
        dados = []
        for rotulo, entrada in campos.items():
            if rotulo == "Observações":
                dados.append(entrada.get("1.0", "end").strip())
            else:
                dados.append(entrada.get().strip())
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/compras.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Compra registrada com sucesso.")
            for rotulo, entrada in campos.items():
                entrada.delete(0, tk.END) if rotulo != "Observações" else entrada.delete("1.0", "end")
            carregar_compras()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def exportar_csv():
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

    tk.Button(botoes_frame, text="Salvar Compra 💾", bg="#996633", fg="white", font=("Helvetica", 12, "bold"), command=salvar_compra).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Exportar CSV 📁", bg="#333366", fg="white", font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    # Tabela
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(pady=10, fill="both", expand=True)

    colunas = tuple(campos.keys())
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=140, anchor="center")

    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

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
