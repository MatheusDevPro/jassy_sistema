import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from datetime import datetime

def tela_ordem_producao(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("Ordens de Produção")

    tk.Label(janela, text="🏭 Ordens de Produção", font=("Arial", 18, "bold"), fg="#1F4E79").pack(pady=10)

    # Filtros
    frame_filtros = tk.Frame(janela, bd=2, relief="groove", padx=10, pady=10)
    frame_filtros.pack(padx=20, pady=10, fill="x")

    tk.Label(frame_filtros, text="Data Início:").grid(row=0, column=0)
    data_inicio_entry = tk.Entry(frame_filtros)
    data_inicio_entry.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtros, text="Data Fim:").grid(row=0, column=2)
    data_fim_entry = tk.Entry(frame_filtros)
    data_fim_entry.grid(row=0, column=3, padx=5)

    tk.Label(frame_filtros, text="Status:").grid(row=1, column=0)
    status_combo = ttk.Combobox(frame_filtros, values=["Todos", "Aberta", "Em Produção", "Concluída", "Cancelada"])
    status_combo.grid(row=1, column=1)
    status_combo.set("Todos")

    tk.Label(frame_filtros, text="Responsável:").grid(row=1, column=2)
    responsavel_entry = tk.Entry(frame_filtros)
    responsavel_entry.grid(row=1, column=3)

    tk.Label(frame_filtros, text="Produto:").grid(row=2, column=0)
    produto_entry = tk.Entry(frame_filtros)
    produto_entry.grid(row=2, column=1)

    # Tabela
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(fill="both", expand=True, padx=20)

    colunas = ("data", "ordem", "produto", "quantidade", "responsavel", "status", "obs")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col.capitalize())
        tabela.column(col, width=130)
    tabela.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    ordens_exemplo = [
        ("2025-05-20", "OP001", "Pão Francês", 500, "Carlos", "Aberta", "Início do lote A"),
        ("2025-05-21", "OP002", "Bolo de Cenoura", 100, "Joana", "Em Produção", "Falta ingrediente"),
        ("2025-05-22", "OP003", "Torta de Limão", 60, "Lucas", "Concluída", "Finalizado sem perdas"),
    ]

    def carregar_ordens(dados):
        for i in tabela.get_children():
            tabela.delete(i)
        for ordem in dados:
            tabela.insert("", tk.END, values=ordem)

    carregar_ordens(ordens_exemplo)

    def buscar_ordens():
        filtro = []
        for o in ordens_exemplo:
            if responsavel_entry.get().lower() not in o[4].lower():
                continue
            if produto_entry.get().lower() not in o[2].lower():
                continue
            if status_combo.get() != "Todos" and status_combo.get() != o[5]:
                continue
            filtro.append(o)
        carregar_ordens(filtro)

    def gerar_pdf():
        c = canvas.Canvas("ordens_producao.pdf")
        c.drawString(50, 800, "Ordens de Produção")
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
        ws.append(["Data", "Ordem", "Produto", "Quantidade", "Responsável", "Status", "Observações"])
        for item in tabela.get_children():
            ws.append(tabela.item(item)["values"])
        wb.save("ordens_producao.xlsx")
        messagebox.showinfo("Excel", "Excel gerado com sucesso.")

    def detalhes_ordem():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma ordem.")
            return
        valores = tabela.item(item[0])["values"]
        texto = "\n".join(f"{colunas[i].capitalize()}: {valores[i]}" for i in range(len(valores)))
        messagebox.showinfo("Detalhes da Ordem", texto)

    def nova_ordem():
        def salvar_ordem():
            nova = (
                datetime.now().strftime("%Y-%m-%d"),
                codigo_entry.get(),
                produto_novo_entry.get(),
                int(qtd_entry.get()),
                responsavel_novo_entry.get(),
                status_novo_combo.get(),
                obs_entry.get()
            )
            ordens_exemplo.append(nova)
            carregar_ordens(ordens_exemplo)
            top.destroy()

        top = tk.Toplevel(janela)
        top.title("Nova Ordem de Produção")

        tk.Label(top, text="Código:").grid(row=0, column=0)
        codigo_entry = tk.Entry(top)
        codigo_entry.grid(row=0, column=1)

        tk.Label(top, text="Produto:").grid(row=1, column=0)
        produto_novo_entry = tk.Entry(top)
        produto_novo_entry.grid(row=1, column=1)

        tk.Label(top, text="Quantidade:").grid(row=2, column=0)
        qtd_entry = tk.Entry(top)
        qtd_entry.grid(row=2, column=1)

        tk.Label(top, text="Responsável:").grid(row=3, column=0)
        responsavel_novo_entry = tk.Entry(top)
        responsavel_novo_entry.grid(row=3, column=1)

        tk.Label(top, text="Status:").grid(row=4, column=0)
        status_novo_combo = ttk.Combobox(top, values=["Aberta", "Em Produção", "Concluída", "Cancelada"])
        status_novo_combo.set("Aberta")
        status_novo_combo.grid(row=4, column=1)

        tk.Label(top, text="Observações:").grid(row=5, column=0)
        obs_entry = tk.Entry(top, width=40)
        obs_entry.grid(row=5, column=1)

        tk.Button(top, text="Salvar", bg="green", fg="white", command=salvar_ordem).grid(row=6, column=0, columnspan=2, pady=10)

    def atualizar_tabela():
        carregar_ordens(ordens_exemplo)

    # Botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="🔍 Buscar", bg="#1F4E79", fg="white", width=12, command=buscar_ordens).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="➕ Nova Ordem", bg="#5bc0de", fg="white", width=14, command=nova_ordem).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="📝 Detalhes", bg="#9C27B0", fg="white", width=12, command=detalhes_ordem).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="📄 PDF", bg="#4CAF50", fg="white", width=12, command=gerar_pdf).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="📊 Excel", bg="#2196F3", fg="white", width=12, command=exportar_excel).grid(row=0, column=4, padx=5)
    tk.Button(frame_botoes, text="🔁 Atualizar", bg="#f0ad4e", fg="white", width=12, command=atualizar_tabela).grid(row=0, column=5, padx=5)
    tk.Button(frame_botoes, text="❌ Fechar", bg="#d9534f", fg="white", width=12, command=janela.quit).grid(row=0, column=6, padx=5)

# Teste
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1150x600")
    tela_ordem_producao(root)
    root.mainloop()
