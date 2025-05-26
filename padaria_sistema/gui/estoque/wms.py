import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os

# Simulando permissões por usuário
permissoes_usuarios = {
    "admin": {"exportar_pdf": True, "ver_detalhes": True},
    "estoquista": {"exportar_pdf": False, "ver_detalhes": True},
    "visitante": {"exportar_pdf": False, "ver_detalhes": False}
}

usuario_logado = "admin"  # Simula um login atual

# Simula banco de dados de movimentações
movimentacoes = [
    {"produto": "Cimento", "entrada": 100, "saida": 40},
    {"produto": "Areia", "entrada": 200, "saida": 80},
    {"produto": "Brita", "entrada": 150, "saida": 50},
]

# Função para calcular totais e atualizar a tabela
def atualizar_tabela(tree):
    for item in tree.get_children():
        tree.delete(item)

    for item in movimentacoes:
        estoque_atual = item["entrada"] - item["saida"]
        tree.insert("", "end", values=(
            item["produto"],
            item["entrada"],
            item["saida"],
            estoque_atual
        ))

# Exporta para PDF
def exportar_pdf():
    if not permissoes_usuarios[usuario_logado]["exportar_pdf"]:
        messagebox.showwarning("Permissão negada", "Você não tem permissão para exportar para PDF.")
        return






# Interface Tkinter
def tela_wms(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != "Menu":
            widget.destroy()

    frame = tk.Frame(janela, bg="#f0f8ff")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame, text="📦 Sistema WMS - Gerenciamento de Estoque", font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#003366").pack(pady=10)

    colunas = ("Produto", "Entradas", "Saídas", "Estoque Atual")
    tree = ttk.Treeview(frame, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    tree.pack(pady=10, fill="x")

    atualizar_tabela(tree)

    botoes_frame = tk.Frame(frame, bg="#f0f8ff")
    botoes_frame.pack(pady=10)

    tk.Button(botoes_frame, text="🔄 Atualizar", bg="#4caf50", fg="white", font=("Helvetica", 12), command=lambda: atualizar_tabela(tree)).pack(side="left", padx=5)

    tk.Button(botoes_frame, text="📄 Exportar PDF", bg="#2196f3", fg="white", font=("Helvetica", 12), command=exportar_pdf).pack(side="left", padx=5)

# Executar janela principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema WMS")
    root.geometry("700x500")
    tela_wms(root)
    root.mainloop()
