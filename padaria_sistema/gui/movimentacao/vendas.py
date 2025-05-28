import tkinter as tk
from tkinter import messagebox, ttk
import os, csv
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3 # Import the sqlite3 module

def tela_vendas(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.configure(bg="#e6f2ff")
    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Registro de Vendas 💰", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10, padx=10)

    categorias = ["Eletrônicos", "Alimentos", "Vestuário", "Cosméticos", "Livros", "Outros"]
    status_venda = ["Pendente", "Pago", "Cancelado"]
    condicoes_pagamento = ["À vista", "2x", "3x", "4x ou mais"]
    formas_pagamento = ["Dinheiro", "Cartão", "Pix", "Boleto"]
    entrega_opcoes = ["Retirada no Local", "Entrega"]

    numero_pedido = datetime.now().strftime("%Y%m%d%H%M%S")

    campos = {
        "Nº Pedido": tk.Entry(campos_frame, width=25),
        "Data da Venda": DateEntry(campos_frame, width=22, date_pattern='dd/mm/yyyy'),
        "Cliente": tk.Entry(campos_frame, width=25),
        "CPF/CNPJ": tk.Entry(campos_frame, width=25),
        "Produto": tk.Entry(campos_frame, width=25),
        "Descrição": tk.Entry(campos_frame, width=25),
        "Categoria": ttk.Combobox(campos_frame, values=categorias, state="readonly", width=23),
        "Quantidade": tk.Entry(campos_frame, width=25),
        "Preço Unitário": tk.Entry(campos_frame, width=25),
        "Desconto (R$)": tk.Entry(campos_frame, width=25),
        "Acréscimo (R$)": tk.Entry(campos_frame, width=25),
        "Valor Total Líquido": tk.Entry(campos_frame, width=25, state="readonly"),
        "Vendedor": tk.Entry(campos_frame, width=25),
        "Forma de Pagamento": ttk.Combobox(campos_frame, values=formas_pagamento, state="readonly", width=23),
        "Condição de Pagamento": ttk.Combobox(campos_frame, values=condicoes_pagamento, state="readonly", width=23),
        "Entrega": ttk.Combobox(campos_frame, values=entrega_opcoes, state="readonly", width=23),
        "Status": ttk.Combobox(campos_frame, values=status_venda, state="readonly", width=23),
    }

    campos["Nº Pedido"].insert(0, numero_pedido)
    campos["Nº Pedido"].config(state="readonly")

    # Posicionamento
    linha, coluna = 0, 0
    for rotulo, entrada in campos.items():
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66")\
            .grid(row=linha, column=coluna*2, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna*2+1, padx=8, pady=6, sticky="w")
        coluna += 1
        if coluna > 1:
            coluna = 0
            linha += 1

    tk.Label(campos_frame, text="Observações:", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66")\
        .grid(row=linha, column=0, padx=8, pady=6, sticky="ne")
    obs = tk.Text(campos_frame, width=55, height=3)
    obs.grid(row=linha, column=1, columnspan=3, padx=8, pady=6, sticky="w")
    linha += 1

    def calcular_total(event=None):
        try:
            qnt = int(campos["Quantidade"].get())
            preco = float(campos["Preço Unitário"].get())
            desc = float(campos["Desconto (R$)"].get() or 0)
            acres = float(campos["Acréscimo (R$)"].get() or 0)
            total = qnt * preco - desc + acres
            campos["Valor Total Líquido"].config(state="normal")
            campos["Valor Total Líquido"].delete(0, tk.END)
            campos["Valor Total Líquido"].insert(0, f"{total:.2f}")
            campos["Valor Total Líquido"].config(state="readonly")
        except ValueError: # Catch specific error for invalid number conversion
            campos["Valor Total Líquido"].config(state="normal")
            campos["Valor Total Líquido"].delete(0, tk.END)
            campos["Valor Total Líquido"].insert(0, "0.00")
            campos["Valor Total Líquido"].config(state="readonly")

    for campo in ["Quantidade", "Preço Unitário", "Desconto (R$)", "Acréscimo (R$)"]:
        campos[campo].bind("<KeyRelease>", calcular_total)

    # --- Database Functions ---
    def connect_db():
        os.makedirs("dados", exist_ok=True) # Ensure 'dados' directory exists
        conn = sqlite3.connect("dados/vendas.db") # Connect to the database file
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero_pedido TEXT,
                data_venda TEXT,
                cliente TEXT,
                cpf_cnpj TEXT,
                produto TEXT,
                descricao TEXT,
                categoria TEXT,
                quantidade INTEGER,
                preco_unitario REAL,
                desconto REAL,
                acrescimo REAL,
                valor_total_liquido REAL,
                vendedor TEXT,
                forma_pagamento TEXT,
                condicao_pagamento TEXT,
                entrega TEXT,
                status TEXT,
                observacoes TEXT
            )
        ''')
        conn.commit()
        return conn, cursor

    def salvar():
        dados = []
        for key, campo in campos.items():
            if isinstance(campo, DateEntry):
                dados.append(campo.get_date().strftime("%d/%m/%Y"))
            else:
                dados.append(campo.get().strip())

        observacao = obs.get("1.0", tk.END).strip() or "-"
        dados.append(observacao)

        # Validate mandatory fields
        obrigatorios = [k for k in campos if "Valor Total" not in k and "Desconto" not in k and "Acréscimo" not in k]
        for i, k in enumerate(campos):
            # The 'dados' list order must match the 'campos' dictionary order
            if k in obrigatorios and not dados[list(campos).index(k)]: # Check the corresponding data in 'dados'
                messagebox.showwarning("Aviso", f"Preencha o campo: {k}")
                return

        try:
            quantidade = int(dados[list(campos).index("Quantidade")])
            valor_total_liquido = float(dados[list(campos).index("Valor Total Líquido")])
            if quantidade <= 0 or valor_total_liquido <= 0:
                messagebox.showwarning("Erro", "Quantidade e Valor Total devem ser maiores que zero.")
                return
        except ValueError:
            messagebox.showwarning("Erro", "Quantidade e Preço Unitário devem ser números válidos.")
            return

        conn, cursor = connect_db()
        try:
            cursor.execute('''
                INSERT INTO vendas (
                    numero_pedido, data_venda, cliente, cpf_cnpj, produto, descricao,
                    categoria, quantidade, preco_unitario, desconto, acrescimo,
                    valor_total_liquido, vendedor, forma_pagamento, condicao_pagamento,
                    entrega, status, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(dados))
            conn.commit()
            messagebox.showinfo("Salvo", "Venda registrada com sucesso no banco de dados.")

            # Clear fields after saving
            for campo in campos.values():
                if isinstance(campo, tk.Entry) and campo.cget("state") == "normal": # Only clear editable entries
                    campo.delete(0, tk.END)
                elif isinstance(campo, ttk.Combobox):
                    campo.set("")
                elif isinstance(campo, DateEntry):
                    campo.set_date(datetime.today())
            obs.delete("1.0", tk.END)
            campos["Nº Pedido"].config(state="normal") # Temporarily enable to update
            campos["Nº Pedido"].delete(0, tk.END)
            campos["Nº Pedido"].insert(0, datetime.now().strftime("%Y%m%d%H%M%S"))
            campos["Nº Pedido"].config(state="readonly")
            campos["Valor Total Líquido"].config(state="readonly")

            carregar_vendas() # Reload data into Treeview
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao salvar: {e}")
        finally:
            conn.close()

    def exportar_csv():
        conn, cursor = connect_db()
        try:
            cursor.execute("SELECT * FROM vendas")
            rows = cursor.fetchall()
            if not rows:
                messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
                return

            csv_file_path = "dados/vendas.csv"
            with open(csv_file_path, "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                # Write header row (excluding 'id' column from database)
                header = [h[0] for h in cursor.description] # Get column names from cursor description
                if 'id' in header:
                    header.remove('id')
                writer.writerow(header)

                # Write data rows
                for row in rows:
                    # Exclude the 'id' column from the exported row if present
                    row_list = list(row)
                    if len(row_list) > len(header): # Assuming 'id' is the extra column
                        row_list.pop(0) # Remove the first element (id)
                    writer.writerow(row_list)
            messagebox.showinfo("Exportado", f"Dados exportados para {csv_file_path}")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao exportar: {e}")
        finally:
            conn.close()

    botoes = tk.Frame(frame, bg="#e6f2ff")
    botoes.pack(pady=10)

    tk.Button(botoes, text="💾 Registrar Venda", command=salvar, bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20).pack(side="left", padx=10)
    tk.Button(botoes, text="📁 Exportar CSV", command=exportar_csv, bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20).pack(side="left", padx=10)

    tabela_frame = tk.LabelFrame(frame, text="📋 Vendas Registradas", bg="#e6f2ff",
                                  font=("Helvetica", 12, "bold"), fg="#004d80", bd=2, relief="groove")
    tabela_frame.pack(pady=15, padx=20, fill="both", expand=True)

    # Use the database column names directly for Treeview columns (excluding 'id')
    db_col_names = [
        "numero_pedido", "data_venda", "cliente", "cpf_cnpj", "produto", "descricao",
        "categoria", "quantidade", "preco_unitario", "desconto", "acrescimo",
        "valor_total_liquido", "vendedor", "forma_pagamento", "condicao_pagamento",
        "entrega", "status", "observacoes"
    ]
    # Map database column names to more readable labels for the Treeview headings
    display_col_names = list(campos.keys()) + ["Observações"] # Use your original UI labels

    tabela = ttk.Treeview(tabela_frame, columns=db_col_names, show="headings", height=12) # Use db_col_names as internal identifiers
    for i, col in enumerate(db_col_names):
        tabela.heading(col, text=display_col_names[i]) # Display user-friendly headings
        tabela.column(col, width=120, anchor="center")

    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    scroll_y.grid(row=0, column=1, sticky="ns", pady=8)
    scroll_x.grid(row=1, column=0, sticky="ew", padx=8)

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    def carregar_vendas():
        tabela.delete(*tabela.get_children())
        conn, cursor = connect_db()
        try:
            cursor.execute("SELECT * FROM vendas")
            rows = cursor.fetchall()
            for row in rows:
                # Exclude the 'id' column when inserting into the Treeview
                tabela.insert("", "end", values=row[1:]) # Skip the first element (id)
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao carregar dados: {e}")
        finally:
            conn.close()

    carregar_vendas()