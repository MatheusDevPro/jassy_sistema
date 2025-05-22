import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from datetime import datetime

def tela_helpdesk(janela):
    # Limpar widgets anteriores (exceto menu)
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("🖥️ Helpdesk")
    janela.geometry("1150x650")
    janela.configure(bg="#f5f7fa")

    # Título
    titulo = tk.Label(janela, text="🖥️ Helpdesk - Sistema de Chamados", font=("Arial", 20, "bold"), fg="#0a4275", bg="#f5f7fa")
    titulo.pack(pady=15)

    # Frame Filtros
    frame_filtros = tk.Frame(janela, bg="#ffffff", bd=2, relief="groove")
    frame_filtros.pack(fill="x", padx=20, pady=10)

    # --- Filtros ---
    tk.Label(frame_filtros, text="Data Início:", bg="#ffffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entrada_data_inicio = tk.Entry(frame_filtros)
    entrada_data_inicio.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_filtros, text="Data Fim:", bg="#ffffff").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    entrada_data_fim = tk.Entry(frame_filtros)
    entrada_data_fim.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_filtros, text="Status:", bg="#ffffff").grid(row=0, column=4, sticky="w", padx=5, pady=5)
    status_combo = ttk.Combobox(frame_filtros, values=["Todos", "Aberto", "Em andamento", "Resolvido", "Fechado", "Cancelado"], state="readonly", width=15)
    status_combo.grid(row=0, column=5, padx=5, pady=5)
    status_combo.set("Todos")

    tk.Label(frame_filtros, text="Prioridade:", bg="#ffffff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    prioridade_combo = ttk.Combobox(frame_filtros, values=["Todas", "Baixa", "Média", "Alta", "Crítica"], state="readonly", width=15)
    prioridade_combo.grid(row=1, column=1, padx=5, pady=5)
    prioridade_combo.set("Todas")

    tk.Label(frame_filtros, text="Categoria:", bg="#ffffff").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    categoria_combo = ttk.Combobox(frame_filtros, values=["Todas", "Hardware", "Software", "Rede", "Acesso", "Outros"], state="readonly", width=15)
    categoria_combo.grid(row=1, column=3, padx=5, pady=5)
    categoria_combo.set("Todas")

    tk.Label(frame_filtros, text="Técnico:", bg="#ffffff").grid(row=1, column=4, sticky="w", padx=5, pady=5)
    tecnico_entry = tk.Entry(frame_filtros, width=18)
    tecnico_entry.grid(row=1, column=5, padx=5, pady=5)

    # Frame formulário para novo / editar chamado
    frame_form = tk.Frame(janela, bg="#e9ecef", bd=2, relief="groove")
    frame_form.pack(fill="x", padx=20, pady=10)

    # Inputs do formulário
    tk.Label(frame_form, text="Título:", bg="#e9ecef").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    titulo_entry = tk.Entry(frame_form, width=40)
    titulo_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Categoria:", bg="#e9ecef").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    categoria_form_combo = ttk.Combobox(frame_form, values=["Hardware", "Software", "Rede", "Acesso", "Outros"], state="readonly", width=18)
    categoria_form_combo.grid(row=0, column=3, padx=5, pady=5)
    categoria_form_combo.set("Hardware")

    tk.Label(frame_form, text="Prioridade:", bg="#e9ecef").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    prioridade_form_combo = ttk.Combobox(frame_form, values=["Baixa", "Média", "Alta", "Crítica"], state="readonly", width=18)
    prioridade_form_combo.grid(row=1, column=1, padx=5, pady=5)
    prioridade_form_combo.set("Média")

    tk.Label(frame_form, text="Status:", bg="#e9ecef").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    status_form_combo = ttk.Combobox(frame_form, values=["Aberto", "Em andamento", "Resolvido", "Fechado", "Cancelado"], state="readonly", width=18)
    status_form_combo.grid(row=1, column=3, padx=5, pady=5)
    status_form_combo.set("Aberto")

    tk.Label(frame_form, text="Técnico Responsável:", bg="#e9ecef").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    tecnico_form_entry = tk.Entry(frame_form, width=40)
    tecnico_form_entry.grid(row=2, column=1, padx=5, pady=5)

    # Checkboxes
    urgente_var = tk.IntVar()
    checkbox_urgente = tk.Checkbutton(frame_form, text="Urgente", variable=urgente_var, bg="#e9ecef")
    checkbox_urgente.grid(row=2, column=2, padx=5, pady=5, sticky="w")

    cliente_contatado_var = tk.IntVar()
    checkbox_cliente = tk.Checkbutton(frame_form, text="Cliente contatado", variable=cliente_contatado_var, bg="#e9ecef")
    checkbox_cliente.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    # Descrição (Text)
    tk.Label(frame_form, text="Descrição detalhada:", bg="#e9ecef").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
    descricao_text = tk.Text(frame_form, height=5, width=85)
    descricao_text.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

    # Frame Botões
    frame_botoes = tk.Frame(janela, bg="#f5f7fa")
    frame_botoes.pack(pady=10)

    # Tabela
    frame_tabela = tk.Frame(janela, bg="#ffffff", bd=2, relief="groove")
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

    colunas = ("id", "data_abertura", "titulo", "categoria", "prioridade", "status", "tecnico", "urgente", "cliente_contatado")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", selectmode="browse")

    headings = {
        "id": "ID",
        "data_abertura": "Data Abertura",
        "titulo": "Título",
        "categoria": "Categoria",
        "prioridade": "Prioridade",
        "status": "Status",
        "tecnico": "Técnico",
        "urgente": "Urgente",
        "cliente_contatado": "Cliente Contatado"
    }

    for col in colunas:
        tabela.heading(col, text=headings[col])
        tabela.column(col, width=100, anchor="center")

    tabela.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Dados exemplo
    chamados = []
    contador_id = 1

    # Funções
    def limpar_form():
        titulo_entry.delete(0, tk.END)
        categoria_form_combo.set("Hardware")
        prioridade_form_combo.set("Média")
        status_form_combo.set("Aberto")
        tecnico_form_entry.delete(0, tk.END)
        urgente_var.set(0)
        cliente_contatado_var.set(0)
        descricao_text.delete("1.0", tk.END)

    def carregar_tabela(dados):
        for i in tabela.get_children():
            tabela.delete(i)
        for c in dados:
            vals = (
                c["id"],
                c["data_abertura"],
                c["titulo"],
                c["categoria"],
                c["prioridade"],
                c["status"],
                c["tecnico"],
                "Sim" if c["urgente"] else "Não",
                "Sim" if c["cliente_contatado"] else "Não"
            )
            tabela.insert("", tk.END, values=vals)

    def buscar():
        filtro = []
        data_inicio = entrada_data_inicio.get()
        data_fim = entrada_data_fim.get()
        status_f = status_combo.get()
        prioridade_f = prioridade_combo.get()
        categoria_f = categoria_combo.get()
        tecnico_f = tecnico_entry.get().lower()

        for c in chamados:
            # Filtrar data (se preenchido)
            try:
                dt_abertura = datetime.strptime(c["data_abertura"], "%Y-%m-%d")
            except:
                dt_abertura = None
            try:
                di = datetime.strptime(data_inicio, "%Y-%m-%d") if data_inicio else None
                df = datetime.strptime(data_fim, "%Y-%m-%d") if data_fim else None
            except:
                di = df = None

            if di and dt_abertura and dt_abertura < di:
                continue
            if df and dt_abertura and dt_abertura > df:
                continue

            if status_f != "Todos" and c["status"] != status_f:
                continue
            if prioridade_f != "Todas" and c["prioridade"] != prioridade_f:
                continue
            if categoria_f != "Todas" and c["categoria"] != categoria_f:
                continue
            if tecnico_f and tecnico_f not in c["tecnico"].lower():
                continue
            filtro.append(c)

        carregar_tabela(filtro)

    def inserir_chamado():
        nonlocal contador_id
        titulo_val = titulo_entry.get().strip()
        tecnico_val = tecnico_form_entry.get().strip()
        descricao_val = descricao_text.get("1.0", tk.END).strip()

        if not titulo_val:
            messagebox.showwarning("Aviso", "Informe o título do chamado.")
            return
        if not tecnico_val:
            messagebox.showwarning("Aviso", "Informe o técnico responsável.")
            return

        novo = {
            "id": contador_id,
            "data_abertura": datetime.now().strftime("%Y-%m-%d"),
            "titulo": titulo_val,
            "categoria": categoria_form_combo.get(),
            "prioridade": prioridade_form_combo.get(),
            "status": status_form_combo.get(),
            "tecnico": tecnico_val,
            "urgente": bool(urgente_var.get()),
            "cliente_contatado": bool(cliente_contatado_var.get()),
            "descricao": descricao_val
        }
        chamados.append(novo)
        contador_id += 1
        carregar_tabela(chamados)
        limpar_form()
        messagebox.showinfo("Sucesso", "Chamado inserido com sucesso.")

    def selecionar_chamado(event):
        selected = tabela.selection()
        if not selected:
            return
        item = tabela.item(selected[0])["values"]
        # carregar dados no form
        for c in chamados:
            if c["id"] == item[0]:
                titulo_entry.delete(0, tk.END)
                titulo_entry.insert(0, c["titulo"])

                categoria_form_combo.set(c["categoria"])
                prioridade_form_combo.set(c["prioridade"])
                status_form_combo.set(c["status"])
                tecnico_form_entry.delete(0, tk.END)
                tecnico_form_entry.insert(0, c["tecnico"])
                urgente_var.set(1 if c["urgente"] else 0)
                cliente_contatado_var.set(1 if c["cliente_contatado"] else 0)
                descricao_text.delete("1.0", tk.END)
                descricao_text.insert("1.0", c["descricao"])
                break

    def atualizar_chamado():
        selected = tabela.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um chamado para atualizar.")
            return
        item = tabela.item(selected[0])["values"]
        for c in chamados:
            if c["id"] == item[0]:
                c["titulo"] = titulo_entry.get().strip()
                c["categoria"] = categoria_form_combo.get()
                c["prioridade"] = prioridade_form_combo.get()
                c["status"] = status_form_combo.get()
                c["tecnico"] = tecnico_form_entry.get().strip()
                c["urgente"] = bool(urgente_var.get())
                c["cliente_contatado"] = bool(cliente_contatado_var.get())
                c["descricao"] = descricao_text.get("1.0", tk.END).strip()
                break
        carregar_tabela(chamados)
        messagebox.showinfo("Sucesso", "Chamado atualizado com sucesso.")

    def excluir_chamado():
        selected = tabela.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um chamado para excluir.")
            return
        item = tabela.item(selected[0])["values"]
        for i, c in enumerate(chamados):
            if c["id"] == item[0]:
                del chamados[i]
                break
        carregar_tabela(chamados)
        limpar_form()
        messagebox.showinfo("Sucesso", "Chamado excluído com sucesso.")

    def exportar_excel():
        if not chamados:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return
        wb = Workbook()
        ws = wb.active
        ws.title = "Chamados"
        ws.append(list(headings.values()))
        for c in chamados:
            ws.append([
                c["id"],
                c["data_abertura"],
                c["titulo"],
                c["categoria"],
                c["prioridade"],
                c["status"],
                c["tecnico"],
                "Sim" if c["urgente"] else "Não",
                "Sim" if c["cliente_contatado"] else "Não"
            ])
        try:
            wb.save("chamados_helpdesk.xlsx")
            messagebox.showinfo("Sucesso", "Dados exportados para chamados_helpdesk.xlsx")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo Excel:\n{e}")

    def exportar_pdf():
        if not chamados:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return
        c = canvas.Canvas("chamados_helpdesk.pdf")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, 800, "Relatório de Chamados Helpdesk")
        c.setFont("Helvetica", 10)

        y = 780
        for idx, cdata in enumerate(chamados, 1):
            texto = f"{idx}. [{cdata['data_abertura']}] {cdata['titulo']} - {cdata['status']} - Técnico: {cdata['tecnico']}"
            c.drawString(30, y, texto)
            y -= 15
            if y < 50:
                c.showPage()
                y = 800
        c.save()
        messagebox.showinfo("Sucesso", "PDF gerado: chamados_helpdesk.pdf")

    def imprimir_chamado():
        selected = tabela.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um chamado para imprimir.")
            return
        item = tabela.item(selected[0])["values"]
        for cdata in chamados:
            if cdata["id"] == item[0]:
                texto = (
                    f"ID: {cdata['id']}\n"
                    f"Data Abertura: {cdata['data_abertura']}\n"
                    f"Título: {cdata['titulo']}\n"
                    f"Categoria: {cdata['categoria']}\n"
                    f"Prioridade: {cdata['prioridade']}\n"
                    f"Status: {cdata['status']}\n"
                    f"Técnico: {cdata['tecnico']}\n"
                    f"Urgente: {'Sim' if cdata['urgente'] else 'Não'}\n"
                    f"Cliente Contatado: {'Sim' if cdata['cliente_contatado'] else 'Não'}\n"
                    f"Descrição:\n{cdata['descricao']}\n"
                )
                messagebox.showinfo("Imprimir Chamado", texto)
                break

    # Botões
    btn_inserir = tk.Button(frame_botoes, text="➕ Inserir Chamado", bg="#28a745", fg="white", font=("Arial", 11, "bold"), command=inserir_chamado)
    btn_inserir.grid(row=0, column=0, padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="✏️ Atualizar Chamado", bg="#007bff", fg="white", font=("Arial", 11, "bold"), command=atualizar_chamado)
    btn_atualizar.grid(row=0, column=1, padx=5)

    btn_excluir = tk.Button(frame_botoes, text="🗑️ Excluir Chamado", bg="#dc3545", fg="white", font=("Arial", 11, "bold"), command=excluir_chamado)
    btn_excluir.grid(row=0, column=2, padx=5)

    btn_buscar = tk.Button(frame_botoes, text="🔍 Buscar", bg="#17a2b8", fg="white", font=("Arial", 11, "bold"), command=buscar)
    btn_buscar.grid(row=0, column=3, padx=5)

    btn_exportar_excel = tk.Button(frame_botoes, text="📁 Exportar Excel", bg="#6f42c1", fg="white", font=("Arial", 11, "bold"), command=exportar_excel)
    btn_exportar_excel.grid(row=0, column=4, padx=5)

    btn_exportar_pdf = tk.Button(frame_botoes, text="📄 Exportar PDF", bg="#fd7e14", fg="white", font=("Arial", 11, "bold"), command=exportar_pdf)
    btn_exportar_pdf.grid(row=0, column=5, padx=5)

    btn_imprimir = tk.Button(frame_botoes, text="🖨️ Imprimir Chamado", bg="#343a40", fg="white", font=("Arial", 11, "bold"), command=imprimir_chamado)
    btn_imprimir.grid(row=0, column=6, padx=5)

    # Evento para carregar dados na edição ao selecionar na tabela
    tabela.bind("<<TreeviewSelect>>", selecionar_chamado)

    # Inicializa a tabela vazia
    carregar_tabela(chamados)

# Para testar sozinho, descomente abaixo:

# if __name__ == "__main__":
#     root = tk.Tk()
#     tela_helpdesk(root)
#     root.mainloop()
