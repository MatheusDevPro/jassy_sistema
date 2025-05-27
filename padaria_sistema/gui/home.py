import tkinter as tk
from tkinter import ttk

def mostrar_home(janela):
    style.theme_use('clam')

    # Limpa conteúdo anterior (exceto menu)
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.configure(bg="#f9f9f9")
    janela.geometry("1200x960")

    # --- Menu lateral ---
    menu_lateral = ttk.Frame(janela, width=180, relief="flat", style="Menu.TFrame")
    menu_lateral.pack(side="left", fill="y")

    # Estilo do menu lateral
    style.configure("Menu.TFrame", background="#f0f0f0")
    style.configure("Menu.TButton",
                    background="#f0f0f0", foreground="#555",
                    font=("Segoe UI", 11),
                    padding=8)
    style.map("Menu.TButton",
              background=[('active', '#d7d7d7')],
              foreground=[('active', '#222')])

    # Logo/Title no menu lateral
    logo = ttk.Label(menu_lateral, text="🤖 Jessy", font=("Segoe UI", 20, "bold"), background="#f0f0f0", foreground="#333")
    logo.pack(pady=30)

    # Botões do menu lateral
    def botao_menu(texto):
        btn = ttk.Button(menu_lateral, text=texto, style="Menu.TButton")
        btn.bind("<Enter>", lambda e: btn.configure(cursor="hand2"))
        btn.bind("<Leave>", lambda e: btn.configure(cursor=""))
        return btn

    botoes = ["🏠 Home", "📦 Estoque", "🛒 Vendas", "💰 Financeiro", "📈 Relatórios", "⚙ Configurações"]
    for b in botoes:
        botao_menu(b).pack(fill="x", padx=20, pady=6)

    # --- Conteúdo principal ---
    conteudo = ttk.Frame(janela, padding=30, style="Content.TFrame")
    conteudo.pack(side="left", fill="both", expand=True)

    # Estilo conteúdo
    style.configure("Content.TFrame", background="#f9f9f9")

    # Container centralizado (usando pack com expand + anchor center)
    centralizador = ttk.Frame(conteudo, style="Content.TFrame")
    centralizador.pack(expand=True)
    
    # Título e subtítulo
    titulo = ttk.Label(centralizador, text="Jessy - Gestão Integrada",
                       font=("Segoe UI", 28, "bold"), foreground="#444", background="#f9f9f9")
    titulo.pack(anchor="center")

    subtitulo = ttk.Label(centralizador, text="Tecnologia para impulsionar seu negócio",
                          font=("Segoe UI", 14, "italic"), foreground="#777", background="#f9f9f9")
    subtitulo.pack(anchor="center", pady=(5, 30))

    # Cards interativos
    cards_frame = ttk.Frame(centralizador, style="Content.TFrame")
    cards_frame.pack()

    def criar_card(parent, texto, emoji, cor):
        card = ttk.Frame(parent, width=160, height=110)
        card.pack_propagate(False)
        card.grid_propagate(False)

        # Cor neutra com destaque suave (usar bg claro e borda)
        card_style_name = f"{texto}.TFrame"
        style.configure(card_style_name,
                        background=cor,
                        relief="flat")
        card.configure(style=card_style_name)

        label = ttk.Label(card, text=f"{emoji}\n{texto}",
                          font=("Segoe UI", 13, "bold"),
                          foreground="white",
                          background=cor,
                          anchor="center", justify="center")
        label.pack(expand=True, fill="both")

        # Cursor e hover
        def enter(e):
            card.configure(relief="raised")
            card.configure(cursor="hand2")
        def leave(e):
            card.configure(relief="flat")
            card.configure(cursor="")
        card.bind("<Enter>", enter)
        card.bind("<Leave>", leave)

        def click_event(event):
            print(f"{texto} clicado!")
        card.bind("<Button-1>", click_event)
        label.bind("<Button-1>", click_event)

        return card

    # Cores neutras mais suaves e elegantes
    cores_cards = ["#4a90e2", "#50b948", "#f39c12", "#8e44ad"]
    textos = ["Estoque", "Vendas", "Financeiro", "Relatórios"]
    emojis = ["📦", "🛒", "💰", "📈"]

    for i, (t, e, c) in enumerate(zip(textos, emojis, cores_cards)):
        criar_card(cards_frame, t, e, c).grid(row=0, column=i, padx=12)

    # Separador
    sep = ttk.Separator(centralizador, orient="horizontal")
    sep.pack(fill="x", pady=25)

    # Indicadores gráficos simplificados
    indicadores_frame = ttk.Frame(centralizador, style="Content.TFrame")
    indicadores_frame.pack(fill="x")

    titulo_indicador = ttk.Label(indicadores_frame, text="Indicadores Rápidos",
                                 font=("Segoe UI", 18, "bold"),
                                 foreground="#444", background="#f9f9f9")
    titulo_indicador.pack(anchor="center", pady=(0, 15))

    canvas = tk.Canvas(indicadores_frame, height=220, bg="#fff", highlightthickness=1, highlightbackground="#ddd")
    canvas.pack(fill="x", padx=30)

    # Barras indicadores com cores neutras e vibrantes
    barra_cores = ["#5dade2", "#58d68d", "#f5b041", "#af7ac5", "#ec7063"]
    alturas = [100, 140, 90, 120, 110]
    rotulos = ["Vendas", "Estoque", "Compras", "Pedidos", "Clientes"]

    for i, (altura, cor, rotulo) in enumerate(zip(alturas, barra_cores, rotulos)):
        x0 = 80 + i * 90
        y0 = 180 - altura
        x1 = x0 + 45
        y1 = 180
        canvas.create_rectangle(x0, y0, x1, y1, fill=cor, width=0, outline="#444")
        canvas.create_text(x0 + 22, y1 + 20, text=rotulo, font=("Segoe UI", 10), fill="#444")

    canvas.create_text(350, 210, text="Gráfico ilustrativo de desempenho", font=("Segoe UI", 9), fill="#777")

    # Notificações estilo card
    notif_frame = ttk.LabelFrame(centralizador, text="Notificações do Sistema", padding=10)
    notif_frame.pack(fill="x", padx=30, pady=20)

    notificacoes = [
        ("⚠️ Validar Setor logistico alta demanda de trabalho!", "#c0392b"),
        ("✅ Backup automático realizado hoje às 15:00.", "#27ae60"),
        ("📦 Novas requisições estoque aguardando aprovação.", "#2980b9"),
    ]

    for msg, cor in notificacoes:
        label = ttk.Label(notif_frame, text=msg, foreground=cor, font=("Segoe UI", 11))
        label.pack(anchor="w", pady=2)

    # Resumo rápido com cards
    resumo_frame = ttk.Frame(centralizador, style="Content.TFrame")
    resumo_frame.pack(fill="x", pady=10)

    def resumo_card(parent, titulo, valor, cor):
        card = ttk.Frame(parent, width=160, height=70)
        card.pack_propagate(False)
        card.grid_propagate(False)

        style_name = f"{titulo}.TFrame"
        style.configure(style_name, background=cor, relief="flat")
        card.configure(style=style_name)

        ttk.Label(card, text=titulo, foreground="white", font=("Segoe UI", 11, "bold"), background=cor).pack(anchor="center")
        ttk.Label(card, text=valor, foreground="white", font=("Segoe UI", 15, "bold"), background=cor).pack(anchor="center")
        return card

    resumo_itens = [
        ("🧾 Produtos", "128", "#3498db"),
        ("📊 Vendas Hoje", "R$ 1.430,00", "#2ecc71"),
        ("🕒 Pendentes", "5 Pedidos", "#f39c12"),
        ("👥 Clientes", "74 ativos", "#9b59b6"),
    ]

    for i, (t, v, c) in enumerate(resumo_itens):
        resumo_card(resumo_frame, t, v, c).grid(row=0, column=i, padx=12)

    # Rodapé discreto
    rodape = ttk.Label(janela, text="🛈 Jassy Sistema Gestão - Versão 1.1",
                       font=("Segoe UI", 9), foreground="#999", background="#f9f9f9")
    rodape.pack(side="bottom", fill="x", pady=5)

# Exemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema Jessy - Home")
    mostrar_home(root)
    root.mainloop()
