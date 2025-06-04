import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import os, csv
import sqlite3 # Import the sqlite3 module
from datetime import datetime

def tela_compras(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#fffaf0")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Registro de Compras 🛒", font=("Helvetica", 18, "bold"), bg="#fffaf0", fg="#663300").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#fffaf0")
    campos_frame.pack(pady=10, padx=10)

    categorias = ["Alimentos", "Bebidas", "Limpeza", "Eletrônicos", "Roupas", "Outros"]
    unidades = ["Un", "Kg", "g", "L", "ml", "Pacote", "Caixa"]
    formas_pagamento = ["Dinheiro", "Crédito", "Débito", "Pix", "Transferência", "Boleto", "Cheque"]
    status_compra = ["Pendente", "Pago", "Cancelado"]
    condicoes_pagamento = ["À Vista", "30 dias", "30/60", "30/60/90"]
    tipo_frete = ["CIF", "FOB"]

    campos = {
        # FORNECEDOR
        "Fornecedor": tk.Entry(campos_frame, width=30),
        "CNPJ do Fornecedor": tk.Entry(campos_frame, width=30),
        "Nome Fantasia": tk.Entry(campos_frame, width=30),
        "E-mail do Fornecedor": tk.Entry(campos_frame, width=30),
        "Telefone do Fornecedor": tk.Entry(campos_frame, width=30),

        # PRODUTO
        "Código do Produto": tk.Entry(campos_frame, width=30),
        "Nome do Produto": tk.Entry(campos_frame, width=30),
        "Categoria": ttk.Combobox(campos_frame, width=27, values=categorias, state="readonly"),
        "Unidade de Medida": ttk.Combobox(campos_frame, width=27, values=unidades, state="readonly"),
        "Quantidade": tk.Entry(campos_frame, width=30),
        "Valor Unitário": tk.Entry(campos_frame, width=30),
        "Valor Total": tk.Entry(campos_frame, width=30),

        # DOCUMENTO
        "Número da Nota Fiscal": tk.Entry(campos_frame, width=30),
        "Série da NF": tk.Entry(campos_frame, width=30),
        "Chave de Acesso": tk.Entry(campos_frame, width=30),

        # PAGAMENTO
        "Forma de Pagamento": ttk.Combobox(campos_frame, width=27, values=formas_pagamento, state="readonly"),
        "Condição de Pagamento": ttk.Combobox(campos_frame, width=27, values=condicoes_pagamento, state="readonly"),
        "Status da Compra": ttk.Combobox(campos_frame, width=27, values=status_compra, state="readonly"),
        "Data da Compra": DateEntry(campos_frame, width=30, date_pattern='dd/mm/yyyy'),
        "Data de Recebimento": DateEntry(campos_frame, width=30, date_pattern='dd/mm/yyyy'),
        "Data de Vencimento": DateEntry(campos_frame, width=30, date_pattern='dd/mm/yyyy'),

        # LOGÍSTICA
        "Transportadora": tk.Entry(campos_frame, width=30),
        "Tipo de Frete": ttk.Combobox(campos_frame, width=27, values=tipo_frete, state="readonly"),
        "Valor do Frete": tk.Entry(campos_frame, width=30),

        # OBS
        "Observações": tk.Text(campos_frame, width=62, height=4)
    }

    # Definir valores padrão
    campos["Categoria"].set(categorias[0])
    campos["Unidade de Medida"].set(unidades[0])
    campos["Forma de Pagamento"].set(formas_pagamento[0])
    campos["Condição de Pagamento"].set(condicoes_pagamento[0])
    campos["Status da Compra"].set(status_compra[0])
    campos["Tipo de Frete"].set(tipo_frete[0])

    # Distribuir os campos (em colunas)
    # The 'i' counter needs to be managed carefully for row/column distribution
    # and to ensure "Observações" gets its dedicated row.
    current_row, current_col = 0, 0
    for rotulo, entrada in campos.items():
        if rotulo == "Observações":
            # Observações takes a full row at the end
            tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#fffaf0").grid(row=current_row, column=0, sticky="nw", padx=5, pady=5)
            entrada.grid(row=current_row, column=1, columnspan=3, sticky="w", padx=5, pady=5)
        else:
            tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#fffaf0").grid(row=current_row, column=current_col*2, sticky="e", padx=5, pady=5)
            entrada.grid(row=current_row, column=current_col*2 + 1, sticky="w", padx=5, pady=5)
            current_col += 1
            if current_col > 1: # Move to next row after 2 columns
                current_col = 0
                current_row += 1
    # Ensure 'Observações' is placed correctly after all other fields
    # If "Observações" is the last item, current_row would already be incremented correctly by the loop.
    # Otherwise, you might need an extra increment if it was placed manually outside the loop.
    # Given the loop structure, it should naturally place it after all other grid items.

    # --- Database Functions ---
    def connect_db():
        os.makedirs("dados", exist_ok=True) # Ensure 'dados' directory exists
        conn = sqlite3.connect("dados/compras.db") # Connect to the database file
        cursor = conn.cursor()
        # Create table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fornecedor TEXT,
                cnpj_fornecedor TEXT,
                nome_fantasia TEXT,
                email_fornecedor TEXT,
                telefone_fornecedor TEXT,
                codigo_produto TEXT,
                nome_produto TEXT,
                categoria TEXT,
                unidade_medida TEXT,
                quantidade REAL,
                valor_unitario REAL,
                valor_total REAL,
                numero_nota_fiscal TEXT,
                serie_nf TEXT,
                chave_acesso TEXT,
                forma_pagamento TEXT,
                condicao_pagamento TEXT,
                status_compra TEXT,
                data_compra TEXT,
                data_recebimento TEXT,
                data_vencimento TEXT,
                transportadora TEXT,
                tipo_frete TEXT,
                valor_frete REAL,
                observacoes TEXT
            )
        ''')
        conn.commit()
        return conn, cursor

    def salvar_compra():
        dados = []
        for rotulo, entrada in campos.items():
            if isinstance(entrada, DateEntry):
                dados.append(entrada.get_date().strftime("%d/%m/%Y"))
            elif isinstance(entrada, ttk.Combobox):
                dados.append(entrada.get().strip())
            elif rotulo == "Observações":
                dados.append(entrada.get("1.0", tk.END).strip())
            else:
                dados.append(entrada.get().strip())

        # Basic validation for empty fields
        for i, val in enumerate(dados):
            if not val and list(campos.keys())[i] != "Observações": # Allow Observations to be empty
                messagebox.showwarning("Atenção", f"Preencha o campo: {list(campos.keys())[i]}")
                return

        # Specific validation for numeric fields
        try:
            quantidade = float(campos["Quantidade"].get())
            valor_unitario = float(campos["Valor Unitário"].get())
            valor_total_calc = quantidade * valor_unitario
            # Update 'Valor Total' field
            campos["Valor Total"].config(state="normal")
            campos["Valor Total"].delete(0, tk.END)
            campos["Valor Total"].insert(0, f"{valor_total_calc:.2f}")
            campos["Valor Total"].config(state="readonly")
            
            valor_total_display = float(campos["Valor Total"].get()) # Get the value from the updated field

            if quantidade <= 0 or valor_unitario <= 0:
                messagebox.showwarning("Erro de Entrada", "Quantidade e Valor Unitário devem ser maiores que zero.")
                return
        except ValueError:
            messagebox.showwarning("Erro de Entrada", "Quantidade, Valor Unitário e Valor do Frete devem ser números válidos.")
            return

        conn, cursor = connect_db()
        try:
            # Prepare data tuple in the exact order of DB columns
            data_to_insert = (
                campos["Fornecedor"].get().strip(),
                campos["CNPJ do Fornecedor"].get().strip(),
                campos["Nome Fantasia"].get().strip(),
                campos["E-mail do Fornecedor"].get().strip(),
                campos["Telefone do Fornecedor"].get().strip(),
                campos["Código do Produto"].get().strip(),
                campos["Nome do Produto"].get().strip(),
                campos["Categoria"].get().strip(),
                campos["Unidade de Medida"].get().strip(),
                float(campos["Quantidade"].get()),
                float(campos["Valor Unitário"].get()),
                float(campos["Valor Total"].get()), # Use the calculated value
                campos["Número da Nota Fiscal"].get().strip(),
                campos["Série da NF"].get().strip(),
                campos["Chave de Acesso"].get().strip(),
                campos["Forma de Pagamento"].get().strip(),
                campos["Condição de Pagamento"].get().strip(),
                campos["Status da Compra"].get().strip(),
                campos["Data da Compra"].get_date().strftime("%d/%m/%Y"),
                campos["Data de Recebimento"].get_date().strftime("%d/%m/%Y"),
                campos["Data de Vencimento"].get_date().strftime("%d/%m/%Y"),
                campos["Transportadora"].get().strip(),
                campos["Tipo de Frete"].get().strip(),
                float(campos["Valor do Frete"].get() or 0.0), # Handle empty frete value
                campos["Observações"].get("1.0", tk.END).strip() or "-"
            )

            cursor.execute('''
                INSERT INTO compras (
                    fornecedor, cnpj_fornecedor, nome_fantasia, email_fornecedor, telefone_fornecedor,
                    codigo_produto, nome_produto, categoria, unidade_medida, quantidade, valor_unitario,
                    valor_total, numero_nota_fiscal, serie_nf, chave_acesso, forma_pagamento,
                    condicao_pagamento, status_compra, data_compra, data_recebimento, data_vencimento,
                    transportadora, tipo_frete, valor_frete, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data_to_insert)
            conn.commit()
            messagebox.showinfo("Sucesso", "Compra registrada com sucesso no banco de dados.")

            # Clear fields after saving
            for rotulo, entrada in campos.items():
                if isinstance(entrada, tk.Entry):
                    entrada.delete(0, tk.END)
                elif isinstance(entrada, ttk.Combobox):
                    entrada.set("") # Clear combobox selection
                elif isinstance(entrada, DateEntry):
                    entrada.set_date(datetime.today()) # Reset to current date
                elif rotulo == "Observações":
                    entrada.delete("1.0", tk.END)
            
            # Reset default combobox values if desired
            campos["Categoria"].set(categorias[0])
            campos["Unidade de Medida"].set(unidades[0])
            campos["Forma de Pagamento"].set(formas_pagamento[0])
            campos["Condição de Pagamento"].set(condicoes_pagamento[0])
            campos["Status da Compra"].set(status_compra[0])
            campos["Tipo de Frete"].set(tipo_frete[0])

            campos["Valor Total"].config(state="normal") # Enable to clear if needed
            campos["Valor Total"].delete(0, tk.END)
            campos["Valor Total"].config(state="readonly") # Back to readonly

            carregar_compras() # Reload data into Treeview
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao salvar: {e}")
        finally:
            conn.close()

    def calcular_valor_total(event=None):
        try:
            qnt = float(campos["Quantidade"].get())
            preco_unit = float(campos["Valor Unitário"].get())
            total = qnt * preco_unit
            campos["Valor Total"].config(state="normal")
            campos["Valor Total"].delete(0, tk.END)
            campos["Valor Total"].insert(0, f"{total:.2f}")
            campos["Valor Total"].config(state="readonly")
        except ValueError:
            campos["Valor Total"].config(state="normal")
            campos["Valor Total"].delete(0, tk.END)
            campos["Valor Total"].insert(0, "0.00")
            campos["Valor Total"].config(state="readonly")

    # Bind calculation to relevant fields
    campos["Quantidade"].bind("<KeyRelease>", calcular_valor_total)
    campos["Valor Unitário"].bind("<KeyRelease>", calcular_valor_total)


    def exportar_csv():
        conn, cursor = connect_db()
        try:
            cursor.execute("SELECT * FROM compras")
            rows = cursor.fetchall()
            if not rows:
                messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
                return

            csv_file_path = "dados/compras.csv"
            with open(csv_file_path, "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                # Get column names from cursor description (excluding 'id')
                header = [description[0] for description in cursor.description]
                if 'id' in header:
                    header.remove('id')
                writer.writerow(header)

                # Write data rows, excluding the 'id' column
                for row in rows:
                    row_list = list(row)
                    if len(row_list) > len(header): # Assuming 'id' is the extra column at index 0
                        row_list.pop(0)
                    writer.writerows([row_list]) # writerows expects an iterable of rows, so pass [row_list]

            messagebox.showinfo("Exportado", f"Dados exportados para {csv_file_path}")
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao exportar: {e}")
        finally:
            conn.close()

    # Botões
    botoes_frame = tk.Frame(frame, bg="#fffaf0")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Salvar Compra 💾", bg="#996633", fg="white", font=("Helvetica", 12, "bold"), command=salvar_compra).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Exportar CSV 📁", bg="#333366", fg="white", font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    # Tabela
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(pady=10, fill="both", expand=True)

    # Use database column names for Treeview internal columns, and map to display names
    db_col_names = [
        "fornecedor", "cnpj_fornecedor", "nome_fantasia", "email_fornecedor", "telefone_fornecedor",
        "codigo_produto", "nome_produto", "categoria", "unidade_medida", "quantidade", "valor_unitario",
        "valor_total", "numero_nota_fiscal", "serie_nf", "chave_acesso", "forma_pagamento",
        "condicao_pagamento", "status_compra", "data_compra", "data_recebimento", "data_vencimento",
        "transportadora", "tipo_frete", "valor_frete", "observacoes"
    ]
    display_col_names = list(campos.keys()) # Use your original UI labels as display names

    tabela = ttk.Treeview(tabela_frame, columns=db_col_names, show="headings", height=10)
    for i, col in enumerate(db_col_names):
        tabela.heading(col, text=display_col_names[i]) # Set user-friendly heading
        tabela.column(col, width=140, anchor="center")

    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    def carregar_compras():
        tabela.delete(*tabela.get_children())
        conn, cursor = connect_db()
        try:
            cursor.execute("SELECT * FROM compras")
            rows = cursor.fetchall()
            for row in rows:
                # Insert data into Treeview, skipping the 'id' column
                tabela.insert("", "end", values=row[1:]) # Skip the first element (id)
        except sqlite3.Error as e:
            messagebox.showerror("Erro no Banco de Dados", f"Ocorreu um erro ao carregar dados: {e}")
        finally:
            conn.close()

    carregar_compras()