import tkinter as tk
from tkinter import messagebox


# Importações do seu sistema (exemplo: algumas já definidas)
from gui.home import mostrar_home
from gui.cadastro.clientes import tela_clientes
from gui.cadastro.produtos import tela_produtos
from gui.movimentacao.vendas import tela_vendas
from gui.cadastro.funcionarios import tela_funcionarios
from gui.cadastro.fornecedores import tela_fornecedores
from gui.financeiro.financeiro import tela_financeiro
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
from gui.RH.gestao_pessoal import tela_gestao_pessoal
from gui.RH.folha_pagamento import tela_folha_pagamento
from gui.RH.controle_ponto import tela_controle_ponto
from gui.RH.relatorios_rh import tela_relatorios_rh
from gui.CRM.gestao_oportunidades import tela_gestao_oportunidades
from gui.CRM.contatos_historico import tela_contatos_historico
from gui.CRM.agenda_compromissos import tela_agenda_compromissos
from gui.CRM.relatorios_crm import tela_relatorios_crm
from gui.producao.chamados_producao import tela_chamados_producao
from gui.producao.ordem_producao import tela_ordem_producao
from gui.producao.controle_qualidade import tela_controle_qualidade
from gui.Marketing.campanhas_marketing  import tela_campanhas_marketing
from gui.Marketing.analise_mercado import tela_analise_mercado
from gui.Marketing.relatorios_marketing import tela_relatorios_marketing
from gui.suporte.helpdesk import tela_helpdesk
from gui.suporte.contatos_suporte import contatos_suporte
from gui.adm.cadastro_usuario import tela_cadastro_usuario

def placeholder():
    messagebox.showinfo("Em Desenvolvimento", "Esta funcionalidade ainda não foi implementada.")

def limpar_janela(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
          widget.destroy()

def mostrar_tela(janela, func_tela, titulo="Sistema de Gestão"):
    limpar_janela(janela)
    janela.title(titulo)
    func_tela(janela)

def main_app():
    janela = tk.Tk()
    janela.title("🐾 Jassy - Gestão")
    janela.geometry("1000x750")
    janela.configure(bg="#f8f8ff")

    menu_bar = tk.Menu(janela)

    # Menu Início
    menu_bar.add_command(label="🏠 Início", command=lambda: mostrar_tela(janela, mostrar_home, "Início - Jassy Gestão"))

    # Menu Cadastros
    menu_cadastros = tk.Menu(menu_bar, tearoff=0)
    menu_cadastros.add_command(label="👤 Clientes", command=lambda: mostrar_tela(janela, tela_clientes, "Clientes"))
    menu_cadastros.add_command(label="📦 Produtos", command=lambda: mostrar_tela(janela, tela_produtos, "Produtos"))
    menu_cadastros.add_command(label="👨‍🍳 Funcionários", command=lambda: mostrar_tela(janela, tela_funcionarios, "Funcionários"))
    menu_cadastros.add_command(label="📨 Fornecedores", command=lambda: mostrar_tela(janela, tela_fornecedores, "Fornecedores"))
    menu_bar.add_cascade(label="📋 Cadastros", menu=menu_cadastros)

    # Menu Movimentações
    menu_movimentacoes = tk.Menu(menu_bar, tearoff=0)
    menu_movimentacoes.add_command(label="💰 Vendas", command=lambda: mostrar_tela(janela, tela_vendas, "Vendas"))
    menu_movimentacoes.add_command(label="🛒 Compras", command=lambda: mostrar_tela(janela, tela_compras, "Compras"))
    menu_movimentacoes.add_command(label="📦 Entrada de Estoque", command=lambda: mostrar_tela(janela, tela_entrada_estoque, "Entrada de Estoque"))
    menu_movimentacoes.add_command(label="🚚 Saída de Estoque", command=lambda: mostrar_tela(janela, tela_saida_estoque, "Saída de Estoque"))
    menu_movimentacoes.add_command(label="↩️ Devoluções", command=lambda: mostrar_tela(janela, tela_devolucoes, "Devoluções"))
    menu_bar.add_cascade(label="🔁 Movimentações", menu=menu_movimentacoes)

    # Menu Estoque
    menu_estoque = tk.Menu(menu_bar, tearoff=0)
    menu_estoque.add_command(label="📋 Consulta de Estoque", command=lambda: mostrar_tela(janela, tela_consulta_estoque, "Consulta de Estoque"))
    menu_estoque.add_command(label="🛠️ Ajuste de Inventário", command=lambda: mostrar_tela(janela, tela_ajuste_inventario, "Ajuste de Inventário"))
    menu_estoque.add_command(label="🛠️ Baixa de Estoque", command=lambda: mostrar_tela(janela, tela_baixa_estoque, "Baixa de Estoque"))
    menu_estoque.add_command(label="🛠️ Requisição de Compras", command=lambda: mostrar_tela(janela, tela_requisicao_compras, "Requisição de Compras"))
    menu_estoque.add_command(label="🔄 Transferência entre Depósitos", command=lambda: mostrar_tela(janela, tela_transferencia_depositos, "Transferência entre Depósitos"))
    menu_bar.add_cascade(label="📦 Estoque", menu=menu_estoque)

    # Menu Financeiro
    menu_financeiro = tk.Menu(menu_bar, tearoff=0)
    menu_financeiro.add_command(label="📊 Fluxo de Caixa", command=lambda: mostrar_tela(janela, tela_financeiro, "Fluxo de Caixa"))
    menu_financeiro.add_command(label="💸 Contas a Pagar", command=lambda: mostrar_tela(janela, tela_contas_a_pagar, "Contas a Pagar"))
    menu_financeiro.add_command(label="💸 Contas a Receber", command=lambda: mostrar_tela(janela, tela_contas_a_receber, "Contas a Receber"))
    menu_financeiro.add_command(label="🏦 Conciliação Bancária", command=lambda: mostrar_tela(janela, tela_conciliacao_bancaria, "Conciliação Bancária"))
    menu_financeiro.add_command(label="📉 Demonstrativo de Lucros", command=lambda: mostrar_tela(janela, tela_demonstrativo_lucros, "Demonstrativo de Lucros"))
    menu_bar.add_cascade(label="💰 Financeiro", menu=menu_financeiro)

    # Menu Faturamento
    menu_faturamento = tk.Menu(menu_bar, tearoff=0)
    menu_faturamento.add_command(label="📄 Emissão de Boletos", command=lambda: mostrar_tela(janela, tela_emissao_boletos, "Emissão de Boletos"))
    menu_faturamento.add_command(label="📄 Emissão de Notas Fiscais", command=lambda: mostrar_tela(janela, tela_emissao_nf, "Emissão de Notas Fiscais"))
    menu_faturamento.add_command(label="📄 Boletos Emitidos", command=lambda: mostrar_tela(janela, tela_boletos_emitidos, "Boletos Emitidos"))
    menu_faturamento.add_command(label="📄 Notas Fiscais Emitidas", command=lambda: mostrar_tela(janela, tela_notas_emitidas, "Notas Fiscais Emitidas"))
    menu_bar.add_cascade(label="💰 Faturamento", menu=menu_faturamento)

    # Menu Relatórios
    menu_relatorios = tk.Menu(menu_bar, tearoff=0)
    menu_relatorios.add_command(label="📈 Relatório de Vendas", command=lambda: mostrar_tela(janela, tela_relatorio_vendas, "Relatório de Vendas"))
    menu_relatorios.add_command(label="🔥 Produtos Mais Vendidos", command=lambda: mostrar_tela(janela, tela_produtos_mais_vendidos, "Produtos Mais Vendidos"))
    menu_relatorios.add_command(label="📊 Relatório de Clientes", command=lambda: mostrar_tela(janela, tela_relatorio_clientes, "Relatório de Clientes"))
    menu_relatorios.add_command(label="📦 Relatório de Estoque", command=lambda: mostrar_tela(janela, tela_relatorio_estoque, "Relatório de Estoque"))
    menu_relatorios.add_command(label="🧾 Relatórios Personalizados", command=lambda: mostrar_tela(janela, tela_relatorios_personalizados, "Relatórios Personalizados"))
    menu_bar.add_cascade(label="📈 Relatórios", menu=menu_relatorios)

    # Novo Menu RH (Recursos Humanos)
    menu_rh = tk.Menu(menu_bar, tearoff=0)
    menu_rh.add_command(label="👥 Gestão de Pessoal", command=lambda: tela_gestao_pessoal(janela))
    menu_rh.add_command(label="🧾 Folha de Pagamento", command=lambda: tela_folha_pagamento(janela))
    menu_rh.add_command(label="📅 Controle de Ponto", command=lambda:tela_controle_ponto(janela))
    menu_rh.add_command(label="📊 Relatórios RH", command=lambda: tela_relatorios_rh(janela))
    menu_bar.add_cascade(label="👔 RH", menu=menu_rh)

    # Novo Menu CRM / Projetos
    menu_crm = tk.Menu(menu_bar, tearoff=0)
    menu_crm.add_command(label="📇 Gestão de Oportunidades", command=lambda:tela_gestao_oportunidades(janela))  # tela_gestao_oportunidades
    menu_crm.add_command(label="📞 Contatos e Histórico", command=lambda: tela_contatos_historico(janela))
    menu_crm.add_command(label="📅 Agenda e Compromissos", command=lambda: tela_agenda_compromissos(janela))
    menu_crm.add_command(label="📊 Relatórios CRM", command=lambda: tela_relatorios_crm(janela))
    menu_bar.add_cascade(label="📊 CRM / Projetos", menu=menu_crm)

    # Novo Menu Produção (caso tenha)
    menu_producao = tk.Menu(menu_bar, tearoff=0)
    menu_producao.add_command(label="🛠️ Chamados Produção", command=lambda: tela_chamados_producao(janela))  # tela_chamados_producao
    menu_producao.add_command(label="⚙️ Ordens de Produção", command=lambda: tela_ordem_producao(janela))  # tela_ordem_producao
    menu_producao.add_command(label="📋 Controle de Qualidade", command=lambda: tela_controle_qualidade(janela))
    menu_bar.add_cascade(label="🏭 Produção", menu=menu_producao)

    # Novo Menu Marketing
    menu_marketing = tk.Menu(menu_bar, tearoff=0)
    menu_marketing.add_command(label="📢 Campanhas", command=lambda: tela_campanhas_marketing(janela))  # tela_campanhas_marketing
    menu_marketing.add_command(label="📊 Análise de Mercado", command=lambda: tela_analise_mercado(janela))
    menu_marketing.add_command(label="📈 Relatórios Marketing", command=lambda: tela_relatorios_marketing(janela))
    menu_bar.add_cascade(label="📣 Marketing", menu=menu_marketing)

    # Novo Menu Suporte / Helpdesk
    menu_suporte = tk.Menu(menu_bar, tearoff=0)
    menu_suporte.add_command(label="🎫 Helpdesk", command=lambda: tela_helpdesk(janela))  # tela_helpdesk
    menu_suporte.add_command(label="📞 Contatos Suporte", command=lambda: contatos_suporte(janela))
    menu_bar.add_cascade(label="🛠️ Suporte", menu=menu_suporte)

    # Menu Administração / Configurações
    menu_administracao = tk.Menu(menu_bar, tearoff=0)
    menu_administracao.add_command(label="⚙️ Parâmetros do Sistema", command=lambda: mostrar_tela(janela, tela_parametros_sistema, "Parâmetros do Sistema"))
    menu_administracao.add_command(label="🔒 Permissões de Acesso", command=lambda: mostrar_tela(janela, tela_permissoes_acesso, "Permissões de Acesso"))
    menu_administracao.add_command(label="🔒 cadastro de usuario", command=lambda: mostrar_tela(janela, tela_cadastro_usuario, "cadastro de usuario"))
    menu_administracao.add_command(label="🎨 Personalização da Interface", command=lambda: mostrar_tela(janela, tela_personalizacao_interface, "Personalização da Interface"))
    menu_administracao.add_command(label="🔄 Backup e Restauração", command=lambda: mostrar_tela(janela, tela_backup, "Backup e Restauração"))
    menu_administracao.add_command(label="🔗 Integrações", command=lambda: mostrar_tela(janela, tela_integracoes, "Integrações"))
    menu_bar.add_cascade(label="⚙️ Administração", menu=menu_administracao)

    # Sair
    menu_bar.add_command(label="🚪 Sair", command=janela.destroy)

    janela.config(menu=menu_bar)

    # Começa na tela inicial
    mostrar_tela(janela, mostrar_home, "Início - Jassy Gestão")

    janela.mainloop()


# Tela de login (mantive seu código original, com leve melhoria)
def tela_login():
    login_win = tk.Tk()
    login_win.title("🐾 Login - Jassy Gestão")
    login_win.geometry("300x230")
    login_win.configure(bg="#f8f8ff")

    # Centralizar janela
    screen_width = login_win.winfo_screenwidth()
    screen_height = login_win.winfo_screenheight()
    x = (screen_width // 2) - (300 // 2)
    y = (screen_height // 2) - (230 // 2)
    login_win.geometry(f"+{x}+{y}")

    label_titulo = tk.Label(login_win, text="🐾 Login Jassy", font=("Arial", 14, "bold"), fg="#1E90FF", bg="#f8f8ff")
    label_titulo.pack(pady=10)

    label_usuario = tk.Label(login_win, text="Usuário:", font=("Arial", 10), bg="#f8f8ff")
    label_usuario.pack()
    entry_usuario = tk.Entry(login_win, font=("Arial", 10))
    entry_usuario.pack()

    label_senha = tk.Label(login_win, text="Senha:", font=("Arial", 10), bg="#f8f8ff")
    label_senha.pack()
    entry_senha = tk.Entry(login_win, font=("Arial", 10), show="*")
    entry_senha.pack()

    label_erro = tk.Label(login_win, text="", fg="red", bg="#f8f8ff")
    label_erro.pack(pady=5)

    def validar_login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        # Simples validação fixa
        if usuario == "matheus" and senha == "123456":
            login_win.destroy()
            main_app()
        else:
            label_erro.config(text="Usuário ou senha inválidos")
            # messagebox.showerror("Erro", "Usuário ou senha inválidos")

    botao_login = tk.Button(login_win, text="Login", font=("Arial", 10, "bold"), bg="#1E90FF", fg="white", command=validar_login)
    botao_login.pack(pady=10)

    login_win.mainloop()

# Iniciar o programa
if __name__ == "__main__":
    tela_login()
