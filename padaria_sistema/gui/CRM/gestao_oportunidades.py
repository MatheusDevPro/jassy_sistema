import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

ARQUIVO_DADOS = "oportunidades.txt"
dados_oportunidades = []

CAMPOS = [
    "cliente", "responsavel", "telefone", "email",
    "produto", "segmento", "etapa",
    "valor", "status", "origem", "probabilidade",
    "data_criacao", "fechamento_previsto", "observacoes"
]


def salvar_em_txt():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        for op in dados_oportunidades:
            linha = ";".join([op.get(campo, "") for campo in CAMPOS])
            f.write(linha + "\n")


def carregar_de_txt():
    if not os.path.exists(ARQUIVO_DADOS):
        return
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        for linha in f:
            valores = linha.strip().split(";")
            if len(valores) == len(CAMPOS):
                dados_oportunidades.append(dict(zip(CAMPOS, valores)))


def tela_gestao_oportunidades(janela):
    def atualizar_tabela():
        tree.delete(*tree.get_children())
        for i, oportunidade in enumerate(dados_oportunidades):
            tree.insert("", "end", iid=i, values=(
                oportunidade["cliente"],
                oportunidade["produto"],
                oportunidade["responsavel"],
                oportunidade["valor"],
                oportunidade["status"],
                oportunidade["fechamento_previsto"]
            ))
        atualizar_resumo()

    def atualizar_resumo():
        total = len(dados_oportunidades)
        valor_total = sum(float(op.get("valor", "0").replace(",", ".")) for op in dados_oportunidades)
        label_resumo.config(
            text=f"Total: {total} oportunidades | Valor Estimado: R$ {valor_total:,.2f}"
            .replace(",", "X").replace(".", ",").replace("X", "."))

    def abrir_formulario(editar=False):
        def salvar():
            nova = {
                campo: entradas[campo].get() if campo != "observacoes"
                else texto_obs.get("1.0", tk.END).strip()
                for campo in CAMPOS
            }

            if not nova["cliente"] or not nova["responsavel"] or not nova["valor"]:
                messagebox.showwarning("Campos obrigatórios", "Cliente, Responsável e Valor são obrigatórios.")
                return

            if editar:
                selecionado = tree.focus()
                if selecionado:
                    dados_oportunidades[int(selecionado)] = nova
            else:
                dados_oportunidades.append(nova)

            salvar_em_txt()
            atualizar_tabela()
            form.destroy()

        form = tk.Toplevel(janela)
        form.title("Cadastro de Oportunidade")
        form.geometry("700x750")
        form.resizable(False, False)

        frame_form = tk.Frame(form)
        frame_form.pack(pady=10, padx=10, fill="both", expand=True)

        entradas = {}
        row = 0
        for campo in CAMPOS:
            if campo == "observacoes":
                tk.Label(frame_form, text="Observações:").grid(row=row, column=0, sticky="nw", padx=5, pady=(10, 0))
                texto_obs = tk.Text(frame_form, height=6, width=70)
                texto_obs.grid(row=row + 1, column=0, columnspan=2, padx=5, pady=(0, 10))
                row += 2
                continue
            tk.Label(frame_form, text=f"{campo.capitalize().replace('_', ' ')}:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
            entrada = tk.Entry(frame_form, width=50)
            entrada.grid(row=row, column=1, padx=5, pady=2, sticky="w")
            entradas[campo] = entrada
            row += 1

        entradas["data_criacao"].insert(0, datetime.today().strftime("%d/%m/%Y"))

        if editar:
            selecionado = tree.focus()
            if selecionado:
                dados = dados_oportunidades[int(selecionado)]
                for campo in CAMPOS:
                    if campo == "observacoes":
                        texto_obs.insert("1.0", dados.get(campo, ""))
                    else:
                        entradas[campo].insert(0, dados.get(campo, ""))

        tk.Button(form, text="Salvar", bg="#2e8b57", fg="white", width=20, command=salvar).pack(pady=20)

    def excluir():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione uma linha.")
            return
        if messagebox.askyesno("Confirmação", "Deseja excluir esta oportunidade?"):
            del dados_oportunidades[int(selecionado)]
            salvar_em_txt()
            atualizar_tabela()

    def exportar():
        if not dados_oportunidades:
            messagebox.showinfo("Nada para exportar", "Nenhuma oportunidade registrada.")
            return
        arquivo = "export_oportunidades.csv"
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(";".join(CAMPOS) + "\n")
            for op in dados_oportunidades:
                f.write(";".join([op.get(c, "") for c in CAMPOS]) + "\n")
        messagebox.showinfo("Exportado", f"Arquivo gerado: {arquivo}")

    # Limpa a janela
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    tk.Label(janela, text="📇 Gestão de Oportunidades", font=("Arial", 18, "bold"), fg="#1e90ff").pack(pady=10)

    frame_top = tk.Frame(janela)
    frame_top.pack(pady=5)

    tk.Button(frame_top, text="➕ Nova", bg="#1e90ff", fg="white", width=10, command=lambda: abrir_formulario(False)).pack(side="left", padx=5)
    tk.Button(frame_top, text="✏️ Editar", width=10, command=lambda: abrir_formulario(True)).pack(side="left", padx=5)
    tk.Button(frame_top, text="❌ Excluir", bg="red", fg="white", width=10, command=excluir).pack(side="left", padx=5)
    tk.Button(frame_top, text="📤 Exportar", bg="#ffa500", width=10, command=exportar).pack(side="left", padx=5)

    columns = ("cliente", "produto", "responsavel", "valor", "status", "fechamento_previsto")
    tree = ttk.Treeview(janela, columns=columns, show="headings", height=20)
    for col in columns:
        largura = 150 if col in ["cliente", "produto", "responsavel"] else 120
        tree.heading(col, text=col.capitalize().replace("_", " "))
        tree.column(col, width=largura, anchor="center")
    tree.pack(pady=10, fill="x", padx=20)

    label_resumo = tk.Label(janela, text="", font=("Arial", 10, "italic"))
    label_resumo.pack(pady=(5, 10))

    carregar_de_txt()
    atualizar_tabela()


# Execução principal
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Oportunidades")
    root.geometry("900x700")
    root.resizable(False, False)
    tela_gestao_oportunidades(root)
    root.mainloop()
