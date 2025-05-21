import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime

def tela_gestao_pessoal(janela):
    janela.title("👥 Gestão de Pessoal - Jassy Gestão")
    janela.configure(bg="#f8f8ff")

    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    titulo = tk.Label(frame, text="👥 Gestão de Pessoal", font=("Segoe UI", 18, "bold"), fg="#1E90FF", bg="#f8f8ff")
    titulo.pack(pady=10)

    form_frame = tk.LabelFrame(frame, text="Dados do Funcionário", font=("Segoe UI", 12, "bold"), fg="#333", bg="#f8f8ff", padx=10, pady=10)
    form_frame.pack(fill=tk.X, padx=5, pady=10)

    campos = [
        ("ID:", tk.Entry(form_frame, state="readonly", width=10)),
        ("Nome Completo:", tk.Entry(form_frame, width=30)),
        ("CPF:", tk.Entry(form_frame, width=20)),
        ("Data de Nascimento:", tk.Entry(form_frame, width=20)),
        ("Telefone:", tk.Entry(form_frame, width=20)),
        ("Email:", tk.Entry(form_frame, width=30)),
        ("Sexo:", ttk.Combobox(form_frame, values=["Masculino", "Feminino", "Outro"], state="readonly", width=18)),
        ("Estado Civil:", ttk.Combobox(form_frame, values=["Solteiro", "Casado", "Divorciado", "Viúvo"], state="readonly", width=18)),
        ("Escolaridade:", ttk.Combobox(form_frame, values=["Fundamental", "Médio", "Superior", "Pós-graduação"], state="readonly", width=18)),
        ("Salário:", tk.Entry(form_frame, width=20)),
        ("CTPS:", tk.Entry(form_frame, width=20)),
        ("PIS/PASEP:", tk.Entry(form_frame, width=20)),
        ("Nº Dependentes:", tk.Entry(form_frame, width=5)),
        ("CEP:", tk.Entry(form_frame, width=10)),
        ("Rua:", tk.Entry(form_frame, width=30)),
        ("Número:", tk.Entry(form_frame, width=10)),
        ("Bairro:", tk.Entry(form_frame, width=20)),
        ("Cidade:", tk.Entry(form_frame, width=20)),
        ("UF:", ttk.Combobox(form_frame, values=["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"], state="readonly", width=5)),
        ("Cargo:", ttk.Combobox(form_frame, values=["Analista", "Desenvolvedor", "Gerente", "Assistente", "Estagiário", "Supervisor"], state="readonly", width=20)),
        ("Departamento:", ttk.Combobox(form_frame, values=["TI", "Financeiro", "RH", "Marketing", "Vendas", "Produção", "Suporte"], state="readonly", width=20)),
        ("Data de Admissão:", tk.Entry(form_frame, width=20)),
        ("Status:", ttk.Combobox(form_frame, values=["Ativo", "Inativo", "Afastado"], state="readonly", width=20))
    ]

    for i, (label_text, entry_widget) in enumerate(campos):
        row, col = divmod(i, 2)
        tk.Label(form_frame, text=label_text, bg="#f8f8ff").grid(row=row, column=col*2, sticky="e", padx=5, pady=3)
        entry_widget.grid(row=row, column=col*2+1, sticky="w", padx=5, pady=3)

    tk.Label(form_frame, text="Observações:", bg="#f8f8ff").grid(row=len(campos)//2+1, column=0, sticky="ne", padx=5, pady=3)
    obs_text = tk.Text(form_frame, height=4, width=80)
    obs_text.grid(row=len(campos)//2+1, column=1, columnspan=3, sticky="w", padx=5, pady=3)

    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(fill=tk.X, pady=10)

    tk.Button(botoes_frame, text="💾 Salvar", bg="#1E90FF", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(botoes_frame, text="🗑️ Excluir", bg="#FF4500", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(botoes_frame, text="🧹 Limpar", bg="#696969", fg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=5)

    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(fill=tk.BOTH, expand=True)

    colunas = ("ID", "Nome", "CPF", "Cargo", "Departamento", "Status")
    tree = ttk.Treeview(tabela_frame, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100 if col == "ID" else 150)
    tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    scrollbar = ttk.Scrollbar(tabela_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
