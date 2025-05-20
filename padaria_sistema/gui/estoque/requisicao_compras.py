import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


def tela_requisicao_compras(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#eef9f1")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🛒 Requisição de Compras", font=("Helvetica", 20, "bold"), bg="#eef9f1", fg="#2e8b57").pack(pady=15)

    form_frame = tk.Frame(frame, bg="#eef9f1")
    form_frame.pack(pady=10, padx=10)

    # Campos adicionais e mais completos
    campos = {
        "Código Produto": tk.Entry(form_frame, width=20),
        "Nome Produto": tk.Entry(form_frame, width=30),
        "Unidade Medida": ttk.Combobox(form_frame, values=["Un", "Kg", "L", "Pacote", "Caixa"], width=18),
        "Quantidade": tk.Entry(form_frame, width=15),
        "Urgência": ttk.Combobox(form_frame, values=["Baixa", "Média", "Alta"], width=18),
        "Justificativa": tk.Entry(form_frame, width=40),
        "Data Prevista Entrega": tk.Entry(form_frame, width=20),
        "Solicitante": tk.Entry(form_frame, width=25),
        "Departamento": ttk.Combobox(form_frame, values=["Compras", "Financeiro", "Produção", "TI", "RH"], width=23),
        "Status": ttk.Combobox(form_frame, values=["Aberta", "Aprovada", "Rejeitada"], width=18)
    }

    # Definindo grid com duas colunas de campos para melhor uso do espaço
    labels = list(campos.keys())
    for i, label in enumerate(labels):
        row = i // 2
        col = (i % 2) * 2  # 0 ou 2
        tk.Label(form_frame, text=label + ":", font=("Helvetica", 12), bg="#eef9f1", fg="#004d33").grid(row=row, column=col, sticky="e", padx=5, pady=8)
        campos[label].grid(row=row, column=col+1, sticky="w", padx=5, pady=8)

    # Inicializar combos com valor vazio
    campos["Unidade Medida"].set("")
    campos["Urgência"].set("")
    campos["Departamento"].set("")
    campos["Status"].set("Aberta")  # Status padrão

    def salvar_requisicao():
        dados = []
        for campo in labels:
            valor = campos[campo].get().strip()
            if campo in ["Código Produto", "Nome Produto", "Quantidade", "Urgência", "Solicitante", "Departamento"]:
                # Campos obrigatórios principais
                if not valor:
                    messagebox.showwarning("Campos obrigatórios", f"Por favor, preencha o campo '{campo}'.")
                    return
            dados.append(valor)

        # Data atual no formato
        dados.append(datetime.now().strftime('%d/%m/%Y %H:%M'))

        # Salvar em arquivo
        try:
            with open("dados/requisicoes.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Requisição registrada com sucesso.")
            for c in campos.values():
                c.delete(0, tk.END) if isinstance(c, tk.Entry) else c.set("")
            campos["Status"].set("Aberta")
            carregar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar requisição: {e}")

    btn_salvar = tk.Button(frame, text="Salvar Requisição", bg="#2e8b57", fg="white", font=("Helvetica", 14, "bold"), command=salvar_requisicao)
    btn_salvar.pack(pady=15)

    # Tabela para exibir requisições
    colunas = labels + ["Data Cadastro"]
    tabela = ttk.Treeview(frame, columns=colunas, show="headings", height=12)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=130, anchor="center")
    tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def carregar_tabela():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/requisicoes.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = linha.strip().split(" | ")
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    carregar_tabela()
