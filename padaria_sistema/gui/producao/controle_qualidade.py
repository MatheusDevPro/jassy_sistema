import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from datetime import datetime

def tela_controle_qualidade(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.title("Controle de Qualidade")

    tk.Label(janela, text="🔬 Controle de Qualidade", font=("Arial", 18, "bold"), fg="#0B3D91").pack(pady=10)

    frame_principal = tk.Frame(janela)
    frame_principal.pack(padx=20, pady=10, fill="both", expand=True)

    # === Seção Dados da Avaliação ===
    secao_dados = tk.LabelFrame(frame_principal, text="📋 Dados da Avaliação", padx=10, pady=10)
    secao_dados.pack(fill="x", padx=10, pady=5)

    tk.Label(secao_dados, text="Produto:").grid(row=0, column=0)
    produto_combo = ttk.Combobox(secao_dados, values=["Pão Francês", "Bolo de Chocolate", "Torta", "Outros"], width=30)
    produto_combo.grid(row=0, column=1, padx=5)
    produto_combo.set("Pão Francês")

    tk.Label(secao_dados, text="Lote:").grid(row=0, column=2)
    lote_entry = tk.Entry(secao_dados)
    lote_entry.grid(row=0, column=3, padx=5)

    tk.Label(secao_dados, text="Data Avaliação:").grid(row=1, column=0)
    data_entry = tk.Entry(secao_dados)
    data_entry.grid(row=1, column=1, padx=5)
    data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    tk.Label(secao_dados, text="Responsável:").grid(row=1, column=2)
    responsavel_entry = tk.Entry(secao_dados)
    responsavel_entry.grid(row=1, column=3, padx=5)

    # === Seção de Avaliação Técnica ===
    secao_avaliacao = tk.LabelFrame(frame_principal, text="🧪 Avaliação Técnica", padx=10, pady=10)
    secao_avaliacao.pack(fill="x", padx=10, pady=5)

    parametros = {
        "Aparência": tk.IntVar(),
        "Peso": tk.IntVar(),
        "Textura": tk.IntVar(),
        "Sabor": tk.IntVar(),
        "Aroma": tk.IntVar(),
        "Validade OK": tk.IntVar(),
        "Embalagem OK": tk.IntVar()
    }

    col = 0
    for i, (param, var) in enumerate(parametros.items()):
        chk = tk.Checkbutton(secao_avaliacao, text=param, variable=var)
        chk.grid(row=i//4, column=col % 4, sticky="w", padx=10)
        col += 1

    # === Seção de Observações ===
    secao_obs = tk.LabelFrame(frame_principal, text="📝 Observações Gerais", padx=10, pady=10)
    secao_obs.pack(fill="x", padx=10, pady=5)

    obs_text = tk.Text(secao_obs, height=3)
    obs_text.pack(fill="x")

    # === Histórico de Avaliações ===
    secao_tabela = tk.LabelFrame(frame_principal, text="📊 Histórico de Qualidade", padx=10, pady=10)
    secao_tabela.pack(fill="both", expand=True, padx=10, pady=5)

    colunas = ("produto", "lote", "data", "responsavel", "aparencia", "peso", "textura", "sabor", "validade", "embalagem")
    tabela = ttk.Treeview(secao_tabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col.capitalize())
        tabela.column(col, width=110)
    tabela.pack(fill="both", expand=True)

    # === Funções ===
    historico = []

    def salvar_aval():
        dados = (
            produto_combo.get(),
            lote_entry.get(),
            data_entry.get(),
            responsavel_entry.get(),
            "✓" if parametros["Aparência"].get() else "✗",
            "✓" if parametros["Peso"].get() else "✗",
            "✓" if parametros["Textura"].get() else "✗",
            "✓" if parametros["Sabor"].get() else "✗",
            "✓" if parametros["Validade OK"].get() else "✗",
            "✓" if parametros["Embalagem OK"].get() else "✗",
        )
        historico.append(dados)
        tabela.insert("", tk.END, values=dados)
        messagebox.showinfo("Sucesso", "Avaliação registrada com sucesso.")
        limpar_campos()

    def limpar_campos():
        lote_entry.delete(0, tk.END)
        responsavel_entry.delete(0, tk.END)
        obs_text.delete("1.0", tk.END)
        for var in parametros.values():
            var.set(0)

    def gerar_pdf():
        c = canvas.Canvas("controle_qualidade.pdf")
        c.drawString(50, 800, "Relatório de Controle de Qualidade")
        y = 770
        for item in tabela.get_children():
            linha = tabela.item(item)["values"]
            c.drawString(50, y, ", ".join(str(i) for i in linha))
            y -= 20
            if y < 50:
                c.showPage()
                y = 800
        c.save()
        messagebox.showinfo("PDF", "PDF gerado com sucesso.")

    def detalhes():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um item da tabela.")
            return
        valores = tabela.item(sel[0])["values"]
        info = "\n".join(f"{colunas[i].capitalize()}: {valores[i]}" for i in range(len(valores)))
        messagebox.showinfo("Detalhes da Avaliação", info)

    # === Botões ===
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="💾 Salvar", bg="#4CAF50", fg="white", width=12, command=salvar_aval).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="🧹 Limpar", bg="#FFC107", fg="black", width=12, command=limpar_campos).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="📄 Gerar PDF", bg="#2196F3", fg="white", width=12, command=gerar_pdf).grid(row=0, column=2, padx=5)
    tk.Button(frame_botoes, text="🔍 Detalhes", bg="#9C27B0", fg="white", width=12, command=detalhes).grid(row=0, column=3, padx=5)
    tk.Button(frame_botoes, text="❌ Fechar", bg="#f44336", fg="white", width=12, command=janela.quit).grid(row=0, column=4, padx=5)

# Teste isolado
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x700")
    tela_controle_qualidade(root)
    root.mainloop()
