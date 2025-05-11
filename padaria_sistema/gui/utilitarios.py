import tkinter as tk
from tkinter import messagebox

# Função para exibir tela de utilitários
def tela_utilitarios(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
             widget.destroy()

    frame = tk.Frame(janela, bg="#f9f9f9")
    frame.pack(fill="both", expand=True)

    titulo = tk.Label(frame, text="Utilitários 🛠️", font=("Helvetica", 18, "bold"), bg="#f9f9f9", fg="#006699")
    titulo.pack(pady=10)

    # Função para limpar todos os dados
    def limpar_dados():
        try:
            with open("dados/funcionarios.txt", "w", encoding="utf-8") as arq:
                arq.write("")
            with open("dados/fornecedores.txt", "w", encoding="utf-8") as arq:
                arq.write("")
            with open("dados/financeiro.txt", "w", encoding="utf-8") as arq:
                arq.write("")
            with open("dados/produtos.txt", "w", encoding="utf-8") as arq:
                arq.write("")
            with open("dados/vendas.txt", "w", encoding="utf-8") as arq:
                arq.write("")
            messagebox.showinfo("Sucesso", "Todos os dados foram limpos com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar os dados: {e}")

    tk.Button(frame, text="Limpar Dados 📂", bg="#ff6347", fg="white", font=("Helvetica", 12, "bold"), command=limpar_dados).pack(pady=15)

    # Função para exibir relatórios
    def exibir_relatorio():
        try:
            with open("dados/financeiro.txt", "r", encoding="utf-8") as f:
                dados = f.read()
            messagebox.showinfo("Relatório Financeiro", dados)
        except FileNotFoundError:
            messagebox.showinfo("Relatório Financeiro", "Nenhum dado financeiro registrado.")
    
    tk.Button(frame, text="Exibir Relatório Financeiro 📑", bg="#339966", fg="white", font=("Helvetica", 12, "bold"), command=exibir_relatorio).pack(pady=15)
