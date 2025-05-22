import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import re

class Tooltip:
    """Tooltip simples para widgets Tkinter"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + cy + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Remove bordas
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=5, ipady=3)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def tela_parametros_sistema(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.configure(bg="#f0f4f7")

    frame = ttk.Frame(janela, padding=15)
    frame.pack(fill="both", expand=True)

    titulo = ttk.Label(frame, text="🛠️ Parâmetros do Sistema", font=("Helvetica", 20, "bold"), foreground="#003366")
    titulo.pack(pady=(0,15))

    # Frame Configurações Gerais
    campos_frame = ttk.LabelFrame(frame, text="Configurações Gerais")
    campos_frame.pack(fill="x", pady=10)

    # Dicionário para guardar widgets de entrada
    parametros = {}

    def criar_label_entry(texto, linha, largura=40, tooltip_text=None):
        label = ttk.Label(campos_frame, text=texto + ":")
        label.grid(row=linha, column=0, sticky="e", padx=8, pady=6)
        entry = ttk.Entry(campos_frame, width=largura)
        entry.grid(row=linha, column=1, sticky="w", padx=8, pady=6)
        if tooltip_text:
            Tooltip(entry, tooltip_text)
        return entry

    parametros["Nome do Sistema"] = criar_label_entry("Nome do Sistema", 0, tooltip_text="Nome do software/sistema")
    parametros["Nome da Empresa"] = criar_label_entry("Nome da Empresa", 1)
    parametros["CNPJ"] = criar_label_entry("CNPJ", 2, tooltip_text="Formato: 00.000.000/0000-00")
    parametros["Telefone da Empresa"] = criar_label_entry("Telefone da Empresa", 3, tooltip_text="DDD + Número")
    parametros["Email de Notificações"] = criar_label_entry("Email de Notificações", 4)
    parametros["Site da Empresa"] = criar_label_entry("Site da Empresa", 5, tooltip_text="URL completa, ex: https://exemplo.com")
    parametros["Endereço"] = criar_label_entry("Endereço", 6)
    parametros["Horário de Atendimento"] = criar_label_entry("Horário de Atendimento", 7, tooltip_text="Ex: Seg-Sex 8h às 18h")
    parametros["Caminho para Backups"] = criar_label_entry("Caminho para Backups", 8)

    def selecionar_pasta_backup():
        caminho = filedialog.askdirectory()
        if caminho:
            parametros["Caminho para Backups"].delete(0, tk.END)
            parametros["Caminho para Backups"].insert(0, caminho)

    btn_selecionar_pasta = ttk.Button(campos_frame, text="Selecionar Pasta", command=selecionar_pasta_backup)
    btn_selecionar_pasta.grid(row=8, column=2, padx=8, pady=6)

    parametros["Impressora Padrão"] = criar_label_entry("Impressora Padrão", 9, tooltip_text="Nome da impressora no sistema")

    # Frame Preferências
    opcoes_frame = ttk.LabelFrame(frame, text="Preferências")
    opcoes_frame.pack(fill="x", pady=10)

    ttk.Label(opcoes_frame, text="Tema do Sistema:").grid(row=0, column=0, sticky="e", padx=8, pady=5)
    tema = ttk.Combobox(opcoes_frame, values=["Claro", "Escuro"], state="readonly", width=37)
    tema.grid(row=0, column=1, sticky="w", padx=8, pady=5)
    tema.set("Claro")

    ttk.Label(opcoes_frame, text="Casas Decimais:").grid(row=1, column=0, sticky="e", padx=8, pady=5)
    casas_decimais = ttk.Combobox(opcoes_frame, values=["0","1", "2", "3", "4"], state="readonly", width=37)
    casas_decimais.grid(row=1, column=1, sticky="w", padx=8, pady=5)
    casas_decimais.set("2")

    ttk.Label(opcoes_frame, text="Backup Automático:").grid(row=2, column=0, sticky="e", padx=8, pady=5)
    intervalo_backup = ttk.Combobox(opcoes_frame, values=["Desativado", "Diário", "Semanal", "Mensal"], state="readonly", width=37)
    intervalo_backup.grid(row=2, column=1, sticky="w", padx=8, pady=5)
    intervalo_backup.set("Semanal")

    exibir_popup = tk.BooleanVar(value=True)
    check_popup = ttk.Checkbutton(opcoes_frame, text="Exibir mensagens pop-up", variable=exibir_popup)
    check_popup.grid(row=3, column=1, sticky="w", pady=8, padx=8)

    # Checkbox para ativar logs detalhados
    logs_detalhados = tk.BooleanVar(value=False)
    check_logs = ttk.Checkbutton(opcoes_frame, text="Ativar logs detalhados", variable=logs_detalhados)
    check_logs.grid(row=4, column=1, sticky="w", pady=8, padx=8)

    # Testar conexão com impressora (simulado)
    def testar_impressora():
        nome_imp = parametros["Impressora Padrão"].get().strip()
        if not nome_imp:
            messagebox.showwarning("Aviso", "Informe o nome da impressora para testar a conexão.")
            return
        # Aqui poderia ser um teste real, mas simularemos
        messagebox.showinfo("Teste Impressora", f"Conexão com impressora '{nome_imp}' testada com sucesso!")

    btn_teste_impressora = ttk.Button(opcoes_frame, text="Testar Impressora", command=testar_impressora)
    btn_teste_impressora.grid(row=5, column=1, sticky="w", padx=8, pady=(0,10))

    # Funções para salvar/carregar/resetar configurações
    arquivo_config = "dados/parametros_sistema.json"

    def validar_email(email):
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(regex, email) is not None

    def validar_cnpj(cnpj):
        # Simples validação de formato
        regex = r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$'
        return re.match(regex, cnpj) is not None

    def validar_caminho(caminho):
        return os.path.isdir(caminho)

    def validar_campos():
        cnpj = parametros["CNPJ"].get().strip()
        email = parametros["Email de Notificações"].get().strip()
        caminho = parametros["Caminho para Backups"].get().strip()

        if cnpj and not validar_cnpj(cnpj):
            messagebox.showerror("Erro", "CNPJ inválido. Use o formato 00.000.000/0000-00")
            return False
        if email and not validar_email(email):
            messagebox.showerror("Erro", "Email inválido.")
            return False
        if caminho and not validar_caminho(caminho):
            messagebox.showerror("Erro", "Caminho para backups inválido ou não encontrado.")
            return False
        return True

    def salvar_parametros():
        if not validar_campos():
            return

        dados = {k: e.get().strip() for k, e in parametros.items()}
        dados.update({
            "Tema": tema.get(),
            "Casas Decimais": casas_decimais.get(),
            "Backup Automático": intervalo_backup.get(),
            "Exibir Pop-up": exibir_popup.get(),
            "Logs Detalhados": logs_detalhados.get()
        })

        os.makedirs("dados", exist_ok=True)
        try:
            with open(arquivo_config, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Sucesso", "Parâmetros salvos com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar parâmetros:\n{e}")

    def carregar_parametros():
        if not os.path.exists(arquivo_config):
            return
        try:
            with open(arquivo_config, "r", encoding="utf-8") as f:
                dados = json.load(f)
            for k, e in parametros.items():
                e.delete(0, tk.END)
                e.insert(0, dados.get(k, ""))
            tema.set(dados.get("Tema", "Claro"))
            casas_decimais.set(dados.get("Casas Decimais", "2"))
            intervalo_backup.set(dados.get("Backup Automático", "Semanal"))
            exibir_popup.set(dados.get("Exibir Pop-up", True))
            logs_detalhados.set(dados.get("Logs Detalhados", False))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar parâmetros:\n{e}")

    def resetar_campos():
        for e in parametros.values():
            e.delete(0, tk.END)
        tema.set("Claro")
        casas_decimais.set("2")
        intervalo_backup.set("Semanal")
        exibir_popup.set(True)
        logs_detalhados.set(False)

    def limpar_config_salva():
        if os.path.exists(arquivo_config):
            if messagebox.askyesno("Confirmar", "Deseja realmente apagar as configurações salvas?"):
                try:
                    os.remove(arquivo_config)
                    resetar_campos()
                    messagebox.showinfo("Sucesso", "Configurações salvas apagadas.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao apagar configurações:\n{e}")
        else:
            messagebox.showinfo("Info", "Não há configurações salvas para apagar.")

    # Frame Botões
    botoes = ttk.Frame(frame)
    botoes.pack(pady=15)

    btn_salvar = ttk.Button(botoes, text="💾 Salvar", command=salvar_parametros)
    btn_salvar.grid(row=0, column=0, padx=8)

    btn_carregar = ttk.Button(botoes, text="🔄 Carregar", command=carregar_parametros)
    btn_carregar.grid(row=0, column=1, padx=8)

    btn_resetar = ttk.Button(botoes, text="🧹 Resetar Campos", command=resetar_campos)
    btn_resetar.grid(row=0, column=2, padx=8)

    btn_limpar = ttk.Button(botoes, text="❌ Apagar Configurações Salvas", command=limpar_config_salva)
    btn_limpar.grid(row=0, column=3, padx=8)

    carregar_parametros()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Configurações do Sistema")
    root.geometry("750x700")
    root.resizable(False, False)
    tela_parametros_sistema(root)
    root.mainloop()
