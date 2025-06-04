import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from openpyxl import Workbook
from reportlab.pdfgen import canvas

def tela_relatorios_marketing(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("📊 Relatórios de Marketing")
    
    titulo = tk.Label(janela, text="📈 Relatórios de Marketing", font=("Arial", 18, "bold"), fg="#283593")
    titulo.pack(pady=10)

    frame_filtros = tk.LabelFrame(janela, text="Filtros", padx=10, pady=10, fg="#1A237E", font=("Arial", 10, "bold"))
    frame_filtros.pack(fill="x", padx=20, pady=5)

    tk.Label(frame_filtros, text="Período de:").grid(row=0, column=0)
    data_inicio = tk.Entry(frame_filtros, width=15)
    data_inicio.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtros, text="até:").grid(row=0, column=2)
    data_fim = tk.Entry(frame_filtros, width=15)
    data_fim.grid(row=0, column=3, padx=5)

    tk.Label(frame_filtros, text="Campanha:").grid(row=1, column=0)
    entrada_campanha = tk.Entry(frame_filtros)
    entrada_campanha.grid(row=1, column=1)

    tk.Label(frame_filtros, text="Canal:").grid(row=1, column=2)
    canal_combo = ttk.Combobox(frame_filtros, values=["Todos", "Email", "WhatsApp", "Instagram", "Facebook"])
    canal_combo.set("Todos")
    canal_combo.grid(row=1, column=3)

    tk.Label(frame_filtros, text="Status:").grid(row=2, column=0)
    status_combo = ttk.Combobox(frame_filtros, values=["Todos", "Ativa", "Encerrada", "Pausada"])
    status_combo.set("Todos")
    status_combo.grid(row=2, column=1)

    ativo_var = tk.IntVar()
    tk.Checkbutton(frame_filtros, text="Somente campanhas ativas", variable=ativo_var).grid(row=2, column=2, columnspan=2)

    def buscar():
        filtro = []
        for camp in dados_exemplo:
            if entrada_campanha.get().lower() not in camp[0].lower():
                continue
            if canal_combo.get() != "Todos" and canal_combo.get() != camp[2]:
                continue
            if status_combo.get() != "Todos" and status_combo.get() != camp[3]:
                continue
            if ativo_var.get() == 1 and camp[3] != "Ativa":
                continue
            filtro.append(camp)
        carregar_tabela(filtro)

    def exportar_excel():
        wb = Workbook()
        ws = wb.active
        ws.append(["Campanha", "Data", "Canal", "Status", "Leads", "Conversões", "ROI"])
        for item in tabela.get_children():
            ws.append(tabela.item(item)["values"])
        wb.save("relatorio_marketing.xlsx")
        messagebox.showinfo("Sucesso", "Arquivo Excel gerado com sucesso.")

    def gerar_pdf():
        c = canvas.Canvas("relatorio_marketing.pdf")
        c.drawString(50, 800, "Relatório de Marketing")
        y = 770
        for item in tabela.get_children():
            linha = tabela.item(item)["values"]
            c.drawString(50, y, ", ".join(str(i) for i in linha))
            y -= 20
        c.save()
        messagebox.showinfo("Sucesso", "PDF gerado com sucesso.")

    def enviar_email():
        messagebox.showinfo("Envio por Email", "Relatório enviado por email com sucesso.")

    def enviar_whatsapp():
        messagebox.showinfo("Envio por WhatsApp", "Relatório enviado via WhatsApp.")

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    botoes = [
        ("🔎 Buscar", buscar, "#283593"),
        ("📤 Exportar Excel", exportar_excel, "#1976D2"),
        ("📄 Gerar PDF", gerar_pdf, "#4CAF50"),
        ("📧 Enviar Email", enviar_email, "#7B1FA2"),
        ("📱 WhatsApp", enviar_whatsapp, "#388E3C")
    ]

    for i, (texto, comando, cor) in enumerate(botoes):
        tk.Button(frame_botoes, text=texto, command=comando, bg=cor, fg="white", width=18).grid(row=0, column=i, padx=5)

    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

    colunas = ("campanha", "data", "canal", "status", "leads", "conversoes", "roi")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col.capitalize())
        tabela.column(col, width=140)
    tabela.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    dados_exemplo = [
        ("Campanha Páscoa", "2025-03-25", "Email", "Ativa", 1200, 240, "35%"),
        ("Promoção Black Friday", "2024-11-20", "Instagram", "Encerrada", 3000, 500, "42%"),
        ("Lançamento Produto X", "2025-04-10", "WhatsApp", "Ativa", 900, 150, "28%"),
        ("Campanha Natal", "2024-12-01", "Facebook", "Encerrada", 2000, 410, "38%"),
    ]

    def carregar_tabela(dados):
        for i in tabela.get_children():
            tabela.delete(i)
        for camp in dados:
            tabela.insert("", tk.END, values=camp)

    carregar_tabela(dados_exemplo)

# Execução
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1150x650")
    tela_relatorios_marketing(root)
    root.mainloop()
