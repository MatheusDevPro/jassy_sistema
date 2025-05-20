import tkinter as tk
from tkinter import ttk, messagebox

def tela_gestao_pessoal(janela):
    janela.title("👥 Gestão de Pessoal - Jassy Gestão")
    janela.configure(bg="#f8f8ff")

    # Limpa conteúdo anterior
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
          widget.destroy()

    # Frame principal
    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    # --- Título ---
    titulo = tk.Label(frame, text="👥 Gestão de Pessoal", font=("Arial", 18, "bold"), fg="#1E90FF", bg="#f8f8ff")
    titulo.pack(pady=10)

    # --- Dados do funcionário ---
    form_frame = tk.LabelFrame(frame, text="Dados do Funcionário", font=("Arial", 12, "bold"), fg="#333", bg="#f8f8ff", padx=10, pady=10)
    form_frame.pack(fill=tk.X, padx=5, pady=10)

    # Campos
    labels = [
        "ID", "Nome Completo", "CPF", "Data de Nascimento", "Telefone", 
        "Email", "Endereço", "Cargo", "Departamento", "Data Admissão", "Status"
    ]

    # Variáveis para armazenar os dados da tela
    var_id = tk.StringVar()
    var_nome = tk.StringVar()
    var_cpf = tk.StringVar()
    var_data_nasc = tk.StringVar()
    var_telefone = tk.StringVar()
    var_email = tk.StringVar()
    var_endereco = tk.StringVar()
    var_cargo = tk.StringVar()
    var_departamento = tk.StringVar()
    var_data_admissao = tk.StringVar()
    var_status = tk.StringVar(value="Ativo")

    # Labels e Entradas na grid
    # Linha 0
    tk.Label(form_frame, text="ID:", bg="#f8f8ff").grid(row=0, column=0, sticky="e", padx=5, pady=3)
    entry_id = tk.Entry(form_frame, textvariable=var_id, state="readonly", width=10)
    entry_id.grid(row=0, column=1, sticky="w", padx=5, pady=3)

    tk.Label(form_frame, text="Nome Completo:", bg="#f8f8ff").grid(row=0, column=2, sticky="e", padx=5, pady=3)
    entry_nome = tk.Entry(form_frame, textvariable=var_nome, width=30)
    entry_nome.grid(row=0, column=3, sticky="w", padx=5, pady=3)

    # Linha 1
    tk.Label(form_frame, text="CPF:", bg="#f8f8ff").grid(row=1, column=0, sticky="e", padx=5, pady=3)
    entry_cpf = tk.Entry(form_frame, textvariable=var_cpf, width=20)
    entry_cpf.grid(row=1, column=1, sticky="w", padx=5, pady=3)

    tk.Label(form_frame, text="Data de Nascimento:", bg="#f8f8ff").grid(row=1, column=2, sticky="e", padx=5, pady=3)
    entry_data_nasc = tk.Entry(form_frame, textvariable=var_data_nasc, width=20)
    entry_data_nasc.grid(row=1, column=3, sticky="w", padx=5, pady=3)

    # Linha 2
    tk.Label(form_frame, text="Telefone:", bg="#f8f8ff").grid(row=2, column=0, sticky="e", padx=5, pady=3)
    entry_telefone = tk.Entry(form_frame, textvariable=var_telefone, width=20)
    entry_telefone.grid(row=2, column=1, sticky="w", padx=5, pady=3)

    tk.Label(form_frame, text="Email:", bg="#f8f8ff").grid(row=2, column=2, sticky="e", padx=5, pady=3)
    entry_email = tk.Entry(form_frame, textvariable=var_email, width=30)
    entry_email.grid(row=2, column=3, sticky="w", padx=5, pady=3)

    # Linha 3
    tk.Label(form_frame, text="Endereço:", bg="#f8f8ff").grid(row=3, column=0, sticky="e", padx=5, pady=3)
    entry_endereco = tk.Entry(form_frame, textvariable=var_endereco, width=50)
    entry_endereco.grid(row=3, column=1, columnspan=3, sticky="w", padx=5, pady=3)

    # Linha 4
    tk.Label(form_frame, text="Cargo:", bg="#f8f8ff").grid(row=4, column=0, sticky="e", padx=5, pady=3)
    combo_cargo = ttk.Combobox(form_frame, textvariable=var_cargo, width=20, state="readonly")
    combo_cargo['values'] = ("Analista", "Desenvolvedor", "Gerente", "Assistente", "Estagiário", "Supervisor")
    combo_cargo.grid(row=4, column=1, sticky="w", padx=5, pady=3)

    tk.Label(form_frame, text="Departamento:", bg="#f8f8ff").grid(row=4, column=2, sticky="e", padx=5, pady=3)
    combo_departamento = ttk.Combobox(form_frame, textvariable=var_departamento, width=20, state="readonly")
    combo_departamento['values'] = ("TI", "Financeiro", "RH", "Marketing", "Vendas", "Produção", "Suporte")
    combo_departamento.grid(row=4, column=3, sticky="w", padx=5, pady=3)

    # Linha 5
    tk.Label(form_frame, text="Data de Admissão:", bg="#f8f8ff").grid(row=5, column=0, sticky="e", padx=5, pady=3)
    entry_data_admissao = tk.Entry(form_frame, textvariable=var_data_admissao, width=20)
    entry_data_admissao.grid(row=5, column=1, sticky="w", padx=5, pady=3)

    tk.Label(form_frame, text="Status:", bg="#f8f8ff").grid(row=5, column=2, sticky="e", padx=5, pady=3)
    combo_status = ttk.Combobox(form_frame, textvariable=var_status, width=20, state="readonly")
    combo_status['values'] = ("Ativo", "Inativo", "Afastado")
    combo_status.grid(row=5, column=3, sticky="w", padx=5, pady=3)

    # --- Botões de ação ---
    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(fill=tk.X, pady=10)

    def limpar_campos():
        var_id.set("")
        var_nome.set("")
        var_cpf.set("")
        var_data_nasc.set("")
        var_telefone.set("")
        var_email.set("")
        var_endereco.set("")
        var_cargo.set("")
        var_departamento.set("")
        var_data_admissao.set("")
        var_status.set("Ativo")
        entry_nome.focus()

    def validar_campos():
        if not var_nome.get().strip():
            messagebox.showwarning("Validação", "O campo Nome Completo é obrigatório.")
            return False
        if not var_cpf.get().strip():
            messagebox.showwarning("Validação", "O campo CPF é obrigatório.")
            return False
        # Pode adicionar outras validações aqui (email, datas, etc.)
        return True

    # Dados simulados (lista de dicionários)
    dados_funcionarios = []

    # Treeview para mostrar lista de funcionários
    tree_frame = tk.Frame(frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)

    colunas = ("ID", "Nome", "CPF", "Cargo", "Departamento", "Status")
    tree = ttk.Treeview(tree_frame, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100 if col == "ID" else 150)

    tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    # Scrollbar vertical
    scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Funções para manipular os dados simulados e a Treeview

    def carregar_dados_na_tabela():
        # Limpa a tabela
        for i in tree.get_children():
            tree.delete(i)
        # Adiciona os dados atuais
        for func in dados_funcionarios:
            tree.insert("", "end", values=(func["id"], func["nome"], func["cpf"], func["cargo"], func["departamento"], func["status"]))

    def salvar_funcionario():
        if not validar_campos():
            return
        if var_id.get() == "":
            # Inserir novo funcionário
            novo_id = len(dados_funcionarios) + 1
            dados_funcionarios.append({
                "id": novo_id,
                "nome": var_nome.get(),
                "cpf": var_cpf.get(),
                "data_nasc": var_data_nasc.get(),
                "telefone": var_telefone.get(),
                "email": var_email.get(),
                "endereco": var_endereco.get(),
                "cargo": var_cargo.get(),
                "departamento": var_departamento.get(),
                "data_admissao": var_data_admissao.get(),
                "status": var_status.get()
            })
            messagebox.showinfo("Sucesso", f"Funcionário {var_nome.get()} cadastrado com sucesso!")
        else:
            # Editar funcionário existente
            for func in dados_funcionarios:
                if func["id"] == int(var_id.get()):
                    func["nome"] = var_nome.get()
                    func["cpf"] = var_cpf.get()
                    func["data_nasc"] = var_data_nasc.get()
                    func["telefone"] = var_telefone.get()
                    func["email"] = var_email.get()
                    func["endereco"] = var_endereco.get()
                    func["cargo"] = var_cargo.get()
                    func["departamento"] = var_departamento.get()
                    func["data_admissao"] = var_data_admissao.get()
                    func["status"] = var_status.get()
                    messagebox.showinfo("Sucesso", f"Funcionário {var_nome.get()} atualizado com sucesso!")
                    break
        limpar_campos()
        carregar_dados_na_tabela()

    def excluir_funcionario():
        if var_id.get() == "":
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir.")
            return
        resposta = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o funcionário {var_nome.get()}?")
        if resposta:
            global dados_funcionarios
            dados_funcionarios = [f for f in dados_funcionarios if f["id"] != int(var_id.get())]
            messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso.")
            limpar_campos()
            carregar_dados_na_tabela()

    def selecionar_funcionario(event):
        selecionado = tree.focus()
        if selecionado:
            valores = tree.item(selecionado, 'values')
            if valores:
                var_id.set(valores[0])
                # Buscar dados completos no array pelo id
                for func in dados_funcionarios:
                    if func["id"] == int(valores[0]):
                        var_nome.set(func["nome"])
                        var_cpf.set(func["cpf"])
                        var_data_nasc.set(func["data_nasc"])
                        var_telefone.set(func["telefone"])
                        var_email.set(func["email"])
                        var_endereco.set(func["endereco"])
                        var_cargo.set(func["cargo"])
                        var_departamento.set(func["departamento"])
                        var_data_admissao.set(func["data_admissao"])
                        var_status.set(func["status"])
                        break

    btn_salvar = tk.Button(botoes_frame, text="💾 Salvar", bg="#1E90FF", fg="white", font=("Arial", 10, "bold"), command=salvar_funcionario)
    btn_salvar.pack(side=tk.LEFT, padx=5)

    btn_excluir = tk.Button(botoes_frame, text="🗑️ Excluir", bg="#FF4500", fg="white", font=("Arial", 10, "bold"), command=excluir_funcionario)
    btn_excluir.pack(side=tk.LEFT, padx=5)

    btn_limpar = tk.Button(botoes_frame, text="🧹 Limpar", bg="#696969", fg="white", font=("Arial", 10, "bold"), command=limpar_campos)
    btn_limpar.pack(side=tk.LEFT, padx=5)

    # Evento ao clicar na tabela
    tree.bind("<<TreeviewSelect>>", selecionar_funcionario)

    # Inicializa tabela vazia
    carregar_dados_na_tabela()

    # Foca no campo nome para começar
    entry_nome.focus()
