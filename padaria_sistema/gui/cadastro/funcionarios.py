import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import re
import sqlite3
import json # Adicionado para exportação JSON

# --- Funções de Banco de Dados (SQLite) para Funcionários ---

DATABASE_NAME_FUNCIONARIOS = "funcionarios.db"

def connect_db_funcionarios():
    """Conecta ao banco de dados SQLite para funcionários."""
    try:
        conn = sqlite3.connect(DATABASE_NAME_FUNCIONARIOS)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao banco de dados de funcionários: {e}")
        return None

def create_table_funcionarios():
    """Cria a tabela 'funcionarios' se ela não existir."""
    conn = connect_db_funcionarios()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                rg TEXT,
                cargo TEXT,
                salario REAL,
                data_admissao TEXT,
                telefone TEXT,
                email TEXT,
                endereco TEXT,
                cidade TEXT,
                estado_uf TEXT,
                estado_civil TEXT,
                escolaridade TEXT,
                numero_pis TEXT,
                horario_trabalho TEXT,
                banco TEXT
            )
        ''')
        conn.commit()
        conn.close()

def inserir_funcionario_db(funcionario_data):
    """Insere um novo funcionário no banco de dados."""
    conn = connect_db_funcionarios()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO funcionarios (nome, cpf, rg, cargo, salario, data_admissao,
                                          telefone, email, endereco, cidade, estado_uf,
                                          estado_civil, escolaridade, numero_pis,
                                          horario_trabalho, banco)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (funcionario_data["Nome"], funcionario_data["CPF"], funcionario_data["RG"],
                  funcionario_data["Cargo"], funcionario_data["Salário"], funcionario_data["Data de Admissão"],
                  funcionario_data["Telefone"], funcionario_data["Email"], funcionario_data["Endereço"],
                  funcionario_data["Cidade"], funcionario_data["Estado (UF)"], funcionario_data["Estado Civil"],
                  funcionario_data["Escolaridade"], funcionario_data["Nº PIS"],
                  funcionario_data["Horário de Trabalho"], funcionario_data["Banco"]))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF já cadastrado. Por favor, verifique ou altere o CPF.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao inserir funcionário: {e}")
            return False
        finally:
            conn.close()

def buscar_funcionarios_db(filtro=None):
    """Busca funcionários no banco de dados, opcionalmente com filtro."""
    conn = connect_db_funcionarios()
    if conn:
        cursor = conn.cursor()
        query = "SELECT id, nome, cpf, rg, cargo, salario, data_admissao, telefone, email, endereco, cidade, estado_uf, estado_civil, escolaridade, numero_pis, horario_trabalho, banco FROM funcionarios"
        params = []
        if filtro:
            query += " WHERE lower(nome) LIKE ? OR cpf LIKE ?"
            params = [f"%{filtro.lower()}%", f"%{filtro}%"]
        cursor.execute(query, params)
        funcionarios = cursor.fetchall()
        conn.close()
        return funcionarios
    return []

def atualizar_funcionario_db(funcionario_id, funcionario_data):
    """Atualiza um funcionário existente no banco de dados."""
    conn = connect_db_funcionarios()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE funcionarios SET
                    nome = ?, cpf = ?, rg = ?, cargo = ?, salario = ?, data_admissao = ?,
                    telefone = ?, email = ?, endereco = ?, cidade = ?, estado_uf = ?,
                    estado_civil = ?, escolaridade = ?, numero_pis = ?,
                    horario_trabalho = ?, banco = ?
                WHERE id = ?
            ''', (funcionario_data["Nome"], funcionario_data["CPF"], funcionario_data["RG"],
                  funcionario_data["Cargo"], funcionario_data["Salário"], funcionario_data["Data de Admissão"],
                  funcionario_data["Telefone"], funcionario_data["Email"], funcionario_data["Endereço"],
                  funcionario_data["Cidade"], funcionario_data["Estado (UF)"], funcionario_data["Estado Civil"],
                  funcionario_data["Escolaridade"], funcionario_data["Nº PIS"],
                  funcionario_data["Horário de Trabalho"], funcionario_data["Banco"], funcionario_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF já cadastrado para outro funcionário. Por favor, verifique.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao atualizar funcionário: {e}")
            return False
        finally:
            conn.close()

def excluir_funcionario_db(funcionario_id):
    """Exclui um funcionário do banco de dados."""
    conn = connect_db_funcionarios()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM funcionarios WHERE id = ?", (funcionario_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao excluir funcionário: {e}")
            return False
        finally:
            conn.close()

# --- Funções de Exportação para Funcionários ---

def exportar_funcionarios_json():
    """Exporta todos os funcionários do banco de dados para um arquivo JSON."""
    funcionarios_raw = buscar_funcionarios_db()

    if not funcionarios_raw:
        messagebox.showinfo("Exportar JSON", "Não há funcionários para exportar.")
        return

    funcionarios_list = []
    for funcionario_row in funcionarios_raw:
        funcionario_dict = dict(funcionario_row)
        funcionarios_list.append(funcionario_dict)

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Salvar Funcionários como JSON"
    )

    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(funcionarios_list, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Exportar JSON", f"Funcionários exportados com sucesso para:\n{file_path}")
        except IOError as e:
            messagebox.showerror("Erro de Exportação", f"Não foi possível salvar o arquivo:\n{e}")
    else:
        messagebox.showwarning("Exportar JSON", "Operação de exportação cancelada.")

# --- Funções da Interface Gráfica (Tkinter) para Funcionários ---

def tela_funcionarios(janela):
    # Garante que a tabela seja criada ao iniciar a tela
    create_table_funcionarios()

    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Funcionários 👨‍💼", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    # Dicionário para armazenar as referências aos campos de entrada
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

    # Variável Tkinter para armazenar o ID do funcionário selecionado.
    funcionario_selecionado_id = tk.StringVar()

    for i, (rotulo, entrada) in enumerate(campos_info.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")
        entradas[rotulo] = entrada # Armazena a referência para a entrada

    def validar_dados_funcionario(dados_dict):
        """Valida os dados dos campos do formulário de funcionário."""
        # Campos obrigatórios
        campos_obrigatorios = ["Nome", "CPF", "Data de Admissão", "Telefone", "Email", "Salário", "Cargo"]
        for campo in campos_obrigatorios:
            if not dados_dict.get(campo) or str(dados_dict.get(campo)).strip() == '':
                messagebox.showerror("Erro de Validação", f"O campo '{campo}' é obrigatório e não pode estar vazio.")
                return False

        # Valida CPF (11 dígitos numéricos, sem pontos ou traços para o DB)
        if not re.fullmatch(r"^\d{11}$", dados_dict["CPF"].replace('.', '').replace('-', '')):
            messagebox.showerror("Erro", "CPF deve conter 11 dígitos numéricos.")
            return False

        # Valida Telefone (10 ou 11 dígitos, sem caracteres especiais para o DB)
        if not re.fullmatch(r"^\d{10,11}$", dados_dict["Telefone"].replace('(', '').replace(')', '').replace('-', '').replace(' ', '')):
            messagebox.showerror("Erro", "Telefone deve conter 10 ou 11 dígitos (DDD + número).")
            return False

        # Valida Email
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", dados_dict["Email"]):
            messagebox.showerror("Erro", "E-mail inválido.")
            return False
        
        # Valida Salário
        try:
            salario = float(dados_dict["Salário"].replace(',', '.')) # Permite vírgula como decimal
            if salario < 0:
                messagebox.showerror("Erro", "Salário não pode ser negativo.")
                return False
        except ValueError:
            messagebox.showerror("Erro", "Salário deve ser um número válido.")
            return False

        # Valida Data de Admissão
        try:
            datetime.strptime(dados_dict["Data de Admissão"], "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Data de Admissão deve estar no formato dd/mm/aaaa.")
            return False

        # Valida Cargo
        if dados_dict["Cargo"] not in cargos:
            messagebox.showerror("Erro", "Selecione um cargo válido.")
            return False
        
        # Valida Estado (UF)
        if dados_dict["Estado (UF)"] and dados_dict["Estado (UF)"] not in estados:
            messagebox.showerror("Erro", "Selecione um estado (UF) válido.")
            return False
        
        # Valida Estado Civil
        if dados_dict["Estado Civil"] and dados_dict["Estado Civil"] not in estados_civis:
            messagebox.showerror("Erro", "Selecione um estado civil válido.")
            return False
        
        # Valida Escolaridade
        if dados_dict["Escolaridade"] and dados_dict["Escolaridade"] not in escolaridades:
            messagebox.showerror("Erro", "Selecione uma escolaridade válida.")
            return False

        return True

    def obter_dados_funcionario():
        """Obtém os dados dos campos de entrada do formulário de funcionário."""
        dados_dict = {}
        for rotulo, entrada in campos_info.items():
            if isinstance(entrada, DateEntry):
                dados_dict[rotulo] = entrada.get_date().strftime("%d/%m/%Y")
            else:
                # Remove formatação de CPF e Telefone antes de salvar no DB
                if rotulo == "CPF":
                    dados_dict[rotulo] = entrada.get().strip().replace('.', '').replace('-', '')
                elif rotulo == "Telefone":
                    dados_dict[rotulo] = entrada.get().strip().replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
                else:
                    dados_dict[rotulo] = entrada.get().strip()
        return dados_dict

    def limpar_formulario():
        """Limpa todos os campos do formulário de funcionário e a seleção da Treeview."""
        for entrada in entradas.values():
            if isinstance(entrada, ttk.Combobox):
                entrada.set("")
            elif isinstance(entrada, DateEntry):
                entrada.set_date(datetime.today())
            else:
                entrada.delete(0, tk.END)
        funcionario_selecionado_id.set("")
        for item in tabela.selection():
            tabela.selection_remove(item)
        # Reexibe o botão de salvar e esconde o de atualizar
        atualizar_btn.pack_forget()
        salvar_btn.pack(side="left", padx=10)

    def formatar_cpf_telefone(cpf, telefone):
        """Formata CPF e Telefone para exibição na Treeview."""
        cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf
        if len(telefone) == 10:
            telefone_formatado = f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
        elif len(telefone) == 11:
            telefone_formatado = f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
        else:
            telefone_formatado = telefone
        return cpf_formatado, telefone_formatado

    def salvar_funcionario_action():
        """Ação para salvar um novo funcionário no banco de dados."""
        dados = obter_dados_funcionario()

        if not validar_dados_funcionario(dados):
            return

        if inserir_funcionario_db(dados):
            messagebox.showinfo("Sucesso", "Funcionário salvo com sucesso.")
            limpar_formulario()
            carregar_funcionarios()

    def carregar_funcionarios(filtro=None):
        """Carrega funcionários do banco de dados para a tabela."""
        tabela.delete(*tabela.get_children())
        funcionarios_do_db = buscar_funcionarios_db(filtro)
        for funcionario_row in funcionarios_do_db:
            # Formata CPF e Telefone para exibição na Treeview
            cpf_formatado, telefone_formatado = formatar_cpf_telefone(
                str(funcionario_row["cpf"]), str(funcionario_row["telefone"]))

            # Cria uma lista de valores com o ID e os dados formatados
            values_to_display = [
                funcionario_row["id"],
                funcionario_row["nome"],
                cpf_formatado,
                funcionario_row["rg"],
                funcionario_row["cargo"],
                funcionario_row["salario"],
                funcionario_row["data_admissao"],
                telefone_formatado,
                funcionario_row["email"],
                funcionario_row["endereco"],
                funcionario_row["cidade"],
                funcionario_row["estado_uf"],
                funcionario_row["estado_civil"],
                funcionario_row["escolaridade"],
                funcionario_row["numero_pis"],
                funcionario_row["horario_trabalho"],
                funcionario_row["banco"]
            ]
            tabela.insert("", "end", values=values_to_display)

    def preencher_campos_edicao(event):
        """Preenche os campos do formulário com os dados do funcionário selecionado na tabela."""
        selected_item = tabela.focus()
        if selected_item:
            values_from_treeview = tabela.item(selected_item, 'values')
            limpar_formulario() # Limpa para evitar duplicidade ou dados antigos

            funcionario_selecionado_id.set(values_from_treeview[0]) # Armazena o ID

            # Preenche os campos, ignorando o ID (índice 0 da treeview)
            # Reverte a formatação de CPF e Telefone para o formato "cru" para os campos de entrada
            for i, (rotulo, entrada) in enumerate(campos_info.items()):
                # O índice 'i' para 'campos_info' corresponde aos campos do formulário.
                # Para acessar o valor correspondente de 'values_from_treeview', usamos 'i + 1'
                # porque 'values_from_treeview[0]' é o ID.
                if (i + 1) < len(values_from_treeview):
                    valor_do_campo = values_from_treeview[i + 1]
                    if isinstance(entrada, DateEntry):
                        try:
                            data_obj = datetime.strptime(str(valor_do_campo), "%d/%m/%Y").date()
                            entrada.set_date(data_obj)
                        except (ValueError, TypeError):
                            entrada.set_date(datetime.today())
                    elif isinstance(entrada, ttk.Combobox):
                        entrada.set(str(valor_do_campo))
                    else:
                        # Remove formatação de CPF e Telefone antes de inserir no campo
                        if rotulo == "CPF":
                            entrada.insert(0, str(valor_do_campo).replace('.', '').replace('-', ''))
                        elif rotulo == "Telefone":
                            entrada.insert(0, str(valor_do_campo).replace('(', '').replace(')', '').replace('-', '').replace(' ', ''))
                        else:
                            entrada.insert(0, str(valor_do_campo))
            
            # Esconde o botão de salvar e exibe o de atualizar
            salvar_btn.pack_forget()
            atualizar_btn.pack(side="left", padx=10)
        else:
            limpar_formulario() # Se nada estiver selecionado, limpa os campos


    def atualizar_funcionario_action():
        """Atualiza os dados de um funcionário selecionado no banco de dados."""
        funcionario_id_db = funcionario_selecionado_id.get()

        if not funcionario_id_db:
            messagebox.showwarning("Atenção", "Selecione um funcionário na tabela para atualizar.")
            return

        dados_atualizados = obter_dados_funcionario()

        # Antes de validar, verifica se o CPF está sendo alterado para um CPF já existente
        # para outro funcionário (se o CPF do funcionário atual não for o mesmo que o do formulário).
        conn = connect_db_funcionarios()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM funcionarios WHERE cpf = ? AND id != ?", (dados_atualizados["CPF"], funcionario_id_db))
            if cursor.fetchone():
                messagebox.showerror("Erro", "CPF já cadastrado para outro funcionário. Por favor, verifique.")
                conn.close()
                return False
            conn.close()

        if not validar_dados_funcionario(dados_atualizados):
            return

        if messagebox.askyesno("Confirmar Alteração", "Tem certeza que deseja alterar este funcionário?"):
            if atualizar_funcionario_db(funcionario_id_db, dados_atualizados):
                messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso.")
                limpar_formulario()
                carregar_funcionarios()
            # else: a mensagem de erro já é mostrada pela função de DB
        else:
            messagebox.showinfo("Cancelado", "Alteração cancelada.")

    def excluir_funcionario_action():
        """Exclui um funcionário selecionado do banco de dados."""
        funcionario_id_db = funcionario_selecionado_id.get()

        if not funcionario_id_db:
            messagebox.showwarning("Atenção", "Selecione um funcionário na tabela para excluir.")
            return

        selected_item_treeview = tabela.focus()
        if selected_item_treeview:
            funcionario_nome = tabela.item(selected_item_treeview, 'values')[1] # Nome está no índice 1
        else:
            funcionario_nome = "Desconhecido"

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o funcionário '{funcionario_nome}' (ID: {funcionario_id_db})? Esta ação é irreversível."):
            if excluir_funcionario_db(funcionario_id_db):
                messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso.")
                limpar_formulario()
                carregar_funcionarios()
            # else: a mensagem de erro já é mostrada pela função de DB
        else:
            messagebox.showinfo("Cancelado", "Exclusão cancelada.")

    # --- Layout dos Botões e Busca ---

    filtro_frame = tk.Frame(frame, bg="#e6f2ff")
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="🔍 Buscar por Nome ou CPF:", font=("Helvetica", 11), bg="#e6f2ff").pack(side="left", padx=5)
    entrada_filtro = tk.Entry(filtro_frame, width=40)
    entrada_filtro.pack(side="left")
    tk.Button(filtro_frame, text="Buscar", bg="#005580", fg="white", font=("Helvetica", 10, "bold"), command=lambda: carregar_funcionarios(entrada_filtro.get())).pack(side="left", padx=5)
    tk.Button(filtro_frame, text="🔄 Atualizar Lista Completa", bg="#ffcc00", fg="black", font=("Helvetica", 10, "bold"), command=lambda: carregar_funcionarios(None)).pack(side="left", padx=5)

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    salvar_btn = tk.Button(botoes_frame, text="💾 Salvar Funcionário", bg="#339966", fg="white",
                            font=("Helvetica", 12, "bold"), width=20, command=salvar_funcionario_action)
    salvar_btn.pack(side="left", padx=10)

    atualizar_btn = tk.Button(botoes_frame, text="✏️ Atualizar Funcionário", bg="#ff9900", fg="white",
                               font=("Helvetica", 12, "bold"), width=20, command=atualizar_funcionario_action)

    tk.Button(botoes_frame, text="🗑️ Excluir Funcionário", bg="#cc0000", fg="white",
             font=("Helvetica", 12, "bold"), width=20, command=excluir_funcionario_action).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📥 Exportar JSON", bg="#6A5ACD", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_funcionarios_json).pack(side="left", padx=10)

    # --- Tabela de Funcionários (Treeview) ---

    tabela_frame = tk.LabelFrame(frame, text="📋 Funcionários Cadastrados", bg="#e6f2ff",
                                  font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    # Definir colunas da Treeview, incluindo 'ID' que será escondido
    colunas = ["ID", "Nome", "CPF", "RG", "Cargo", "Salário", "Data de Admissão",
               "Telefone", "Email", "Endereço", "Cidade", "Estado (UF)",
               "Estado Civil", "Escolaridade", "Nº PIS", "Horário de Trabalho", "Banco"]

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    # Ajuste a largura conforme necessário
    tabela.column("Nome", width=150)
    tabela.column("Email", width=180)
    tabela.column("Endereço", width=180)
    tabela.column("Horário de Trabalho", width=150)

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

    carregar_funcionarios()

# --- Exemplo de como iniciar a aplicação (se executado como script principal) ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestão de Funcionários")
    root.geometry("1500x900") # Ajustado para acomodar mais campos e tabela
    root.config(bg="#e6f2ff")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Módulos", menu=file_menu)
    file_menu.add_command(label="Funcionários", command=lambda: tela_funcionarios(root))
    file_menu.add_separator()
    file_menu.add_command(label="Sair", command=root.quit)

    tela_funcionarios(root)

    root.mainloop()