import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
import sqlite3 # Certifique-se de que sqlite3 esteja importado

# Supondo que as funções de banco de dados (connect_db_produtos, buscar_produtos_db)
# estejam definidas e acessíveis no mesmo arquivo ou importadas de um módulo.
# Para este exemplo, vou incluí-las novamente para clareza, mas no seu código real,
# elas devem estar no topo do seu arquivo principal.

# --- Funções de Banco de Dados (SQLite) para Produtos (repetidas para auto-suficiência deste bloco) ---

DATABASE_NAME_PRODUTOS = "produtos.db"

def connect_db_produtos():
    """Conecta ao banco de dados SQLite para produtos."""
    try:
        conn = sqlite3.connect(DATABASE_NAME_PRODUTOS)
        conn.row_factory = sqlite3.Row # Permite acesso às colunas por nome
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao banco de dados de produtos: {e}")
        return None

def buscar_produtos_db(filtro=None):
    """Busca produtos no banco de dados, opcionalmente com filtro."""
    conn = connect_db_produtos()
    if conn:
        cursor = conn.cursor()
        query = "SELECT id, nome, codigo, preco, quantidade, data_validade, fornecedor, descricao, categoria, unidade_medida, localizacao_estoque, marca, garantia_meses, peso_kg FROM produtos"
        params = []
        if filtro:
            # Busca por nome ou código (case-insensitive)
            query += " WHERE lower(nome) LIKE ? OR lower(codigo) LIKE ?"
            params = [f"%{filtro.lower()}%", f"%{filtro.lower()}%"]
        cursor.execute(query, params)
        produtos = cursor.fetchall()
        conn.close()
        return produtos
    return []

# --- Função de Exportação CSV (agora integrada ao banco de dados) ---

def exportar_csv_db():
    """Exporta todos os produtos do banco de dados para um arquivo CSV."""
    produtos_raw = buscar_produtos_db() # Busca todos os produtos do DB

    if not produtos_raw:
        messagebox.showinfo("Exportar CSV", "Não há produtos para exportar.")
        return

    # Cabeçalhos do CSV (correspondentes às colunas que serão exibidas, sem o ID)
    colunas_csv = ["Nome", "Código", "Preço", "Quantidade", "Data de Validade",
                   "Fornecedor", "Descrição", "Categoria", "Unidade de Medida",
                   "Localização no Estoque", "Marca", "Garantia (meses)", "Peso (kg)"]

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
        title="Salvar Estoque como CSV"
    )

    if file_path:
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(colunas_csv)
                for produto_row in produtos_raw:
                    # 'produto_row' é um sqlite3.Row, então podemos acessar por nome da coluna
                    row_data = [
                        produto_row['nome'], produto_row['codigo'], produto_row['preco'],
                        produto_row['quantidade'], produto_row['data_validade'],
                        produto_row['fornecedor'], produto_row['descricao'],
                        produto_row['categoria'], produto_row['unidade_medida'],
                        produto_row['localizacao_estoque'], produto_row['marca'],
                        produto_row['garantia_meses'], produto_row['peso_kg']
                    ]
                    writer.writerow(row_data)
            messagebox.showinfo("Exportado", f"Estoque exportado com sucesso para:\n{file_path}")
        except IOError as e:
            messagebox.showerror("Erro de Exportação", f"Não foi possível salvar o arquivo CSV:\n{e}")
    else:
        messagebox.showwarning("Exportar CSV", "Operação de exportação cancelada.")

# --- Tela de Consulta de Estoque Aprimorada ---

def tela_consulta_estoque(janela):
    # Limpar a tela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu': # Preserva a barra de menu
            widget.destroy()

    # Frame principal da tela de consulta
    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📋 Consulta de Estoque", font=("Helvetica", 18, "bold"),
             bg="#f8f8ff", fg="#004d66").pack(pady=10)

    # Campo de pesquisa
    pesquisa_frame = tk.Frame(frame, bg="#f8f8ff")
    pesquisa_frame.pack(pady=5)

    tk.Label(pesquisa_frame, text="🔍 Buscar por Nome ou Código:", font=("Helvetica", 12),
             bg="#f8f8ff").pack(side="left", padx=5)

    entrada_pesquisa = tk.Entry(pesquisa_frame, width=40, font=("Helvetica", 12))
    entrada_pesquisa.pack(side="left", padx=5)

    def pesquisar_estoque():
        termo = entrada_pesquisa.get().strip()
        carregar_estoque(filtro=termo) # Usa a função de carregar com filtro

    tk.Button(pesquisa_frame, text="🔍 Pesquisar", bg="#cd853f", fg="white",
              font=("Helvetica", 11, "bold"), command=pesquisar_estoque).pack(side="left", padx=5)

    # Tabela de resultados (Treeview)
    tabela_frame = tk.Frame(frame, bg="#f8f8ff")
    tabela_frame.pack(pady=10, padx=20, fill="both", expand=True) # Preencher e expandir

    # Colunas a serem exibidas na consulta (sem o ID do DB)
    colunas_exibicao = ["Nome", "Código", "Preço", "Quantidade", "Data de Validade",
                        "Fornecedor", "Descrição", "Categoria", "Unidade de Medida",
                        "Localização no Estoque", "Marca", "Garantia (meses)", "Peso (kg)"]

    tabela = ttk.Treeview(tabela_frame, columns=colunas_exibicao, show="headings")

    for col in colunas_exibicao:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    # Ajustes de largura para colunas específicas para melhor visualização
    tabela.column("Nome", width=150)
    tabela.column("Descrição", width=200)
    tabela.column("Localização no Estoque", width=150)
    tabela.column("Fornecedor", width=150)
    tabela.column("Data de Validade", width=120)

    # Barras de rolagem para a Treeview
    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew") # A tabela preenche a célula
    scroll_y.grid(row=0, column=1, sticky="ns") # Barra y ao lado da tabela
    scroll_x.grid(row=1, column=0, sticky="ew") # Barra x abaixo da tabela

    # Configura o redimensionamento da tabela dentro do frame
    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    def carregar_estoque(filtro=None):
        """Carrega produtos do banco de dados para a tabela de consulta."""
        tabela.delete(*tabela.get_children()) # Limpa a tabela existente
        produtos_do_db = buscar_produtos_db(filtro) # Busca produtos do DB com ou sem filtro
        for produto_row in produtos_do_db:
            # Obtém os valores do produto, pulando o 'id' (primeiro elemento)
            values_to_display = tuple(produto_row[1:])
            tabela.insert("", "end", values=values_to_display)

    # Botões inferiores
    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="🔄 Atualizar Tudo", bg="#a0522d", fg="white",
              font=("Helvetica", 12, "bold"), command=lambda: carregar_estoque(None)).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar CSV", bg="#8b4513", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv_db).pack(side="left", padx=10)

    # Carrega dados inicialmente ao abrir a tela de consulta
    carregar_estoque()