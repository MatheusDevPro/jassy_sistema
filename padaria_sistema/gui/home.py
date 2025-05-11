import tkinter as tk

def mostrar_home(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f5f5f5")
    frame.pack(fill="both", expand=True)

    titulo = tk.Label(frame, text="🍞 Jessy - Gestão", font=("Helvetica", 24, "bold"), bg="#f5f5f5", fg="#2e4053")
    titulo.pack(pady=30)

    subtitulo = tk.Label(frame, text="Tecnologia para impulsionar seu negócio", font=("Helvetica", 16, "italic"), bg="#f5f5f5", fg="#34495e")
    subtitulo.pack(pady=10)

    texto = tk.Label(frame, text="Use o menu acima para navegar entre os módulos de gestão.\nControle de estoque, vendas, finanças e muito mais com facilidade.", font=("Helvetica", 13), bg="#f5f5f5", fg="#555")
    texto.pack(pady=20)

    # Desenho ilustrativo com Canvas (em vez da imagem)
    canvas = tk.Canvas(frame, width=500, height=300, bg="#ffffff", bd=2, relief="ridge")
    canvas.pack(pady=30)

    # Painel central (representa sistema)
    canvas.create_rectangle(100, 60, 400, 220, fill="#e8f8f5", outline="#2e86c1", width=2)
    canvas.create_text(250, 80, text="Painel de Gestão", font=("Helvetica", 14, "bold"), fill="#2e4053")

    # Gráficos (barras)
    canvas.create_rectangle(130, 180, 150, 210, fill="#76d7c4")
    canvas.create_rectangle(170, 160, 190, 210, fill="#f7dc6f")
    canvas.create_rectangle(210, 140, 230, 210, fill="#f1948a")
    canvas.create_rectangle(250, 170, 270, 210, fill="#a569bd")
    canvas.create_rectangle(290, 150, 310, 210, fill="#5dade2")

    # Engrenagem estilizada
    canvas.create_oval(360, 140, 390, 170, outline="#5d6d7e", width=2)
    canvas.create_line(375, 135, 375, 175, fill="#5d6d7e", width=2)
    canvas.create_line(355, 155, 395, 155, fill="#5d6d7e", width=2)

    # Ícone de gráfico circular
    canvas.create_oval(120, 100, 160, 140, fill="#d6eaf8", outline="#2980b9")
    canvas.create_arc(120, 100, 160, 140, start=0, extent=120, fill="#5dade2")

    # Pequeno texto inferior
    canvas.create_text(250, 240, text="Representação gráfica da gestão integrada", font=("Helvetica", 10), fill="#888")

