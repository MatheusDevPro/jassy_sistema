import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

def tela_integracoes(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f0f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🔌 Integrações com Sistemas Externos", font=("Helvetica", 18, "bold"),
             bg="#f0f8ff", fg="#003366").pack(pady=15)

    campos_frame = tk.LabelFrame(frame, text="Configurações Gerais", bg="#f0f8ff", fg="#003366",
                                 font=("Helvetica", 12, "bold"))
    campos_frame.pack(padx=20, pady=10, fill="x")

    opcoes = {
        "Integração com ERP": tk.BooleanVar(),
        "Integração Fiscal (NFe)": tk.BooleanVar(),
        "Integração com Gateway de Pagamento": tk.BooleanVar(),
        "Integração com API de Consulta CEP": tk.BooleanVar(),
        "Integração com Sistema de Estoque 3º": tk.BooleanVar(),
        "Webhooks para Recebimento em Tempo Real": tk.BooleanVar()
    }

    for i, (texto, var) in enumerate(opcoes.items()):
        tk.Checkbutton(campos_frame, text=texto, variable=var,
                       font=("Helvetica", 11), bg="#f0f8ff").grid(row=i, column=0, sticky="w", padx=15, pady=3)

    # Seção de chaves/API tokens
    api_frame = tk.LabelFrame(frame, text="Chaves de API / URLs de Integração", bg="#f0f8ff", fg="#003366",
                              font=("Helvetica", 12, "bold"))
    api_frame.pack(padx=20, pady=10, fill="x")

    campos_api = {
        "Token API ERP": tk.Entry(api_frame, width=50),
        "URL API NFe": tk.Entry(api_frame, width=50),
        "Token Gateway Pagamento": tk.Entry(api_frame, width=50),
        "URL Webhook Notificações": tk.Entry(api_frame, width=50),
    }

    for i, (rotulo, entrada) in enumerate(campos_api.items()):
        tk.Label(api_frame, text=rotulo + ":", bg="#f0f8ff", font=("Helvetica", 11)).grid(row=i, column=0, sticky="e", padx=5, pady=6)
        entrada.grid(row=i, column=1, sticky="w", padx=5, pady=6)

    # Ações
    botoes_frame = tk.Frame(frame, bg="#f0f8ff")
    botoes_frame.pack(pady=15)

    def salvar_configuracoes():
        configuracoes = {
            "opcoes": {k: v.get() for k, v in opcoes.items()},
            "api": {k: entrada.get().strip() for k, entrada in campos_api.items()}
        }

        os.makedirs("dados", exist_ok=True)
        with open("dados/integracoes.json", "w", encoding="utf-8") as f:
            json.dump(configuracoes, f, indent=4)
        messagebox.showinfo("Salvo", "Configurações de integração salvas com sucesso.")

    def carregar_configuracoes():
        if os.path.exists("dados/integracoes.json"):
            with open("dados/integracoes.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                for chave, valor in config.get("opcoes", {}).items():
                    if chave in opcoes:
                        opcoes[chave].set(valor)
                for chave, valor in config.get("api", {}).items():
                    if chave in campos_api:
                        campos_api[chave].delete(0, tk.END)
                        campos_api[chave].insert(0, valor)

    tk.Button(botoes_frame, text="💾 Salvar", bg="#006699", fg="white",
              font=("Helvetica", 12, "bold"), width=15, command=salvar_configuracoes).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="🔄 Carregar", bg="#339966", fg="white",
              font=("Helvetica", 12, "bold"), width=15, command=carregar_configuracoes).pack(side="left", padx=10)

    carregar_configuracoes()
