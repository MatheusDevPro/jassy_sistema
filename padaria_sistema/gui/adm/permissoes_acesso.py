import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import re
from datetime import datetime

def tela_permissoes_acesso(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("Gerenciar Permissões de Acesso")
    janela.geometry("900x700")
    janela.configure(bg="#f2f2f2")

    frame = ttk.Frame(janela, padding=15)
    frame.pack(fill="both", expand=True)

    titulo = ttk.Label(frame, text="🔐 Gerenciar Permissões de Acesso", font=("Helvetica", 20, "bold"), foreground="#00334d")
    titulo.pack(pady=10)

    # --- Frame Cadastro ---
    cadastro_frame = ttk.LabelFrame(frame, text="Cadastrar / Editar Usuário", padding=15)
    cadastro_frame.pack(fill="x", pady=10)

    # Campos extras que vamos usar
    campos = {
        "Usuário": ttk.Entry(cadastro_frame, width=30),
        "Senha": ttk.Entry(cadastro_frame, width=30, show="*"),
        "Nome Completo": ttk.Entry(cadastro_frame, width=50),
        "Email": ttk.Entry(cadastro_frame, width=50),
        "Telefone": ttk.Entry(cadastro_frame, width=30),
        "Departamento": ttk.Combobox(cadastro_frame, values=["TI", "Vendas", "Financeiro", "RH", "Administração", "Outros"], width=27),
        "Função": ttk.Combobox(cadastro_frame, values=["Administrador", "Operador", "Caixa", "Visualizador"], width=27),
        "Status": ttk.Combobox(cadastro_frame, values=["Ativo", "Inativo"], width=27),
        "Data Cadastro": ttk.Entry(cadastro_frame, width=30),
        "Observações": ttk.Entry(cadastro_frame, width=50),
    }

    # Preencher data cadastro com data atual
    campos["Data Cadastro"].insert(0, datetime.now().strftime("%d/%m/%Y"))

    # Layout grid 10 campos (labels + inputs)
    for i, (rotulo, widget_campo) in enumerate(campos.items()):
        ttk.Label(cadastro_frame, text=f"{rotulo}:", font=("Helvetica", 12)).grid(row=i, column=0, sticky="e", padx=5, pady=5)
        widget_campo.grid(row=i, column=1, sticky="w", padx=5, pady=5)

    # --- Frame Permissões ---
    permissoes_frame = ttk.LabelFrame(frame, text="Permissões do Usuário", padding=10)
    permissoes_frame.pack(fill="x", pady=10)

    permissoes = {
        "Produtos": tk.BooleanVar(),
        "Caixa": tk.BooleanVar(),
        "Parâmetros": tk.BooleanVar(),
        "Relatórios": tk.BooleanVar(),
        "Usuários": tk.BooleanVar(),
        "Estoque": tk.BooleanVar(),
        "Financeiro": tk.BooleanVar(),
        "Atendimento": tk.BooleanVar(),
        "Marketing": tk.BooleanVar(),
        "Suporte": tk.BooleanVar(),
    }

    # Dispor checkbuttons em duas colunas
    for i, (nome_perm, var) in enumerate(permissoes.items()):
        coluna = 0 if i < 5 else 1
        linha = i if i < 5 else i - 5
        chk = ttk.Checkbutton(permissoes_frame, text=nome_perm, variable=var)
        chk.grid(row=linha, column=coluna, sticky="w", padx=10, pady=5)

    # --- Funções para lidar com dados ---
    arquivo_usuarios = "dados/usuarios.json"
    os.makedirs("dados", exist_ok=True)

    def validar_email(email):
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(regex, email) is not None

    def limpar_campos():
        for widget in campos.values():
            widget.delete(0, tk.END) if isinstance(widget, ttk.Entry) else widget.set("")
        campos["Departamento"].set("")
        campos["Função"].set("")
        campos["Status"].set("Ativo")
        campos["Data Cadastro"].insert(0, datetime.now().strftime("%d/%m/%Y"))
        for var in permissoes.values():
            var.set(False)

    def carregar_usuarios():
        tabela.delete(*tabela.get_children())
        if not os.path.exists(arquivo_usuarios):
            return
        with open(arquivo_usuarios, "r", encoding="utf-8") as f:
            try:
                usuarios = json.load(f)
            except json.JSONDecodeError:
                usuarios = []
        for usuario in usuarios:
            permissoes_texto = ", ".join([k for k,v in usuario.get("Permissoes", {}).items() if v])
            tabela.insert("", "end", values=(
                usuario.get("Usuario"),
                usuario.get("Nome Completo"),
                usuario.get("Função"),
                usuario.get("Status"),
                permissoes_texto
            ))

    def salvar_usuario():
        usuario = campos["Usuário"].get().strip()
        senha = campos["Senha"].get().strip()
        nome = campos["Nome Completo"].get().strip()
        email = campos["Email"].get().strip()
        telefone = campos["Telefone"].get().strip()
        departamento = campos["Departamento"].get().strip()
        funcao = campos["Função"].get().strip()
        status = campos["Status"].get().strip()
        data_cadastro = campos["Data Cadastro"].get().strip()
        observacoes = campos["Observações"].get().strip()

        if not usuario or not senha or not funcao:
            messagebox.showwarning("Campos obrigatórios", "Usuário, senha e função são obrigatórios.")
            return
        if email and not validar_email(email):
            messagebox.showerror("Email inválido", "Informe um email válido.")
            return

        # Carregar dados existentes
        usuarios = []
        if os.path.exists(arquivo_usuarios):
            with open(arquivo_usuarios, "r", encoding="utf-8") as f:
                try:
                    usuarios = json.load(f)
                except json.JSONDecodeError:
                    usuarios = []

        # Verificar se usuário já existe para editar
        usuario_existente = next((u for u in usuarios if u["Usuario"] == usuario), None)

        dados_usuario = {
            "Usuario": usuario,
            "Senha": senha,
            "Nome Completo": nome,
            "Email": email,
            "Telefone": telefone,
            "Departamento": departamento,
            "Função": funcao,
            "Status": status,
            "Data Cadastro": data_cadastro,
            "Observações": observacoes,
            "Permissoes": {k: v.get() for k, v in permissoes.items()}
        }

        if usuario_existente:
            # Atualizar dados existentes
            idx = usuarios.index(usuario_existente)
            usuarios[idx] = dados_usuario
            msg = f"Usuário '{usuario}' atualizado com sucesso."
        else:
            # Verificar usuário único
            if any(u["Usuario"] == usuario for u in usuarios):
                messagebox.showerror("Erro", "Usuário já cadastrado.")
                return
            usuarios.append(dados_usuario)
            msg = f"Usuário '{usuario}' cadastrado com sucesso."

        with open(arquivo_usuarios, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sucesso", msg)
        limpar_campos()
        carregar_usuarios()

    def excluir_usuario():
        usuario = campos["Usuário"].get().strip()
        if not usuario:
            messagebox.showwarning("Atenção", "Informe o usuário para excluir.")
            return
        if not os.path.exists(arquivo_usuarios):
            messagebox.showinfo("Info", "Nenhum usuário cadastrado.")
            return

        with open(arquivo_usuarios, "r", encoding="utf-8") as f:
            try:
                usuarios = json.load(f)
            except json.JSONDecodeError:
                usuarios = []

        usuarios_novos = [u for u in usuarios if u["Usuario"] != usuario]

        if len(usuarios_novos) == len(usuarios):
            messagebox.showinfo("Info", "Usuário não encontrado.")
            return

        with open(arquivo_usuarios, "w", encoding="utf-8") as f:
            json.dump(usuarios_novos, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sucesso", f"Usuário '{usuario}' excluído.")
        limpar_campos()
        carregar_usuarios()

    def selecionar_usuario():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione um usuário na tabela para carregar.")
            return
        item = tabela.item(selecionado[0])
        usuario_sel = item['values'][0]

        with open(arquivo_usuarios, "r", encoding="utf-8") as f:
            usuarios = json.load(f)

        usuario_dados = next((u for u in usuarios if u["Usuario"] == usuario_sel), None)
        if not usuario_dados:
            messagebox.showerror("Erro", "Dados do usuário não encontrados.")
            return

        # Preencher campos
        for k in campos.keys():
            valor = usuario_dados.get(k.replace(" ", ""), usuario_dados.get(k, ""))
            if k in ["Departamento", "Função", "Status"]:
                campos[k].set(usuario_dados.get(k, ""))
            else:
                campos[k].delete(0, tk.END)
                campos[k].insert(0, usuario_dados.get(k, ""))
        # Ajustar permissões
        for p_nome, var in permissoes.items():
            var.set(usuario_dados.get("Permissoes", {}).get(p_nome, False))

    def buscar_usuario():
        busca = campos["Usuário"].get().strip()
        if not busca:
            messagebox.showwarning("Busca", "Informe o nome de usuário para buscar.")
            return

        if not os.path.exists(arquivo_usuarios):
            messagebox.showinfo("Info", "Nenhum usuário cadastrado.")
            return

        with open(arquivo_usuarios, "r", encoding="utf-8") as f:
            usuarios = json.load(f)

        encontrados = [u for u in usuarios if busca.lower() in u["Usuario"].lower()]

        if not encontrados:
            messagebox.showinfo("Busca", f"Nenhum usuário encontrado para '{busca}'.")
            return

        tabela.delete(*tabela.get_children())
        for u in encontrados:
            permissoes_texto = ", ".join([k for k, v in u.get("Permissoes", {}).items() if v])
            tabela.insert("", "end", values=(u.get("Usuario"), u.get("Nome Completo"), u.get("Função"), u.get("Status"), permissoes_texto))

    # --- Frame Tabela de Usuários ---
    tabela_frame = ttk.LabelFrame(frame, text="👥 Usuários Cadastrados")
    tabela_frame.pack(fill="both", expand=True, pady=15)

    colunas = ("Usuário", "Nome Completo", "Função", "Status", "Permissões")

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, anchor="center", width=150)

    scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    tabela_frame.rowconfigure(0, weight=1)
    tabela_frame.columnconfigure(0, weight=1)

    # --- Frame Botões ---
    botoes_frame = ttk.Frame(frame)
    botoes_frame.pack(pady=10)

    btn_salvar = ttk.Button(botoes_frame, text="💾 Salvar", command=salvar_usuario)
    btn_salvar.grid(row=0, column=0, padx=10)

    btn_excluir = ttk.Button(botoes_frame, text="🗑️ Excluir", command=excluir_usuario)
    btn_excluir.grid(row=0, column=1, padx=10)

    btn_selecionar = ttk.Button(botoes_frame, text="📋 Selecionar", command=selecionar_usuario)
    btn_selecionar.grid(row=0, column=2, padx=10)

    btn_buscar = ttk.Button(botoes_frame, text="🔍 Buscar", command=buscar_usuario)
    btn_buscar.grid(row=0, column=3, padx=10)

    btn_limpar = ttk.Button(botoes_frame, text="🧹 Limpar Campos", command=limpar_campos)
    btn_limpar.grid(row=0, column=4, padx=10)

    # Carregar lista inicial de usuários
    carregar_usuarios()


if __name__ == "__main__":
    root = tk.Tk()
    tela_permissoes_acesso(root)
    root.mainloop()
