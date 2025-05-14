import tkinter as tk
from tkinter import messagebox, ttk
import os

def tela_permissoes_acesso(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f2f2f2")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🔐 Gerenciar Permissões de Acesso", font=("Helvetica", 18, "bold"),
             bg="#f2f2f2", fg="#333").pack(pady=15)

    campos_frame = tk.LabelFrame(frame, text="Cadastrar Novo Usuário", bg="#f2f2f2",
                                 font=("Helvetica", 12, "bold"), fg="#004466", padx=10, pady=10)
    campos_frame.pack(pady=10, padx=20, fill="x")

    campos = {
        "Usuário": tk.Entry(campos_frame, width=30),
        "Senha": tk.Entry(campos_frame, width=30, show="*"),
        "Função": ttk.Combobox(campos_frame, values=["Administrador", "Operador", "Caixa", "Visualizador"], width=27)
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#f2f2f2", fg="#00334d") \
            .grid(row=i, column=0, padx=10, pady=6, sticky="e")
        entrada.grid(row=i, column=1, padx=10, pady=6, sticky="w")

    def salvar_usuario():
        usuario = campos["Usuário"].get().strip()
        senha = campos["Senha"].get().strip()
        funcao = campos["Função"].get().strip()

        if not all([usuario, senha, funcao]):
            messagebox.showwarning("Campos Incompletos", "Preencha todos os campos.")
            return

        os.makedirs("dados", exist_ok=True)

        with open("dados/usuarios.txt", "a", encoding="utf-8") as f:
            f.write(f"{usuario} | {senha} | {funcao}\n")

        messagebox.showinfo("Usuário Salvo", f"Usuário '{usuario}' cadastrado com função '{funcao}'.")
        for entrada in campos.values():
            entrada.delete(0, tk.END)
        carregar_usuarios()

    tk.Button(campos_frame, text="💾 Salvar Usuário", bg="#004d99", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=salvar_usuario).grid(row=3, columnspan=2, pady=10)

    # --- Tabela de usuários ---
    tabela_frame = tk.LabelFrame(frame, text="👥 Usuários Cadastrados", bg="#f2f2f2",
                                 font=("Helvetica", 12, "bold"), fg="#00334d", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    colunas = ("Usuário", "Função")

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=200, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    scroll.grid(row=0, column=1, sticky="ns", pady=8)

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    def carregar_usuarios():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/usuarios.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    partes = [x.strip() for x in linha.strip().split("|")]
                    if len(partes) == 3:
                        tabela.insert("", "end", values=(partes[0], partes[2]))
        except FileNotFoundError:
            pass

    carregar_usuarios()

    # --- Legenda ---
    legenda = tk.Label(frame, text="⚠️ As permissões determinam o acesso a telas como: Produtos, Caixa, Parâmetros, etc.",
                       font=("Helvetica", 10, "italic"), bg="#f2f2f2", fg="#666")
    legenda.pack(pady=5)
