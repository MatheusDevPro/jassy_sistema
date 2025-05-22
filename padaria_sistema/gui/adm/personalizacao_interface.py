import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font
import json
import os


def tela_personalizacao_interface(janela):
    # Limpar widgets anteriores (exceto menu)
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f0f0f0")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="🎨 Personalização da Interface", font=("Helvetica", 20, "bold"),
             bg="#f0f0f0", fg="#333").pack(pady=20)

    config_frame = tk.LabelFrame(frame, text="Preferências Visuais", bg="#f0f0f0",
                                 font=("Helvetica", 14, "bold"), fg="#00334d", padx=20, pady=20)
    config_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Função para criar labels e widgets com padrão
    def cria_label(texto, linha):
        return tk.Label(config_frame, text=texto, bg="#f0f0f0", font=("Helvetica", 12), anchor="e")

    # Variáveis
    tema_var = tk.StringVar(value="Claro")
    cor_destaque = tk.StringVar(value="#004080")
    fonte_var = tk.StringVar(value="Helvetica")
    tamanho_var = tk.IntVar(value=12)
    icones_var = tk.StringVar(value="Emojis")
    animacoes_var = tk.BooleanVar(value=True)
    layout_var = tk.StringVar(value="Padrão")
    cor_fundo_var = tk.StringVar(value="#ffffff")
    cor_texto_var = tk.StringVar(value="#000000")
    espaco_entre_widgets_var = tk.IntVar(value=10)
    borda_entradas_var = tk.IntVar(value=2)
    usar_sombra_var = tk.BooleanVar(value=True)
    estilo_botoes_var = tk.StringVar(value="Padrão")
    mostrar_dicas_var = tk.BooleanVar(value=True)

    # Linha 0: Tema
    cria_label("Tema:", 0).grid(row=0, column=0, sticky="e", pady=6)
    ttk.Combobox(config_frame, textvariable=tema_var, values=["Claro", "Escuro", "Personalizado"], width=25).grid(row=0, column=1, padx=10, pady=6, sticky="w")

    # Linha 1: Cor de Destaque
    cria_label("Cor de Destaque:", 1).grid(row=1, column=0, sticky="e", pady=6)
    cor_preview = tk.Label(config_frame, width=3, bg=cor_destaque.get(), relief="solid")
    cor_preview.grid(row=1, column=2, padx=5)
    def escolher_cor_destaque():
        cor = colorchooser.askcolor(title="Escolha a cor de destaque")
        if cor[1]:
            cor_destaque.set(cor[1])
            cor_preview.config(bg=cor[1])
    tk.Button(config_frame, text="Selecionar Cor", command=escolher_cor_destaque).grid(row=1, column=1, padx=10, pady=6, sticky="w")

    # Linha 2: Cor de Fundo (se tema personalizado)
    cria_label("Cor de Fundo:", 2).grid(row=2, column=0, sticky="e", pady=6)
    cor_fundo_preview = tk.Label(config_frame, width=3, bg=cor_fundo_var.get(), relief="solid")
    cor_fundo_preview.grid(row=2, column=2, padx=5)
    def escolher_cor_fundo():
        cor = colorchooser.askcolor(title="Escolha a cor de fundo")
        if cor[1]:
            cor_fundo_var.set(cor[1])
            cor_fundo_preview.config(bg=cor[1])
    tk.Button(config_frame, text="Selecionar Cor", command=escolher_cor_fundo).grid(row=2, column=1, padx=10, pady=6, sticky="w")

    # Linha 3: Cor do Texto (se tema personalizado)
    cria_label("Cor do Texto:", 3).grid(row=3, column=0, sticky="e", pady=6)
    cor_texto_preview = tk.Label(config_frame, width=3, bg=cor_texto_var.get(), relief="solid")
    cor_texto_preview.grid(row=3, column=2, padx=5)
    def escolher_cor_texto():
        cor = colorchooser.askcolor(title="Escolha a cor do texto")
        if cor[1]:
            cor_texto_var.set(cor[1])
            cor_texto_preview.config(bg=cor[1])
    tk.Button(config_frame, text="Selecionar Cor", command=escolher_cor_texto).grid(row=3, column=1, padx=10, pady=6, sticky="w")

    # Linha 4: Fonte
    cria_label("Fonte:", 4).grid(row=4, column=0, sticky="e", pady=6)
    fontes_disponiveis = list(font.families())
    fontes_disponiveis.sort()
    ttk.Combobox(config_frame, textvariable=fonte_var,
                 values=fontes_disponiveis, width=25).grid(row=4, column=1, padx=10, pady=6, sticky="w")

    # Linha 5: Tamanho da Fonte
    cria_label("Tamanho da Fonte:", 5).grid(row=5, column=0, sticky="e", pady=6)
    tk.Spinbox(config_frame, from_=8, to=48, textvariable=tamanho_var, width=6).grid(row=5, column=1, padx=10, pady=6, sticky="w")

    # Linha 6: Espaçamento entre Widgets
    cria_label("Espaçamento (px):", 6).grid(row=6, column=0, sticky="e", pady=6)
    tk.Spinbox(config_frame, from_=0, to=50, textvariable=espaco_entre_widgets_var, width=6).grid(row=6, column=1, padx=10, pady=6, sticky="w")

    # Linha 7: Borda das Entradas
    cria_label("Borda das Entradas:", 7).grid(row=7, column=0, sticky="e", pady=6)
    tk.Spinbox(config_frame, from_=0, to=10, textvariable=borda_entradas_var, width=6).grid(row=7, column=1, padx=10, pady=6, sticky="w")

    # Linha 8: Estilo dos Ícones
    cria_label("Estilo dos Ícones:", 8).grid(row=8, column=0, sticky="e", pady=6)
    ttk.Combobox(config_frame, textvariable=icones_var, values=["Emojis", "Clássicos", "Minimalistas", "Personalizados"], width=25).grid(row=8, column=1, padx=10, pady=6, sticky="w")

    # Linha 9: Estilo dos Botões
    cria_label("Estilo dos Botões:", 9).grid(row=9, column=0, sticky="e", pady=6)
    ttk.Combobox(config_frame, textvariable=estilo_botoes_var, values=["Padrão", "Arredondado", "Plano", "3D"], width=25).grid(row=9, column=1, padx=10, pady=6, sticky="w")

    # Linha 10: Ativar Animações
    cria_label("Ativar Animações:", 10).grid(row=10, column=0, sticky="e", pady=6)
    ttk.Checkbutton(config_frame, variable=animacoes_var).grid(row=10, column=1, sticky="w", padx=10)

    # Linha 11: Usar sombra em widgets
    cria_label("Usar sombra em widgets:", 11).grid(row=11, column=0, sticky="e", pady=6)
    ttk.Checkbutton(config_frame, variable=usar_sombra_var).grid(row=11, column=1, sticky="w", padx=10)

    # Linha 12: Layout da Interface
    cria_label("Layout da Interface:", 12).grid(row=12, column=0, sticky="e", pady=6)
    ttk.Combobox(config_frame, textvariable=layout_var, values=["Padrão", "Compacto", "Espaçado", "Customizado"], width=25).grid(row=12, column=1, padx=10, pady=6, sticky="w")

    # Linha 13: Mostrar dicas e tooltips
    cria_label("Mostrar dicas:", 13).grid(row=13, column=0, sticky="e", pady=6)
    ttk.Checkbutton(config_frame, variable=mostrar_dicas_var).grid(row=13, column=1, sticky="w", padx=10)

    # Botões para aplicar e restaurar preferências
    botoes_frame = tk.Frame(frame, bg="#f0f0f0")
    botoes_frame.pack(pady=20)

    def aplicar_personalizacao():
        config = {
            "tema": tema_var.get(),
            "cor_destaque": cor_destaque.get(),
            "cor_fundo": cor_fundo_var.get(),
            "cor_texto": cor_texto_var.get(),
            "fonte": fonte_var.get(),
            "tamanho_fonte": tamanho_var.get(),
            "espaco_entre_widgets": espaco_entre_widgets_var.get(),
            "borda_entradas": borda_entradas_var.get(),
            "icones": icones_var.get(),
            "estilo_botoes": estilo_botoes_var.get(),
            "animacoes": animacoes_var.get(),
            "usar_sombra": usar_sombra_var.get(),
            "layout": layout_var.get(),
            "mostrar_dicas": mostrar_dicas_var.get()
        }
        os.makedirs("config", exist_ok=True)
        with open("config/interface.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        messagebox.showinfo("Sucesso", "Preferências salvas! Reinicie o sistema para aplicar.")

    def restaurar_padroes():
        tema_var.set("Claro")
        cor_destaque.set("#004080")
        cor_preview.config(bg="#004080")
        cor_fundo_var.set("#ffffff")
        cor_fundo_preview.config(bg="#ffffff")
        cor_texto_var.set("#000000")
        cor_texto_preview.config(bg="#000000")
        fonte_var.set("Helvetica")
        tamanho_var.set(12)
        espaco_entre_widgets_var.set(10)
        borda_entradas_var.set(2)
        icones_var.set("Emojis")
        estilo_botoes_var.set("Padrão")
        animacoes_var.set(True)
        usar_sombra_var.set(True)
        layout_var.set("Padrão")
        mostrar_dicas_var.set(True)
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
                cor_fundo_var.set(config.get("cor_fundo", "#ffffff"))
                cor_fundo_preview.config(bg=cor_fundo_var.get())
                cor_texto_var.set(config.get("cor_texto", "#000000"))
                cor_texto_preview.config(bg=cor_texto_var.get())
                fonte_var.set(config.get("fonte", "Helvetica"))
                tamanho_var.set(config.get("tamanho_fonte", 12))
                espaco_entre_widgets_var.set(config.get("espaco_entre_widgets", 10))
                borda_entradas_var.set(config.get("borda_entradas", 2))
                icones_var.set(config.get("icones", "Emojis"))
                estilo_botoes_var.set(config.get("estilo_botoes", "Padrão"))
                animacoes_var.set(config.get("animacoes", True))
                usar_sombra_var.set(config.get("usar_sombra", True))
                layout_var.set(config.get("layout", "Padrão"))
                mostrar_dicas_var.set(config.get("mostrar_dicas", True))
        except FileNotFoundError:
            pass

    carregar_preferencias()
