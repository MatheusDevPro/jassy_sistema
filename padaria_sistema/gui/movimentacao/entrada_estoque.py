import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from tkcalendar import DateEntry

def tela_entrada_estoque(janela):
    # Limpar a tela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Frame principal
    frame = tk.Frame(janela, bg="#f0f5f5")
    frame.pack(fill="both", expand=True)

    # Título
    tk.Label(frame, text="📦 Entrada de Estoque", font=("Helvetica", 18, "bold"),
             bg="#f0f5f5", fg="#003366").pack(pady=10)

    # Frame dos campos
    campos_frame = tk.Frame(frame, bg="#f0f5f5")
    campos_frame.pack(pady=10, padx=10)

    # Valores para combos
    categorias = ["Alimentos", "Bebidas", "Limpeza", "Eletrônicos", "Roupas", "Outros"]
    unidades = ["Un", "Kg", "g", "L", "ml", "Pacote", "Caixa"]
    status_produto = ["Ativo", "Inativo"]

    campos = {
        "Produto": tk.Entry(campos_frame, width=30),
        "Código do Produto": tk.Entry(campos_frame, width=30),
        "Categoria": ttk.Combobox(campos_frame, width=27, values=categorias, state="readonly"),
        "Unidade de Medida": ttk.Combobox(campos_frame, width=27, values=unidades, state="readonly"),
        "Quantidade Entrada": tk.Entry(campos_frame, width=30),
        "Valor Unitário (R$)": tk.Entry(campos_frame, width=30),
        "Data de Entrada": DateEntry(campos_frame, width=30, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy'),
        "Número da Nota Fiscal": tk.Entry(campos_frame, width=30),
        "Fornecedor": tk.Entry(campos_frame, width=30),
        "Lote": tk.Entry(campos_frame, width=30),
        "Validade": DateEntry(campos_frame, width=30, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy'),
        "Status do Produto": ttk.Combobox(campos_frame, width=27, values=status_produto, state="readonly"),
        "Responsável": tk.Entry(campos_frame, width=30),
        "Data Última Atualização": DateEntry(campos_frame, width=30, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy'),
        "Observações": tk.Text(campos_frame, width=62, height=4)
    }

    # Set default values for comboboxes
    campos["Categoria"].current(0)
    campos["Unidade de Medida"].current(0)
    campos["Status do Produto"].current(0)

    # Distribuir os campos em 2 colunas (com exceção de Observações que ocupa toda a largura)
    campos_por_coluna = 7
    i = 0
    for rotulo, entrada in campos.items():
        if rotulo == "Observações":
            # Observações ocupa toda a largura abaixo dos outros campos
            tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#f0f5f5")\
                .grid(row=campos_por_coluna, column=0, sticky="nw", padx=5, pady=5)
            entrada.grid(row=campos_por_coluna, column=1, columnspan=3, sticky="w", padx=5, pady=5)
        else:
            coluna = (i // campos_por_coluna) * 2  # coluna 0 ou 2
            linha = i % campos_por_coluna

            tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#f0f5f5")\
                .grid(row=linha, column=coluna, sticky="e", padx=5, pady=5)
            entrada.grid(row=linha, column=coluna + 1, sticky="w", padx=5, pady=5)
            i += 1

    # Salvar Entrada
    def salvar_entrada():
        dados = []
        for rotulo, entrada in campos.items():
            if rotulo == "Observações":
                dados.append(entrada.get("1.0", "end").strip())
            else:
                dados.append(entrada.get().strip())
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/entrada_estoque.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Entrada registrada com sucesso.")
            for rotulo, entrada in campos.items():
                if rotulo == "Observações":
                    entrada.delete("1.0", "end")
                else:
                    entrada.delete(0, tk.END)
            carregar_entradas()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    # Exportar CSV
    def exportar_csv():
        try:
            with open("dados/entrada_estoque.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/entrada_estoque.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/entrada_estoque.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Botões
    botoes_frame = tk.Frame(frame, bg="#f0f5f5")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar Entrada 💾", bg="#007399", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_entrada).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Exportar CSV 📁", bg="#00334d", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    # Tabela com Scroll vertical e horizontal
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(pady=10, fill="both", expand=True)

    colunas = tuple(campos.keys())
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)

    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    # Carregar dados
    def carregar_entradas():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/entrada_estoque.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    carregar_entradas()
