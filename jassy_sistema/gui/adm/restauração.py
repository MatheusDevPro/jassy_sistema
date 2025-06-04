import tkinter as tk
from tkinter import messagebox, filedialog
import os
import zipfile
import datetime

def tela_backup(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    frame = tk.Frame(janela, bg="#fffaf0")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="💾 Backup / Restauração", font=("Helvetica", 18, "bold"),
             bg="#fffaf0", fg="#333333").pack(pady=20)

    descricao = tk.Label(frame, text="Faça backup e restaure os dados do sistema com segurança.",
                         font=("Helvetica", 12), bg="#fffaf0", fg="#555555")
    descricao.pack(pady=5)

    info_ultimo_backup = tk.Label(frame, text="", font=("Helvetica", 11, "italic"), bg="#fffaf0", fg="#666666")
    info_ultimo_backup.pack(pady=10)

    def atualizar_info_backup():
        if os.path.exists("dados/ultimo_backup.txt"):
            with open("dados/ultimo_backup.txt", "r", encoding="utf-8") as f:
                data = f.read().strip()
                info_ultimo_backup.config(text=f"🕒 Último backup realizado em: {data}")
        else:
            info_ultimo_backup.config(text="🕒 Nenhum backup encontrado.")

    def realizar_backup():
        try:
            os.makedirs("backups", exist_ok=True)
            data_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"backup_{data_str}.zip"
            caminho_backup = os.path.join("backups", nome_arquivo)

            with zipfile.ZipFile(caminho_backup, "w") as zipf:
                for pasta_raiz, _, arquivos in os.walk("dados"):
                    for arquivo in arquivos:
                        caminho_completo = os.path.join(pasta_raiz, arquivo)
                        zipf.write(caminho_completo, arcname=os.path.relpath(caminho_completo, "dados"))

            with open("dados/ultimo_backup.txt", "w", encoding="utf-8") as f:
                f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

            messagebox.showinfo("Backup Concluído", f"Backup salvo em '{caminho_backup}'.")
            atualizar_info_backup()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar backup:\n{str(e)}")

    def restaurar_backup():
        arquivo = filedialog.askopenfilename(title="Selecionar Arquivo de Backup",
                                             filetypes=[("Arquivos ZIP", "*.zip")])
        if not arquivo:
            return

        try:
            with zipfile.ZipFile(arquivo, "r") as zipf:
                zipf.extractall("dados")

            messagebox.showinfo("Restauração Concluída", "Backup restaurado com sucesso.")
            with open("dados/ultimo_backup.txt", "w", encoding="utf-8") as f:
                f.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

            atualizar_info_backup()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar backup:\n{str(e)}")

    botoes_frame = tk.Frame(frame, bg="#fffaf0")
    botoes_frame.pack(pady=20)

    tk.Button(botoes_frame, text="🧷 Criar Backup", bg="#007b5f", fg="white",
              font=("Helvetica", 12, "bold"), width=20, cursor="hand2", command=realizar_backup).pack(side="left", padx=15)

    tk.Button(botoes_frame, text="♻️ Restaurar Backup", bg="#b34700", fg="white",
              font=("Helvetica", 12, "bold"), width=20, cursor="hand2", command=restaurar_backup).pack(side="left", padx=15)

    atualizar_info_backup()
