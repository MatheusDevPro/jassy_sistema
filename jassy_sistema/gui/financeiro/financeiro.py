import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def tela_financeiro(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📊 Gestão Financeira", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.LabelFrame(frame, text="Lançamento Financeiro", bg="#e6f2ff", fg="#003d66",
                                 font=("Helvetica", 12, "bold"), padx=10, pady=10)
    campos_frame.pack(pady=10, padx=20, fill="x")

    # Campos de entrada
    campos = {
        "Data": tk.Entry(campos_frame),
        "Tipo": ttk.Combobox(campos_frame, values=["Receita", "Despesa"], state="readonly"),
        "Categoria": ttk.Combobox(campos_frame, values=["Venda", "Salário", "Aluguel", "Imposto", "Conta", "Outros"], state="readonly"),
        "Descrição": tk.Entry(campos_frame, width=50),
        "Valor": tk.Entry(campos_frame),
        "Forma de Pagamento": ttk.Combobox(campos_frame, values=["Dinheiro", "Cartão", "PIX", "Boleto"], state="readonly")
    }

    # Posição dos campos
    for i, (rotulo, widget) in enumerate(campos.items()):
        tk.Label(campos_frame, text=rotulo + ":", bg="#e6f2ff", font=("Helvetica", 11)).grid(row=i // 2, column=(i % 2) * 2, padx=5, pady=6, sticky="e")
        widget.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=5, pady=6, sticky="w")

    # Tabela de registros
    tabela_frame = tk.Frame(frame, bg="#e6f2ff")
    tabela_frame.pack(pady=10, padx=20, fill="both", expand=True)

    colunas = ["data", "tipo", "categoria", "descricao", "valor", "forma"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=8)
    for col in colunas:
        tabela.heading(col, text=col.capitalize())
        tabela.column(col, width=100)
    tabela.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Função para adicionar entrada
    def adicionar_registro():
        try:
            data = campos["Data"].get() or datetime.now().strftime("%d/%m/%Y")
            tipo = campos["Tipo"].get()
            categoria = campos["Categoria"].get()
            descricao = campos["Descrição"].get()
            valor = float(campos["Valor"].get())
            forma = campos["Forma de Pagamento"].get()

            if not all([tipo, categoria, descricao, forma]):
                raise ValueError("Campos obrigatórios vazios")

            tabela.insert("", "end", values=(data, tipo, categoria, descricao, f"R$ {valor:.2f}", forma))
            atualizar_saldo()
            limpar_campos()
        except ValueError:
            messagebox.showwarning("Erro", "Preencha todos os campos corretamente e insira valor numérico.")

    def limpar_campos():
        for campo in campos.values():
            if isinstance(campo, ttk.Combobox):
                campo.set("")
            else:
                campo.delete(0, tk.END)

    def excluir_registro():
        for item in tabela.selection():
            tabela.delete(item)
        atualizar_saldo()

    def atualizar_saldo():
        saldo = 0
        for row in tabela.get_children():
            tipo = tabela.item(row)['values'][1]
            valor_str = tabela.item(row)['values'][4].replace("R$ ", "").replace(",", ".")
            valor = float(valor_str)
            saldo += valor if tipo == "Receita" else -valor
        saldo_label.config(text=f"💰 Saldo Atual: R$ {saldo:.2f}")

    # Botões de ação
    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=5)

    tk.Button(botoes_frame, text="➕ Adicionar", command=adicionar_registro,
              bg="#339966", fg="white", font=("Helvetica", 11, "bold"), width=15).pack(side="left", padx=5)

    tk.Button(botoes_frame, text="🗑️ Excluir", command=excluir_registro,
              bg="#cc0000", fg="white", font=("Helvetica", 11, "bold"), width=15).pack(side="left", padx=5)

    tk.Button(botoes_frame, text="🧹 Limpar Campos", command=limpar_campos,
              bg="#999999", fg="white", font=("Helvetica", 11), width=15).pack(side="left", padx=5)

    # Saldo
    saldo_label = tk.Label(frame, text="💰 Saldo Atual: R$ 0.00", bg="#e6f2ff",
                           fg="#006600", font=("Helvetica", 13, "bold"))
    saldo_label.pack(pady=10)
