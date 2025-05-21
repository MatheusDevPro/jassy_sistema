import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import re

ARQUIVO_CONTATOS = "historico_contatos.txt"
dados_contatos = []

CAMPOS_CONTATO = ["cliente", "data", "tipo", "responsavel", "assunto", "descricao"]

# Função para validar o formato da data
def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# Função para validar campos obrigatórios
def validar_campos(campos):
    if not campos["cliente"] or not campos["data"] or not campos["tipo"]:
        return False
    return True

def salvar_contatos_em_txt():
    with open(ARQUIVO_CONTATOS, "w", encoding="utf-8") as f:
        for contato in dados_contatos:
            linha = ";".join([contato.get(campo, "") for campo in CAMPOS_CONTATO])
            f.write(linha + "\n")

def carregar_contatos_de_txt():
    dados_contatos.clear()
    if not os.path.exists(ARQUIVO_CONTATOS):
        return
    with open(ARQUIVO_CONTATOS, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split(";")
            if len(partes) == len(CAMPOS_CONTATO):
                dados_contatos.append(dict(zip(CAMPOS_CONTATO, partes)))

def tela_contatos_historico(janela):
    def atualizar_tabela():
        tree.delete(*tree.get_children())
        for i, contato in enumerate(dados_contatos):
            tree.insert("", "end", iid=i, values=(
                contato["cliente"],
                contato["data"],
                contato["tipo"],
                contato["responsavel"],
                contato["assunto"]
            ))

    def abrir_formulario(editar=False):
        def salvar():
            campos = {
                campo: entradas[campo].get() if campo != "descricao"
                else texto_desc.get("1.0", tk.END).strip()
                for campo in CAMPOS_CONTATO
            }

            # Validação dos campos obrigatórios
            if not validar_campos(campos):
                messagebox.showwarning("Campos obrigatórios", "Cliente, Data e Tipo são obrigatórios.")
                return

            # Validação da data
            if not validar_data(campos["data"]):
                messagebox.showwarning("Data inválida", "O formato da data deve ser dd/mm/aaaa.")
                return

            # Verificação se a descrição não está vazia
            if campos["descricao"] == "":
                messagebox.showwarning("Descrição inválida", "Descrição não pode estar vazia.")
                return

            if editar:
                sel = tree.focus()
                if sel:
                    dados_contatos[int(sel)] = campos
            else:
                dados_contatos.append(campos)

            salvar_contatos_em_txt()
            atualizar_tabela()
            form.destroy()

        form = tk.Toplevel(janela)
        form.title("Registro de Contato")
        form.geometry("600x600")
        form.resizable(False, False)

        frame = tk.Frame(form)
        frame.pack(padx=10, pady=10)

        entradas = {}
        row = 0
        for campo in CAMPOS_CONTATO:
            if campo == "descricao":
                tk.Label(frame, text="Descrição:").grid(row=row, column=0, sticky="nw", pady=(10, 0))
                texto_desc = tk.Text(frame, height=6, width=60)
                texto_desc.grid(row=row + 1, column=0, columnspan=2, pady=(0, 10))
                row += 2
                continue
            tk.Label(frame, text=f"{campo.capitalize()}:").grid(row=row, column=0, sticky="w", pady=2)
            entrada = tk.Entry(frame, width=50)
            entrada.grid(row=row, column=1, pady=2, sticky="w")
            entradas[campo] = entrada
            row += 1

        entradas["data"].insert(0, datetime.today().strftime("%d/%m/%Y"))

        if editar:
            sel = tree.focus()
            if sel:
                dados = dados_contatos[int(sel)]
                for campo in CAMPOS_CONTATO:
                    if campo == "descricao":
                        texto_desc.insert("1.0", dados.get(campo, ""))
                    else:
                        entradas[campo].insert(0, dados.get(campo, ""))

        tk.Button(form, text="Salvar", bg="#2e8b57", fg="white", command=salvar, width=20).pack(pady=15)

    def excluir():
        sel = tree.focus()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma linha.")
            return
        if messagebox.askyesno("Confirmação", "Deseja excluir este contato?"):
            del dados_contatos[int(sel)]
            salvar_contatos_em_txt()
            atualizar_tabela()

    # Limpar janela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    tk.Label(janela, text="📞 Contatos e Histórico", font=("Arial", 18, "bold"), fg="#1e90ff").pack(pady=10)

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=5)

    tk.Button(frame_botoes, text="➕ Novo", bg="#1e90ff", fg="white", width=10, command=lambda: abrir_formulario(False)).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="✏️ Editar", width=10, command=lambda: abrir_formulario(True)).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="❌ Excluir", bg="red", fg="white", width=10, command=excluir).pack(side="left", padx=5)

    columns = ("cliente", "data", "tipo", "responsavel", "assunto")
    tree = ttk.Treeview(janela, columns=columns, show="headings", height=20)
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150 if col != "assunto" else 200, anchor="center")
    tree.pack(padx=20, pady=10, fill="x")

    carregar_contatos_de_txt()
    atualizar_tabela()

