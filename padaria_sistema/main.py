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
    login_win.geometry("420x560")
    login_win.configure(bg="#1e1e2f")
    login_win.resizable(False, False)

    canvas = tk.Canvas(login_win, width=420, height=560, bg="#1e1e2f", bd=0, highlightthickness=0)
    canvas.pack()

    # Fundo com gradiente simulando
    canvas.create_rectangle(0, 0, 420, 560, fill="#5c6bc0", outline="")

    # Card de login com sombra
    card = tk.Frame(login_win, bg="white", padx=20, pady=20, highlightbackground="#aaa", highlightthickness=1)
    card.place(relx=0.5, rely=0.5, anchor="center")

    # Logo / título
    tk.Label(card, text="🔐 Jassy Gestão", font=("Arial", 20, "bold"), fg="#3f51b5", bg="white").pack(pady=(5, 15))

    # Entrada de usuário
    tk.Label(card, text="👤 Usuário", font=("Arial", 11), fg="#444", bg="white").pack(anchor="w")
    entry_usuario = tk.Entry(card, font=("Arial", 12), bd=2, relief="solid", fg="#555", bg="#f0f0f5", insertbackground='black')
    entry_usuario.pack(fill="x", pady=(0, 10), ipady=6)

    entry_usuario.bind("<FocusIn>", lambda event: entry_usuario.config(bg="#e8eaf6"))
    entry_usuario.bind("<FocusOut>", lambda event: entry_usuario.config(bg="#f0f0f5"))

    # Entrada de senha
    tk.Label(card, text="🔒 Senha", font=("Arial", 11), fg="#444", bg="white").pack(anchor="w")
    entry_senha = tk.Entry(card, font=("Arial", 12), bd=2, relief="solid", show="*", fg="#555", bg="#f0f0f5", insertbackground='black')
    entry_senha.pack(fill="x", pady=(0, 10), ipady=6)

    entry_senha.bind("<FocusIn>", lambda event: entry_senha.config(bg="#e8eaf6"))
    entry_senha.bind("<FocusOut>", lambda event: entry_senha.config(bg="#f0f0f5"))

    # Mostrar/ocultar senha
    def toggle_senha():
        entry_senha.config(show="" if entry_senha.cget('show') == "*" else "*")

    tk.Checkbutton(card, text="Mostrar senha", command=toggle_senha, font=("Arial", 10), fg="#3f51b5", selectcolor="#f0f0f5", bg="white").pack(pady=5, anchor="w")

    # Mensagem de erro
    lbl_erro = tk.Label(card, text="", fg="red", font=("Arial", 10), bg="white")
    lbl_erro.pack(pady=(5, 0))

    # Validação de login
    def validar_login():
        usuario = entry_usuario.get().strip()
        senha = entry_senha.get().strip()

        if usuario == "" or senha == "":
            lbl_erro.config(text="❌ Usuário e senha não podem estar vazios")
            return

        if usuario == "matheus" and senha == "123456":
            login_win.destroy()
            main_app()  # Substitua por sua função principal
        else:
            lbl_erro.config(text="❌ Usuário ou senha inválidos")

    # Botão de login
    def on_enter(event):
        login_button.config(bg="#3f51b5", fg="white")

    def on_leave(event):
        login_button.config(bg="white", fg="#3f51b5")

    login_button = tk.Button(
        card,
        text="Entrar no sistema",
        font=("Arial", 13, "bold"),
        width=25,
        bg="white",
        fg="#3f51b5",
        command=validar_login,
        relief="solid",
        bd=2,
        cursor="hand2"
    )
    login_button.pack(pady=20)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    login_win.mainloop()

# Exemplo de função principal

# Rodar
tela_login()