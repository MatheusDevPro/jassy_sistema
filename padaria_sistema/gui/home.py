import tkinter as tk
from tkinter import ttk

def mostrar_home(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.configure(bg="#f0f4f8")
    frame = tk.Frame(janela, bg="#f0f4f8")
    frame.pack(fill="both", expand=True)

    # Título
    titulo = tk.Label(frame, text="🤖 Jessy - Gestão Integrada", font=("Segoe UI", 26, "bold"),
                      bg="#f0f4f8", fg="#2c3e50")
    titulo.pack(pady=(30, 10))

    subtitulo = tk.Label(frame, text="Tecnologia para impulsionar seu negócio", font=("Segoe UI", 15, "italic"),
                         bg="#f0f4f8", fg="#34495e")
    subtitulo.pack()

    # Cards de atalho
    card_frame = tk.Frame(frame, bg="#f0f4f8")
    card_frame.pack(pady=20)

    def criar_card(texto, emoji, cor):
        card = tk.Frame(card_frame, bg=cor, width=140, height=100, bd=1, relief="ridge")
        card.pack_propagate(0)
        label = tk.Label(card, text=f"{emoji}\n{texto}", font=("Segoe UI", 11, "bold"),
                         fg="white", bg=cor, justify="center")
        label.pack(expand=True)
        return card

    criar_card("Estoque", "📦", "#2980b9").grid(row=0, column=0, padx=10)
    criar_card("Vendas", "🛒", "#27ae60").grid(row=0, column=1, padx=10)
    criar_card("Financeiro", "💰", "#d35400").grid(row=0, column=2, padx=10)
    criar_card("Relatórios", "📈", "#8e44ad").grid(row=0, column=3, padx=10)

    # Painel visual com gráficos
    painel = tk.Frame(frame, bg="white", bd=2, relief="groove")
    painel.pack(padx=40, pady=20, fill="both", expand=False)

    titulo_painel = tk.Label(painel, text="📊 Indicadores Rápidos", font=("Segoe UI", 14, "bold"),
                             bg="white", fg="#2c3e50")
    titulo_painel.pack(pady=(10, 0))

    canvas = tk.Canvas(painel, width=520, height=230, bg="#ffffff", highlightthickness=0)
    canvas.pack(pady=15)

    barra_cores = ["#5dade2", "#58d68d", "#f5b041", "#af7ac5", "#ec7063"]
    alturas = [100, 140, 90, 120, 110]
    rotulos = ["Vendas", "Estoque", "Compras", "Pedidos", "Clientes"]

    for i, (altura, cor, rotulo) in enumerate(zip(alturas, barra_cores, rotulos)):
        x0 = 60 + i * 85
        y0 = 180 - altura
        x1 = x0 + 40
        y1 = 180
        canvas.create_rectangle(x0, y0, x1, y1, fill=cor, width=0)
        canvas.create_text(x0 + 20, y1 + 15, text=rotulo, font=("Segoe UI", 10), fill="#34495e")

    canvas.create_text(260, 215, text="Gráfico ilustrativo de desempenho", font=("Segoe UI", 9), fill="#888")

    # Bloco de Notificações
    notificacoes = tk.LabelFrame(frame, text="🔔 Notificações do Sistema", font=("Segoe UI", 12, "bold"),
                                 bg="#fefefe", fg="#2c3e50", padx=10, pady=10)
    notificacoes.pack(padx=40, pady=10, fill="x")

    tk.Label(notificacoes, text="⚠️  Estoque de Farinha está abaixo do mínimo!", font=("Segoe UI", 10),
             bg="#fefefe", fg="#c0392b").pack(anchor="w", pady=2)

    tk.Label(notificacoes, text="✅  Backup automático realizado hoje às 02:00.", font=("Segoe UI", 10),
             bg="#fefefe", fg="#27ae60").pack(anchor="w", pady=2)

    tk.Label(notificacoes, text="📦  Novas requisições aguardando aprovação.", font=("Segoe UI", 10),
             bg="#fefefe", fg="#2980b9").pack(anchor="w", pady=2)

    # Resumo Rápido
    resumo_frame = tk.Frame(frame, bg="#f0f4f8")
    resumo_frame.pack(pady=(10, 30))

    def resumo_dado(titulo, valor, cor):
        bloco = tk.Frame(resumo_frame, bg=cor, width=150, height=60, bd=1, relief="solid")
        bloco.pack_propagate(0)
        tk.Label(bloco, text=titulo, font=("Segoe UI", 10, "bold"), fg="white", bg=cor).pack()
        tk.Label(bloco, text=valor, font=("Segoe UI", 14), fg="white", bg=cor).pack()
        return bloco

    resumo_dado("🧾 Produtos", "128", "#3498db").grid(row=0, column=0, padx=10)
    resumo_dado("📊 Vendas Hoje", "R$ 1.430,00", "#2ecc71").grid(row=0, column=1, padx=10)
    resumo_dado("🕒 Pendentes", "5 Pedidos", "#f39c12").grid(row=0, column=2, padx=10)
    resumo_dado("👥 Clientes", "74 ativos", "#9b59b6").grid(row=0, column=3, padx=10)

    # Rodapé
    rodape = tk.Label(frame, text="🛈 Sistema atualizado com as últimas melhorias - Versão 1.2",
                      font=("Segoe UI", 9), bg="#f0f4f8", fg="#7f8c8d")
    rodape.pack(pady=(5, 20))
