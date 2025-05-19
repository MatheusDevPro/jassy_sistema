import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
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

    # Valores possíveis para Comboboxes
    categorias = ["Eletrônicos", "Alimentos", "Vestuário", "Cosméticos", "Livros", "Outros"]
    status_venda = ["Pendente", "Pago", "Cancelado"]
    condicoes_pagamento = ["À vista", "Parcelado 2x", "Parcelado 3x", "Parcelado 4x ou mais"]

    # Criando os campos
    campos = {
        "Código": tk.Entry(campos_frame, width=25),
        "Produto": tk.Entry(campos_frame, width=25),
        "Descrição": tk.Entry(campos_frame, width=25),
        "Categoria": ttk.Combobox(campos_frame, values=categorias, state="readonly", width=23),
        "Quantidade": tk.Entry(campos_frame, width=25),
        "Preço Unitário": tk.Entry(campos_frame, width=25),
        "Data da Venda": DateEntry(campos_frame, width=22, date_pattern='dd/mm/yyyy'),
        "Cliente": tk.Entry(campos_frame, width=25),
        "Vendedor": tk.Entry(campos_frame, width=25),
        "Status": ttk.Combobox(campos_frame, values=status_venda, state="readonly", width=23),
        "Condição de Pagamento": ttk.Combobox(campos_frame, values=condicoes_pagamento, state="readonly", width=23),
        "Valor Total": tk.Entry(campos_frame, width=25, state="readonly"),
    }

    # Posicionamento em grid (duas colunas)
    linhas = 0
    colunas = 0
    for i, (rotulo, entrada) in enumerate(campos.items()):
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linhas, column=colunas*2, padx=8, pady=6, sticky="e")
        entrada.grid(row=linhas, column=colunas*2 + 1, padx=8, pady=6, sticky="w")
        colunas += 1
        if colunas > 1:
            colunas = 0
            linhas += 1

    # Campo de Observações (Text widget maior, ocupa 2 colunas)
    tk.Label(campos_frame, text="Observações:", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
        .grid(row=linhas, column=0, padx=8, pady=6, sticky="ne")
    texto_obs = tk.Text(campos_frame, width=55, height=4)
    texto_obs.grid(row=linhas, column=1, columnspan=3, padx=8, pady=6, sticky="w")
    linhas += 1

    # Função para calcular valor total automaticamente
    def calcular_total(event=None):
        try:
            quantidade = int(campos["Quantidade"].get())
            preco_unitario = float(campos["Preço Unitário"].get())
            total = quantidade * preco_unitario
            campos["Valor Total"].config(state="normal")
            campos["Valor Total"].delete(0, tk.END)
            campos["Valor Total"].insert(0, f"{total:.2f}")
            campos["Valor Total"].config(state="readonly")
        except ValueError:
            campos["Valor Total"].config(state="normal")
            campos["Valor Total"].delete(0, tk.END)
            campos["Valor Total"].insert(0, "0.00")
            campos["Valor Total"].config(state="readonly")

    campos["Quantidade"].bind("<KeyRelease>", calcular_total)
    campos["Preço Unitário"].bind("<KeyRelease>", calcular_total)

    def salvar_venda():
        valores = []
        for key, entrada in campos.items():
            if isinstance(entrada, DateEntry):
                valores.append(entrada.get_date().strftime('%d/%m/%Y'))
            else:
                valores.append(entrada.get().strip())

        obs_text = texto_obs.get("1.0", tk.END).strip()
        if not obs_text:
            obs_text = "-"
        valores.append(obs_text)  # Adiciona observações no final

        # Verificar campos obrigatórios (excluindo Valor Total e Observações)
        obrigatorios = list(campos.keys())
        obrigatorios.remove("Valor Total")
        for i, campo in enumerate(campos):
            if campo in obrigatorios and valores[i] == "":
                messagebox.showwarning("Atenção", f"Preencha o campo '{campo}'.")
                return

        if valores[obrigatorios.index("Quantidade")] == "0" or valores[-2] == "0.00":
            messagebox.showwarning("Atenção", "Quantidade e Valor Total devem ser maiores que zero.")
            return

        os.makedirs("dados", exist_ok=True)

        # Salvar com separador | e incluir observações no final
        with open("dados/vendas.txt", "a", encoding="utf-8") as arq:
            arq.write(" | ".join(valores) + "\n")

        messagebox.showinfo("Sucesso", "Venda registrada com sucesso.")

        # Limpar campos
        for entrada in campos.values():
            if isinstance(entrada, tk.Entry):
                entrada.config(state="normal")
                entrada.delete(0, tk.END)
                if entrada == campos["Valor Total"]:
                    entrada.config(state="readonly")
            elif isinstance(entrada, ttk.Combobox):
                entrada.set("")
            elif isinstance(entrada, DateEntry):
                entrada.set_date(datetime.today())
        texto_obs.delete("1.0", tk.END)

        carregar_vendas()

    def exportar_csv():
        try:
            with open("dados/vendas.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split(" | ") for linha in f if linha.strip()]
            with open("dados/vendas.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(list(campos.keys()) + ["Observações"])
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
