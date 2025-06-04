import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# Gera o PDF da nota fiscal
def gerar_nf_pdf(dados):
    os.makedirs("dados", exist_ok=True)
    nome_arquivo = os.path.join("dados", f"nota_fiscal_{dados['numero_nf']}.pdf")
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    # Cabeçalho
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, altura - 50, "NOTA FISCAL - FICTÍCIA")

    # Dados da empresa
    c.setFont("Helvetica", 10)
    c.drawString(50, altura - 90, f"Emitente: {dados['emitente']} ({dados['cnpj_emitente']})")
    c.drawString(50, altura - 110, f"Endereço: {dados['endereco_emitente']}")
    c.drawString(50, altura - 130, f"Cidade: {dados['cidade_emitente']} / {dados['uf_emitente']} - CEP: {dados['cep_emitente']}")

    # Dados da nota
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, altura - 160, f"Número NF: {dados['numero_nf']}")
    c.drawString(50, altura - 180, f"Data de Emissão: {dados['data_emissao']}")
    c.drawString(50, altura - 200, f"Valor Total: R$ {dados['valor_total']:.2f}")

    # Dados do cliente
    c.setFont("Helvetica", 10)
    c.drawString(50, altura - 230, f"Destinatário: {dados['cliente']} ({dados['cpf_cnpj_cliente']})")
    c.drawString(50, altura - 250, f"Endereço: {dados['endereco_cliente']}")
    c.drawString(50, altura - 270, f"Cidade/UF: {dados['cidade_cliente']} / {dados['uf_cliente']} - CEP: {dados['cep_cliente']}")

    # Observações
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, altura - 300, "Esta nota fiscal é fictícia e gerada apenas para fins de demonstração.")

    c.save()
    os.startfile(nome_arquivo)  # Abre automaticamente no Windows

# Tela gráfica de emissão de NF
def tela_emissao_nf(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#f8f8ff")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="📄 Emissão de Notas Fiscais", font=("Helvetica", 18, "bold"),
             bg="#f8f8ff", fg="#004d66").pack(pady=10)

    campos_frame = tk.Frame(frame, bg="#f8f8ff")
    campos_frame.pack(pady=10)

    campos = {
        "Emitente": tk.Entry(campos_frame, width=30),
        "CNPJ Emitente": tk.Entry(campos_frame, width=20),
        "Endereço Emitente": tk.Entry(campos_frame, width=30),
        "Cidade Emitente": tk.Entry(campos_frame, width=20),
        "UF Emitente": tk.Entry(campos_frame, width=10),
        "CEP Emitente": tk.Entry(campos_frame, width=10),
        "Número NF": tk.Entry(campos_frame, width=15),
        "Data de Emissão": tk.Entry(campos_frame, width=15),
        "Valor Total": tk.Entry(campos_frame, width=10),
        "Cliente": tk.Entry(campos_frame, width=30),
        "CPF/CNPJ Cliente": tk.Entry(campos_frame, width=20),
        "Endereço Cliente": tk.Entry(campos_frame, width=30),
        "Cidade Cliente": tk.Entry(campos_frame, width=20),
        "UF Cliente": tk.Entry(campos_frame, width=10),
        "CEP Cliente": tk.Entry(campos_frame, width=10)
    }

    for i, (rotulo, entrada) in enumerate(campos.items()):
        tk.Label(campos_frame, text=rotulo + ":", font=("Helvetica", 11), bg="#f8f8ff") \
            .grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entrada.grid(row=i, column=1, padx=10, pady=5, sticky="w")

    def emitir_nf():
        try:
            dados = {
                "emitente": campos["Emitente"].get(),
                "cnpj_emitente": campos["CNPJ Emitente"].get(),
                "endereco_emitente": campos["Endereço Emitente"].get(),
                "cidade_emitente": campos["Cidade Emitente"].get(),
                "uf_emitente": campos["UF Emitente"].get(),
                "cep_emitente": campos["CEP Emitente"].get(),
                "numero_nf": campos["Número NF"].get(),
                "data_emissao": campos["Data de Emissão"].get(),
                "valor_total": float(campos["Valor Total"].get().replace(",", ".")),
                "cliente": campos["Cliente"].get(),
                "cpf_cnpj_cliente": campos["CPF/CNPJ Cliente"].get(),
                "endereco_cliente": campos["Endereço Cliente"].get(),
                "cidade_cliente": campos["Cidade Cliente"].get(),
                "uf_cliente": campos["UF Cliente"].get(),
                "cep_cliente": campos["CEP Cliente"].get()
            }

            if not all(dados.values()):
                raise ValueError("Todos os campos devem ser preenchidos.")
            
            datetime.strptime(dados["data_emissao"], "%d/%m/%Y")

            gerar_nf_pdf(dados)
            messagebox.showinfo("Sucesso", "Nota fiscal gerada com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar nota fiscal:\n{e}")

    botoes_frame = tk.Frame(frame, bg="#f8f8ff")
    botoes_frame.pack(pady=10)

    ttk.Button(botoes_frame, text="🖨️ Emitir Nota", width=20, command=emitir_nf).pack(side="left", padx=10)
