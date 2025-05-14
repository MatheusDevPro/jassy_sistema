import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime
from matplotlib import pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas

def tela_demonstrativo_lucros(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
          widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📉 Demonstrativo de Lucros", font=("Helvetica", 18, "bold"),
             bg="#f8f8ff", fg="#004d66").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#f8f8ff")
    campos_frame.pack(pady=10)

    campos = {
        "Data": tk.Entry(campos_frame, width=25),
        "Receita": tk.Entry(campos_frame, width=25),
        "Despesa": tk.Entry(campos_frame, width=25),
        "Categoria": ttk.Combobox(campos_frame, values=["Venda", "Serviço", "Outros"], width=22)
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#f8f8ff") \
            .grid(row=i, column=0, padx=10, pady=6, sticky="e")
        entrada.grid(row=i, column=1, padx=10, pady=6, sticky="w")

    def adicionar_entrada():
        dados = [entrada.get().strip() for entrada in campos.values()]
        if all(dados):
            os.makedirs("dados", exist_ok=True)
            with open("dados/lucros.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Entrada adicionada com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            carregar_dados()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")

    def calcular_lucro():
        total_receita = 0.0
        total_despesa = 0.0
        try:
            with open("dados/lucros.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    _, receita, despesa, _ = [v.strip() for v in linha.strip().split("|")]
                    total_receita += float(receita)
                    total_despesa += float(despesa)
            lucro = total_receita - total_despesa
            messagebox.showinfo("Lucro Calculado", f"💰 Receita: R${total_receita:.2f}\n💸 Despesa: R${total_despesa:.2f}\n📊 Lucro: R${lucro:.2f}")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Nenhum dado encontrado.")

    def exportar_csv():
        try:
            with open("dados/lucros.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/lucros.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(["Data", "Receita", "Despesa", "Categoria"])
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados para 'lucros.csv'")
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de dados não encontrado.")

    def gerar_pdf():
        try:
            with open("dados/lucros.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]

            pdf_path = "dados/lucros_relatorio.pdf"
            c = pdf_canvas.Canvas(pdf_path, pagesize=A4)
            c.setFont("Helvetica", 12)
            c.drawString(50, 800, "📉 Relatório de Demonstrativo de Lucros")
            y = 770
            for linha in linhas:
                texto = f"{linha[0]} | Receita: R${linha[1]} | Despesa: R${linha[2]} | Categoria: {linha[3]}"
                c.drawString(50, y, texto)
                y -= 20
                if y < 50:
                    c.showPage()
                    y = 800
            c.save()
            messagebox.showinfo("PDF Gerado", f"Relatório salvo em '{pdf_path}'")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

    def gerar_grafico():
        datas, receitas, despesas = [], [], []
        try:
            with open("dados/lucros.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    data, receita, despesa, _ = [v.strip() for v in linha.strip().split("|")]
                    datas.append(data)
                    receitas.append(float(receita))
                    despesas.append(float(despesa))
            lucro = [r - d for r, d in zip(receitas, despesas)]
            plt.figure(figsize=(10, 5))
            plt.plot(datas, receitas, label="Receita", marker='o')
            plt.plot(datas, despesas, label="Despesa", marker='o')
            plt.plot(datas, lucro, label="Lucro", linestyle="--", marker='x')
            plt.title("Gráfico de Lucros")
            plt.xlabel("Data")
            plt.ylabel("R$ Valor")
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.grid(True)
            plt.show()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=10)

    ttk.Button(botoes_frame, text="➕ Adicionar Entrada", width=20, command=adicionar_entrada).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="💰 Calcular Lucro", width=20, command=calcular_lucro).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="📁 Exportar CSV", width=20, command=exportar_csv).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="📄 Gerar PDF", width=20, command=gerar_pdf).pack(side="left", padx=10)
    ttk.Button(botoes_frame, text="📈 Gerar Gráfico", width=20, command=gerar_grafico).pack(side="left", padx=10)

    # Tabela
    tabela_frame = tk.LabelFrame(frame, text="📊 Relatório de Lucros", bg="#f8f8ff", font=("Helvetica", 12, "bold"),
                                 fg="#003d66", bd=2, relief="groove")
    tabela_frame.pack(padx=20, pady=15, fill="both", expand=True)

    colunas = ("Data", "Receita", "Despesa", "Categoria")
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=12)
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=150, anchor="center")

    scroll = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll.set)

    tabela.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    scroll.grid(row=0, column=1, sticky="ns", pady=8)

    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    def carregar_dados():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/lucros.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    dados = [dado.strip() for dado in linha.strip().split("|")]
                    if len(dados) == 4:
                        tabela.insert("", "end", values=dados)
        except FileNotFoundError:
            pass

    carregar_dados()
