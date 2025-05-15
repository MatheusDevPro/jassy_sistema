import tkinter as tk
from tkinter import messagebox

# Importações do seu sistema
from gui.home import mostrar_home
from gui.cadastro.clientes import tela_clientes
from gui.cadastro.produtos import tela_produtos
from gui.movimentacao.vendas import tela_vendas
from gui.cadastro.funcionarios import tela_funcionarios
from gui.cadastro.fornecedores import tela_fornecedores
from gui.financeiro.financeiro import tela_financeiro
from gui.cadastro.usuarios import tela_usuarios
from gui.movimentacao.compras import tela_compras
from gui.movimentacao.entrada_estoque import tela_entrada_estoque
from gui.movimentacao.saida_estoque import tela_saida_estoque
from gui.movimentacao.devolucoes import tela_devolucoes
from gui.estoque.estoque_consulta import tela_consulta_estoque
from gui.estoque.estoque_ajuste import tela_ajuste_inventario
from gui.estoque.transferencia_depositos import tela_transferencia_depositos
from gui.financeiro.contas_a_pagar import tela_contas_a_pagar
from gui.financeiro.contas_a_receber import tela_contas_a_receber
from gui.financeiro.conciliacao_bancaria import tela_conciliacao_bancaria
from gui.financeiro.demonstrativo_de_lucros import tela_demonstrativo_lucros
from gui.faturamento.boleto import tela_emissao_boletos
from gui.faturamento.emissao_nf import tela_emissao_nf
from gui.faturamento.boletos_emitidos import tela_boletos_emitidos
from gui.faturamento.notas_emitidas import tela_notas_emitidas
from gui.relatorio.relatorio_vendas import tela_relatorio_vendas
from gui.relatorio.relatorio_produtos_mais_vendidos import tela_produtos_mais_vendidos
from gui.relatorio.relatorio_clientes import tela_relatorio_clientes
from gui.relatorio.relatorio_estoque import tela_relatorio_estoque
from gui.relatorio.relatorios_personalizados import tela_relatorios_personalizados
from gui.adm.parametros_sistema import tela_parametros_sistema
from gui.adm.restauração import tela_backup
from gui.adm.permissoes_acesso import tela_permissoes_acesso
from gui.adm.personalizacao_interface import tela_personalizacao_interface
from gui.adm.integracoes import tela_integracoes
from gui.estoque.requisicao_compras import tela_requisicao_compras
from gui.estoque.baixa_estoque import tela_baixa_estoque


def placeholder():
    print("Função ainda não implementada")

def main_app():
    janela = tk.Tk()
    janela.title("🐾 Jassy - Gestão")
    janela.geometry("1000x750")
    janela.configure(bg="#f8f8ff")

    menu_bar = tk.Menu(janela)

    menu_bar.add_command(label="🏠 Início", command=lambda: mostrar_home(janela))

    menu_cadastros = tk.Menu(menu_bar, tearoff=0)
    menu_cadastros.add_command(label="👤 Clientes", command=lambda: tela_clientes(janela))
    menu_cadastros.add_command(label="📦 Produtos", command=lambda: tela_produtos(janela))
    menu_cadastros.add_command(label="👨‍🍳 Funcionários", command=lambda: tela_funcionarios(janela))
    menu_cadastros.add_command(label="📨 Fornecedores", command=lambda: tela_fornecedores(janela))
    menu_cadastros.add_command(label="🔐 Usuários / Permissões", command=lambda: tela_usuarios(janela))
    menu_bar.add_cascade(label="📋 Cadastros", menu=menu_cadastros)

    menu_movimentacoes = tk.Menu(menu_bar, tearoff=0)
    menu_movimentacoes.add_command(label="💰 Vendas", command=lambda: tela_vendas(janela))
    menu_movimentacoes.add_command(label="🛒 Compras", command=lambda: tela_compras(janela))
    menu_movimentacoes.add_command(label="📦 Entrada de Estoque", command=lambda: tela_entrada_estoque(janela))
    menu_movimentacoes.add_command(label="🚚 Saída de Estoque", command=lambda: tela_saida_estoque(janela))
    menu_movimentacoes.add_command(label="↩️ Devoluções", command=lambda: tela_devolucoes(janela))
    menu_bar.add_cascade(label="🔁 Movimentações", menu=menu_movimentacoes)

    menu_estoque = tk.Menu(menu_bar, tearoff=0)
    menu_estoque.add_command(label="📋 Consulta de Estoque", command=lambda: tela_consulta_estoque(janela))
    menu_estoque.add_command(label="🛠️ Ajuste de Inventário", command=lambda: tela_ajuste_inventario(janela))
    menu_estoque.add_command(label="🛠️ Baixa de estoque", command=lambda: tela_baixa_estoque(janela))
    menu_estoque.add_command(label="🛠️ Requisição compras", command=lambda: tela_requisicao_compras(janela))
    menu_estoque.add_command(label="🔄 Transferência entre Depósitos", command=lambda: tela_transferencia_depositos(janela))
    menu_bar.add_cascade(label="📦 Estoque", menu=menu_estoque)

    menu_financeiro = tk.Menu(menu_bar, tearoff=0)
    menu_financeiro.add_command(label="📊 Fluxo de Caixa", command=lambda: tela_financeiro(janela))
    menu_financeiro.add_command(label="💸 Contas a Pagar", command=lambda: tela_contas_a_pagar(janela))
    menu_financeiro.add_command(label="💸 Contas a Receber", command=lambda: tela_contas_a_receber(janela))
    menu_financeiro.add_command(label="🏦 Conciliação Bancária", command=lambda: tela_conciliacao_bancaria(janela))
    menu_financeiro.add_command(label="📉 Demonstrativo de Lucros", command=lambda: tela_demonstrativo_lucros(janela))
    menu_bar.add_cascade(label="💰 Financeiro", menu=menu_financeiro)

    menu_faturamento = tk.Menu(menu_bar, tearoff=0)
    menu_faturamento.add_command(label="📄 Emissão de Boletos", command=lambda: tela_emissao_boletos(janela))
    menu_faturamento.add_command(label="📄 Emissão de Notas fiscais", command=lambda: tela_emissao_nf(janela))
    menu_faturamento.add_command(label="📄 Boletos emitidos", command=lambda: tela_boletos_emitidos(janela))
    menu_faturamento.add_command(label="📄 Notas Fiscais emitidas", command=lambda: tela_notas_emitidas(janela))
    menu_bar.add_cascade(label="💰 Faturamento", menu=menu_faturamento)

    menu_relatorios = tk.Menu(menu_bar, tearoff=0)
    menu_relatorios.add_command(label="📈 Relatório de Vendas", command=lambda: tela_relatorio_vendas(janela))
    menu_relatorios.add_command(label="🔥 Produtos Mais Vendidos", command=lambda: tela_produtos_mais_vendidos(janela))
    menu_relatorios.add_command(label="📊 Relatório de Clientes", command=lambda: tela_relatorio_clientes(janela))
    menu_relatorios.add_command(label="📦 Relatório de Estoque", command=lambda: tela_relatorio_estoque(janela))
    menu_relatorios.add_command(label="🧾 Relatórios Personalizados", command=lambda: tela_relatorios_personalizados(janela))
    menu_bar.add_cascade(label="📈 Relatórios", menu=menu_relatorios)

    menu_admin = tk.Menu(menu_bar, tearoff=0)
    menu_admin.add_command(label="🛠️Parâmetros do Sistema", command=lambda: tela_parametros_sistema(janela))
    menu_admin.add_command(label="💾 Backup / Restauração", command=lambda: tela_backup(janela))
    menu_admin.add_command(label="🔐 Permissões de Acesso", command=lambda: tela_permissoes_acesso(janela))
    menu_admin.add_command(label="🎨 Personalização da Interface", command=lambda: tela_personalizacao_interface(janela))
    menu_admin.add_command(label="🔌 Integrações", command=lambda: tela_integracoes(janela))
    menu_bar.add_cascade(label="⚙️ Administração", menu=menu_admin)

    menu_ajuda = tk.Menu(menu_bar, tearoff=0)
    menu_ajuda.add_command(label="📘 Manual do Usuário", command=placeholder)
    menu_ajuda.add_command(label="📞 Suporte", command=placeholder)
    menu_ajuda.add_command(label="ℹ️ Sobre o Sistema", command=placeholder)
    menu_bar.add_cascade(label="❓ Ajuda", menu=menu_ajuda)

    menu_bar.add_command(label="🚪 Sair", command=janela.quit)
    janela.config(menu=menu_bar)
    mostrar_home(janela)
    janela.mainloop()


def tela_login():
    login_win = tk.Tk()
    login_win.title("🔐 Login - Jassy Gestão")
    login_win.geometry("500x500")
    login_win.configure(bg="#dde7f0")
    login_win.resizable(False, False)

    # Fundo com cor suave
    background = tk.Frame(login_win, bg="#dde7f0")
    background.place(relwidth=1, relheight=1)

    # Card central
    card = tk.Frame(background, bg="white", bd=0, relief="ridge")
    card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=400)

    # Título
    tk.Label(card, text="👋 Bem-vindo ao Jassy", font=("Segoe UI", 16, "bold"),
             bg="white", fg="#2c3e50").pack(pady=(20, 5))

    tk.Label(card, text="Acesse sua conta para continuar", font=("Segoe UI", 10),
             bg="white", fg="#7f8c8d").pack()

    # Campo usuário
    frame_usuario = tk.Frame(card, bg="white")
    frame_usuario.pack(padx=30, pady=(30, 10), fill="x")

    tk.Label(frame_usuario, text="👤 Usuário", bg="white", anchor="w",
             font=("Segoe UI", 10, "bold")).pack(fill="x")
    entry_usuario = tk.Entry(frame_usuario, font=("Segoe UI", 10), bd=1, relief="solid")
    entry_usuario.pack(fill="x", ipady=6)

    # Campo senha
    frame_senha = tk.Frame(card, bg="white")
    frame_senha.pack(padx=30, pady=(10, 5), fill="x")

    tk.Label(frame_senha, text="🔒 Senha", bg="white", anchor="w",
             font=("Segoe UI", 10, "bold")).pack(fill="x")

    senha_frame = tk.Frame(frame_senha, bg="white")
    senha_frame.pack(fill="x")

    entry_senha = tk.Entry(senha_frame, font=("Segoe UI", 10), show="*", bd=1, relief="solid")
    entry_senha.pack(side="left", fill="x", expand=True, ipady=6)

    def toggle_senha():
        if entry_senha.cget('show') == "":
            entry_senha.config(show="*")
            btn_ver_senha.config(text="👁️")
        else:
            entry_senha.config(show="")
            btn_ver_senha.config(text="🙈")

    btn_ver_senha = tk.Button(senha_frame, text="👁️", bg="white", relief="flat",
                              command=toggle_senha, font=("Segoe UI", 9))
    btn_ver_senha.pack(side="left", padx=5)

    # Mensagem de erro
    lbl_erro = tk.Label(card, text="", font=("Segoe UI", 9), fg="#e74c3c", bg="white")
    lbl_erro.pack(pady=(5, 0))

    # Botão de login com estilo
    def on_enter(e):
        btn_login.config(bg="#2c3e50")

    def on_leave(e):
        btn_login.config(bg="#2980b9")

    def validar_login():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()
        if usuario == "matheus" and senha == "123456":
            login_win.destroy()
            main_app()
        else:
            lbl_erro.config(text="❌ Usuário ou senha inválidos")

    btn_login = tk.Button(card, text="Entrar", font=("Segoe UI", 11, "bold"), bg="#2980b9",
                          fg="white", relief="flat", command=validar_login)
    btn_login.pack(pady=(20, 5), ipadx=20, ipady=6)
    btn_login.bind("<Enter>", on_enter)
    btn_login.bind("<Leave>", on_leave)

    # Rodapé
    tk.Label(card, text="🔸 Jassy Gestão © 2025", font=("Segoe UI", 9),
             fg="#bdc3c7", bg="white").pack(side="bottom", pady=10)

    login_win.mainloop()



# Início do sistema
if __name__ == "__main__":
    tela_login()
