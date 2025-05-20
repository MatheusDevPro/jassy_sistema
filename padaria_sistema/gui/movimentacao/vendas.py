import tkinter as tk
from tkinter import messagebox, ttk
import os, csv
from tkcalendar import DateEntry
from datetime import datetime

def tela_vendas(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.configure(bg="#e6f2ff")
    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Registro de Vendas 💰", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10, padx=10)

    categorias = ["Eletrônicos", "Alimentos", "Vestuário", "Cosméticos", "Livros", "Outros"]
    status_venda = ["Pendente", "Pago", "Cancelado"]
    condicoes_pagamento = ["À vista", "2x", "3x", "4x ou mais"]
    formas_pagamento = ["Dinheiro", "Cartão", "Pix", "Boleto"]
    entrega_opcoes = ["Retirada no Local", "Entrega"]

    numero_pedido = datetime.now().strftime("%Y%m%d%H%M%S")

    campos = {
        "Nº Pedido": tk.Entry(campos_frame, width=25),
        "Data da Venda": DateEntry(campos_frame, width=22, date_pattern='dd/mm/yyyy'),
        "Cliente": tk.Entry(campos_frame, width=25),
        "CPF/CNPJ": tk.Entry(campos_frame, width=25),
        "Produto": tk.Entry(campos_frame, width=25),
        "Descrição": tk.Entry(campos_frame, width=25),
        "Categoria": ttk.Combobox(campos_frame, values=categorias, state="readonly", width=23),
        "Quantidade": tk.Entry(campos_frame, width=25),
        "Preço Unitário": tk.Entry(campos_frame, width=25),
        "Desconto (R$)": tk.Entry(campos_frame, width=25),
        "Acréscimo (R$)": tk.Entry(campos_frame, width=25),
        "Valor Total Líquido": tk.Entry(campos_frame, width=25, state="readonly"),
        "Vendedor": tk.Entry(campos_frame, width=25),
        "Forma de Pagamento": ttk.Combobox(campos_frame, values=formas_pagamento, state="readonly", width=23),
        "Condição de Pagamento": ttk.Combobox(campos_frame, values=condicoes_pagamento, state="readonly", width=23),
        "Entrega": ttk.Combobox(campos_frame, values=entrega_opcoes, state="readonly", width=23),
        "Status": ttk.Combobox(campos_frame, values=status_venda, state="readonly", width=23),
    }

    campos["Nº Pedido"].insert(0, numero_pedido)
    campos["Nº Pedido"].config(state="readonly")

    # Posicionamento
    linha, coluna = 0, 0
    for rotulo, entrada in campos.items():
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66")\
            .grid(row=linha, column=coluna*2, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna*2+1, padx=8, pady=6, sticky="w")
        coluna += 1
        if coluna > 1:
            coluna = 0
            linha += 1

    tk.Label(campos_frame, text="Observações:", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66")\
        .grid(row=linha, column=0, padx=8, pady=6, sticky="ne")
    obs = tk.Text(campos_frame, width=55, height=3)
    obs.grid(row=linha, column=1, columnspan=3, padx=8, pady=6, sticky="w")
    linha += 1

    def calcular_total(event=None):
        try:
            qnt = int(campos["Quantidade"].get())
            preco = float(campos["Preço Unitário"].get())
            desc = float(campos["Desconto (R$)"].get() or 0)
            acres = float(campos["Acréscimo (R$)"].get() or 0)
            total = qnt * preco - desc + acres
            campos["Valor Total Líquido"].config(state="normal")
            campos["Valor Total Líquido"].delete(0, tk.END)
            campos["Valor Total Líquido"].insert(0, f"{total:.2f}")
            campos["Valor Total Líquido"].config(state="readonly")
        except:
            campos["Valor Total Líquido"].config(state="normal")
            campos["Valor Total Líquido"].delete(0, tk.END)
            campos["Valor Total Líquido"].insert(0, "0.00")
            campos["Valor Total Líquido"].config(state="readonly")

    for campo in ["Quantidade", "Preço Unitário", "Desconto (R$)", "Acréscimo (R$)"]:
        campos[campo].bind("<KeyRelease>", calcular_total)

    def salvar():
        dados = []
        for key, campo in campos.items():
            if isinstance(campo, DateEntry):
                dados.append(campo.get_date().strftime("%d/%m/%Y"))
            else:
                dados.append(campo.get().strip())

        observacao = obs.get("1.0", tk.END).strip() or "-"
        dados.append(observacao)

        obrigatorios = [k for k in campos if "Valor Total" not in k and "Desconto" not in k and "Acréscimo" not in k]
        for i, k in enumerate(campos):
            if k in obrigatorios and not dados[i]:
                messagebox.showwarning("Aviso", f"Preencha o campo: {k}")
                return

        if dados[list(campos).index("Quantidade")] == "0" or dados[list(campos).index("Valor Total Líquido")] == "0.00":
            messagebox.showwarning("Erro", "Quantidade e Valor Total devem ser maiores que zero.")
            return

        os.makedirs("dados", exist_ok=True)
        with open("dados/vendas.txt", "a", encoding="utf-8") as arq:
            arq.write(" | ".join(dados) + "\n")
        messagebox.showinfo("Salvo", "Venda registrada com sucesso.")

        for campo in campos.values():
            if isinstance(campo, tk.Entry):
                campo.config(state="normal")
                campo.delete(0, tk.END)
            elif isinstance(campo, ttk.Combobox):
                campo.set("")
            elif isinstance(campo, DateEntry):
                campo.set_date(datetime.today())
        obs.delete("1.0", tk.END)
        campos["Nº Pedido"].insert(0, datetime.now().strftime("%Y%m%d%H%M%S"))
        campos["Nº Pedido"].config(state="readonly")
        campos["Valor Total Líquido"].config(state="readonly")

        carregar_vendas()

    def exportar_csv():
        try:
            with open("dados/vendas.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split(" | ") for linha in f if linha.strip()]
            with open("dados/vendas.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(list(campos.keys()) + ["Observações"])
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Exportado para dados/vendas.csv")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado para exportar.")

    botoes = tk.Frame(frame, bg="#e6f2ff")
    botoes.pack(pady=10)

    tk.Button(botoes, text="💾 Registrar Venda", command=salvar, bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20).pack(side="left", padx=10)
    tk.Button(botoes, text="📁 Exportar CSV", command=exportar_csv, bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20).pack(side="left", padx=10)

    tabela_frame = tk.LabelFrame(frame, text="📋 Vendas Registradas", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = list(campos.keys()) + ["Observações"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=12)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    scroll_y.grid(row=0, column=1, sticky="ns", pady=8)
    scroll_x.grid(row=1, column=0, sticky="ew", padx=8)

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    def carregar_vendas():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/vendas.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split(" | ")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    carregar_vendas()
