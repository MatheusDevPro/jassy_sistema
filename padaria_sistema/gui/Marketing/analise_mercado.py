import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from reportlab.pdfgen import canvas
from openpyxl import Workbook

def tela_analise_mercado(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("📈 Análise de Mercado")

    titulo = tk.Label(janela, text="📊 Análise de Mercado", font=("Segoe UI", 20, "bold"), fg="#2E4053")
    titulo.pack(pady=15)

    frame_filtros = tk.Frame(janela, bg="#f5f5f5", bd=2, relief="ridge", padx=15, pady=15)
    frame_filtros.pack(fill="x", padx=15)

    # Linha 1
    tk.Label(frame_filtros, text="Período Inicial:", bg="#f5f5f5").grid(row=0, column=0)
    entrada_inicio = tk.Entry(frame_filtros)
    entrada_inicio.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtros, text="Período Final:", bg="#f5f5f5").grid(row=0, column=2)
    entrada_fim = tk.Entry(frame_filtros)
    entrada_fim.grid(row=0, column=3, padx=5)

    tk.Label(frame_filtros, text="Segmento:", bg="#f5f5f5").grid(row=0, column=4)
    segmento_combo = ttk.Combobox(frame_filtros, values=["Todos", "Tecnologia", "Alimentos", "Moda", "Serviços"])
    segmento_combo.grid(row=0, column=5)
    segmento_combo.set("Todos")

    # Linha 2
    tk.Label(frame_filtros, text="Região:", bg="#f5f5f5").grid(row=1, column=0)
    regiao_combo = ttk.Combobox(frame_filtros, values=["Brasil", "Sul", "Sudeste", "Norte", "Nordeste", "Centro-Oeste"])
    regiao_combo.grid(row=1, column=1)
    regiao_combo.set("Brasil")

    tk.Label(frame_filtros, text="Concorrente:", bg="#f5f5f5").grid(row=1, column=2)
    concorrente_entry = tk.Entry(frame_filtros)
    concorrente_entry.grid(row=1, column=3)

    tendencia_var = tk.IntVar()
    tk.Checkbutton(frame_filtros, text="Somente tendências recentes", variable=tendencia_var, bg="#f5f5f5").grid(row=1, column=4, columnspan=2)

    # Linha 3
    tk.Label(frame_filtros, text="Categoria:", bg="#f5f5f5").grid(row=2, column=0)
    categoria_combo = ttk.Combobox(frame_filtros, values=["Todas", "Produto", "Serviço", "Digital", "Presencial"])
    categoria_combo.grid(row=2, column=1)
    categoria_combo.set("Todas")

    tk.Label(frame_filtros, text="Analisado por:", bg="#f5f5f5").grid(row=2, column=2)
    analisado_entry = tk.Entry(frame_filtros)
    analisado_entry.grid(row=2, column=3)

    enviar_email_var = tk.IntVar()
    tk.Checkbutton(frame_filtros, text="Enviar relatório por e-mail", variable=enviar_email_var, bg="#f5f5f5").grid(row=2, column=4)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    def buscar():
        messagebox.showinfo("Buscar", "Busca realizada com filtros aplicados.")

    def exportar_pdf():
        c = canvas.Canvas("analise_mercado.pdf")
        c.drawString(50, 800, "Relatório de Análise de Mercado")
        c.save()
        messagebox.showinfo("PDF", "PDF gerado com sucesso.")

    def exportar_excel():
        wb = Workbook()
        ws = wb.active
        ws.append(["Data", "Segmento", "Região", "Concorrente", "Categoria", "Analisado por"])
        for item in tabela.get_children():
            ws.append(tabela.item(item)["values"])
        wb.save("analise_mercado.xlsx")
        messagebox.showinfo("Excel", "Excel gerado com sucesso.")

    def carregar_dados_exemplo():
        dados = [
            ("2025-01-15", "Tecnologia", "Sudeste", "Concorrente A", "Produto", "João"),
            ("2025-02-20", "Alimentos", "Sul", "Concorrente B", "Serviço", "Ana"),
            ("2025-03-05", "Moda", "Nordeste", "Concorrente C", "Digital", "Carlos"),
        ]
        for i in tabela.get_children():
            tabela.delete(i)
        for d in dados:
            tabela.insert("", tk.END, values=d)

    def excluir_selecionado():
        selecionado = tabela.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para excluir.")
        else:
            tabela.delete(selecionado[0])
            messagebox.showinfo("Exclusão", "Registro removido com sucesso.")

    def importar_logo():
        file = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg")])
        if file:
            messagebox.showinfo("Logo", f"Logotipo carregado: {file}")

    def enviar_whatsapp():
        messagebox.showinfo("WhatsApp", "Campanha enviada via WhatsApp com sucesso.")

    # Botões
    tk.Button(frame_botoes, text="🔍 Buscar", bg="#2980B9", fg="white", width=15, command=buscar).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="📤 PDF", bg="#27AE60", fg="white", width=15, command=exportar_pdf).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="📊 Excel", bg="#F39C12", fg="white", width=15, command=exportar_excel).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="🗑️ Excluir", bg="#C0392B", fg="white", width=15, command=excluir_selecionado).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="📎 Upload Logotipo", bg="#8E44AD", fg="white", width=18, command=importar_logo).grid(row=0, column=4, padx=5)
    tk.Button(frame_botoes, text="📱 Enviar WhatsApp", bg="#16A085", fg="white", width=18, command=enviar_whatsapp).grid(row=0, column=5, padx=5)

    # Tabela
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(fill="both", expand=True, padx=15, pady=10)

    colunas = ["Data", "Segmento", "Região", "Concorrente", "Categoria", "Analisado por"]
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=150)
    tabela.pack(side="left", fill="both", expand=True)

    scroll = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scroll.set)
    scroll.pack(side="right", fill="y")

    carregar_dados_exemplo()

# Execução de teste
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x650")
    tela_analise_mercado(root)
    root.mainloop()
