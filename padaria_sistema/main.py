
import tkinter as tk
from gui.home import mostrar_home
from gui.clientes import tela_clientes
from gui.produtos import tela_produtos
from gui.vendas import tela_vendas
from gui.funcionarios import tela_funcionarios
from gui.fornecedores import tela_fornecedores
from gui.financeiro import tela_financeiro
from gui.usuarios import tela_usuarios
from gui.compras import tela_compras
from gui.entrada_estoque import tela_entrada_estoque
from gui.saida_estoque import tela_saida_estoque
from gui.devolucoes import tela_devolucoes
from gui.estoque_consulta import tela_consulta_estoque
from gui.estoque_ajuste import tela_ajuste_inventario
from gui.transferencia_depositos import tela_transferencia_depositos
from gui.contas_a_pagar import tela_contas_a_pagar
from gui.contas_a_receber import tela_contas_a_receber
from gui.conciliacao_bancaria import tela_conciliacao_bancaria
from gui.demonstrativo_de_lucros import tela_demonstrativo_lucros
from gui.boleto import tela_emissao_boletos
from gui.emissao_nf import tela_emissao_nf
from gui.boletos_emitidos import tela_boletos_emitidos
from gui.notas_emitidas import tela_notas_emitidas
from gui.relatorio_vendas import tela_relatorio_vendas
from gui.relatorio_produtos_mais_vendidos import tela_produtos_mais_vendidos
from gui.relatorio_clientes import tela_relatorio_clientes
from gui.relatorio_estoque import tela_relatorio_estoque
from gui.relatorios_personalizados import tela_relatorios_personalizados




# Placeholder para funções que ainda não foram implementadas
def placeholder():
    print("Função ainda não implementada")

janela = tk.Tk()
janela.title("🍞 Jassy - Gestão")
janela.geometry("1000x750")
janela.configure(bg="#f8f8ff")

menu_bar = tk.Menu(janela)

# 🏠 Início
menu_bar.add_command(label="🏠 Início", command=lambda: mostrar_home(janela))

# 📋 Cadastros
menu_cadastros = tk.Menu(menu_bar, tearoff=0)
menu_cadastros.add_command(label="👤 Clientes", command=lambda: tela_clientes(janela))
menu_cadastros.add_command(label="📦 Produtos", command=lambda: tela_produtos(janela))
menu_cadastros.add_command(label="👨‍🍳 Funcionários", command=lambda: tela_funcionarios(janela))
menu_cadastros.add_command(label="📨 Fornecedores", command=lambda: tela_fornecedores(janela))
menu_cadastros.add_command(label="🔐 Usuários / Permissões", command=lambda: tela_usuarios(janela))
menu_bar.add_cascade(label="📋 Cadastros", menu=menu_cadastros)

# 🔁 Movimentações
menu_movimentacoes = tk.Menu(menu_bar, tearoff=0)
menu_movimentacoes.add_command(label="💰 Vendas", command=lambda: tela_vendas(janela))
menu_movimentacoes.add_command(label="🛒 Compras", command=lambda: tela_compras(janela))
menu_movimentacoes.add_command(label="📦 Entrada de Estoque", command=lambda: tela_entrada_estoque(janela))
menu_movimentacoes.add_command(label="🚚 Saída de Estoque", command=lambda: tela_saida_estoque(janela))
menu_movimentacoes.add_command(label="↩️ Devoluções", command=lambda: tela_devolucoes(janela))
menu_bar.add_cascade(label="🔁 Movimentações", menu=menu_movimentacoes)

# 📦 Estoque
menu_estoque = tk.Menu(menu_bar, tearoff=0)
menu_estoque.add_command(label="📋 Consulta de Estoque", command=lambda: tela_consulta_estoque(janela))
menu_estoque.add_command(label="🛠️ Ajuste de Inventário", command=lambda: tela_ajuste_inventario(janela))
menu_estoque.add_command(label="🔄 Transferência entre Depósitos", command=lambda: tela_transferencia_depositos(janela))
menu_bar.add_cascade(label="📦 Estoque", menu=menu_estoque)

# 💰 Financeiro
menu_financeiro = tk.Menu(menu_bar, tearoff=0)
menu_financeiro.add_command(label="📊 Fluxo de Caixa", command=lambda: tela_financeiro(janela))
menu_financeiro.add_command(label="💸 Contas a Pagar", command=lambda: tela_contas_a_pagar(janela))
menu_financeiro.add_command(label="💸 Contas a Receber", command=lambda: tela_contas_a_receber(janela))
menu_financeiro.add_command(label="🏦 Conciliação Bancária", command=lambda: tela_conciliacao_bancaria(janela))
menu_financeiro.add_command(label="📉 Demonstrativo de Lucros", command=lambda: tela_demonstrativo_lucros(janela))
menu_bar.add_cascade(label="💰 Financeiro", menu=menu_financeiro)

#faturamento
menu_faturamento = tk.Menu(menu_bar, tearoff=0)
menu_faturamento.add_command(label="📄 Emissão de Boletos", command=lambda: tela_emissao_boletos(janela))
menu_faturamento.add_command(label="📄 Emissão de Notas fiscais", command=lambda: tela_emissao_nf(janela))
menu_faturamento.add_command(label="📄 Boletos emitidos", command=lambda: tela_boletos_emitidos(janela))
menu_faturamento.add_command(label="📄 Notas Fiscais emitidas", command=lambda: tela_notas_emitidas(janela))
menu_bar.add_cascade(label="💰 Faturamento", menu=menu_faturamento)

# 📈 Relatórios
menu_relatorios = tk.Menu(menu_bar, tearoff=0)
menu_relatorios.add_command(label="📈 Relatório de Vendas", command=lambda: tela_relatorio_vendas(janela))
menu_relatorios.add_command(label="🔥 Produtos Mais Vendidos", command=lambda: tela_produtos_mais_vendidos(janela))
menu_relatorios.add_command(label="📊 Relatório de Clientes", command=lambda: tela_relatorio_clientes(janela))
menu_relatorios.add_command(label="📦 Relatório de Estoque", command=lambda: tela_relatorio_estoque(janela))
menu_relatorios.add_command(label="🧾 Relatórios Personalizados", command=lambda: tela_relatorios_personalizados(janela))
menu_bar.add_cascade(label="📈 Relatórios", menu=menu_relatorios)

# ⚙️ Administração
menu_admin = tk.Menu(menu_bar, tearoff=0)
menu_admin.add_command(label="🛠️Parâmetros do Sistema", command=placeholder)
menu_admin.add_command(label="💾 Backup / Restauração", command=placeholder)
menu_admin.add_command(label="🔐 Permissões de Acesso", command=placeholder)
menu_admin.add_command(label="🎨 Personalização da Interface", command=placeholder)
menu_admin.add_command(label="🔌 Integrações", command=placeholder)
menu_bar.add_cascade(label="⚙️ Administração", menu=menu_admin)

# ❓ Ajuda
menu_ajuda = tk.Menu(menu_bar, tearoff=0)
menu_ajuda.add_command(label="📘 Manual do Usuário", command=placeholder)
menu_ajuda.add_command(label="📞 Suporte", command=placeholder)
menu_ajuda.add_command(label="ℹ️ Sobre o Sistema", command=placeholder)
menu_bar.add_cascade(label="❓ Ajuda", menu=menu_ajuda)

# 🚪 Sair
menu_bar.add_command(label="🚪 Sair", command=janela.quit)

# Aplica o menu
janela.config(menu=menu_bar)

# Tela inicial
mostrar_home(janela)

# Loop principal
janela.mainloop()
