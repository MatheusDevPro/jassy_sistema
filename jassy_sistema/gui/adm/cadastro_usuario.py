import tkinter as tk
from tkinter import ttk, messagebox
import os

def tela_cadastro_usuario(janela):
    # Limpa a janela (exceto menu)
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("👤 Cadastro de Usuários")
    janela.geometry("1000x700")
    janela.minsize(900, 650)
    janela.resizable(True, True)
    janela.configure(bg="#f2f2f2")

    frame = tk.Frame(janela, bg="#f2f2f2")
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)

    # Título
    titulo = tk.Label(frame, text="👤 Cadastro Completo de Usuário", font=("Helvetica", 22, "bold"),
                      bg="#f2f2f2", fg="#004466")
    titulo.grid(row=0, column=0, sticky="w", pady=(0, 15))

    # --- Formulário ---
    formulario_frame = tk.LabelFrame(frame, text="Dados do Usuário", bg="#f2f2f2",
                                    font=("Helvetica", 14, "bold"), fg="#004466", padx=20, pady=20)
    formulario_frame.grid(row=1, column=0, sticky="ew")
    formulario_frame.columnconfigure(1, weight=1)
    formulario_frame.columnconfigure(3, weight=1)

    # Campos: label + entry/combo etc
    campos = {
        "Nome Completo": tk.Entry(formulario_frame),
        "Usuário": tk.Entry(formulario_frame),
        "Senha": tk.Entry(formulario_frame, show="*"),
        "Email": tk.Entry(formulario_frame),
        "Telefone": tk.Entry(formulario_frame),
        "Gênero": ttk.Combobox(formulario_frame, values=["Masculino", "Feminino", "Outro"]),
        "Estado Civil": ttk.Combobox(formulario_frame, values=["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]),
        "Profissão": tk.Entry(formulario_frame),
        "Cidade": tk.Entry(formulario_frame),
        "Estado": ttk.Combobox(formulario_frame,
                               values=["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
                                       "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
                                       "RS", "RO", "RR", "SC", "SP", "SE", "TO"]),
    }

    # Layout em grid 5 linhas x 4 colunas (2 colunas de labels + inputs por linha)
    labels = list(campos.keys())
    linha = 0
    for i in range(0, len(labels), 2):
        # label coluna 0
        tk.Label(formulario_frame, text=labels[i] + ":", font=("Helvetica", 12),
                 bg="#f2f2f2", fg="#00334d").grid(row=linha, column=0, sticky="e", padx=10, pady=8)
        campos[labels[i]].grid(row=linha, column=1, sticky="ew", padx=10, pady=8)
        if i + 1 < len(labels):
            # label coluna 2
            tk.Label(formulario_frame, text=labels[i + 1] + ":", font=("Helvetica", 12),
                     bg="#f2f2f2", fg="#00334d").grid(row=linha, column=2, sticky="e", padx=10, pady=8)
            campos[labels[i + 1]].grid(row=linha, column=3, sticky="ew", padx=10, pady=8)
        linha += 1

    # Configura combo boxes para permitir digitar e selecionar
    for key in ["Gênero", "Estado Civil", "Estado"]:
        campos[key]["state"] = "readonly"

    # Botão salvar
    def salvar_usuario():
        dados = {}
        for key, entry in campos.items():
            valor = entry.get().strip()
            if not valor:
                messagebox.showwarning("Campo vazio", f"Por favor, preencha o campo '{key}'.")
                return
            dados[key] = valor

        # Cria pasta dados, se não existir
        os.makedirs("dados", exist_ok=True)
        caminho = "dados/usuarios.txt"

        # Salva no formato separado por |, mantendo ordem dos campos
        with open(caminho, "a", encoding="utf-8") as f:
            linha = " | ".join(dados[key] for key in labels)
            f.write(linha + "\n")

        messagebox.showinfo("Sucesso", f"Usuário '{dados['Usuário']}' cadastrado com sucesso!")

        # Limpa campos
        for entry in campos.values():
            entry.delete(0, tk.END)

        carregar_usuario()

    btn_salvar = tk.Button(formulario_frame, text="💾 Salvar Usuário", bg="#004d99", fg="white",
                          font=("Helvetica", 14, "bold"), width=20, command=salvar_usuario)
    btn_salvar.grid(row=linha, column=0, columnspan=4, pady=20)

    # --- Tabela abaixo ---
    tabela_frame = tk.LabelFrame(frame, text="👥 Usuários Cadastrados", bg="#f2f2f2",
                                 font=("Helvetica", 14, "bold"), fg="#004466", padx=10, pady=10)
    tabela_frame.grid(row=2, column=0, sticky="nsew", pady=10)
    tabela_frame.columnconfigure(0, weight=1)
    tabela_frame.rowconfigure(0, weight=1)

    colunas_tabela = labels  # mesmas colunas do formulário
    tabela = ttk.Treeview(tabela_frame, columns=colunas_tabela, show="headings", selectmode="browse")
    tabela.grid(row=0, column=0, sticky="nsew")

    # Scrollbars
    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    scroll_x.grid(row=1, column=0, sticky="ew")

    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    # Configura colunas tabela
    for col in colunas_tabela:
        tabela.heading(col, text=col, anchor="center")
        tabela.column(col, anchor="center", width=110)

    # Zebra striping e estilo
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="white",
                    foreground="#333",
                    rowheight=28,
                    fieldbackground="white",
                    font=("Helvetica", 11))
    style.configure("Treeview.Heading",
                    font=("Helvetica", 13, "bold"),
                    foreground="#004466")
    style.map("Treeview", background=[("selected", "#3399ff")], foreground=[("selected", "white")])
    tabela.tag_configure("oddrow", background="#f9f9f9")
    tabela.tag_configure("evenrow", background="#e6f0ff")

    # Função carregar usuários do arquivo
    def carregar_usuario():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/usuarios.txt", "r", encoding="utf-8") as f:
                for i, linha in enumerate(f):
                    dados = [x.strip() for x in linha.strip().split("|")]
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    if len(dados) == len(colunas_tabela):
                        tabela.insert("", "end", values=dados, tags=(tag,))
        except FileNotFoundError:
            pass

    carregar_usuario()

    # Botão atualizar tabela
    btn_atualizar = tk.Button(frame, text="🔄 Atualizar Lista", bg="#0066cc", fg="white",
                              font=("Helvetica", 12, "bold"), command=carregar_usuario)
    btn_atualizar.grid(row=3, column=0, sticky="e", pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    tela_cadastro_usuario(root)
    root.mainloop()
