import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
import os


def tela_personalizacao_interface(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f0f0f0")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🎨 Personalização da Interface", font=("Helvetica", 18, "bold"),
             bg="#f0f0f0", fg="#333").pack(pady=20)

    config_frame = tk.LabelFrame(frame, text="Preferências Visuais", bg="#f0f0f0",
                                 font=("Helvetica", 12, "bold"), fg="#00334d", padx=20, pady=20)
    config_frame.pack(padx=20, pady=10, fill="x")

    # Tema
    tema_var = tk.StringVar(value="Claro")
    tk.Label(config_frame, text="Tema:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=0, sticky="e")
    ttk.Combobox(config_frame, textvariable=tema_var, values=["Claro", "Escuro"], width=20).grid(row=0, column=1, padx=10, pady=5)

    # Cor destaque
    cor_destaque = tk.StringVar(value="#004080")
    tk.Label(config_frame, text="Cor de Destaque:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=1, column=0, sticky="e")
    cor_preview = tk.Label(config_frame, width=3, bg=cor_destaque.get(), relief="solid")
    cor_preview.grid(row=1, column=2, padx=5)

    def escolher_cor():
        cor = colorchooser.askcolor(title="Escolha a cor de destaque")
        if cor[1]:
            cor_destaque.set(cor[1])
            cor_preview.config(bg=cor[1])

    tk.Button(config_frame, text="Selecionar Cor", command=escolher_cor).grid(row=1, column=1, padx=10, pady=5)

    # Fonte
    fonte_var = tk.StringVar(value="Helvetica")
    tk.Label(config_frame, text="Fonte:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=2, column=0, sticky="e")
    ttk.Combobox(config_frame, textvariable=fonte_var,
                 values=["Helvetica", "Arial", "Calibri", "Verdana", "Times New Roman"], width=20).grid(row=2, column=1, padx=10, pady=5)

    # Tamanho da fonte
    tamanho_var = tk.IntVar(value=12)
    tk.Label(config_frame, text="Tamanho da Fonte:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=3, column=0, sticky="e")
    tk.Spinbox(config_frame, from_=8, to=24, textvariable=tamanho_var, width=5).grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Estilo de ícones
    icones_var = tk.StringVar(value="Emojis")
    tk.Label(config_frame, text="Estilo dos Ícones:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=4, column=0, sticky="e")
    ttk.Combobox(config_frame, textvariable=icones_var, values=["Emojis", "Clássicos", "Minimalistas"], width=20).grid(row=4, column=1, padx=10, pady=5)

    # Animações
    animacoes_var = tk.BooleanVar(value=True)
    tk.Label(config_frame, text="Ativar Animações:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=5, column=0, sticky="e")
    ttk.Checkbutton(config_frame, variable=animacoes_var).grid(row=5, column=1, sticky="w", padx=10)

    # Layout
    layout_var = tk.StringVar(value="Padrão")
    tk.Label(config_frame, text="Layout da Interface:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=6, column=0, sticky="e")
    ttk.Combobox(config_frame, textvariable=layout_var, values=["Padrão", "Compacto", "Espaçado"], width=20).grid(row=6, column=1, padx=10, pady=5)

    # Aplicar/Restaurar
    botoes_frame = tk.Frame(frame, bg="#f0f0f0")
    botoes_frame.pack(pady=20)

    def aplicar_personalizacao():
        config = {
            "tema": tema_var.get(),
            "cor_destaque": cor_destaque.get(),
            "fonte": fonte_var.get(),
            "tamanho_fonte": tamanho_var.get(),
            "icones": icones_var.get(),
            "animacoes": animacoes_var.get(),
            "layout": layout_var.get()
        }
        os.makedirs("config", exist_ok=True)
        with open("config/interface.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        messagebox.showinfo("Sucesso", "Preferências salvas! Reinicie o sistema para aplicar.")

    def restaurar_padroes():
        tema_var.set("Claro")
        cor_destaque.set("#004080")
        cor_preview.config(bg="#004080")
        fonte_var.set("Helvetica")
        tamanho_var.set(12)
        icones_var.set("Emojis")
        animacoes_var.set(True)
        layout_var.set("Padrão")
        messagebox.showinfo("Restaurado", "Preferências restauradas para o padrão.")

    tk.Button(botoes_frame, text="💾 Aplicar Preferências", bg="#0066cc", fg="white",
              font=("Helvetica", 12, "bold"), command=aplicar_personalizacao).pack(side="left", padx=10)

    tk.Button(botoes_frame, text="🔄 Restaurar Padrões", bg="#cccccc", fg="black",
              font=("Helvetica", 12), command=restaurar_padroes).pack(side="left", padx=10)

    def carregar_preferencias():
        try:
            with open("config/interface.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                tema_var.set(config.get("tema", "Claro"))
                cor_destaque.set(config.get("cor_destaque", "#004080"))
                cor_preview.config(bg=cor_destaque.get())
                fonte_var.set(config.get("fonte", "Helvetica"))
                tamanho_var.set(config.get("tamanho_fonte", 12))
                icones_var.set(config.get("icones", "Emojis"))
                animacoes_var.set(config.get("animacoes", True))
                layout_var.set(config.get("layout", "Padrão"))
        except FileNotFoundError:
            pass

    carregar_preferencias()
