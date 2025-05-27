import tkinter as tk
from tkinter import messagebox, ttk, filedialog # Importa filedialog
from tkcalendar import DateEntry
from datetime import datetime
import re
import sqlite3
import json

# --- Funções de Banco de Dados (SQLite) ---

DATABASE_NAME = "clientes.db"

def connect_db():
    """Conecta ao banco de dados SQLite."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        # Permite acessar colunas por nome para debug, mas usaremos índices.
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao banco de dados: {e}")
        return None

def create_table():
    """Cria a tabela 'clientes' se ela não existir."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                data_nascimento TEXT,
                sexo TEXT,
                rg TEXT,
                data_cadastro TEXT,
                cidade TEXT,
                estado TEXT,
                cep TEXT,
                bairro TEXT,
                numero TEXT,
                complemento TEXT,
                data_validade TEXT,
                email TEXT,
                telefone TEXT,
                endereco TEXT
            )
        ''')
        conn.commit()
        conn.close()

def inserir_cliente_db(cliente_data):
    """Insere um novo cliente no banco de dados."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO clientes (nome, cpf, data_nascimento, sexo, rg, data_cadastro,
                                      cidade, estado, cep, bairro, numero, complemento,
                                      data_validade, email, telefone, endereco)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cliente_data["Nome"], cliente_data["CPF"], cliente_data["Data de Nascimento"],
                  cliente_data["Sexo"], cliente_data["RG"], cliente_data["Data de Cadastro"],
                  cliente_data["Cidade"], cliente_data["Estado"], cliente_data["CEP"],
                  cliente_data["Bairro"], cliente_data["Número"], cliente_data["Complemento"],
                  cliente_data["Data de Validade"], cliente_data["E-mail"],
                  cliente_data["Telefone"], cliente_data["Endereço"]))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF já cadastrado. Por favor, verifique ou altere o CPF.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao inserir cliente: {e}")
            return False
        finally:
            conn.close()

def buscar_clientes_db(filtro=None):
    """Busca clientes no banco de dados, opcionalmente com filtro."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        # Seleciona TODAS as colunas, incluindo o ID
        query = "SELECT id, nome, cpf, data_nascimento, sexo, rg, data_cadastro, cidade, estado, cep, bairro, numero, complemento, data_validade, email, telefone, endereco FROM clientes"
        params = []
        if filtro:
            query += " WHERE lower(nome) LIKE ? OR cpf LIKE ?"
            params = [f"%{filtro.lower()}%", f"%{filtro}%"]
        cursor.execute(query, params)
        clientes = cursor.fetchall()
        conn.close()
        return clientes
    return []

def atualizar_cliente_db(cliente_id, cliente_data):
    """Atualiza um cliente existente no banco de dados."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE clientes SET
                    nome = ?, cpf = ?, data_nascimento = ?, sexo = ?, rg = ?,
                    data_cadastro = ?, cidade = ?, estado = ?, cep = ?,
                    bairro = ?, numero = ?, complemento = ?, data_validade = ?,
                    email = ?, telefone = ?, endereco = ?
                WHERE id = ?
            ''', (cliente_data["Nome"], cliente_data["CPF"], cliente_data["Data de Nascimento"],
                  cliente_data["Sexo"], cliente_data["RG"], cliente_data["Data de Cadastro"],
                  cliente_data["Cidade"], cliente_data["Estado"], cliente_data["CEP"],
                  cliente_data["Bairro"], cliente_data["Número"], cliente_data["Complemento"],
                  cliente_data["Data de Validade"], cliente_data["E-mail"],
                  cliente_data["Telefone"], cliente_data["Endereço"], cliente_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF já cadastrado para outro cliente. Por favor, verifique.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao atualizar cliente: {e}")
            return False
        finally:
            conn.close()

def excluir_cliente_db(cliente_id):
    """Exclui um cliente do banco de dados."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao excluir cliente: {e}")
            return False
        finally:
            conn.close()

# --- Funções de Exportação ---

def exportar_clientes_json():
    """Exporta todos os clientes do banco de dados para um arquivo JSON."""
    clientes_raw = buscar_clientes_db() # Busca todos os clientes
    
    if not clientes_raw:
        messagebox.showinfo("Exportar JSON", "Não há clientes para exportar.")
        return

    # Converte os objetos Row do SQLite para dicionários Python
    clientes_list = []
    for cliente_row in clientes_raw:
        cliente_dict = dict(cliente_row) # Converte sqlite3.Row para dicionário
        clientes_list.append(cliente_dict)

    # Abre a caixa de diálogo para salvar o arquivo
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Salvar Clientes como JSON"
    )

    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(clientes_list, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Exportar JSON", f"Clientes exportados com sucesso para:\n{file_path}")
        except IOError as e:
            messagebox.showerror("Erro de Exportação", f"Não foi possível salvar o arquivo:\n{e}")
    else:
        messagebox.showwarning("Exportar JSON", "Operação de exportação cancelada.")


# --- Funções da Interface Gráfica (Tkinter) ---

def tela_clientes(janela):
    # Garante que a tabela seja criada ao iniciar a tela
    create_table()

    # Limpa widgets existentes na janela principal, exceto menus
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Clientes 👤", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    sexos = ["Masculino", "Feminino", "Binário", "Não-binário", "Lésbica", "Gay", "Bissexual", "Outro"]
    estados_brasileiros = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
        "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
        "SP", "SE", "TO"
    ]

    # Dicionário para armazenar as referências aos campos de entrada
    # e um campo oculto para armazenar o ID do cliente selecionado para alteração
    campos = {
        "Nome": tk.Entry(campos_frame, width=30),
        "CPF": tk.Entry(campos_frame, width=30),
        "Data de Nascimento": DateEntry(campos_frame, width=27, date_pattern='dd/mm/yyyy'),
        "Sexo": ttk.Combobox(campos_frame, values=sexos, width=28, state="readonly"),
        "RG": tk.Entry(campos_frame, width=30),
        "Data de Cadastro": DateEntry(campos_frame, width=27, date_pattern='dd/mm/yyyy'),
        "Cidade": tk.Entry(campos_frame, width=30),
        "Estado": ttk.Combobox(campos_frame, values=estados_brasileiros, width=28, state="readonly"), # Mantido como Combobox
        "CEP": tk.Entry(campos_frame, width=30),
        "Bairro": tk.Entry(campos_frame, width=30),
        "Número": tk.Entry(campos_frame, width=30),
        "Complemento": tk.Entry(campos_frame, width=30),
        "Data de Validade": DateEntry(campos_frame, width=27, date_pattern='dd/mm/yyyy'),
        "E-mail": tk.Entry(campos_frame, width=30),
        "Telefone": tk.Entry(campos_frame, width=30),
        "Endereço": tk.Entry(campos_frame, width=30)
    }

    # Adiciona uma variável Tkinter para armazenar o ID do cliente selecionado.
    cliente_selecionado_id = tk.StringVar()

    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    def validar_dados(dados_dict):
        """Valida os dados dos campos do formulário."""
        # Campos obrigatórios
        campos_obrigatorios = ["Nome", "CPF", "Data de Nascimento", "Sexo", "E-mail", "Telefone", "Estado"] # Estado é obrigatório
        for campo in campos_obrigatorios:
            if not dados_dict.get(campo) or dados_dict.get(campo).strip() == '':
                messagebox.showerror("Erro de Validação", f"O campo '{campo}' é obrigatório e não pode estar vazio.")
                return False

        if not re.fullmatch(r"\d{11}", dados_dict["CPF"]):
            messagebox.showerror("Erro", "CPF deve conter 11 dígitos numéricos.")
            return False
        if dados_dict["CEP"] and not re.fullmatch(r"\d{8}", dados_dict["CEP"]):
            messagebox.showerror("Erro", "CEP deve conter 8 dígitos, se preenchido.")
            return False
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", dados_dict["E-mail"]):
            messagebox.showerror("Erro", "E-mail inválido.")
            return False
        # Permite 10 ou 11 dígitos para telefone (com DDD)
        if not re.fullmatch(r"^\d{10,11}$", dados_dict["Telefone"]):
            messagebox.showerror("Erro", "Telefone deve conter 10 ou 11 dígitos (incluindo DDD).")
            return False
        if dados_dict["Número"] and not dados_dict["Número"].isdigit():
            messagebox.showerror("Erro", "Número deve ser numérico, se preenchido.")
            return False
        if dados_dict["Sexo"] not in sexos:
            messagebox.showerror("Erro", "Selecione um sexo válido.")
            return False
        if dados_dict["Estado"] not in estados_brasileiros: # Valida o estado
            messagebox.showerror("Erro", "Selecione um estado válido.")
            return False
        if dados_dict["RG"] and len(dados_dict["RG"]) < 5:
            messagebox.showerror("Erro", "RG deve conter ao menos 5 caracteres, se preenchido.")
            return False
        return True

    def obter_dados():
        """Obtém os dados dos campos de entrada."""
        return {
            rotulo: entrada.get().strip() if not isinstance(entrada, DateEntry)
            else entrada.get_date().strftime("%d/%m/%Y")
            for rotulo, entrada in campos.items()
        }

    def limpar_campos():
        """Limpa todos os campos do formulário e a seleção da Treeview."""
        for entrada in campos.values():
            if isinstance(entrada, ttk.Combobox):
                entrada.set("")
            elif isinstance(entrada, DateEntry):
                entrada.set_date(datetime.today()) # Reseta para a data atual
            else:
                entrada.delete(0, tk.END)
        # Limpa o ID armazenado para evitar alterações acidentais
        cliente_selecionado_id.set("")
        # Limpa qualquer seleção na Treeview
        for item in tabela.selection():
            tabela.selection_remove(item)


    def salvar_cliente():
        """Salva um novo cliente no banco de dados."""
        dados = obter_dados()

        if not validar_dados(dados):
            return # Sai se a validação falhar

        if inserir_cliente_db(dados):
            messagebox.showinfo("Sucesso", "Cliente salvo com sucesso.")
            limpar_campos()
            carregar_clientes() # Recarrega a tabela após salvar

    def carregar_clientes(filtro=None):
        """Carrega clientes do banco de dados para a tabela."""
        tabela.delete(*tabela.get_children()) # Limpa a tabela atual
        clientes_do_db = buscar_clientes_db(filtro)
        for cliente_row in clientes_do_db:
            # cliente_row é um objeto sqlite3.Row, que pode ser acessado por índice ou nome.
            # Convertemos para tupla para garantir a compatibilidade com values.
            # O ID (cliente_row[0]) é o primeiro elemento.
            values_to_display = (cliente_row[0],) + tuple(cliente_row[1:])
            tabela.insert("", "end", values=values_to_display)

    def preencher_campos_edicao(event):
        """Preenche os campos do formulário com os dados do cliente selecionado na tabela."""
        selected_item = tabela.focus() # Obtém o item focado (selecionado)
        if selected_item:
            # Pega os valores visíveis da linha selecionada.
            # O primeiro valor (índice 0) é o ID do banco de dados.
            values_from_treeview = tabela.item(selected_item, 'values')

            # Limpa os campos antes de preencher para evitar acumulação de texto
            limpar_campos()

            # Armazena o ID do cliente selecionado na variável Tkinter
            cliente_selecionado_id.set(values_from_treeview[0])

            # Percorre os campos do dicionário 'campos' e preenche.
            # O dicionário 'campos' não inclui o 'ID', então começamos do índice 1 de 'values_from_treeview'.
            for i, (rotulo, entrada) in enumerate(campos.items()):
                # O índice 'i' para 'campos' corresponde aos campos do formulário (Nome, CPF, etc.).
                # Para acessar o valor correspondente de 'values_from_treeview', usamos 'i + 1'
                # porque 'values_from_treeview[0]' é o ID.
                if (i + 1) < len(values_from_treeview):
                    valor_do_campo = values_from_treeview[i + 1]
                    if isinstance(entrada, DateEntry):
                        try:
                            # Garante que a data_obj seja um objeto date
                            data_obj = datetime.strptime(str(valor_do_campo), "%d/%m/%Y").date()
                            entrada.set_date(data_obj)
                        except (ValueError, TypeError): # Lida com datas inválidas ou nulas
                            entrada.set_date(datetime.today()) # Fallback se a data for inválida
                    elif isinstance(entrada, ttk.Combobox):
                        entrada.set(str(valor_do_campo))
                    else:
                        entrada.insert(0, str(valor_do_campo)) # Insere o valor como string
        else:
            # Se nada estiver selecionado ou a seleção for removida
            limpar_campos()


    def alterar_cliente():
        """Atualiza os dados de um cliente selecionado no banco de dados."""
        # Obtém o ID do cliente que está armazenado na variável cliente_selecionado_id
        cliente_id_db = cliente_selecionado_id.get()

        if not cliente_id_db: # Se a variável estiver vazia, significa que nenhum cliente foi selecionado
            messagebox.showwarning("Atenção", "Selecione um cliente na tabela para alterar.")
            return

        dados_atualizados = obter_dados()

        # Antes de validar, verifica se o CPF está sendo alterado para um CPF já existente
        # para outro cliente (se o CPF do cliente atual não for o mesmo que o do formulário).
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM clientes WHERE cpf = ? AND id != ?", (dados_atualizados["CPF"], cliente_id_db))
            if cursor.fetchone():
                messagebox.showerror("Erro", "CPF já cadastrado para outro cliente. Por favor, verifique.")
                conn.close()
                return False # Impede a alteração
            conn.close()

        if not validar_dados(dados_atualizados):
            return # Sai se a validação falhar

        if messagebox.askyesno("Confirmar Alteração", "Tem certeza que deseja alterar este cliente?"):
            if atualizar_cliente_db(cliente_id_db, dados_atualizados):
                messagebox.showinfo("Sucesso", "Cliente alterado com sucesso.")
                limpar_campos()
                carregar_clientes() # Recarrega a tabela para mostrar as alterações
            # else: a mensagem de erro já é mostrada pela função de DB
        else:
            messagebox.showinfo("Cancelado", "Alteração cancelada.")


    def excluir_cliente():
        """Exclui um cliente selecionado do banco de dados."""
        # Obtém o ID do cliente que está armazenado na variável cliente_selecionado_id
        cliente_id_db = cliente_selecionado_id.get()

        if not cliente_id_db: # Se a variável estiver vazia, significa que nenhum cliente foi selecionado
            messagebox.showwarning("Atenção", "Selecione um cliente na tabela para excluir.")
            return

        # Pega o nome do cliente para a mensagem de confirmação diretamente da Treeview,
        # usando o item atualmente focado, já que o ID foi validado acima.
        selected_item_treeview = tabela.focus()
        if selected_item_treeview:
            cliente_nome = tabela.item(selected_item_treeview, 'values')[1] # Nome está no índice 1
        else:
            cliente_nome = "Desconhecido" # Fallback caso haja um erro de seleção (improvável aqui)

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o cliente '{cliente_nome}' (ID: {cliente_id_db})? Esta ação é irreversível."):
            if excluir_cliente_db(cliente_id_db):
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")
                limpar_campos()
                carregar_clientes()
            # else: a mensagem de erro já é mostrada pela função de DB
        else:
            messagebox.showinfo("Cancelado", "Exclusão cancelada.")


    # --- Layout dos Botões e Busca ---

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="💾 Salvar Cliente", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=salvar_cliente).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="✔️ Validar Dados", bg="#007acc", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=lambda: validar_dados(obter_dados())).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="✏️ Alterar Cliente", bg="#ff9900", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=alterar_cliente).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="🗑️ Excluir Cliente", bg="#cc0000", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=excluir_cliente).pack(side="left", padx=10)

    # Novo botão para exportar JSON
    tk.Button(botoes_frame, text="📥 Exportar JSON", bg="#6A5ACD", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_clientes_json).pack(side="left", padx=10)


    # Campo de busca
    busca_frame = tk.Frame(frame, bg="#e6f2ff")
    busca_frame.pack(pady=5)

    tk.Label(busca_frame, text="🔍 Buscar por Nome ou CPF:", font=("Helvetica", 12),
             bg="#e6f2ff", fg="#003d66").pack(side="left", padx=5)

    entrada_busca = tk.Entry(busca_frame, width=40)
    entrada_busca.pack(side="left", padx=5)

    def buscar_cliente():
        texto = entrada_busca.get().strip()
        carregar_clientes(filtro=texto)

    tk.Button(busca_frame, text="Buscar", bg="#005580", fg="white",
              font=("Helvetica", 10, "bold"), command=buscar_cliente).pack(side="left", padx=5)

    tk.Button(busca_frame, text="🔄 Atualizar Lista Completa", bg="#ffcc00", fg="black",
              font=("Helvetica", 10, "bold"), command=lambda: carregar_clientes(None)).pack(side="left", padx=5)


    # --- Tabela de Clientes (Treeview) ---

    tabela_frame = tk.LabelFrame(frame, text="📋 Clientes Cadastrados", bg="#e6f2ff",
                                 font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    # Definir colunas da Treeview, incluindo 'ID' que será escondido
    colunas = ["ID", "Nome", "CPF", "Data de Nascimento", "Sexo", "RG", "Data de Cadastro",
               "Cidade", "Estado", "CEP", "Bairro", "Número", "Complemento",
               "Data de Validade", "E-mail", "Telefone", "Endereço"]

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    # Configura o cabeçalho e largura para cada coluna
    for col in colunas:
        tabela.heading(col, text=col)
        # Ajuste a largura conforme necessário, Nome e Endereço podem ser maiores
        tabela.column(col, width=120, anchor="center")

    # Colunas com largura ajustada para melhor visualização (opcional)
    tabela.column("Nome", width=180)
    tabela.column("E-mail", width=180)
    tabela.column("Endereço", width=200)

    # Esconder a coluna ID
    tabela.column('ID', width=0, stretch=tk.NO) # Torna a coluna invisível e não redimensionável

    # Adiciona barras de rolagem
    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    # Configura o redimensionamento da tabela com o frame pai
    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    # Evento para carregar dados do cliente na tela ao selecionar na tabela
    tabela.bind("<<TreeviewSelect>>", preencher_campos_edicao)

    carregar_clientes() # Carrega os clientes ao iniciar a tela

# --- Exemplo de como iniciar a aplicação ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestão de Clientes")
    root.geometry("1200x800")
    root.config(bg="#e6f2ff") # Cor de fundo da janela principal

    # Configuração do menu principal (opcional, para navegação entre telas)
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Módulos", menu=file_menu)
    file_menu.add_command(label="Clientes", command=lambda: tela_clientes(root))
    file_menu.add_separator()
    file_menu.add_command(label="Sair", command=root.quit)

    tela_clientes(root) # Carrega a tela de clientes ao iniciar

    root.mainloop()