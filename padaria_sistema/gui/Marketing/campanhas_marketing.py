import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.pdfgen import canvas
from openpyxl import Workbook
from datetime import datetime
import os

def tela_campanhas_marketing(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("📢 Campanhas de Marketing")

    estilo_bg = "#f2f2f2"
    janela.configure(bg=estilo_bg)

    titulo = tk.Label(janela, text="📢 Campanhas de Marketing", font=("Arial", 20, "bold"), fg="white", bg="#1f4e79")
    titulo.pack(fill="x")

    frame_form = tk.Frame(janela, bg=estilo_bg)
    frame_form.pack(fill="x", padx=20, pady=10)

    def criar_label_input(label_text, row, column):
        tk.Label(frame_form, text=label_text, bg=estilo_bg).grid(row=row, column=column, sticky="w")
        entry = tk.Entry(frame_form, width=30)
        entry.grid(row=row, column=column + 1, padx=5, pady=3)
        return entry

    titulo_entry = criar_label_input("Título:", 0, 0)
    tipo_entry = criar_label_input("Tipo de Campanha:", 0, 2)
    publico_entry = criar_label_input("Público-Alvo:", 1, 0)
    data_inicio_entry = criar_label_input("Data Início:", 1, 2)
    data_fim_entry = criar_label_input("Data Fim:", 2, 0)
    orcamento_entry = criar_label_input("Orçamento (R$):", 2, 2)

    tk.Label(frame_form, text="Canais:", bg=estilo_bg).grid(row=3, column=0, sticky="w")
    canais = {
        "Email": tk.BooleanVar(),
        "WhatsApp": tk.BooleanVar(),
        "Redes Sociais": tk.BooleanVar(),
        "TV": tk.BooleanVar(),
        "Rádio": tk.BooleanVar()
    }
    col = 1
    for canal, var in canais.items():
        tk.Checkbutton(frame_form, text=canal, variable=var, bg=estilo_bg).grid(row=3, column=col, sticky="w")
        col += 1

    status_combo = ttk.Combobox(frame_form, values=["Planejada", "Em andamento", "Concluída", "Cancelada"], width=28)
    status_combo.set("Planejada")
    tk.Label(frame_form, text="Status:", bg=estilo_bg).grid(row=4, column=0, sticky="w")
    status_combo.grid(row=4, column=1, sticky="w")

    tk.Label(frame_form, text="Descrição:", bg=estilo_bg).grid(row=5, column=0, sticky="nw")
    descricao_text = tk.Text(frame_form, height=4, width=60)
    descricao_text.grid(row=5, column=1, columnspan=3, pady=5)

    tk.Label(frame_form, text="Observações:", bg=estilo_bg).grid(row=6, column=0, sticky="nw")
    obs_text = tk.Text(frame_form, height=3, width=60)
    obs_text.grid(row=6, column=1, columnspan=3, pady=5)

    imagem_path = tk.StringVar()
    def selecionar_imagem():
        path = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if path:
            imagem_path.set(path)
            messagebox.showinfo("Imagem", f"Imagem selecionada: {os.path.basename(path)}")

    tk.Button(frame_form, text="📷 Upload Logotipo", command=selecionar_imagem, bg="#5bc0de", fg="white").grid(row=7, column=1, pady=10, sticky="w")

    campanhas = []

    def atualizar_tabela():
        for i in tabela.get_children():
            tabela.delete(i)
        for campanha in campanhas:
            tabela.insert("", "end", values=campanha)

    def adicionar_campanha():
        nova = (
            titulo_entry.get(), tipo_entry.get(), publico_entry.get(),
            data_inicio_entry.get(), data_fim_entry.get(),
            orcamento_entry.get(), status_combo.get(),
            ", ".join([k for k, v in canais.items() if v.get()]),
            descricao_text.get("1.0", "end").strip(),
            obs_text.get("1.0", "end").strip(),
            imagem_path.get()
        )
        campanhas.append(nova)
        atualizar_tabela()
        messagebox.showinfo("Sucesso", "Campanha adicionada com sucesso!")

    def exportar_excel():
        wb = Workbook()
        ws = wb.active
        ws.append(["Título", "Tipo", "Público", "Início", "Fim", "Orçamento", "Status", "Canais", "Descrição", "Observações", "Imagem"])
        for c in campanhas:
            ws.append(c)
        wb.save("campanhas.xlsx")
        messagebox.showinfo("Exportado", "Campanhas exportadas para Excel.")

    def gerar_pdf():
        c = canvas.Canvas("campanhas.pdf")
        c.drawString(50, 800, "Relatório de Campanhas")
        if imagem_path.get():
            try:
                c.drawImage(imagem_path.get(), 450, 750, width=100, height=50)
            except:
                pass
        y = 770
        for camp in campanhas:
            c.drawString(50, y, f"{camp[0]} | {camp[1]} | {camp[6]}")
            y -= 20
        c.save()
        messagebox.showinfo("PDF", "PDF gerado com sucesso.")

    def enviar():
        messagebox.showinfo("Envio", "Campanhas enviadas por Email e WhatsApp (simulado).")

    def imprimir():
        messagebox.showinfo("Impressão", "Enviado para impressão (simulado).")

    frame_botoes = tk.Frame(janela, bg=estilo_bg)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="➕ Adicionar", command=adicionar_campanha, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="📄 PDF", command=gerar_pdf, bg="#673AB7", fg="white", width=12).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="📊 Excel", command=exportar_excel, bg="#2196F3", fg="white", width=12).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="📤 Enviar", command=enviar, bg="#f0ad4e", fg="white", width=12).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="🖨️ Imprimir", command=imprimir, bg="#795548", fg="white", width=12).grid(row=0, column=4, padx=5)

    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

    colunas = ("titulo", "tipo", "publico", "inicio", "fim", "orcamento", "status", "canais", "descricao", "obs", "imagem")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col.capitalize())
        tabela.column(col, width=100, anchor="center")
    tabela.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x720")
    tela_campanhas_marketing(root)
    root.mainloop()