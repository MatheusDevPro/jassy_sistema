import tkinter as tk
from tkinter import messagebox

# Função para exibir tela de fornecedores
def tela_fornecedores(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':  # Não remove o menu
             widget.destroy()

    frame = tk.Frame(janela, bg="#e6f7ff")
    frame.pack(fill="both", expand=True)

    titulo = tk.Label(frame, text="Cadastro de Fornecedores 🏢", font=("Helvetica", 18, "bold"), bg="#e6f7ff", fg="#006699")
    titulo.pack(pady=10)

    campos = {
        "Nome": tk.Entry(frame, width=40),
        "CNPJ": tk.Entry(frame, width=40),
        "Telefone": tk.Entry(frame, width=40),
        "Email": tk.Entry(frame, width=40)
    }

    for rotulo, entrada in campos.items():
        tk.Label(frame, text=rotulo + ":", font=("Helvetica", 12), bg="#e6f7ff").pack(pady=2)
        entrada.pack(pady=2)

    # Função para salvar dados de fornecedores
    def salvar_fornecedor():
        dados = [entrada.get() for entrada in campos.values()]
        if all(dados):
            with open("dados/fornecedores.txt", "a", encoding="utf-8") as arq:
                arq.write(" | ".join(dados) + "\n")
            messagebox.showinfo("Sucesso", "Fornecedor salvo com sucesso.")
            for entrada in campos.values():
                entrada.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")

    tk.Button(frame, text="Salvar Fornecedor 💾", bg="#339966", fg="white", font=("Helvetica", 12, "bold"), command=salvar_fornecedor).pack(pady=15)

    # Área de visualização dos fornecedores cadastrados
    texto = tk.Text(frame, height=10, width=80)
    texto.pack(pady=10)
    try:
        with open("dados/fornecedores.txt", "r", encoding="utf-8") as f:
            texto.insert(tk.END, f.read())
    except FileNotFoundError:
        texto.insert(tk.END, "Nenhum fornecedor cadastrado ainda.")
