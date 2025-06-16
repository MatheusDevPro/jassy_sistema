import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import re
import sqlite3
import json # Adicionado para exportação JSON

# --- Funções de Banco de Dados (SQLite) para Produtos ---

DATABASE_NAME_PRODUTOS = "produtos.db"

def connect_db_produtos():
    """Conecta ao banco de dados SQLite para produtos."""
    try:
        conn = sqlite3.connect(DATABASE_NAME_PRODUTOS)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao banco de dados de produtos: {e}")
        return None

def create_table_produtos():
    """Cria a tabela 'produtos' se ela não existir."""
    conn = connect_db_produtos()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                codigo TEXT UNIQUE NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                data_validade TEXT,
                fornecedor TEXT,
                descricao TEXT,
                categoria TEXT,
                unidade_medida TEXT,
                localizacao_estoque TEXT,
                marca TEXT,
                garantia_meses INTEGER,
                peso_kg REAL
            )
        ''')
        conn.commit()
        conn.close()

def inserir_produto_db(produto_data):
    """Insere um novo produto no banco de dados."""
    conn = connect_db_produtos()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO produtos (nome, codigo, preco, quantidade, data_validade,
                                      fornecedor, descricao, categoria, unidade_medida,
                                      localizacao_estoque, marca, garantia_meses, peso_kg)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (produto_data["Nome"], produto_data["Código"], produto_data["Preço"],
                  produto_data["Quantidade"], produto_data["Data de Validade"],
                  produto_data["Fornecedor"], produto_data["Descrição"],
                  produto_data["Categoria"], produto_data["Unidade de Medida"],
                  produto_data["Localização no Estoque"], produto_data["Marca"],
                  produto_data["Garantia (meses)"], produto_data["Peso (kg)"]))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Código de produto já cadastrado. Por favor, verifique ou altere o código.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao inserir produto: {e}")
            return False
        finally:
            conn.close()

def buscar_produtos_db(filtro=None):
    """Busca produtos no banco de dados, opcionalmente com filtro."""
    conn = connect_db_produtos()
    if conn:
        cursor = conn.cursor()
        query = "SELECT id, nome, codigo, preco, quantidade, data_validade, fornecedor, descricao, categoria, unidade_medida, localizacao_estoque, marca, garantia_meses, peso_kg FROM produtos"
        params = []
        if filtro:
            query += " WHERE lower(nome) LIKE ? OR lower(codigo) LIKE ?"
            params = [f"%{filtro.lower()}%", f"%{filtro.lower()}%"]
        cursor.execute(query, params)
        produtos = cursor.fetchall()
        conn.close()
        return produtos
    return []

def atualizar_produto_db(produto_id, produto_data):
    """Atualiza um produto existente no banco de dados."""
    conn = connect_db_produtos()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                UPDATE produtos SET
                    nome = ?, codigo = ?, preco = ?, quantidade = ?, data_validade = ?,
                    fornecedor = ?, descricao = ?, categoria = ?, unidade_medida = ?,
                    localizacao_estoque = ?, marca = ?, garantia_meses = ?, peso_kg = ?
                WHERE id = ?
            ''', (produto_data["Nome"], produto_data["Código"], produto_data["Preço"],
                  produto_data["Quantidade"], produto_data["Data de Validade"],
                  produto_data["Fornecedor"], produto_data["Descrição"],
                  produto_data["Categoria"], produto_data["Unidade de Medida"],
                  produto_data["Localização no Estoque"], produto_data["Marca"],
                  produto_data["Garantia (meses)"], produto_data["Peso (kg)"], produto_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Código de produto já cadastrado para outro produto. Por favor, verifique.")
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao atualizar produto: {e}")
            return False
        finally:
            conn.close()

def excluir_produto_db(produto_id):
    """Exclui um produto do banco de dados."""
    conn = connect_db_produtos()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Erro ao excluir produto: {e}")
            return False
        finally:
            conn.close()

# --- Funções de Exportação para Produtos ---

def exportar_produtos_json():
    """Exporta todos os produtos do banco de dados para um arquivo JSON."""
    produtos_raw = buscar_produtos_db()

    if not produtos_raw:
        messagebox.showinfo("Exportar JSON", "Não há produtos para exportar.")
        return

    produtos_list = []
    for produto_row in produtos_raw:
        produto_dict = dict(produto_row)
        produtos_list.append(produto_dict)

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Salvar Produtos como JSON"
    )

    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(produtos_list, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Exportar JSON", f"Produtos exportados com sucesso para:\n{file_path}")
        except IOError as e:
            messagebox.showerror("Erro de Exportação", f"Não foi possível salvar o arquivo:\n{e}")
    else:
        messagebox.showwarning("Exportar JSON", "Operação de exportação cancelada.")


# --- Funções da Interface Gráfica (Tkinter) para Produtos ---

def tela_produtos(janela):
    # Garante que a tabela seja criada ao iniciar a tela
    create_table_produtos()

    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Cadastro de Produtos 📦", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    categorias = ["Alimentos", "Bebidas", "Higiene", "Limpeza", "Eletrônicos", "Roupas", "Outros", "Ferramentas", "Móveis", "Brinquedos", "Saúde", "Beleza", "Esportes", "Automotivo", "Jardinagem", "Pet Shop", "Livros", "Papeleria", "Informática", "Construção Civil", "Construção e Reforma", "Saúde e Bem-Estar", "Moda e Acessórios", "Casa e Decoração"]
    unidades = ["UN", "LT", "KG", "MT", "CX", "PCT", "BAG", "GAL", "ML", "G", "CM", "MM"]
    localização_no_Estoque = ["Prateleira 1", "Prateleira 2", "Prateleira 3", "Prateleira 4",
                             "Prateleira 5", "Prateleira 6", "Prateleira",]

    # Mapeamento dos campos para as entradas Tkinter
    campos = {
        "Nome": tk.Entry(campos_frame, width=30),
        "Código": tk.Entry(campos_frame, width=30),
        "Preço": tk.Entry(campos_frame, width=30),
        "Quantidade": tk.Entry(campos_frame, width=30),
        "Data de Validade": DateEntry(campos_frame, width=27, background='darkblue',
                                      foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy'),
        "Fornecedor": tk.Entry(campos_frame, width=30),
        "Descrição": tk.Entry(campos_frame, width=30),
        "Categoria": ttk.Combobox(campos_frame, values=categorias, width=28, state="readonly"),
        "Unidade de Medida": ttk.Combobox(campos_frame, values=unidades, width=28, state="readonly"),
        "Localização no Estoque": ttk.Combobox(campos_frame, value=localização_no_Estoque, width=28, state="readonly"),
        "Marca": tk.Entry(campos_frame, width=30),
        "Garantia (meses)": tk.Entry(campos_frame, width=30),
        "Peso (kg)": tk.Entry(campos_frame, width=30),
    }

    # Variável Tkinter para armazenar o ID do produto selecionado.
    produto_selecionado_id = tk.StringVar()

    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    def validar_dados_produto(dados_dict):
        """Valida os dados dos campos do formulário de produto."""
        # Campos obrigatórios
        campos_obrigatorios = ["Nome", "Código", "Preço", "Quantidade", "Data de Validade", "Categoria", "Unidade de Medida"]
        for campo in campos_obrigatorios:
            if not dados_dict.get(campo) or str(dados_dict.get(campo)).strip() == '':
                messagebox.showerror("Erro de Validação", f"O campo '{campo}' é obrigatório e não pode estar vazio.")
                return False

        try:
            # Convert to string before replacing, then to float
            preco_str = str(dados_dict["Preço"])
            preco = float(preco_str.replace(',', '.')) 
            if preco < 0:
                messagebox.showerror("Erro", "Preço não pode ser negativo.")
                return False
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número válido.")
            return False

        try:
            quantidade = int(dados_dict["Quantidade"])
            if quantidade < 0:
                messagebox.showerror("Erro", "Quantidade não pode ser negativa.")
                return False
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro.")
            return False

        # Valida a data de validade
        try:
            datetime.strptime(dados_dict["Data de Validade"], "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Data de Validade deve estar no formato dd/mm/aaaa.")
            return False

        if dados_dict["Garantia (meses)"]:
            try:
                garantia = int(dados_dict["Garantia (meses)"])
                if garantia < 0:
                    messagebox.showerror("Erro", "Garantia (meses) não pode ser negativa.")
                    return False
            except ValueError:
                messagebox.showerror("Erro", "Garantia (meses) deve ser um número inteiro, se preenchido.")
                return False

        if dados_dict["Peso (kg)"]:
            try:
                # Convert to string before replacing, then to float
                peso_str = str(dados_dict["Peso (kg)"])
                peso = float(peso_str.replace(',', '.')) 
                if peso < 0:
                    messagebox.showerror("Erro", "Peso (kg) não pode ser negativo.")
                    return False
            except ValueError:
                messagebox.showerror("Erro", "Peso (kg) deve ser um número, se preenchido.")
                return False

        if dados_dict["Categoria"] not in categorias:
            messagebox.showerror("Erro", "Selecione uma categoria válida.")
            return False
        if dados_dict["Unidade de Medida"] not in unidades:
            messagebox.showerror("Erro", "Selecione uma unidade de medida válida.")
            return False

        return True

    def obter_dados_produto():
        """Obtém os dados dos campos de entrada do formulário de produto."""
        dados_dict = {}
        for rotulo, entrada in campos.items():
            if isinstance(entrada, DateEntry):
                dados_dict[rotulo] = entrada.get_date().strftime("%d/%m/%Y")
            else:
                dados_dict[rotulo] = entrada.get().strip()
        return dados_dict

    def limpar_formulario():
        """Limpa todos os campos do formulário de produto e a seleção da Treeview."""
        for entrada in campos.values():
            if isinstance(entrada, ttk.Combobox):
                entrada.set("")
            elif isinstance(entrada, DateEntry):
                entrada.set_date(datetime.today())
            else:
                entrada.delete(0, tk.END)
        produto_selecionado_id.set("")
        for item in tabela.selection():
            tabela.selection_remove(item)
        # Reexibe o botão de salvar e esconde o de atualizar
        atualizar_btn.pack_forget()
        salvar_btn.pack(side="left", padx=10)

    def salvar_produto_action():
        """Ação para salvar um novo produto no banco de dados."""
        dados = obter_dados_produto()

        if not validar_dados_produto(dados):
            return

        # Perform the conversion for database insertion after validation
        # This prevents the float conversion from happening twice on the same value
        try:
            dados["Preço"] = float(str(dados["Preço"]).replace(',', '.'))
            if dados["Peso (kg)"]:
                dados["Peso (kg)"] = float(str(dados["Peso (kg)"]).replace(',', '.'))
            else:
                dados["Peso (kg)"] = None # Handle empty string for optional float field
            if dados["Garantia (meses)"]:
                dados["Garantia (meses)"] = int(dados["Garantia (meses)"])
            else:
                dados["Garantia (meses)"] = None # Handle empty string for optional int field

        except ValueError as e:
            messagebox.showerror("Erro de Conversão", f"Erro ao converter dados numéricos: {e}")
            return


        if inserir_produto_db(dados):
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso.")
            limpar_formulario()
            carregar_produtos()

    def carregar_produtos(filtro=None):
        """Carrega produtos do banco de dados para a tabela."""
        tabela.delete(*tabela.get_children())
        produtos_do_db = buscar_produtos_db(filtro)
        for produto_row in produtos_do_db:
            values_to_display = (produto_row[0],) + tuple(produto_row[1:])
            tabela.insert("", "end", values=values_to_display)

    def preencher_campos_edicao(event):
        """Preenche os campos do formulário com os dados do produto selecionado na tabela."""
        selected_item = tabela.focus()
        if selected_item:
            values_from_treeview = tabela.item(selected_item, 'values')
            limpar_formulario() # Limpa para evitar duplicidade ou dados antigos

            produto_selecionado_id.set(values_from_treeview[0]) # Armazena o ID

            # Preenche os campos, ignorando o ID (índice 0 da treeview)
            for i, (rotulo, entrada) in enumerate(campos.items()):
                # O índice 'i' para 'campos' corresponde aos campos do formulário.
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
                        entrada.insert(0, str(valor_do_campo))
            
            # Esconde o botão de salvar e exibe o de atualizar
            salvar_btn.pack_forget()
            atualizar_btn.pack(side="left", padx=10)
        else:
            limpar_formulario() # Se nada estiver selecionado, limpa os campos

    def atualizar_produto_action():
        """Atualiza os dados de um produto selecionado no banco de dados."""
        produto_id_db = produto_selecionado_id.get()

        if not produto_id_db:
            messagebox.showwarning("Atenção", "Selecione um produto na tabela para atualizar.")
            return

        dados_atualizados = obter_dados_produto()

        # Antes de validar, verifica se o Código está sendo alterado para um Código já existente
        # para outro produto (se o Código do produto atual não for o mesmo que o do formulário).
        conn = connect_db_produtos()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM produtos WHERE codigo = ? AND id != ?", (dados_atualizados["Código"], produto_id_db))
            if cursor.fetchone():
                messagebox.showerror("Erro", "Código de produto já cadastrado para outro produto. Por favor, verifique.")
                conn.close()
                return False
            conn.close()


        if not validar_dados_produto(dados_atualizados):
            return

        # Perform the conversion for database update after validation
        try:
            dados_atualizados["Preço"] = float(str(dados_atualizados["Preço"]).replace(',', '.'))
            if dados_atualizados["Peso (kg)"]:
                dados_atualizados["Peso (kg)"] = float(str(dados_atualizados["Peso (kg)"]).replace(',', '.'))
            else:
                dados_atualizados["Peso (kg)"] = None
            if dados_atualizados["Garantia (meses)"]:
                dados_atualizados["Garantia (meses)"] = int(dados_atualizados["Garantia (meses)"])
            else:
                dados_atualizados["Garantia (meses)"] = None

        except ValueError as e:
            messagebox.showerror("Erro de Conversão", f"Erro ao converter dados numéricos para atualização: {e}")
            return


        if messagebox.askyesno("Confirmar Alteração", "Tem certeza que deseja alterar este produto?"):
            if atualizar_produto_db(produto_id_db, dados_atualizados):
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
                limpar_formulario()
                carregar_produtos()
            # else: a mensagem de erro já é mostrada pela função de DB
        else:
            messagebox.showinfo("Cancelado", "Alteração cancelada.")

    def excluir_produto_action():
        """Exclui um produto selecionado do banco de dados."""
        produto_id_db = produto_selecionado_id.get()

        if not produto_id_db:
            messagebox.showwarning("Atenção", "Selecione um produto na tabela para excluir.")
            return

        selected_item_treeview = tabela.focus()
        if selected_item_treeview:
            produto_nome = tabela.item(selected_item_treeview, 'values')[1] # Nome está no índice 1
        else:
            produto_nome = "Desconhecido"

        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o produto '{produto_nome}' (ID: {produto_id_db})? Esta ação é irreversível."):
            if excluir_produto_db(produto_id_db):
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso.")
                limpar_formulario()
                carregar_produtos()
            # else: a mensagem de erro já é mostrada pela função de DB
        else:
            messagebox.showinfo("Cancelado", "Exclusão cancelada.")

    # --- Layout dos Botões e Busca ---

    botoes_frame = tk.Frame(frame, bg="#e6f2ff")
    botoes_frame.pack(pady=10)

    salvar_btn = tk.Button(botoes_frame, text="💾 Salvar Produto", bg="#339966", fg="white",
                            font=("Helvetica", 12, "bold"), width=20, command=salvar_produto_action)
    salvar_btn.pack(side="left", padx=10)

    atualizar_btn = tk.Button(botoes_frame, text="✏️ Atualizar Produto", bg="#ff9900", fg="white",
                               font=("Helvetica", 12, "bold"), width=20, command=atualizar_produto_action)
    # Inicialmente, o botão de atualizar está escondido
    # atualizar_btn.pack(side="left", padx=10) # Será empacotado/desempacotado conforme a seleção

    tk.Button(botoes_frame, text="🗑️ Excluir Produto", bg="#cc0000", fg="white",
             font=("Helvetica", 12, "bold"), width=20, command=excluir_produto_action).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📥 Exportar JSON", bg="#6A5ACD", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=exportar_produtos_json).pack(side="left", padx=10)


    # Campo de busca
    busca_frame = tk.Frame(frame, bg="#e6f2ff")
    busca_frame.pack(pady=5)

    tk.Label(busca_frame, text="🔍 Buscar por Nome ou Código:", font=("Helvetica", 12),
             bg="#e6f2ff", fg="#003d66").pack(side="left", padx=5)

    entrada_busca = tk.Entry(busca_frame, width=40)
    entrada_busca.pack(side="left", padx=5)

    def buscar_produto():
        texto = entrada_busca.get().strip()
        carregar_produtos(filtro=texto)

    tk.Button(busca_frame, text="Buscar", bg="#005580", fg="white",
              font=("Helvetica", 10, "bold"), command=buscar_produto).pack(side="left", padx=5)

    tk.Button(busca_frame, text="🔄 Atualizar Lista Completa", bg="#ffcc00", fg="black",
              font=("Helvetica", 10, "bold"), command=lambda: carregar_produtos(None)).pack(side="left", padx=5)

    # --- Tabela de Produtos (Treeview) ---

    tabela_frame = tk.LabelFrame(frame, text="📋 Produtos Cadastrados", bg="#e6f2ff",
                                  font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    # Definir colunas da Treeview, incluindo 'ID' que será escondido
    colunas = ["ID", "Nome", "Código", "Preço", "Quantidade", "Data de Validade",
               "Fornecedor", "Descrição", "Categoria", "Unidade de Medida",
               "Localização no Estoque", "Marca", "Garantia (meses)", "Peso (kg)"]

    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    # Ajuste a largura conforme necessário
    tabela.column("Nome", width=150)
    tabela.column("Descrição", width=180)
    tabela.column("Localização no Estoque", width=150)
    tabela.column("Fornecedor", width=150)

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

    carregar_produtos() # Carrega os produtos ao iniciar a tela

# --- Exemplo de como iniciar a aplicação (se executado como script principal) ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestão de Produtos")
    root.geometry("1400x850") # Ajustado para acomodar mais campos
    root.config(bg="#e6f2ff")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Módulos", menu=file_menu)
    file_menu.add_command(label="Produtos", command=lambda: tela_produtos(root))
    file_menu.add_separator()
    file_menu.add_command(label="Sair", command=root.quit)

    tela_produtos(root)

    root.mainloop()