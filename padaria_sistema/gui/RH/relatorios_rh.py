import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook

# Simulação de dados (substitua pelos seus dados reais)
dados_funcionarios = [
    {"id": 1, "nome": "Ana Silva", "cpf": "123.456.789-00", "cargo": "Analista", "departamento": "TI", "data_admissao": "10/01/2023", "status": "Ativo"},
    {"id": 2, "nome": "Carlos Souza", "cpf": "987.654.321-00", "cargo": "Gerente", "departamento": "Financeiro", "data_admissao": "15/03/2022", "status": "Inativo"},
    {"id": 3, "nome": "Beatriz Lima", "cpf": "456.789.123-00", "cargo": "Assistente", "departamento": "RH", "data_admissao": "20/07/2021", "status": "Ativo"},
]

def tela_relatorios_rh(janela):
    janela.title("📊 Relatórios RH - Jassy Gestão")
    janela.configure(bg="#f8f8ff")

    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    titulo = tk.Label(frame, text="📊 Relatórios RH", font=("Segoe UI", 18, "bold"), fg="#1E90FF", bg="#f8f8ff")
    titulo.pack(pady=10)

    filtro_frame = tk.LabelFrame(frame, text="Filtros de Pesquisa", font=("Segoe UI", 12, "bold"), bg="#f8f8ff", padx=10, pady=10)
    filtro_frame.pack(fill=tk.X, padx=10, pady=10)

    var_cargo = tk.StringVar()
    var_departamento = tk.StringVar()
    var_status = tk.StringVar()
    var_data_ini = tk.StringVar()
    var_data_fim = tk.StringVar()

    campos = [
        ("Cargo:", var_cargo, ["", "Analista", "Desenvolvedor", "Gerente", "Assistente", "Estagiário", "Supervisor"]),
        ("Departamento:", var_departamento, ["", "TI", "Financeiro", "RH", "Marketing", "Vendas", "Produção", "Suporte"]),
        ("Status:", var_status, ["", "Ativo", "Inativo", "Afastado"])
    ]

    for i, (label_text, var, options) in enumerate(campos):
        tk.Label(filtro_frame, text=label_text, bg="#f8f8ff").grid(row=0, column=i*2, padx=5, pady=5, sticky="e")
        combo = ttk.Combobox(filtro_frame, textvariable=var, state="readonly", values=options, width=18)
        combo.grid(row=0, column=i*2+1, padx=5, pady=5)

    tk.Label(filtro_frame, text="Admissão de:", bg="#f8f8ff").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_data_ini = tk.Entry(filtro_frame, textvariable=var_data_ini, width=15)
    entry_data_ini.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(filtro_frame, text="até:", bg="#f8f8ff").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    entry_data_fim = tk.Entry(filtro_frame, textvariable=var_data_fim, width=15)
    entry_data_fim.grid(row=1, column=3, padx=5, pady=5)

    def limpar_filtros():
        var_cargo.set("")
        var_departamento.set("")
        var_status.set("")
        var_data_ini.set("")
        var_data_fim.set("")
        carregar_resultados()

    def carregar_resultados():
        tree.delete(*tree.get_children())
        for func in dados_funcionarios:
            try:
                if (
                    (not var_cargo.get() or func["cargo"] == var_cargo.get()) and
                    (not var_departamento.get() or func["departamento"] == var_departamento.get()) and
                    (not var_status.get() or func["status"] == var_status.get()) and
                    (not var_data_ini.get() or datetime.strptime(func["data_admissao"], "%d/%m/%Y") >= datetime.strptime(var_data_ini.get(), "%d/%m/%Y")) and
                    (not var_data_fim.get() or datetime.strptime(func["data_admissao"], "%d/%m/%Y") <= datetime.strptime(var_data_fim.get(), "%d/%m/%Y"))
                ):
                    tree.insert("", "end", values=(func["id"], func["nome"], func["cpf"], func["cargo"], func["departamento"], func["data_admissao"], func["status"]))
            except:
                continue

    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    colunas = ("ID", "Nome", "CPF", "Cargo", "Departamento", "Admissão", "Status")
    tree = ttk.Treeview(tabela_frame, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    scrollbar = ttk.Scrollbar(tabela_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(fill=tk.X, pady=10)

    def exportar_pdf():
        if not tree.get_children():
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return

        c = canvas.Canvas("relatorio_rh.pdf", pagesize=letter)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 750, "Relatório RH - Funcionários")
        y = 720

        for item in tree.get_children():
            valores = tree.item(item, "values")
            linha = " | ".join(str(v) for v in valores)
            c.drawString(50, y, linha)
            y -= 20
            if y < 50:
                c.showPage()
                y = 750

        c.save()
        messagebox.showinfo("Sucesso", "PDF exportado como 'relatorio_rh.pdf'.")

    def exportar_excel():
        if not tree.get_children():
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Relatório RH"
        ws.append(colunas)

        for item in tree.get_children():
            valores = tree.item(item, "values")
            ws.append(valores)

        wb.save("relatorio_rh.xlsx")
        messagebox.showinfo("Sucesso", "Excel exportado como 'relatorio_rh.xlsx'.")

    btn_pesquisar = tk.Button(filtro_frame, text="🔍 Pesquisar", bg="#1E90FF", fg="white", font=("Segoe UI", 10, "bold"), command=carregar_resultados)
    btn_pesquisar.grid(row=1, column=4, padx=5, pady=5)

    btn_limpar = tk.Button(filtro_frame, text="🧹 Limpar", bg="#696969", fg="white", font=("Segoe UI", 10, "bold"), command=limpar_filtros)
    btn_limpar.grid(row=1, column=5, padx=5, pady=5)

    btn_exportar = tk.Button(botoes_frame, text="📄 Exportar PDF", bg="#228B22", fg="white", font=("Segoe UI", 10, "bold"), command=exportar_pdf)
    btn_exportar.pack(side=tk.LEFT, padx=5)

    btn_excel = tk.Button(botoes_frame, text="📊 Exportar Excel", bg="#006400", fg="white", font=("Segoe UI", 10, "bold"), command=exportar_excel)
    btn_excel.pack(side=tk.LEFT, padx=5)

    carregar_resultados()
