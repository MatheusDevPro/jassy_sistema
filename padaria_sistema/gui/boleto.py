import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# Função para gerar o boleto com layout realista
def gerar_boleto_pdf(dados):
    nome_arquivo = f"boleto_{dados['nosso_numero']}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    # Cabeçalho do boleto
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, altura - 50, "BOLETO BANCÁRIO - FICTÍCIO")

    # Dados do cedente
    c.setFont("Helvetica", 10)
    c.drawString(50, altura - 100, f"Cedente: {dados['cedente']} ({dados['cpf_cnpj_cedente']})")
    c.drawString(50, altura - 120, f"Agência: {dados['agencia']} - Conta: {dados['conta']}")
    c.drawString(50, altura - 140, f"Nosso Número: {dados['nosso_numero']}")
    
    # Dados do boleto
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, altura - 170, f"Valor: R$ {dados['valor']:.2f}")
    c.drawString(50, altura - 190, f"Vencimento: {dados['vencimento']}")

    # Dados do pagador
    c.setFont("Helvetica", 10)
    c.drawString(50, altura - 220, f"Pagador: {dados['pagador']} ({dados['cpf_cnpj_pagador']})")
    c.drawString(50, altura - 240, f"Endereço: {dados['endereco_pagador']}")
    c.drawString(50, altura - 260, f"Cidade/UF: {dados['cidade_pagador']} / {dados['uf_pagador']} - CEP: {dados['cep_pagador']}")

    # Código de barras (apenas visual, não funcional)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(50, altura - 300, "CÓDIGO DE BARRAS:")
    c.setFont("Courier", 10)
    c.drawString(50, altura - 320, "| 00190.00009 01234.567890 12345.678904 8 88880000050000 |")

    # Instruções de pagamento
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, altura - 350, "Pagamento até o vencimento, após essa data, acrescer encargos.")

    # Rodapé com instruções gerais
    c.setFont("Helvetica", 6)
    c.drawString(50, 50, "Este boleto é fictício e gerado para fins de demonstração. Não possui validade para pagamento.")

    c.save()
    os.startfile(nome_arquivo)  # Abrir automaticamente no Windows

def tela_emissao_boletos(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
          widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📄 Emissão de Boletos", font=("Helvetica", 18, "bold"),
             bg="#f8f8ff", fg="#004d66").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#f8f8ff")
    campos_frame.pack(pady=10)

    campos = {
        "Cedente": tk.Entry(campos_frame, width=30),
        "CPF/CNPJ Cedente": tk.Entry(campos_frame, width=30),
        "Agência": tk.Entry(campos_frame, width=10),
        "Conta": tk.Entry(campos_frame, width=10),
        "Nosso Número": tk.Entry(campos_frame, width=15),
        "Data Vencimento": tk.Entry(campos_frame, width=15),
        "Valor": tk.Entry(campos_frame, width=10),
        "Pagador": tk.Entry(campos_frame, width=30),
        "CPF/CNPJ Pagador": tk.Entry(campos_frame, width=30),
        "Endereço Pagador": tk.Entry(campos_frame, width=30),
        "Cidade Pagador": tk.Entry(campos_frame, width=20),
        "UF Pagador": tk.Entry(campos_frame, width=2),
        "CEP Pagador": tk.Entry(campos_frame, width=10)
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 11), bg="#f8f8ff") \
            .grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entrada.grid(row=i, column=1, padx=10, pady=5, sticky="w")

    def emitir_boleto():
        try:
            dados = {
                "cedente": campos["Cedente"].get(),
                "cpf_cnpj_cedente": campos["CPF/CNPJ Cedente"].get(),
                "agencia": campos["Agência"].get(),
                "conta": campos["Conta"].get(),
                "nosso_numero": campos["Nosso Número"].get(),
                "vencimento": campos["Data Vencimento"].get(),
                "valor": float(campos["Valor"].get().replace(",", ".")),
                "pagador": campos["Pagador"].get(),
                "cpf_cnpj_pagador": campos["CPF/CNPJ Pagador"].get(),
                "endereco_pagador": campos["Endereço Pagador"].get(),
                "cidade_pagador": campos["Cidade Pagador"].get(),
                "uf_pagador": campos["UF Pagador"].get(),
                "cep_pagador": campos["CEP Pagador"].get()
            }

            if not all(dados.values()):
                raise ValueError("Todos os campos devem ser preenchidos.")
            
            datetime.strptime(dados["vencimento"], "%d/%m/%Y")  # Validação da data

            gerar_boleto_pdf(dados)
            messagebox.showinfo("Sucesso", "Boleto PDF gerado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar boleto:\n{e}")

    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=10)

    ttk.Button(botoes_frame, text="🖨️ Emitir Boleto", width=20, command=emitir_boleto).pack(side="left", padx=10)
