import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from datetime import datetime

chamados_exemplo = [
    ("2025-05-20", "Pane elétrica", "Elétrica", "João", "Máquina 01", "Alta", "Aberto", "Disjuntor queimado"),
    ("2025-05-18", "Atualização sistema", "TI", "Carlos", "Servidor", "Média", "Fechado", "Atualização concluída"),
    ("2025-05-21", "Falha mecânica", "Mecânica", "Ana", "Máquina 05", "Crítica", "Em andamento", "Correia rompida"),
]

def tela_chamados_producao(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("Chamados Produção")

    titulo = tk.Label(janela, text="📞 Chamados - Produção", font=("Arial", 18, "bold"), fg="#1F4E79")
    titulo.pack(pady=10)

    frame_filtros = tk.Frame(janela, bd=2, relief="groove", padx=10, pady=10)
    frame_filtros.pack(pady=10, fill="x", padx=20)

    # Campos de filtro
    entrada_data_inicio = tk.Entry(frame_filtros)
    entrada_data_fim = tk.Entry(frame_filtros)
    status_combo = ttk.Combobox(frame_filtros, values=["Todos", "Aberto", "Em andamento", "Fechado", "Cancelado"])
    prioridade_combo = ttk.Combobox(frame_filtros, values=["Todas", "Baixa", "Média", "Alta", "Crítica"])
    responsavel_entry = tk.Entry(frame_filtros)
    maquina_entry = tk.Entry(frame_filtros)
    tipo_combo = ttk.Combobox(frame_filtros, values=["Todos", "Elétrica", "Mecânica", "TI", "Produção", "Qualidade"])
    descricao_entry = tk.Entry(frame_filtros)

    # Posicionamento
    tk.Label(frame_filtros, text="Data Início:").grid(row=0, column=0)
    entrada_data_inicio.grid(row=0, column=1, padx=5)
    tk.Label(frame_filtros, text="Data Fim:").grid(row=0, column=2)
    entrada_data_fim.grid(row=0, column=3, padx=5)
    tk.Label(frame_filtros, text="Status:").grid(row=1, column=0)
    status_combo.grid(row=1, column=1)
    status_combo.set("Todos")
    tk.Label(frame_filtros, text="Prioridade:").grid(row=1, column=2)
    prioridade_combo.grid(row=1, column=3)
    prioridade_combo.set("Todas")
    tk.Label(frame_filtros, text="Responsável:").grid(row=2, column=0)
    responsavel_entry.grid(row=2, column=1)
    tk.Label(frame_filtros, text="Máquina:").grid(row=2, column=2)
    maquina_entry.grid(row=2, column=3)
    tk.Label(frame_filtros, text="Tipo:").grid(row=3, column=0)
    tipo_combo.grid(row=3, column=1)
    tipo_combo.set("Todos")
    tk.Label(frame_filtros, text="Descrição Contém:").grid(row=3, column=2)
    descricao_entry.grid(row=3, column=3)

    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(fill="both", expand=True, padx=20)

    colunas = ("data", "titulo", "tipo", "responsavel", "maquina", "prioridade", "status", "descricao")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col.capitalize())
        tabela.column(col, width=120)
    tabela.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    def carregar_tabela(dados):
        for i in tabela.get_children():
            tabela.delete(i)
        for chamado in dados:
            tabela.insert("", tk.END, values=chamado)

    carregar_tabela(chamados_exemplo)

    def buscar():
        filtro = []
        for c in chamados_exemplo:
            if responsavel_entry.get().lower() not in c[3].lower():
                continue
            if maquina_entry.get().lower() not in c[4].lower():
                continue
            if status_combo.get() != "Todos" and status_combo.get() != c[6]:
                continue
            if prioridade_combo.get() != "Todas" and prioridade_combo.get() != c[5]:
                continue
            if tipo_combo.get() != "Todos" and tipo_combo.get() != c[2]:
                continue
            if descricao_entry.get().lower() not in c[7].lower():
                continue
            filtro.append(c)
        carregar_tabela(filtro)

    def gerar_pdf():
        c = canvas.Canvas("chamados_producao.pdf")
        c.drawString(50, 800, "Chamados - Produção")
        y = 770
        for item in tabela.get_children():
            linha = tabela.item(item)["values"]
            c.drawString(50, y, ", ".join(str(i) for i in linha))
            y -= 20
        c.save()
        messagebox.showinfo("PDF", "PDF gerado com sucesso.")

    def exportar_excel():
        wb = Workbook()
        ws = wb.active
        ws.append(["Data", "Título", "Tipo", "Responsável", "Máquina", "Prioridade", "Status", "Descrição"])
        for item in tabela.get_children():
            ws.append(tabela.item(item)["values"])
        wb.save("chamados_producao.xlsx")
        messagebox.showinfo("Excel", "Excel gerado com sucesso.")

    def detalhes():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um chamado.")
            return
        valores = tabela.item(item[0])["values"]
        texto = "\n".join(f"{colunas[i].capitalize()}: {valores[i]}" for i in range(len(valores)))
        messagebox.showinfo("Detalhes do Chamado", texto)

    def novo_chamado():
        def salvar():
            data = datetime.now().strftime("%Y-%m-%d")
            titulo = titulo_entry.get()
            tipo = tipo_novo.get()
            responsavel = responsavel_novo.get()
            maquina = maquina_novo.get()
            prioridade = prioridade_novo.get()
            status = status_novo.get()
            descricao = descricao_novo.get("1.0", tk.END).strip()
            if not titulo:
                messagebox.showwarning("Aviso", "Informe o título.")
                return
            chamado = (data, titulo, tipo, responsavel, maquina, prioridade, status, descricao)
            chamados_exemplo.append(chamado)
            carregar_tabela(chamados_exemplo)
            janela_cadastro.destroy()

        janela_cadastro = tk.Toplevel(janela)
        janela_cadastro.title("Novo Chamado")

        tk.Label(janela_cadastro, text="Título:").grid(row=0, column=0)
        titulo_entry = tk.Entry(janela_cadastro)
        titulo_entry.grid(row=0, column=1)

        tk.Label(janela_cadastro, text="Tipo:").grid(row=1, column=0)
        tipo_novo = ttk.Combobox(janela_cadastro, values=["Elétrica", "Mecânica", "TI", "Produção", "Qualidade"])
        tipo_novo.grid(row=1, column=1)
        tipo_novo.set("Elétrica")

        tk.Label(janela_cadastro, text="Responsável:").grid(row=2, column=0)
        responsavel_novo = tk.Entry(janela_cadastro)
        responsavel_novo.grid(row=2, column=1)

        tk.Label(janela_cadastro, text="Máquina:").grid(row=3, column=0)
        maquina_novo = tk.Entry(janela_cadastro)
        maquina_novo.grid(row=3, column=1)

        tk.Label(janela_cadastro, text="Prioridade:").grid(row=4, column=0)
        prioridade_novo = ttk.Combobox(janela_cadastro, values=["Baixa", "Média", "Alta", "Crítica"])
        prioridade_novo.grid(row=4, column=1)
        prioridade_novo.set("Média")

        tk.Label(janela_cadastro, text="Status:").grid(row=5, column=0)
        status_novo = ttk.Combobox(janela_cadastro, values=["Aberto", "Em andamento", "Fechado", "Cancelado"])
        status_novo.grid(row=5, column=1)
        status_novo.set("Aberto")

        tk.Label(janela_cadastro, text="Descrição:").grid(row=6, column=0)
        descricao_novo = tk.Text(janela_cadastro, height=4, width=30)
        descricao_novo.grid(row=6, column=1)

        tk.Button(janela_cadastro, text="Salvar", command=salvar, bg="green", fg="white").grid(row=7, column=0, columnspan=2, pady=5)

    def atualizar():
        carregar_tabela(chamados_exemplo)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="🔎 Buscar", bg="#1F4E79", fg="white", width=12, command=buscar).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="➕ Novo Chamado", bg="#5bc0de", fg="white", width=15, command=novo_chamado).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="📝 Detalhes", bg="#9C27B0", fg="white", width=12, command=detalhes).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="📄 PDF", bg="#4CAF50", fg="white", width=12, command=gerar_pdf).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="📊 Excel", bg="#2196F3", fg="white", width=12, command=exportar_excel).grid(row=0, column=4, padx=5)
    tk.Button(frame_botoes, text="🔁 Atualizar", bg="#f0ad4e", fg="white", width=12, command=atualizar).grid(row=0, column=5, padx=5)
    tk.Button(frame_botoes, text="❌ Fechar", bg="#d9534f", fg="white", width=12, command=janela.quit).grid(row=0, column=6, padx=5)

# Teste
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x650")
    tela_chamados_producao(root)
    root.mainloop()
