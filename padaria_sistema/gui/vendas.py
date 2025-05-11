import tkinter as tk
from tkinter import messagebox
import os
import csv

def tela_vendas(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f9f9f9")
    frame.pack(fill="both", expand=True)

    titulo = tk.Label(frame, text="Registro de Vendas 💰", font=("Helvetica", 18, "bold"),
                      bg="#f9f9f9", fg="#006699")
    titulo.pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#f9f9f9")
    campos_frame.pack(pady=10)

    campos = {
        "codigo": tk.Entry(campos_frame, width=30),
        "Produto": tk.Entry(campos_frame, width=30),
        "descrição": tk.Entry(campos_frame, width=30),
        "Quantidade": tk.Entry(campos_frame, width=30),
        "Preço Unitário": tk.Entry(campos_frame, width=30),
        "Data da Venda": tk.Entry(campos_frame, width=30),
        "Valor Total": tk.Entry(campos_frame, width=30),
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#f9f9f9") \
            .grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entrada.grid(row=i, column=1, padx=5, pady=5, sticky="w")

    def calcular_total():
        try:
            quantidade = int(campos["Quantidade"].get())
            preco_unitario = float(campos["Preço Unitário"].get())
            return quantidade * preco_unitario
        except ValueError:
            messagebox.showwarning("Erro", "Insira valores válidos para Quantidade e Preço Unitário.")
            return None

    def atualizar_exibicao_vendas():
        texto.config(state="normal")
        texto.delete(1.0, tk.END)
        total_geral = 0.0

        texto.insert(tk.END, "Produto | Quantidade | Preço Unitário | Data da Venda | Total\n")
        texto.insert(tk.END, "-" * 80 + "\n")

        try:
            with open("dados/vendas.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    texto.insert(tk.END, linha)
                    if "Total:" in linha:
                        try:
                            total_str = linha.strip().split("Total:")[1].strip()
                            total_geral += float(total_str)
                        except (IndexError, ValueError):
                            continue
        except FileNotFoundError:
            texto.insert(tk.END, "Nenhuma venda registrada ainda.\n")

        texto.config(state="disabled")
        label_total_geral.config(text=f"💵 Valor Total de Vendas: R$ {total_geral:.2f}")

    def salvar_venda():
        dados = [entrada.get() for entrada in campos.values()]
        total = calcular_total()

        if all(dados) and total is not None:
            os.makedirs("dados", exist_ok=True)
            with open("dados/vendas.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + f" | Total: {total:.2f}\n")
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
            atualizar_exibicao_vendas()
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos corretamente.")

    def exportar_csv():
        try:
            with open("dados/vendas.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/vendas.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(["Produto", "Quantidade", "Preço Unitário", "Data da Venda", "Total"])
                for linha in linhas:
                    linha = [item.strip().replace("Total:", "").strip() for item in linha]
                    if len(linha) == 5:
                        writer.writerow(linha)
            messagebox.showinfo("Exportado", "Dados exportados para 'dados/vendas.csv'.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado para exportar.")

    # Frame dos botões
    botoes_frame = tk.Frame(frame, bg="#f9f9f9")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="Registrar Venda 💾", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), command=salvar_venda).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="Exportar CSV 📁", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), command=exportar_csv).pack(side="left", padx=10)

    label_total_geral = tk.Label(frame, text="💵 Valor Total de Vendas: R$ 0.00",
                                 font=("Helvetica", 12, "bold"), bg="#f9f9f9", fg="#CC0000")
    label_total_geral.pack(pady=5)

    texto = tk.Text(frame, height=12, width=90, state="disabled", font=("Courier", 10))
    texto.pack(pady=10)

    atualizar_exibicao_vendas()
