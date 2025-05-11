import tkinter as tk
from tkinter import messagebox, ttk
import os
import csv

def tela_usuarios(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#fffaf0")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Gestão de Usuários 🔐", font=("Helvetica", 18, "bold"),
             bg="#fffaf0", fg="#cc6600").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#fffaf0")
    campos_frame.pack(pady=10)

    campos = {
        "Nome": tk.Entry(campos_frame, width=30),
        "Login": tk.Entry(campos_frame, width=30),
        "Senha": tk.Entry(campos_frame, width=30, show="*"),
        "Cargo": tk.Entry(campos_frame, width=30),
        "Permissão": ttk.Combobox(campos_frame, values=["Administrador", "Gerente", "Usuário"], width=28)
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#fffaf0") \
            .grid(row=i, column=0, sticky="e", padx=5, pady=5)
        entrada.grid(row=i, column=1, padx=5, pady=5)

    def salvar_usuario():
        dados = [entrada.get() for entrada in campos.values()]
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/usuarios.txt", "a", encoding="utf-8") as f:
                f.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            campos["Permissão"].set("")
            carregar_usuarios()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    def exportar_csv():
        try:
            with open("dados/usuarios.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/usuarios.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(campos.keys())
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/usuarios.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

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

    def editar_usuario():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um usuário para editar.")
            return

        valores = tabela.item(item)["values"]
        for i, entrada in enumerate(campos.values()):
            entrada.delete(0, tk.END)
            entrada.insert(0, valores[i])
        campos["Permissão"].set(valores[-1])

        # Remove da lista para evitar duplicação
        with open("dados/usuarios.txt", "r", encoding="utf-8") as f:
            linhas = f.readlines()
        with open("dados/usuarios.txt", "w", encoding="utf-8") as f:
            for linha in linhas:
                if not all(str(v).strip() in linha for v in valores):
                    f.write(linha)

        tabela.delete(item)

    botoes_frame = tk.Frame(frame, bg="#fffaf0")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar Usuário 💾", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_usuario).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Editar ✏️", bg="#ff9933", fg="white",
              font=("Helvetica", 12, "bold"), command=editar_usuario).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Excluir 🗑️", bg="#cc0000", fg="white",
              font=("Helvetica", 12, "bold"), command=excluir_usuario).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Exportar CSV 📁", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(pady=10)

    colunas = list(campos.keys())

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("Treeview", font=("Helvetica", 11), rowheight=25)

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0)
    scroll.grid(row=0, column=1, sticky="ns")

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
