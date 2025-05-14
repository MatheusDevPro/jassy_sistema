import tkinter as tk
from tkinter import messagebox

def tela_financeiro(janela):
    # Limpa a janela atual
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
          widget.destroy()

    # Criação do frame principal da tela
    frame = tk.Frame(janela, bg="#e6f2ff")
    frame.pack(fill="both", expand=True)

    # Título
    tk.Label(frame, text="📊 Fluxo de Caixa", font=("Helvetica", 18, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    # Frame para os campos de entrada de dados
    campos_frame = tk.Frame(frame, bg="#e6f2ff")
    campos_frame.pack(pady=10)

    # Definir rótulos e entradas
    campos = {
        "Receitas": tk.Entry(campos_frame, width=30),
        "Despesas": tk.Entry(campos_frame, width=30),
        "Saldo Inicial": tk.Entry(campos_frame, width=30),
        "Saldo Atual": tk.Entry(campos_frame, width=30)
    }

    # Exibir os campos e rótulos
    for i, (rotulo, entrada) in enumerate(campos.items()):
        linha = i // 2
        coluna = (i % 2) * 2
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f2ff", fg="#003d66") \
            .grid(row=linha, column=coluna, padx=8, pady=6, sticky="e")
        entrada.grid(row=linha, column=coluna + 1, padx=8, pady=6, sticky="w")

    # Função para calcular e exibir o saldo
    def calcular_fluxo():
        try:
            # Obter os valores das entradas
            receitas = float(campos["Receitas"].get().strip())
            despesas = float(campos["Despesas"].get().strip())
            saldo_inicial = float(campos["Saldo Inicial"].get().strip())

            # Calcular o saldo atual
            saldo_atual = saldo_inicial + receitas - despesas
            campos["Saldo Atual"].delete(0, tk.END)
            campos["Saldo Atual"].insert(0, f"R$ {saldo_atual:.2f}")
        except ValueError:
            messagebox.showwarning("Atenção", "Por favor, insira valores numéricos válidos.")

    # Botão para calcular o fluxo de caixa
    tk.Button(frame, text="💰 Calcular Fluxo de Caixa", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=calcular_fluxo).pack(pady=10)

    # Exibição do botão de salvar (para salvar os dados em um arquivo ou banco)
    def salvar_fluxo():
        try:
            receitas = float(campos["Receitas"].get().strip())
            despesas = float(campos["Despesas"].get().strip())
            saldo_inicial = float(campos["Saldo Inicial"].get().strip())
            saldo_atual = float(campos["Saldo Atual"].get().strip())

            # Salvar em arquivo ou banco (exemplo simples de salvamento em texto)
            with open("dados/fluxo_caixa.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(f"Receitas: R$ {receitas:.2f}, Despesas: R$ {despesas:.2f}, "
                               f"Saldo Inicial: R$ {saldo_inicial:.2f}, Saldo Atual: R$ {saldo_atual:.2f}\n")

            messagebox.showinfo("Sucesso", "Fluxo de caixa salvo com sucesso!")

        except ValueError:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos corretamente.")

    # Botão de salvar fluxo de caixa
    tk.Button(frame, text="💾 Salvar Fluxo de Caixa", bg="#0059b3", fg="white",
              font=("Helvetica", 12, "bold"), width=20, command=salvar_fluxo).pack(pady=10)
