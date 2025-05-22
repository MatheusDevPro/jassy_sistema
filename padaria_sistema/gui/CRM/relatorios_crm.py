import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from openpyxl import Workbook

def tela_relatorios_crm(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("Relatórios CRM")

    titulo = tk.Label(janela, text="📊 Relatórios CRM", font=("Arial", 18, "bold"), fg="#1F4E79")
    titulo.pack(pady=10)

    frame_filtros = tk.Frame(janela, bd=2, relief="groove", padx=10, pady=10)
    frame_filtros.pack(pady=10, fill="x", padx=20)

    tk.Label(frame_filtros, text="Data Início:").grid(row=0, column=0)
    entrada_data_inicio = tk.Entry(frame_filtros)
    entrada_data_inicio.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtros, text="Data Fim:").grid(row=0, column=2)
    entrada_data_fim = tk.Entry(frame_filtros)
    entrada_data_fim.grid(row=0, column=3, padx=5)

    tk.Label(frame_filtros, text="Tipo:").grid(row=1, column=0)
    tipo_combo = ttk.Combobox(frame_filtros, values=["Todos", "Atendimento", "Visita", "Ligação", "E-mail", "WhatsApp"])
    tipo_combo.grid(row=1, column=1, padx=5)
    tipo_combo.set("Todos")

    tk.Label(frame_filtros, text="Responsável:").grid(row=1, column=2)
    responsavel_combo = ttk.Combobox(frame_filtros, values=["Todos", "João", "Maria", "Carlos"])
    responsavel_combo.grid(row=1, column=3, padx=5)
    responsavel_combo.set("Todos")

    tk.Label(frame_filtros, text="Cliente:").grid(row=2, column=0)
    entrada_cliente = tk.Entry(frame_filtros)
    entrada_cliente.grid(row=2, column=1, padx=5)

    tk.Label(frame_filtros, text="Status:").grid(row=2, column=2)
    status_combo = ttk.Combobox(frame_filtros, values=["Todos", "Em andamento", "Concluído", "Perdido", "Ganho"])
    status_combo.grid(row=2, column=3, padx=5)
    status_combo.set("Todos")

    # TABELA
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(fill="both", expand=True, padx=20)

    colunas = ("data", "cliente", "tipo", "responsavel", "status", "obs")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col.capitalize())
        tabela.column(col, width=120)
    tabela.pack(side="left", fill="both", expand=True)

    scrollbar_vertical = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scrollbar_vertical.set)
    scrollbar_vertical.pack(side="right", fill="y")

    # DADOS EXEMPLO
    dados_exemplo = [
        ("2025-05-10", "Cliente A", "Atendimento", "João", "Concluído", "Tudo certo"),
        ("2025-05-12", "Cliente B", "WhatsApp", "Maria", "Em andamento", "Retornar amanhã"),
        ("2025-05-15", "Cliente C", "Visita", "Carlos", "Ganho", "Fechou contrato"),
    ]

    def carregar_tabela(dados):
        for i in tabela.get_children():
            tabela.delete(i)
        for dado in dados:
            tabela.insert("", tk.END, values=dado)

    carregar_tabela(dados_exemplo)

    # BOTÕES
    def buscar():
        filtro = []
        for dado in dados_exemplo:
            if entrada_cliente.get().lower() not in dado[1].lower():
                continue
            if tipo_combo.get() != "Todos" and tipo_combo.get() != dado[2]:
                continue
            if responsavel_combo.get() != "Todos" and responsavel_combo.get() != dado[3]:
                continue
            if status_combo.get() != "Todos" and status_combo.get() != dado[4]:
                continue
            filtro.append(dado)
        carregar_tabela(filtro)

    def gerar_pdf():
        c = canvas.Canvas("relatorio_crm.pdf")
        c.drawString(50, 800, "Relatório CRM")
        y = 770
        for item in tabela.get_children():
            valores = tabela.item(item)["values"]
            linha = ", ".join(str(v) for v in valores)
            c.drawString(50, y, linha)
            y -= 20
        c.save()
        messagebox.showinfo("PDF", "PDF gerado com sucesso!")

    def exportar_excel():
        wb = Workbook()
        ws = wb.active
        ws.append(["Data", "Cliente", "Tipo", "Responsável", "Status", "Obs"])
        for item in tabela.get_children():
            valores = tabela.item(item)["values"]
            ws.append(valores)
        wb.save("relatorio_crm.xlsx")
        messagebox.showinfo("Excel", "Arquivo Excel salvo com sucesso!")

    def ver_detalhes():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma linha.")
            return
        valores = tabela.item(item[0])["values"]
        texto = f"Data: {valores[0]}\nCliente: {valores[1]}\nTipo: {valores[2]}\nResponsável: {valores[3]}\nStatus: {valores[4]}\nObs: {valores[5]}"
        messagebox.showinfo("Detalhes", texto)

    def limpar():
        entrada_data_inicio.delete(0, tk.END)
        entrada_data_fim.delete(0, tk.END)
        tipo_combo.set("Todos")
        responsavel_combo.set("Todos")
        entrada_cliente.delete(0, tk.END)
        status_combo.set("Todos")
        carregar_tabela(dados_exemplo)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="🔎 Buscar", bg="#1F4E79", fg="white", width=12, command=buscar).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="📄 Gerar PDF", bg="#4CAF50", fg="white", width=15, command=gerar_pdf).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="📊 Exportar Excel", bg="#2196F3", fg="white", width=15, command=exportar_excel).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="📋 Detalhes", bg="#9C27B0", fg="white", width=15, command=ver_detalhes).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="🧹 Limpar Filtros", bg="#f0ad4e", fg="white", width=15, command=limpar).grid(row=0, column=4, padx=5)
    tk.Button(frame_botoes, text="❌ Fechar", bg="#d9534f", fg="white", width=15, command=janela.quit).grid(row=0, column=5, padx=5)

# TESTE
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    tela_relatorios_crm(root)
    root.mainloop()
