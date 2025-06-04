import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def calcular_total_horas(entrada, pausa, retorno, saida):
    try:
        entrada_dt = datetime.strptime(entrada, "%H:%M")
        pausa_dt = datetime.strptime(pausa, "%H:%M")
        retorno_dt = datetime.strptime(retorno, "%H:%M")
        saida_dt = datetime.strptime(saida, "%H:%M")

        antes_pausa = pausa_dt - entrada_dt
        depois_pausa = saida_dt - retorno_dt
        total = antes_pausa + depois_pausa
        return str(total)
    except:
        return "00:00"

def tela_controle_ponto(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="⏱️ Controle de Ponto", font=("Arial", 20, "bold"), bg="#f8f8ff", fg="#333").pack(pady=20)

    # 🔍 Pesquisa
    pesquisa_frame = tk.Frame(frame, bg="#f8f8ff")
    pesquisa_frame.pack(pady=5, fill="x", padx=30)

    tk.Label(pesquisa_frame, text="Buscar por Nome/Matrícula:", font=("Arial", 12), bg="#f8f8ff").pack(side="left", padx=(0,10))
    entry_pesquisa = tk.Entry(pesquisa_frame, font=("Arial", 12), width=40)
    entry_pesquisa.pack(side="left")
    tk.Button(pesquisa_frame, text="Pesquisar", font=("Arial", 11), bg="#3f51b5", fg="white").pack(side="left", padx=10)

    # 📋 Formulário
    form_frame = tk.Frame(frame, bg="#f8f8ff")
    form_frame.pack(padx=30, pady=10, fill="x")

    campos = [
        ("Matrícula", 0), ("Nome", 1), ("Data (dd/mm/aaaa)", 2), ("Hora Entrada", 3),
        ("Hora Pausa", 4), ("Retorno Pausa", 5), ("Hora Saída", 6), ("Turno", 7)
    ]
    entradas = {}

    for texto, linha in campos:
        tk.Label(form_frame, text=texto + ":", font=("Arial", 11), bg="#f8f8ff").grid(row=linha, column=0, sticky="w", pady=2)
        entrada = tk.Entry(form_frame, font=("Arial", 11), width=35)
        entrada.grid(row=linha, column=1, pady=2, padx=10, sticky="w")
        entradas[texto] = entrada

    # 🧮 Cálculo automático
    def registrar_ponto():
        dados = {campo: entradas[campo].get().strip() for campo in entradas}
        obrigatorios = ["Matrícula", "Nome", "Data (dd/mm/aaaa)"]

        for campo in obrigatorios:
            if not dados[campo]:
                messagebox.showwarning("Campo obrigatório", f"O campo '{campo}' é obrigatório.")
                return

        try:
            datetime.strptime(dados["Data (dd/mm/aaaa)"], "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Data inválida", "Use o formato dd/mm/aaaa para a data.")
            return

        total_horas = calcular_total_horas(
            dados["Hora Entrada"], dados["Hora Pausa"],
            dados["Retorno Pausa"], dados["Hora Saída"]
        )

        tabela.insert("", "end", values=[
            dados["Matrícula"], dados["Nome"], dados["Data (dd/mm/aaaa)"],
            dados["Hora Entrada"], dados["Hora Pausa"], dados["Retorno Pausa"],
            dados["Hora Saída"], total_horas, dados["Turno"]
        ])
        atualizar_total()
        for campo in entradas.values():
            campo.delete(0, tk.END)
        txt_obs.delete("1.0", tk.END)

    # 🧾 Tabela
    tabela_frame = tk.Frame(frame)
    tabela_frame.pack(padx=30, pady=10, fill="both", expand=True)

    colunas = ["Matrícula", "Nome", "Data", "Entrada", "Pausa", "Retorno", "Saída", "Total Horas", "Turno"]
    tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, anchor="center", width=110)

    scroll_y = tk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
    scroll_x = tk.Scrollbar(tabela_frame, orient="horizontal", command=tabela.xview)
    tabela.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

    tabela.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    tabela_frame.grid_rowconfigure(0, weight=1)
    tabela_frame.grid_columnconfigure(0, weight=1)

    # 📝 Observações
    obs_frame = tk.Frame(frame, bg="#f8f8ff")
    obs_frame.pack(fill="x", padx=30, pady=10)

    tk.Label(obs_frame, text="Observações:", font=("Arial", 12), bg="#f8f8ff").pack(anchor="w")
    txt_obs = tk.Text(obs_frame, height=4, font=("Arial", 11))
    txt_obs.pack(fill="x")

    # 📊 Rodapé
    rodape_frame = tk.Frame(frame, bg="#f8f8ff")
    rodape_frame.pack(pady=5, fill="x", padx=30)

    lbl_total_ponto = tk.Label(rodape_frame, text="Total de Registros: 0", font=("Arial", 11, "bold"), fg="blue", bg="#f8f8ff")
    lbl_total_ponto.pack(anchor="e")

    def atualizar_total():
        total = len(tabela.get_children())
        lbl_total_ponto.config(text=f"Total de Registros: {total}")

    # 🧰 Botões
    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=20)

    tk.Button(botoes_frame, text="Registrar", font=("Arial", 11), bg="#4caf50", fg="white", width=18, command=registrar_ponto).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Editar", font=("Arial", 11), bg="#2196f3", fg="white", width=15).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Excluir", font=("Arial", 11), bg="#f44336", fg="white", width=15).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Gerar Relatório", font=("Arial", 11), bg="#9c27b0", fg="white", width=15).pack(side="left", padx=10)
    tk.Button(botoes_frame, text="Atualizar Total", font=("Arial", 11), bg="#795548", fg="white", width=15, command=atualizar_total).pack(side="left", padx=10)
