import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os
from datetime import datetime

def tela_consulta_estoque(janela):
    # Clear the screen
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    # Main Frame
    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True, padx=15, pady=15) # Add some padding

    # Title
    tk.Label(frame, text="📋 Consulta e Gestão de Estoque", font=("Helvetica", 20, "bold"),
             bg="#f8f8ff", fg="#004d66").pack(pady=15)

    # --- Search and Filter Section ---
    search_filter_frame = tk.Frame(frame, bg="#f8f8ff")
    search_filter_frame.pack(pady=10, fill="x")

    tk.Label(search_filter_frame, text="🔍 Buscar:", font=("Helvetica", 12),
             bg="#f8f8ff").pack(side="left", padx=5)

    entrada_pesquisa = tk.Entry(search_filter_frame, width=30, font=("Helvetica", 12), bd=2, relief="groove")
    entrada_pesquisa.pack(side="left", padx=5, ipady=2) # ipady for internal padding

    # Category Filter
    tk.Label(search_filter_frame, text="📦 Categoria:", font=("Helvetica", 12),
             bg="#f8f8ff").pack(side="left", padx=(15, 5))

    categorias = ["Todas"] # Will be populated dynamically
    combo_categoria = ttk.Combobox(search_filter_frame, values=categorias, font=("Helvetica", 12), width=15, state="readonly")
    combo_categoria.set("Todas")
    combo_categoria.pack(side="left", padx=5)

    def popular_categorias():
        # Populate categories from the data file
        unique_categories = set()
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                for line in f:
                    values = [v.strip() for v in line.strip().split("|")]
                    if len(values) >= 8: # Ensure category field exists
                        unique_categories.add(values[7]) # Category is the 8th element (index 7)
            combo_categoria['values'] = ["Todas"] + sorted(list(unique_categories))
        except FileNotFoundError:
            pass # No file, no categories yet

    popular_categorias()

    def pesquisar_estoque():
        termo = entrada_pesquisa.get().lower()
        categoria_selecionada = combo_categoria.get()
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) != len(colunas): # Skip malformed lines
                        continue

                    # Filter by search term
                    match_termo = any(termo in v.lower() for v in valores[:2]) # Search by Name or Code

                    # Filter by category
                    match_categoria = True
                    if categoria_selecionada != "Todas" and valores[7] != categoria_selecionada:
                        match_categoria = False

                    if match_termo and match_categoria:
                        tabela.insert("", "end", values=valores)
            aplicar_alertas_visuais() # Apply visual alerts after loading
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Arquivo de estoque não encontrado. Crie um produto primeiro.")

    # Search Button
    tk.Button(search_filter_frame, text="🔍 Pesquisar", bg="#cd853f", fg="white",
              font=("Helvetica", 11, "bold"), command=pesquisar_estoque, relief="raised", bd=2).pack(side="left", padx=10)

    # --- Stock Table ---
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(pady=15, fill="both", expand=True)

    colunas = ["Nome", "Código", "Preço", "Quantidade", "Validade", "Fornecedor", "Descrição", "Categoria"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=15) # Increased height

    # Configure columns and headings
    for col in colunas:
        tabela.heading(col, text=col, command=lambda _col=col: sort_column(tabela, _col, False)) # Add sorting
        tabela.column(col, width=tk.font.Font().measure(col) + 20, anchor="center") # Auto-adjust width for heading
        tabela.column("Nome", width=180) # Specific width for Name
        tabela.column("Descrição", width=200) # Specific width for Description
        tabela.column("Validade", width=100) # Specific width for Validade
        tabela.column("Preço", width=80)
        tabela.column("Quantidade", width=80)

    # Vertical Scrollbar
    scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")

    # Horizontal Scrollbar
    scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(xscrollcommand=scroll_x.set)
    scroll_x.pack(side="bottom", fill="x")

    tabela.pack(side="left", fill="both", expand=True)

    # --- Sorting Function ---
    def sort_column(tree, col, reverse):
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        if col in ["Preço", "Quantidade"]:
            try:
                l.sort(key=lambda t: float(t[0]), reverse=reverse)
            except ValueError: # Handle non-numeric values
                l.sort(key=lambda t: t[0], reverse=reverse)
        elif col == "Validade":
            # Sort dates in YYYY-MM-DD format
            l.sort(key=lambda t: datetime.strptime(t[0], "%d/%m/%Y") if t[0] else datetime.max, reverse=reverse)
        else:
            l.sort(key=lambda t: t[0].lower(), reverse=reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)
        tree.heading(col, command=lambda: sort_column(tree, col, not reverse))

    # --- Visual Alerts (Low Stock / Expired) ---
    def aplicar_alertas_visuais():
        today = datetime.now()
        for item_id in tabela.get_children():
            values = tabela.item(item_id, 'values')
            quantidade = int(values[3])
            validade_str = values[4]

            # Low Stock Alert
            if quantidade <= 10: # Threshold for low stock
                tabela.tag_configure('low_stock', background='#ffcccb') # Light red
                tabela.item(item_id, tags=('low_stock',))
                # Add tooltip for low stock
                tabela.tag_bind('low_stock', '<Enter>', lambda event, q=quantidade: show_tooltip(event, f"Pouco estoque: {q} unidades restantes!"))
                tabela.tag_bind('low_stock', '<Leave>', hide_tooltip)
            else:
                tabela.tag_configure('low_stock', background='') # Reset background
                tabela.item(item_id, tags=())

            # Expiration Alert
            if validade_str:
                try:
                    validade_date = datetime.strptime(validade_str, "%d/%m/%Y")
                    days_until_expiration = (validade_date - today).days

                    if days_until_expiration < 0:
                        tabela.tag_configure('expired', background='#ffd700') # Yellow for expired
                        tabela.item(item_id, tags=('expired',))
                        tabela.tag_bind('expired', '<Enter>', lambda event: show_tooltip(event, "Produto Vencido!"))
                        tabela.tag_bind('expired', '<Leave>', hide_tooltip)
                    elif days_until_expiration <= 30: # Within 30 days
                        tabela.tag_configure('near_expiry', background='#add8e6') # Light blue for near expiry
                        tabela.item(item_id, tags=('near_expiry',))
                        tabela.tag_bind('near_expiry', '<Enter>', lambda event, d=days_until_expiration: show_tooltip(event, f"Vence em {d} dias!"))
                        tabela.tag_bind('near_expiry', '<Leave>', hide_tooltip)
                    else:
                        tabela.tag_configure('expired', background='')
                        tabela.tag_configure('near_expiry', background='')
                        tabela.item(item_id, tags=())

                except ValueError:
                    pass # Invalid date format

    # Tooltip functions
    tooltip_window = None
    def show_tooltip(event, text):
        global tooltip_window
        if tooltip_window:
            return

        x, y, _, _ = tabela.bbox(event.widget.identify_row(event.y), column=0)
        x = event.x_root + 10 # Offset tooltip
        y = event.y_root + 10

        tooltip_window = tk.Toplevel(event.widget)
        tooltip_window.wm_overrideredirect(True)
        tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tooltip_window, text=text, background="#ffffe0", relief="solid", borderwidth=1,
                         font=("Helvetica", 10, "normal"))
        label.pack(padx=1, pady=1)

    def hide_tooltip(event=None):
        global tooltip_window
        if tooltip_window:
            tooltip_window.destroy()
            tooltip_window = None

    def carregar_estoque():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.strip().split("|")]
                    if len(valores) == len(colunas):
                        tabela.insert("", "end", values=valores)
            aplicar_alertas_visuais() # Apply visual alerts after loading
        except FileNotFoundError:
            pass # No file, no data to load

    def exportar_csv():
        try:
            with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            
            # Ensure the 'dados' directory exists
            os.makedirs("dados", exist_ok=True)
            
            with open("dados/estoque_consulta.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(colunas)
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Estoque exportado para 'dados/estoque_consulta.csv' com sucesso!")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao exportar: {e}")

    def remover_produto():
        selected_item = tabela.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um produto para remover.")
            return

        confirm = messagebox.askyesno("Confirmar Remoção", "Tem certeza que deseja remover o produto selecionado?")
        if confirm:
            codigos_para_remover = []
            for item in selected_item:
                codigo = tabela.item(item, 'values')[1] # Get product code (second column)
                codigos_para_remover.append(codigo)

            linhas_restantes = []
            try:
                with open("dados/produtos.txt", "r", encoding="utf-8") as f:
                    for linha in f:
                        valores = [v.strip() for v in linha.strip().split("|")]
                        if len(valores) > 1 and valores[1] not in codigos_para_remover:
                            linhas_restantes.append(linha)
                
                with open("dados/produtos.txt", "w", encoding="utf-8") as f:
                    f.writelines(linhas_restantes)
                
                messagebox.showinfo("Sucesso", "Produto(s) removido(s) com sucesso!")
                carregar_estoque() # Reload the table
            except FileNotFoundError:
                messagebox.showwarning("Erro", "Arquivo de estoque não encontrado.")
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao remover: {e}")

    # --- Bottom Buttons ---
    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=20)

    tk.Button(botoes_frame, text="🔄 Atualizar", bg="#a0522d", fg="white",
              font=("Helvetica", 12, "bold"), command=carregar_estoque, relief="raised", bd=2).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar CSV", bg="#8b4513", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv, relief="raised", bd=2).pack(side="left", padx=10)
    
    tk.Button(botoes_frame, text="🗑️ Remover Produto", bg="#dc143c", fg="white",
              font=("Helvetica", 12, "bold"), command=remover_produto, relief="raised", bd=2).pack(side="left", padx=10)

    # Initial data load
    carregar_estoque()

# Example of how to run this function
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestão de Estoque")
    root.geometry("1000x700") # Set initial window size
    root.configure(bg="#f8f8ff")

    # Create a dummy data file for testing if it doesn't exist
    if not os.path.exists("dados/produtos.txt"):
        os.makedirs("dados", exist_ok=True)
        with open("dados/produtos.txt", "w", encoding="utf-8") as f:
            f.write("Maçã|001|2.50|50|20/12/2025|Hortifruti XYZ|Maçãs frescas e crocantes|Frutas\n")
            f.write("Leite Integral|002|4.00|15|10/06/2025|Laticínios ABC|Leite tipo A, 1L|Laticínios\n")
            f.write("Pão de Forma|003|7.80|5|01/06/2024|Padaria Doce Lar|Pão tradicional 500g|Panificados\n")
            f.write("Arroz Agulhinha|004|6.20|120|05/01/2026|Grãos do Campo|Arroz branco de qualidade|Grãos\n")
            f.write("Iogurte Natural|005|3.20|8|15/05/2025|Laticínios ABC|Iogurte sem açúcar|Laticínios\n")
            f.write("Sabão em Pó|006|15.00|25|30/12/2027|Limpeza Total|Sabão para roupas 1kg|Limpeza\n")
            f.write("Refrigerante Cola|007|6.50|30|15/07/2025|Bebidas Refrescantes|Refrigerante sabor cola 2L|Bebidas\n")
            f.write("Chocolate Amargo|008|9.90|3|28/05/2024|Doces Finos|Chocolate 70% cacau|Doces\n")


    tela_consulta_estoque(root)
    root.mainloop()