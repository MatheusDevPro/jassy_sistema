import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import re
from tkcalendar import DateEntry
from datetime import datetime

def tela_produtos(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Produtos 📦", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    categorias = ["Alimentos", "Bebidas", "Higiene", "Limpeza", "Eletrônicos", "Roupas", "Outros"]
    unidades = ["unidade", "litro", "kg", "metro", "caixa"]

    campos = {
        "Nome": tk.Entry(campos_frame, width=30),
        "Código": tk.Entry(campos_frame, width=30),
        "Preço": tk.Entry(campos_frame, width=30),
        "Quantidade": tk.Entry(campos_frame, width=30),
        "Data de Validade": DateEntry(campos_frame, width=27, background='darkblue',
                                       foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy'),
        "Fornecedor": tk.Entry(campos_frame, width=30),
        "Descrição": tk.Entry(campos_frame, width=30),
        "Categoria": ttk.Combobox(campos_frame, values=categorias, width=28, state="readonly"),
        "Unidade de Medida": ttk.Combobox(campos_frame, values=unidades, width=28, state="readonly"),
        "Localização no Estoque": tk.Entry(campos_frame, width=30),
        "Marca": tk.Entry(campos_frame, width=30),
        "Garantia (meses)": tk.Entry(campos_frame, width=30),
        "Peso (kg)": tk.Entry(campos_frame, width=30),
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    def validar_dados(dados):
        try:
            float(dados[2])  # Preço
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número válido.")
            return False
        if not dados[3].isdigit():
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
            return False
        if not re.match(r"^\d{2}/\d{2}/\d{4}$", dados[4]):
            messagebox.showerror("Erro", "Data de Validade deve estar no formato dd/mm/aaaa.")
            return False
        try:
            float(dados[11])  # Garantia
            float(dados[12])  # Peso
        except ValueError:
            messagebox.showerror("Erro", "Garantia e Peso devem ser números.")
            return False
        return True

    def limpar_formulario():
        for entrada in campos.values():
            if isinstance(entrada, ttk.Combobox):
                entrada.set("")
            elif isinstance(entrada, DateEntry):
                entrada.set_date(datetime.today())
            else:
                entrada.delete(0, tk.END)

    def salvar_produto():
        dados = [
            entrada.get().strip() if not isinstance(entrada, DateEntry)
            else entrada.get_date().strftime("%d/%m/%Y")
            for entrada in campos.values()
        ]
        if all(dados):
            if not validar_dados(dados):
                return
            os.makedirs("dados", exist_ok=True)
            with open("dados/produtos.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso.")
            limpar_formulario()
            carregar_produtos()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def exportar_csv():
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/produtos.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/produtos.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    def carregar_produtos(filtro=""):
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        if filtro.lower() in valores[0].lower() or filtro.lower() in valores[1].lower():
                            tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    def carregar_para_edicao(event):
        item = tabela.selection()
        if item:
            valores = tabela.item(item[0])["values"]
            for i, entrada in enumerate(campos.values()):
                if isinstance(entrada, ttk.Combobox):
                    entrada.set(valores[i])
                elif isinstance(entrada, DateEntry):
                    entrada.set_date(datetime.strptime(valores[i], "%d/%m/%Y"))
                else:
                    entrada.delete(0, tk.END)
                    entrada.insert(0, valores[i])
            salvar_btn.pack_forget()
            atualizar_btn.pack(side="left", padx=10)

    def atualizar_produto():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Seleção", "Nenhum produto selecionado para atualizar.")
            return

        dados = [
            entrada.get().strip() if not isinstance(entrada, DateEntry)
            else entrada.get_date().strftime("%d/%m/%Y")
            for entrada in campos.values()
        ]
        if not all(dados):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        if not validar_dados(dados):
            return

        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                linhas = f.readlines()
            with open("dados/produtos.txt", "w", encoding="utf-8") as f:
                for linha in linhas:
                    valores = linha.strip().split("|")
                    if valores[0].strip() == tabela.item(item[0])["values"][0]:
                        f.write(" | ".join(dados) + "\n")
                    else:
                        f.write(linha)
            messagebox.showinfo("Atualizado", "Produto atualizado com sucesso.")
            limpar_formulario()
            atualizar_btn.pack_forget()
            salvar_btn.pack(side="left", padx=10)
            carregar_produtos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")

    # Campo de Filtro
    filtro_frame = tk.Frame(frame, bg="#e6f2ff")
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="🔎 Buscar Produto:", font=("Helvetica", 11),
             bg="#e6f2ff", fg="#004466").pack(side="left")

    campo_busca = tk.Entry(filtro_frame, width=40)
    campo_busca.pack(side="left", padx=10)

    tk.Button(filtro_frame, text="Buscar", bg="#007acc", fg="white",
              font=("Helvetica", 10, "bold"), command=lambda: carregar_produtos(campo_busca.get())).pack(side="left")

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    salvar_btn = tk.Button(botoes_frame, text="💾 Salvar Produto", bg="#339966", fg="white",
                           font=("Helvetica", 12, "bold"), width=20, command=salvar_produto)
    salvar_btn.pack(side="left", padx=10)

    atualizar_btn = tk.Button(botoes_frame, text="✏️ Atualizar Produto", bg="#ff9933", fg="white",
                              font=("Helvetica", 12, "bold"), width=20, command=atualizar_produto)

    tk.Button(botoes_frame, text="📁 Exportar dados", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_csv).pack(side="left", padx=10)

    tabela_frame = tk.LabelFrame(frame, text="📋 Produtos Cadastrados", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = tuple(campos.keys())
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=130, anchor="center")

    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)

    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    tabela.bind("<Double-1>", carregar_para_edicao)

    carregar_produtos()
