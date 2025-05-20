import tkinter as tk
from tkinter import messagebox, ttk
import os
import csv
from datetime import datetime

def tela_usuarios(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Gestão de Usuários 🔐", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=20)

    # Campos de entrada do formulário
    campos = {
        "Nome": tk.Entry(campos_frame, width=40),
        "Login": tk.Entry(campos_frame, width=40),
        "Senha": tk.Entry(campos_frame, width=40, show="*"),
        "CPF": tk.Entry(campos_frame, width=40),
        "Cargo": tk.Entry(campos_frame, width=40),
        "Permissão": ttk.Combobox(campos_frame, values=["Administrador", "Diretor", "Gerente", "Usuário"], width=28),
        "Status": ttk.Combobox(campos_frame, values=["Ativo", "Inativo", "Bloqueado"], width=28),
        "Observações": tk.Entry(campos_frame, width=40)
    }

    # Layout dos campos
    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=6, pady=4, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=6, pady=4, sticky="w")

    # Campos de busca
    busca_frame = tk.Frame(frame, bg="#e6f2ff")
    busca_frame.pack(pady=10)

    tk.Label(busca_frame, text="Buscar por Nome:", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
        .grid(row=0, column=0, padx=6, pady=4, sticky="e")
    busca_nome = tk.Entry(busca_frame, width=40)
    busca_nome.grid(row=0, column=1, padx=6, pady=4, sticky="w")

    tk.Label(busca_frame, text="Buscar por CPF:", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
        .grid(row=0, column=2, padx=6, pady=4, sticky="e")
    busca_cpf = tk.Entry(busca_frame, width=40)
    busca_cpf.grid(row=0, column=3, padx=6, pady=4, sticky="w")

    def buscar_usuario():
        nome_busca = busca_nome.get().strip()
        cpf_busca = busca_cpf.get().strip()

        # Limpar a tabela antes de atualizar com novos dados
        tabela.delete(*tabela.get_children())

        try:
            with open("dados/usuarios.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        # Filtro por nome e/ou CPF
                        if (nome_busca.lower() in valores[0].lower() or nome_busca == "") and (cpf_busca in valores[3] or cpf_busca == ""):
                            tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    tk.Button(busca_frame, text="Buscar 🔍", bg="#0059b3", fg="white", font=("Helvetica", 12, "bold"), command=buscar_usuario).grid(row=0, column=4, padx=10)

    # Função de salvar usuário
    def salvar_usuario():
        dados = [entrada.get().strip() for entrada in campos.values()]
        data_cadastro = datetime.now().strftime("%d/%m/%Y %H:%M")
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/usuarios.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados + [data_cadastro]) + "\n")
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
            for entrada in campos.values():
                if isinstance(entrada, ttk.Combobox):
                    entrada.set("")
                else:
                    entrada.delete(0, tk.END)
            carregar_usuarios()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    # Função de exportar dados para CSV
    def exportar_csv():
        try:
            with open("dados/usuarios.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/usuarios.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(list(campos.keys()) + ["Data de Cadastro"])
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/usuarios.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Função de excluir usuário
    def excluir_usuario():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um usuário para excluir.")
            return
        if not messagebox.askyesno("Confirmar", "Deseja realmente excluir este usuário?"):
            return

        valores = tabela.item(item)["values"]
        tabela.delete(item)

        with open("dados/usuarios.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
        with open("dados/usuarios.txt", "w", encoding="utf-8") as f:
            for linha in linhas:
                if not all(str(v).strip() in linha for v in valores):
                    f.write(linha)

        messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")

    # Função de editar usuário
    def editar_usuario():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um usuário para editar.")
            return

        valores = tabela.item(item)["values"]
        for i, entrada in enumerate(campos.values()):
            entrada.delete(0, tk.END)
            entrada.insert(0, valores[i])
        campos["Permissão"].set(valores[5])
        campos["Status"].set(valores[6])

        with open("dados/usuarios.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
        with open("dados/usuarios.txt", "w", encoding="utf-8") as f:
            for linha in linhas:
                if not all(str(v).strip() in linha for v in valores):
                    f.write(linha)

        tabela.delete(item)

    # Botões de ação
    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar Usuário 💾", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_usuario).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Editar ✏️", bg="#ff9933", fg="white",
              font=("Helvetica", 12, "bold"), command=editar_usuario).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Excluir 🗑️", bg="#cc0000", fg="white",
              font=("Helvetica", 12, "bold"), command=excluir_usuario).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Exportar CSV 📁", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    # Definição da tabela e scrolls
    tabela_frame = tk.Frame(frame, bg="#e6f2ff", bd=2, relief="groove")
    tabela_frame.pack(padx=20, pady=15, fill="both", expand=True)

    colunas = list(campos.keys()) + ["Data de Cadastro"]

    # Estilo para a tabela
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#e6f2ff", foreground="black", rowheight=25, fieldbackground="#e6f2ff")
    style.configure("Treeview.Heading", background="#006699", foreground="white", font=("Helvetica", 12, "bold"))

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=130, anchor="center")

    # Scroll vertical
    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_y.pack(side="right", fill="y")
    tabela.configure(yscrollcommand=scroll_y.set)

    # Scroll horizontal
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    scroll_x.pack(side="bottom", fill="x")
    tabela.configure(xscrollcommand=scroll_x.set)

    tabela.pack(side="left", fill="both", expand=True)

    # Função para carregar usuários na tabela
    def carregar_usuarios():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/usuarios.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
        except FileNotFoundError:
            pass

    carregar_usuarios()

