import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import csv
import os

def tela_devolucoes(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.configure(bg="#f0fff0")

    # Título centralizado
    titulo = tk.Label(janela, text="↩️ Devoluções de Produtos", font=("Helvetica", 20, "bold"),
                      bg="#f0fff0", fg="#006633")
    titulo.pack(pady=15)

    # Frame container centralizado para todo o conteúdo (exceto título e botões)
    frame_container = tk.Frame(janela, bg="#f0fff0")
    frame_container.pack(expand=True)

    frame_principal = tk.Frame(frame_container, bg="#f0fff0")
    frame_principal.grid(row=0, column=0, padx=20, pady=10)

    # Configurar colunas para expansão equilibrada e tamanho mínimo
    for i in range(2):
        frame_principal.columnconfigure(i, weight=1, minsize=320)

    # === Seção: Dados do Produto ===
    secao_produto = tk.LabelFrame(frame_principal, text="📦 Dados do Produto", bg="#f0fff0",
                                  fg="#006633", font=("Helvetica", 12, "bold"))
    secao_produto.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(secao_produto, text="Produto:", bg="#f0fff0").grid(row=0, column=0, padx=5, pady=8, sticky="e")
    entrada_produto = tk.Entry(secao_produto, width=30)
    entrada_produto.grid(row=0, column=1, padx=5, pady=8)

    tk.Label(secao_produto, text="Código do Produto:", bg="#f0fff0").grid(row=1, column=0, padx=5, pady=8, sticky="e")
    entrada_codigo = tk.Entry(secao_produto, width=30)
    entrada_codigo.grid(row=1, column=1, padx=5, pady=8)

    tk.Label(secao_produto, text="Quantidade Devolvida:", bg="#f0fff0").grid(row=2, column=0, padx=5, pady=8, sticky="e")
    entrada_quantidade = tk.Entry(secao_produto, width=30)
    entrada_quantidade.grid(row=2, column=1, padx=5, pady=8)

    # Checkbox para indicar se o produto está em condições de reutilização
    reutilizacao_var = tk.IntVar()
    chk_reutilizacao = tk.Checkbutton(secao_produto, text="Produto reutilizável", variable=reutilizacao_var,
                                      bg="#f0fff0", fg="#006633", font=("Helvetica", 10, "bold"))
    chk_reutilizacao.grid(row=3, column=0, columnspan=2, pady=8)

    # === Seção: Cliente/Destinatário ===
    secao_cliente = tk.LabelFrame(frame_principal, text="👤 Cliente/Destinatário", bg="#f0fff0",
                                  fg="#006633", font=("Helvetica", 12, "bold"))
    secao_cliente.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    tk.Label(secao_cliente, text="Cliente/Destinatário:", bg="#f0fff0").grid(row=0, column=0, padx=5, pady=8, sticky="e")
    entrada_cliente = tk.Entry(secao_cliente, width=30)
    entrada_cliente.grid(row=0, column=1, padx=5, pady=8)

    tk.Label(secao_cliente, text="Contato:", bg="#f0fff0").grid(row=1, column=0, padx=5, pady=8, sticky="e")
    entrada_contato = tk.Entry(secao_cliente, width=30)
    entrada_contato.grid(row=1, column=1, padx=5, pady=8)

    tk.Label(secao_cliente, text="Email:", bg="#f0fff0").grid(row=2, column=0, padx=5, pady=8, sticky="e")
    entrada_email = tk.Entry(secao_cliente, width=30)
    entrada_email.grid(row=2, column=1, padx=5, pady=8)

    # === Seção: Detalhes da Devolução ===
    secao_devolucao = tk.LabelFrame(frame_principal, text="📝 Detalhes da Devolução", bg="#f0fff0",
                                   fg="#006633", font=("Helvetica", 12, "bold"))
    secao_devolucao.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    tk.Label(secao_devolucao, text="Motivo:", bg="#f0fff0").grid(row=0, column=0, padx=5, pady=8, sticky="e")
    entrada_motivo = tk.Entry(secao_devolucao, width=30)
    entrada_motivo.grid(row=0, column=1, padx=5, pady=8)

    tk.Label(secao_devolucao, text="Data da Devolução:", bg="#f0fff0").grid(row=1, column=0, padx=5, pady=8, sticky="e")
    entrada_data = DateEntry(secao_devolucao, width=27, background='darkblue', foreground='white', date_pattern='dd/mm/yyyy')
    entrada_data.grid(row=1, column=1, padx=5, pady=8)

    # Checkbox para indicar se houve autorização prévia
    autorizacao_var = tk.IntVar()
    chk_autorizacao = tk.Checkbutton(secao_devolucao, text="Autorização prévia obtida", variable=autorizacao_var,
                                     bg="#f0fff0", fg="#006633", font=("Helvetica", 10, "bold"))
    chk_autorizacao.grid(row=2, column=0, columnspan=2, pady=8)

    # === Seção: Responsável ===
    secao_responsavel = tk.LabelFrame(frame_principal, text="👷‍♂️ Responsável", bg="#f0fff0",
                                      fg="#006633", font=("Helvetica", 12, "bold"))
    secao_responsavel.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    tk.Label(secao_responsavel, text="Responsável pelo Registro:", bg="#f0fff0").grid(row=0, column=0, padx=5, pady=8, sticky="e")
    entrada_responsavel = tk.Entry(secao_responsavel, width=30)
    entrada_responsavel.grid(row=0, column=1, padx=5, pady=8)

    tk.Label(secao_responsavel, text="Setor:", bg="#f0fff0").grid(row=1, column=0, padx=5, pady=8, sticky="e")
    entrada_setor = tk.Entry(secao_responsavel, width=30)
    entrada_setor.grid(row=1, column=1, padx=5, pady=8)

    # === Campo de Observações grande e centralizado ===
    frame_obs = tk.Frame(janela, bg="#f0fff0")
    frame_obs.pack(pady=10)

    tk.Label(frame_obs, text="🗒️ Observações:", bg="#f0fff0", font=("Helvetica", 12, "bold")).pack()
    observacoes = tk.Text(frame_obs, height=5, width=80)
    observacoes.pack(pady=5)

    # === Botões centralizados ===
    botoes_frame = tk.Frame(janela, bg="#f0fff0")
    botoes_frame.pack(pady=10)

    def limpar_campos():
        for campo in [entrada_produto, entrada_codigo, entrada_quantidade, entrada_motivo, entrada_cliente, entrada_contato, entrada_email,
                      entrada_responsavel, entrada_setor]:
            campo.delete(0, tk.END)
        observacoes.delete("1.0", tk.END)
        reutilizacao_var.set(0)
        autorizacao_var.set(0)

    def salvar_devolucao():
        dados = [
            entrada_produto.get(),
            entrada_codigo.get(),
            entrada_quantidade.get(),
            entrada_data.get(),
            entrada_motivo.get(),
            entrada_cliente.get(),
            entrada_contato.get(),
            entrada_email.get(),
            "Sim" if reutilizacao_var.get() else "Não",
            "Sim" if autorizacao_var.get() else "Não",
            entrada_responsavel.get(),
            entrada_setor.get(),
            observacoes.get("1.0", tk.END).strip()
        ]
        if not all(dados[:7]) or not dados[10] or not dados[11]:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return
        if not dados[2].isdigit():
            messagebox.showwarning("Erro", "A quantidade devolvida deve ser numérica.")
            return

        os.makedirs("dados", exist_ok=True)
        with open("dados/devolucoes.txt", "a", encoding="utf-8") as f:
            f.write(" | ".join(dados) + "\n")

        messagebox.showinfo("Sucesso", "Devolução registrada com sucesso.")
        limpar_campos()
        carregar_devolucoes()

    def exportar_csv():
        try:
            with open("dados/devolucoes.txt", "r", encoding="utf-8") as f:
                linhas = [linha.strip().split("|") for linha in f if linha.strip()]
            with open("dados/devolucoes.csv", "w", newline="", encoding="utf-8") as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(["Produto", "Código", "Quantidade", "Data", "Motivo", "Cliente", "Contato", "Email",
                                 "Reutilizável", "Autorização", "Responsável", "Setor", "Observações"])
                writer.writerows(linhas)
            messagebox.showinfo("Exportado", "Dados exportados com sucesso.")
        except FileNotFoundError:
            messagebox.showwarning("Erro", "Nenhum dado encontrado.")

    tk.Button(botoes_frame, text="💾 Salvar", font=("Helvetica", 12, "bold"),
              bg="#2e8b57", fg="white", width=15, command=salvar_devolucao).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="📁 Exportar CSV", font=("Helvetica", 12, "bold"),
              bg="#1e6633", fg="white", width=15, command=exportar_csv).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="🧹 Limpar Campos", font=("Helvetica", 12, "bold"),
              bg="#999900", fg="white", width=15, command=limpar_campos).pack(side="left", padx=10)

    # === Tabela com barras de rolagem vertical e horizontal ===
    tabela_frame = tk.Frame(janela)
    tabela_frame.pack(pady=10, fill="both", expand=True)

    colunas = ["Produto", "Código", "Quantidade", "Data", "Motivo", "Cliente", "Contato", "Email",
               "Reutilizável", "Autorização", "Responsável", "Setor", "Observações"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=120, anchor="center")

    # Scrollbar vertical
    scroll_v = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll_v.set)
    scroll_v.grid(row=0, column=1, sticky="ns")

    # Scrollbar horizontal
    scroll_h = ttk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(xscrollcommand=scroll_h.set)
    scroll_h.grid(row=1, column=0, sticky="ew")

    tabela.grid(row=0, column=0, sticky="nsew")

    tabela_frame.rowconfigure(0, weight=1)
    tabela_frame.columnconfigure(0, weight=1)

    # === Filtro de Produto ===
    filtro_frame = tk.Frame(janela, bg="#f0fff0")
    filtro_frame.pack(pady=5)

    tk.Label(filtro_frame, text="🔍 Buscar Produto:", font=("Helvetica", 10), bg="#f0fff0").pack(side="left")
    entrada_filtro = tk.Entry(filtro_frame, width=30)
    entrada_filtro.pack(side="left", padx=5)

    def aplicar_filtro():
        filtro = entrada_filtro.get().lower()
        for item in tabela.get_children():
            valores = tabela.item(item, "values")
            if filtro in valores[0].lower():  # Produto
                tabela.see(item)
                tabela.selection_set(item)
            else:
                tabela.detach(item)

    def limpar_filtro():
        for item in tabela.get_children():
            tabela.reattach(item, '', 'end')
        entrada_filtro.delete(0, tk.END)

    tk.Button(filtro_frame, text="Filtrar", command=aplicar_filtro).pack(side="left", padx=5)
    tk.Button(filtro_frame, text="Limpar", command=limpar_filtro).pack(side="left", padx=5)

    # === Carregamento Inicial da Tabela ===
    def carregar_devolucoes():
        tabela.delete(*tabela.get_children())
        try:
            with open("dados/devolucoes.txt", "r", encoding="utf-8") as f:
                for linha in f:
                    valores = [v.strip() for v in linha.split("|")]
                    tabela.insert("", tk.END, values=valores)
        except FileNotFoundError:
            pass

    carregar_devolucoes()

# Exemplo de chamada da função em janela Tkinter:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Devoluções")
    root.geometry("1100x700")
    tela_devolucoes(root)
    root.mainloop()
