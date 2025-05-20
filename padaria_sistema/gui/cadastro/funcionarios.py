import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import csv
import os
import re
from datetime import datetime

def tela_funcionarios(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Funcionários 👨‍💼", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    entradas = {}

    cargos = ["Gerente", "Atendente", "Cozinheiro", "Entregador", "Caixa",
              "Limpeza", "Estoquista", "Supervisor", "Vendedor", "TI"]

    escolaridades = ["Ensino Fundamental", "Ensino Médio", "Técnico", "Superior", "Pós-graduação"]
    estados_civis = ["Solteiro", "Casado", "Divorciado", "Viúvo"]
    estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
               "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

    campos_info = {
        "Nome": tk.Entry(campos_frame, width=30),
        "CPF": tk.Entry(campos_frame, width=30),
        "RG": tk.Entry(campos_frame, width=30),
        "Cargo": ttk.Combobox(campos_frame, width=30, values=cargos, state="readonly"),
        "Salário": tk.Entry(campos_frame, width=30),
        "Data de Admissão": DateEntry(campos_frame, width=27, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy'),
        "Telefone": tk.Entry(campos_frame, width=30),
        "Email": tk.Entry(campos_frame, width=30),
        "Endereço": tk.Entry(campos_frame, width=30),
        "Cidade": tk.Entry(campos_frame, width=30),
        "Estado (UF)": ttk.Combobox(campos_frame, width=30, values=estados, state="readonly"),
        "Estado Civil": ttk.Combobox(campos_frame, width=30, values=estados_civis, state="readonly"),
        "Escolaridade": ttk.Combobox(campos_frame, width=30, values=escolaridades, state="readonly"),
        "Nº PIS": tk.Entry(campos_frame, width=30),
        "Horário de Trabalho": tk.Entry(campos_frame, width=30),
        "Banco": tk.Entry(campos_frame, width=30),
    }

    for i, (rotulo, entrada) in enumerate(campos_info.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")
        entradas[rotulo] = entrada

    def validar_entrada():
        cpf = entradas["CPF"].get()
        telefone = entradas["Telefone"].get()
        email = entradas["Email"].get()
        salario = entradas["Salário"].get()

        if not re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
            messagebox.showerror("Erro", "CPF inválido. Ex: 000.000.000-00")
            return False
        if not re.fullmatch(r"\(\d{2}\) \d{5}-\d{4}", telefone):
            messagebox.showerror("Erro", "Telefone inválido. Ex: (00) 00000-0000")
            return False
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Erro", "Email inválido.")
            return False
        try:
            float(salario)
        except ValueError:
            messagebox.showerror("Erro", "Salário deve conter apenas números.")
            return False
        return True

    def limpar_formulario():
        for entrada in entradas.values():
            if isinstance(entrada, DateEntry):
                entrada.set_date(datetime.today())
            elif isinstance(entrada, ttk.Combobox):
                entrada.set("")
            else:
                entrada.delete(0, tk.END)

    def salvar_funcionario():
        dados = [
            entrada.get().strip() if not isinstance(entrada, DateEntry)
            else entrada.get_date().strftime("%d/%m/%Y")
            for entrada in entradas.values()
        ]
        if all(dados):
            if not validar_entrada():
                return
            os.makedirs("dados", exist_ok=True)
            with open("dados/funcionarios.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Funcionário salvo com sucesso.")
            limpar_formulario()
            carregar_funcionarios()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def atualizar_funcionario():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Seleção", "Nenhum funcionário selecionado.")
            return
        dados = [
            entrada.get().strip() if not isinstance(entrada, DateEntry)
            else entrada.get_date().strftime("%d/%m/%Y")
            for entrada in entradas.values()
        ]
        if not all(dados):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        if not validar_entrada():
            return

        try:
            with open("dados/funcionarios.txt", "r", encoding="utf-8") as f:
                linhas = f.readlines()
            with open("dados/funcionarios.txt", "w", encoding="utf-8") as f:
                for linha in linhas:
                    valores = linha.strip().split("|")
                    if valores[0].strip() == tabela.item(item[0])["values"][0]:
                        f.write(" | ".join(dados) + "\n")
                    else:
                        f.write(linha)
            messagebox.showinfo("Atualizado", "Funcionário atualizado com sucesso.")
            limpar_formulario()
            atualizar_btn.pack_forget()
            salvar_btn.pack(side="left", padx=10)
            carregar_funcionarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")

    def exportar_csv():
        try:
            with open("dados/funcionarios.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/funcionarios.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(entradas.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Exportado para 'dados/funcionarios.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado para exportar.")

    def carregar_funcionarios(filtro=""):
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/funcionarios.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [valor.strip() for valor in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        if filtro.lower() in valores[0].lower() or filtro.lower() in valores[1].lower():
                            tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    def carregar_para_edicao(event):
        item = tabela.selection()
        if item:
            valores = tabela.item(item[0])["values"]
            for i, entrada in enumerate(entradas.values()):
                if isinstance(entrada, ttk.Combobox):
                    entrada.set(valores[i])
                elif isinstance(entrada, DateEntry):
                    entrada.set_date(datetime.strptime(valores[i], "%d/%m/%Y"))
                else:
                    entrada.delete(0, tk.END)
                    entrada.insert(0, valores[i])
            salvar_btn.pack_forget()
            atualizar_btn.pack(side="left", padx=10)

    # Filtro
    filtro_frame = tk.Frame(frame, bg="#e6f2ff")
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="🔍 Buscar por Nome ou CPF:", font=("Helvetica", 11), bg="#e6f2ff").pack(side="left", padx=5)
    entrada_filtro = tk.Entry(filtro_frame, width=40)
    entrada_filtro.pack(side="left")
    tk.Button(filtro_frame, text="Buscar", command=lambda: carregar_funcionarios(entrada_filtro.get())).pack(side="left", padx=5)

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    salvar_btn = tk.Button(botoes_frame, text="💾 Salvar Funcionário", bg="#339966", fg="white",
                           font=("Helvetica", 12, "bold"), width=20, command=salvar_funcionario)
    salvar_btn.pack(side="left", padx=10)

    atualizar_btn = tk.Button(botoes_frame, text="🔄 Atualizar Funcionário", bg="#ff9933", fg="white",
                              font=("Helvetica", 12, "bold"), width=20, command=atualizar_funcionario)

    tk.Button(botoes_frame, text="📁 Exportar dados", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_csv).pack(side="left", padx=10)

    # Tabela
    tabela_frame = tk.LabelFrame(frame, text="📋 Funcionários Cadastrados", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = tuple(entradas.keys())
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

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

    tabela.bind("<Double-1>", carregar_para_edicao)

    carregar_funcionarios()
