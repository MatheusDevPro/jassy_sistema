import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

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
    campos_frame.pack(pady=10)

    campos = {
        "Código": tk.Entry(campos_frame, width=30),
        "Produto": tk.Entry(campos_frame, width=30),
        "Descrição": tk.Entry(campos_frame, width=30),
        "Quantidade": tk.Entry(campos_frame, width=30),
        "Preço Unitário": tk.Entry(campos_frame, width=30),
        "Data da Venda": tk.Entry(campos_frame, width=30),
        "Valor Total": tk.Entry(campos_frame, width=30, state="readonly")  # Tornar o campo "Valor Total" somente leitura
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    def calcular_total(event=None):
        try:
            quantidade = int(campos["Quantidade"].get())
            preco_unitario = float(campos["Preço Unitário"].get())
            total = quantidade * preco_unitario
            campos["Valor Total"].config(state="normal")  # Torna o campo editável temporariamente
            campos["Valor Total"].delete(0, tk.END)  # Limpa o campo de valor total
            campos["Valor Total"].insert(0, f"{total:.2f}")  # Insere o valor calculado
            campos["Valor Total"].config(state="readonly")  # Torna o campo somente leitura novamente
        except ValueError:
            campos["Valor Total"].config(state="normal")  # Torna o campo editável temporariamente
            campos["Valor Total"].delete(0, tk.END)  # Limpa o campo de valor total
            campos["Valor Total"].insert(0, "0.00")  # Insere valor 0.00 se houver erro nos inputs
            campos["Valor Total"].config(state="readonly")  # Torna o campo somente leitura novamente

    # Vincula a função de cálculo aos campos de Quantidade e Preço Unitário
    campos["Quantidade"].bind("<KeyRelease>", calcular_total)
    campos["Preço Unitário"].bind("<KeyRelease>", calcular_total)

    def salvar_venda():
        # Verifica se todos os campos estão preenchidos corretamente, incluindo o valor total
        if not campos["Valor Total"].get().strip() or campos["Valor Total"].get().strip() == "0.00":
            messagebox.showwarning("Atenção", "O valor total não pode ser vazio ou 0.00.")
            return
        
        dados = [entrada.get().strip() for entrada in campos.values() if entrada.get()]
        total = campos["Valor Total"].get().strip()

        # Verifica se todos os campos foram preenchidos corretamente
        if len(dados) == len(campos) - 1 and total != "0.00":
            os.makedirs("dados", exist_ok=True)
            with open("dados/vendas.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + f" | Total: {total}\n")
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso.")
            for entrada in campos.values():
                if isinstance(entrada, tk.Entry):
                    entrada.delete(0, tk.END)
            carregar_vendas()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")

    def exportar_csv():
        try:
            with open("dados/vendas.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/vendas.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/vendas.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="💾 Registrar Venda", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=salvar_venda).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar dados", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_csv).pack(side="left", padx=10)

    # --- Tabela com Estilo Integrado ---
    tabela_frame = tk.LabelFrame(frame, text="📋 Vendas Registradas", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = tuple(campos.keys())

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=12)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=130, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    scroll.grid(row=0, column=1, sticky="ns", pady=8)

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    def carregar_vendas():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/vendas.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    carregar_vendas()
