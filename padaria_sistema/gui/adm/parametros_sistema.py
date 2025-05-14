import tkinter as tk
from tkinter import messagebox, ttk
import os
import json

def tela_parametros_sistema(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f0f4f7")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🛠️ Parâmetros do Sistema", font=("Helvetica", 18, "bold"),
             bg="#f0f4f7", fg="#003366").pack(pady=15)

    campos_frame = tk.LabelFrame(frame, text="Configurações Gerais", bg="#f0f4f7", fg="#003366",
                                 font=("Helvetica", 12, "bold"), padx=15, pady=10)
    campos_frame.pack(padx=20, pady=10, fill="x")

    parametros = {
        "Nome do Sistema": tk.Entry(campos_frame, width=40),
        "Nome da Empresa": tk.Entry(campos_frame, width=40),
        "CNPJ": tk.Entry(campos_frame, width=40),
        "Email de Notificações": tk.Entry(campos_frame, width=40),
        "Caminho para Backups": tk.Entry(campos_frame, width=40),
        "Impressora Padrão": tk.Entry(campos_frame, width=40)
    }

    for i, (rotulo, entrada) in enumerate(parametros.items()):
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 11), bg="#f0f4f7", fg="#003366") \
            .grid(row=i, column=0, padx=8, pady=6, sticky="e")
        entrada.grid(row=i, column=1, padx=8, pady=6, sticky="w")

    # Opções adicionais (combobox e checkbutton)
    opcoes_frame = tk.LabelFrame(frame, text="Preferências", bg="#f0f4f7", fg="#003366",
                                 font=("Helvetica", 12, "bold"), padx=15, pady=10)
    opcoes_frame.pack(padx=20, pady=10, fill="x")

    tema = ttk.Combobox(opcoes_frame, values=["Claro", "Escuro"], state="readonly", width=37)
    tema.set("Claro")
    casas_decimais = ttk.Combobox(opcoes_frame, values=["1", "2", "3", "4"], state="readonly", width=37)
    casas_decimais.set("2")
    intervalo_backup = ttk.Combobox(opcoes_frame, values=["Desativado", "Diário", "Semanal", "Mensal"], state="readonly", width=37)
    intervalo_backup.set("Semanal")

    exibir_popup = tk.BooleanVar(value=True)
    check_popup = tk.Checkbutton(opcoes_frame, text="Exibir mensagens pop-up", variable=exibir_popup,
                                  bg="#f0f4f7", font=("Helvetica", 11), fg="#003366")

    # Labels e Widgets
    tk.Label(opcoes_frame, text="Tema do Sistema:", bg="#f0f4f7", fg="#003366", font=("Helvetica", 11)) \
        .grid(row=0, column=0, sticky="e", padx=8, pady=5)
    tema.grid(row=0, column=1, sticky="w", padx=8)

    tk.Label(opcoes_frame, text="Casas Decimais:", bg="#f0f4f7", fg="#003366", font=("Helvetica", 11)) \
        .grid(row=1, column=0, sticky="e", padx=8, pady=5)
    casas_decimais.grid(row=1, column=1, sticky="w", padx=8)

    tk.Label(opcoes_frame, text="Backup Automático:", bg="#f0f4f7", fg="#003366", font=("Helvetica", 11)) \
        .grid(row=2, column=0, sticky="e", padx=8, pady=5)
    intervalo_backup.grid(row=2, column=1, sticky="w", padx=8)

    check_popup.grid(row=3, column=1, sticky="w", pady=8)

    def salvar_parametros():
        dados = {k: e.get().strip() for k, e in parametros.items()}
        dados.update({
            "Tema": tema.get(),
            "Casas Decimais": casas_decimais.get(),
            "Backup Automático": intervalo_backup.get(),
            "Exibir Pop-up": exibir_popup.get()
        })

        os.makedirs("dados", exist_ok=True)
        with open("dados/parametros_sistema.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sucesso", "Parâmetros salvos com sucesso.")

    def carregar_parametros():
        try:
            with open("dados/parametros_sistema.json", "r", encoding="utf-8") as f:
                dados = json.load(f)

            for k, e in parametros.items():
                e.insert(0, dados.get(k, ""))

            tema.set(dados.get("Tema", "Claro"))
            casas_decimais.set(dados.get("Casas Decimais", "2"))
            intervalo_backup.set(dados.get("Backup Automático", "Semanal"))
            exibir_popup.set(dados.get("Exibir Pop-up", True))

        except FileNotFoundError:
            pass

    botoes = tk.Frame(frame, bg="#f0f4f7")
    botoes.pack(pady=20)

    tk.Button(botoes, text="💾 Salvar", bg="#339966", fg="white", font=("Helvetica", 12, "bold"),
              width=15, cursor="hand2", command=salvar_parametros).pack(side="left", padx=10)
    tk.Button(botoes, text="🔄 Carregar", bg="#0059b3", fg="white", font=("Helvetica", 12, "bold"),
              width=15, cursor="hand2", command=carregar_parametros).pack(side="left", padx=10)

    carregar_parametros()
