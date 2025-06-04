import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import os
import re
import sqlite3
import json # Adicionado para exportação JSON

# --- Funções de Banco de Dados (SQLite) para Fornecedores ---

DATABASE_NAME_FORNECEDORES = "fornecedores.db"

def connect_db_fornecedores():
    """Conecta ao banco de dados SQLite para fornecedores."""
    try:
        conn = sqlite3.connect(DATABASE_NAME_FORNECEDORES)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao banco de dados de fornecedores: {e}")
        return None

def create_table_fornecedores():
    """Cria a tabela 'fornecedores' se ela não existir."""
    conn = connect_db_fornecedores()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fornecedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_empresa TEXT NOT NULL,
                cnpj TEXT UNIQUE NOT NULL,
                telefone TEXT,
                email TEXT,
                responsavel TEXT,
                produto_fornecido TEXT,
                prazo_entrega TEXT,
                forma_pagamento TEXT,
                endereco TEXT,
                cidade TEXT,
                estado_uf TEXT,
                cep TEXT,
                numero_registro TEXT
            )
        ''')
        conn.commit()
        conn.close()

def inserir_fornecedor_db(fornecedor_data):
    """Insere um novo fornecedor no banco de dados."""
    conn = connect_db_fornecedores()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO fornecedores (nome_empresa, cnpj, telefone, email, responsavel,
                                          produto_fornecido, prazo_entrega, forma_pagamento,
                                          endereco, cidade, estado_uf, cep, numero_registro)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (fornecedor_data["Nome da Empresa"], fornecedor_data["CNPJ"], fornecedor_data["Telefone"],
                  fornecedor_data["Email"], fornecedor_data["Responsável"], fornecedor_data["Produto Fornecido"],
                  fornecedor_data["Prazo de Entrega"], fornecedor_data["Forma de Pagamento"],
                  fornecedor_data["Endereço"], fornecedor_data["Cidade"], fornecedor_data["Estado (UF)"],
                  fornecedor_data["CEP"], fornecedor_data["Número de Registro"]))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CNPJ já cadastrado. Por favor, verifique ou altere o CNPJ.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao inserir fornecedor: {e}")
            return False
        finally:
            conn.close()

def buscar_fornecedores_db(filtro=None):
    """Busca fornecedores no banco de dados, opcionalmente com filtro."""
    conn = connect_db_fornecedores()
    if conn:
        cursor = conn.cursor()
        query = "SELECT id, nome_empresa, cnpj, telefone, email, responsavel, produto_fornecido, prazo_entrega, forma_pagamento, endereco, cidade, estado_uf, cep, numero_registro FROM fornecedores"
        params = []
        if filtro:
            query += " WHERE lower(nome_empresa) LIKE ? OR cnpj LIKE ?"
            params = [f"%{filtro.lower()}%", f"%{filtro}%"]
        cursor.execute(query, params)
        fornecedores = cursor.fetchall()
        conn.close()
        return fornecedores
    return []

def atualizar_fornecedor_db(fornecedor_id, fornecedor_data):
    """Atualiza um fornecedor existente no banco de dados."""
    conn = connect_db_fornecedores()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE fornecedores SET
                    nome_empresa = ?, cnpj = ?, telefone = ?, email = ?, responsavel = ?,
                    produto_fornecido = ?, prazo_entrega = ?, forma_pagamento = ?,
                    endereco = ?, cidade = ?, estado_uf = ?, cep = ?, numero_registro = ?
                WHERE id = ?
            ''', (fornecedor_data["Nome da Empresa"], fornecedor_data["CNPJ"], fornecedor_data["Telefone"],
                  fornecedor_data["Email"], fornecedor_data["Responsável"], fornecedor_data["Produto Fornecido"],
                  fornecedor_data["Prazo de Entrega"], fornecedor_data["Forma de Pagamento"],
                  fornecedor_data["Endereço"], fornecedor_data["Cidade"], fornecedor_data["Estado (UF)"],
                  fornecedor_data["CEP"], fornecedor_data["Número de Registro"], fornecedor_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CNPJ já cadastrado para outro fornecedor. Por favor, verifique.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao atualizar fornecedor: {e}")
            return False
        finally:
            conn.close()

def excluir_fornecedor_db(fornecedor_id):
    """Exclui um fornecedor do banco de dados."""
    conn = connect_db_fornecedores()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM fornecedores WHERE id = ?", (fornecedor_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao excluir fornecedor: {e}")
            return False
        finally:
            conn.close()

# --- Funções de Exportação para Fornecedores ---

def exportar_fornecedores_json():
    """Exporta todos os fornecedores do banco de dados para um arquivo JSON."""
    fornecedores_raw = buscar_fornecedores_db()

    if not fornecedores_raw:
        messagebox.showinfo("Exportar JSON", "Não há fornecedores para exportar.")
        return

    fornecedores_list = []
    for fornecedor_row in fornecedores_raw:
        fornecedor_dict = dict(fornecedor_row)
        fornecedores_list.append(fornecedor_dict)

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Salvar Fornecedores como JSON"
    )

    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(fornecedores_list, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Exportar JSON", f"Fornecedores exportados com sucesso para:\n{file_path}")
        except IOError as e:
            messagebox.showerror("Erro de Exportação", f"Não foi possível salvar o arquivo:\n{e}")
    else:
        messagebox.showwarning("Exportar JSON", "Operação de exportação cancelada.")

# --- Funções da Interface Gráfica (Tkinter) para Fornecedores ---

def tela_fornecedores(janela):
    # Garante que a tabela seja criada ao iniciar a tela
    create_table_fornecedores()

    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Fornecedores 🏢", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    formas_pagamento = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Transferência", "Boleto", "Cheque", "Pix"]
    prazos_entrega = ["1 dia", "2 dias", "3 dias", "4 dias", "5 dias", "6 dias", "7 dias", "10 dias", "15 dias", "30 dias"] # Expandido
    estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
               "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

    # Mapeamento dos campos para as entradas Tkinter
    campos = {
        "Nome da Empresa": tk.Entry(campos_frame, width=30),
        "CNPJ": tk.Entry(campos_frame, width=30),
        "Telefone": tk.Entry(campos_frame, width=30),
        "Email": tk.Entry(campos_frame, width=30),
        "Responsável": tk.Entry(campos_frame, width=30),
        "Produto Fornecido": tk.Entry(campos_frame, width=30),
        "Prazo de Entrega": ttk.Combobox(campos_frame, width=28, values=prazos_entrega, state="readonly"),
        "Forma de Pagamento": ttk.Combobox(campos_frame, width=28, values=formas_pagamento, state="readonly"),
        "Endereço": tk.Entry(campos_frame, width=30),
        "Cidade": tk.Entry(campos_frame, width=30),
        "Estado (UF)": ttk.Combobox(campos_frame, width=28, values=estados, state="readonly"),
        "CEP": tk.Entry(campos_frame, width=30),
        "Número de Registro": tk.Entry(campos_frame, width=30),
    }

    # Variável Tkinter para armazenar o ID do fornecedor selecionado.
    fornecedor_selecionado_id = tk.StringVar()

    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12),
                 bg="#e6f2ff", fg="#003d66").grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    def validar_dados_fornecedor(dados_dict):
        """Valida os dados dos campos do formulário de fornecedor."""
        # Campos obrigatórios
        campos_obrigatorios = ["Nome da Empresa", "CNPJ", "Telefone", "Email", "Responsável",
                               "Produto Fornecido", "Prazo de Entrega", "Forma de Pagamento"]
        for campo in campos_obrigatorios:
            if not dados_dict.get(campo) or str(dados_dict.get(campo)).strip() == '':
                messagebox.showerror("Erro de Validação", f"O campo '{campo}' é obrigatório e não pode estar vazio.")
                return False

        # Valida CNPJ (14 dígitos numéricos, sem pontos ou traços para o DB)
        if not re.fullmatch(r"^\d{14}$", dados_dict["CNPJ"].replace('.', '').replace('/', '').replace('-', '')):
            messagebox.showerror("Erro", "CNPJ inválido. Deve conter 14 dígitos numéricos.")
            return False

        # Valida Telefone (10 ou 11 dígitos, sem caracteres especiais para o DB)
        if not re.fullmatch(r"^\d{10,11}$", dados_dict["Telefone"].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')):
            messagebox.showerror("Erro", "Telefone inválido. Deve conter 10 ou 11 dígitos (DDD + número).")
            return False

        # Valida Email
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", dados_dict["Email"]):
            messagebox.showerror("Erro", "E-mail inválido.")
            return False

        # Valida CEP (8 dígitos numéricos)
        if dados_dict["CEP"]:
            if not re.fullmatch(r"^\d{8}$", dados_dict["CEP"].replace('-', '')):
                messagebox.showerror("Erro", "CEP inválido. Deve conter 8 dígitos numéricos.")
                return False

        # Valida Comboboxes
        if dados_dict["Prazo de Entrega"] not in prazos_entrega:
            messagebox.showerror("Erro", "Selecione um prazo de entrega válido.")
            return False
        if dados_dict["Forma de Pagamento"] not in formas_pagamento:
            messagebox.showerror("Erro", "Selecione uma forma de pagamento válida.")
            return False
        if dados_dict["Estado (UF)"] and dados_dict["Estado (UF)"] not in estados:
            messagebox.showerror("Erro", "Selecione um estado (UF) válido.")
            return False

        return True

    def obter_dados_fornecedor():
        """Obtém os dados dos campos de entrada do formulário de fornecedor."""
        dados_dict = {}
        for rotulo, entrada in campos.items():
            # Remove formatação de CNPJ, Telefone e CEP antes de salvar no DB
            if rotulo == "CNPJ":
                dados_dict[rotulo] = entrada.get().strip().replace('.', '').replace('/', '').replace('-', '')
            elif rotulo == "Telefone":
                dados_dict[rotulo] = entrada.get().strip().replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
            elif rotulo == "CEP":
                dados_dict[rotulo] = entrada.get().strip().replace('-', '')
            else:
                dados_dict[rotulo] = entrada.get().strip()
        return dados_dict

    def limpar_formulario():
        """Limpa todos os campos do formulário de fornecedor e a seleção da Treeview."""
        for entrada in campos.values():
            if isinstance(entrada, ttk.Combobox):
                entrada.set("")
            else:
                entrada.delete(0, tk.END)
        fornecedor_selecionado_id.set("")
        for item in tabela.selection():
            tabela.selection_remove(item)
        # Reexibe o botão de salvar e esconde o de atualizar
        atualizar_btn.pack_forget()
        salvar_btn.pack(side="left", padx=10)

    def formatar_cnpj_telefone_cep(cnpj, telefone, cep):
        """Formata CNPJ, Telefone e CEP para exibição na Treeview."""
        cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}" if len(cnpj) == 14 else cnpj
        
        if len(telefone) == 10:
            telefone_formatado = f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
        elif len(telefone) == 11:
            telefone_formatado = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
        else:
            telefone_formatado = telefone

        cep_formatado = f"{cep[:5]}-{cep[5:]}" if len(cep) == 8 else cep
        return cnpj_formatado, telefone_formatado, cep_formatado

    def salvar_fornecedor_action():
        """Ação para salvar um novo fornecedor no banco de dados."""
        dados = obter_dados_fornecedor()

        if not validar_dados_fornecedor(dados):
            return

        if inserir_fornecedor_db(dados):
            messagebox.showinfo("Sucesso", "Fornecedor salvo com sucesso.")
            limpar_formulario()
            carregar_fornecedores()

    def carregar_fornecedores(filtro=None):
        """Carrega fornecedores do banco de dados para a tabela."""
        tabela.delete(*tabela.get_children())
        fornecedores_do_db = buscar_fornecedores_db(filtro)
        for fornecedor_row in fornecedores_do_db:
            # Formata CNPJ, Telefone e CEP para exibição na Treeview
            cnpj_formatado, telefone_formatado, cep_formatado = formatar_cnpj_telefone_cep(
                str(fornecedor_row["cnpj"]), str(fornecedor_row["telefone"]), str(fornecedor_row["cep"]))

            # Cria uma lista de valores com o ID e os dados formatados
            values_to_display = [
                fornecedor_row["id"],
                fornecedor_row["nome_empresa"],
                cnpj_formatado,
                telefone_formatado,
                fornecedor_row["email"],
                fornecedor_row["responsavel"],
                fornecedor_row["produto_fornecido"],
                fornecedor_row["prazo_entrega"],
                fornecedor_row["forma_pagamento"],
                fornecedor_row["endereco"],
                fornecedor_row["cidade"],
                fornecedor_row["estado_uf"],
                cep_formatado,
                fornecedor_row["numero_registro"]
            ]
            tabela.insert("", "end", values=values_to_display)

    def preencher_campos_edicao(event):
        """Preenche os campos do formulário com os dados do fornecedor selecionado na tabela."""
        selected_item = tabela.focus()
        if selected_item:
            values_from_treeview = tabela.item(selected_item, 'values')
            limpar_formulario() # Limpa para evitar duplicidade ou dados antigos

            fornecedor_selecionado_id.set(values_from_treeview[0]) # Armazena o ID

            # Preenche os campos, ignorando o ID (índice 0 da treeview)
            # Reverte a formatação de CNPJ, Telefone e CEP para o formato "cru" para os campos de entrada
            for i, (rotulo, entrada) in enumerate(campos.items()):
                # O índice 'i' para 'campos' corresponde aos campos do formulário.
                # Para acessar o valor correspondente de 'values_from_treeview', usamos 'i + 1'
                # porque 'values_from_treeview[0]' é o ID.
                if (i + 1) < len(values_from_treeview):
                    valor_do_campo = values_from_treeview[i + 1]
                    if isinstance(entrada, ttk.Combobox):
                        entrada.set(str(valor_do_campo))
                    else:
                        # Remove formatação de CNPJ, Telefone e CEP antes de inserir no campo
                        if rotulo == "CNPJ":
                            entrada.insert(0, str(valor_do_campo).replace('.', '').replace('/', '').replace('-', ''))
                        elif rotulo == "Telefone":
                            entrada.insert(0, str(valor_do_campo).replace('(', '').replace(')', '').replace('-', '').replace(' ', ''))
                        elif rotulo == "CEP":
                            entrada.insert(0, str(valor_do_campo).replace('-', ''))
                        else:
                            entrada.insert(0, str(valor_do_campo))
            
            # Esconde o botão de salvar e exibe o de atualizar
            salvar_btn.pack_forget()
            atualizar_btn.pack(side="left", padx=10)
        else:
            limpar_formulario() # Se nada estiver selecionado, limpa os campos

    def atualizar_fornecedor_action():
        """Atualiza os dados de um fornecedor selecionado no banco de dados."""
        fornecedor_id_db = fornecedor_selecionado_id.get()

        if not fornecedor_id_db:
            messagebox.showwarning("Atenção", "Selecione um fornecedor na tabela para atualizar.")
            return

        dados_atualizados = obter_dados_fornecedor()

        # Antes de validar, verifica se o CNPJ está sendo alterado para um CNPJ já existente
        # para outro fornecedor (se o CNPJ do fornecedor atual não for o mesmo que o do formulário).
        conn = connect_db_fornecedores()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM fornecedores WHERE cnpj = ? AND id != ?", (dados_atualizados["CNPJ"], fornecedor_id_db))
            if cursor.fetchone():
                messagebox.showerror("Erro", "CNPJ já cadastrado para outro fornecedor. Por favor, verifique.")
                conn.close()
                return False
            conn.close()

        if not validar_dados_fornecedor(dados_atualizados):
            return

        if messagebox.askyesno("Confirmar Alteração", "Tem certeza que deseja alterar este fornecedor?"):
            if atualizar_fornecedor_db(fornecedor_id_db, dados_atualizados):
                messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso.")
                limpar_formulario()
                carregar_fornecedores()
            # else: a mensagem de erro já é mostrada pela função de DB
        else:
            messagebox.showinfo("Cancelado", "Alteração cancelada.")

    def excluir_fornecedor_action():
        """Exclui um fornecedor selecionado do banco de dados."""
        fornecedor_id_db = fornecedor_selecionado_id.get()

        if not fornecedor_id_db:
            messagebox.showwarning("Atenção", "Selecione um fornecedor na tabela para excluir.")
            return

        selected_item_treeview = tabela.focus()
        if selected_item_treeview:
            fornecedor_nome = tabela.item(selected_item_treeview, 'values')[1] # Nome da Empresa está no índice 1
        else:
            fornecedor_nome = "Desconhecido"

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o fornecedor '{fornecedor_nome}' (ID: {fornecedor_id_db})? Esta ação é irreversível."):
            if excluir_fornecedor_db(fornecedor_id_db):
                messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso.")
                limpar_formulario()
                carregar_fornecedores()
            # else: a mensagem de erro já é mostrada pela função de DB
        else:
            messagebox.showinfo("Cancelado", "Exclusão cancelada.")

    # --- Layout dos Botões e Busca ---

    filtro_frame = tk.Frame(frame, bg="#e6f2ff")
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="🔍 Buscar por Nome ou CNPJ:", font=("Helvetica", 11), bg="#e6f2ff").pack(side="left", padx=5)
    entrada_filtro = tk.Entry(filtro_frame, width=40)
    entrada_filtro.pack(side="left")
    tk.Button(filtro_frame, text="Buscar", bg="#005580", fg="white", font=("Helvetica", 10, "bold"), command=lambda: carregar_fornecedores(entrada_filtro.get())).pack(side="left", padx=5)
    tk.Button(filtro_frame, text="🔄 Atualizar Lista Completa", bg="#ffcc00", fg="black", font=("Helvetica", 10, "bold"), command=lambda: carregar_fornecedores(None)).pack(side="left", padx=5)

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    salvar_btn = tk.Button(botoes_frame, text="💾 Salvar Fornecedor", bg="#339966", fg="white",
                            font=("Helvetica", 12, "bold"), width=20, command=salvar_fornecedor_action)
    salvar_btn.pack(side="left", padx=10)

    atualizar_btn = tk.Button(botoes_frame, text="✏️ Atualizar Fornecedor", bg="#ff9900", fg="white",
                               font=("Helvetica", 12, "bold"), width=20, command=atualizar_fornecedor_action)

    tk.Button(botoes_frame, text="🗑️ Excluir Fornecedor", bg="#cc0000", fg="white",
             font=("Helvetica", 12, "bold"), width=20, command=excluir_fornecedor_action).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📥 Exportar JSON", bg="#6A5ACD", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_fornecedores_json).pack(side="left", padx=10)

    # --- Tabela de Fornecedores (Treeview) ---

    tabela_frame = tk.LabelFrame(frame, text="📋 Fornecedores Cadastrados", bg="#e6f2ff",
                                  font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    # Definir colunas da Treeview, incluindo 'ID' que será escondido
    colunas = ["ID", "Nome da Empresa", "CNPJ", "Telefone", "Email", "Responsável",
               "Produto Fornecido", "Prazo de Entrega", "Forma de Pagamento",
               "Endereço", "Cidade", "Estado (UF)", "CEP", "Número de Registro"]

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    # Ajuste a largura conforme necessário
    tabela.column("Nome da Empresa", width=180)
    tabela.column("Email", width=180)
    tabela.column("Endereço", width=180)
    tabela.column("Produto Fornecido", width=150)
    tabela.column("Número de Registro", width=150)

    # Esconder a coluna ID
    tabela.column('ID', width=0, stretch=tk.NO)

    # Adiciona barras de rolagem
    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)

    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    tabela.bind("<<TreeviewSelect>>", preencher_campos_edicao)

    carregar_fornecedores()

# --- Exemplo de como iniciar a aplicação (se executado como script principal) ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestão de Fornecedores")
    root.geometry("1600x850") # Ajustado para acomodar mais campos e tabela
    root.config(bg="#e6f2ff")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Módulos", menu=file_menu)
    file_menu.add_command(label="Fornecedores", command=lambda: tela_fornecedores(root))
    file_menu.add_separator()
    file_menu.add_command(label="Sair", command=root.quit)

    tela_fornecedores(root)

    root.mainloop()