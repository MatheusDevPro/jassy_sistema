import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def contatos_suporte():
    janela = tk.Toplevel()
    janela.title("📞 Contatos Suporte")
    janela.geometry("900x500")
    janela.resizable(False, False)

    contatos = []

    # === Frame esquerdo: Contatos Suporte ===
    frame_contatos = tk.Frame(janela)
    frame_contatos.pack(side="left", fill="both", expand=False, padx=10, pady=10)

    # Formulário Contatos
    frame_form = tk.LabelFrame(frame_contatos, text="Cadastro / Edição de Contato", padx=10, pady=10)
    frame_form.pack(fill="x")

    tk.Label(frame_form, text="Nome:").grid(row=0, column=0, sticky="e")
    entry_nome = tk.Entry(frame_form, width=30)
    entry_nome.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(frame_form, text="Telefone:").grid(row=1, column=0, sticky="e")
    entry_telefone = tk.Entry(frame_form, width=30)
    entry_telefone.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(frame_form, text="Email:").grid(row=2, column=0, sticky="e")
    entry_email = tk.Entry(frame_form, width=30)
    entry_email.grid(row=2, column=1, padx=5, pady=2)

    # Tabela Contatos
    frame_tabela = tk.Frame(frame_contatos)
    frame_tabela.pack(fill="both", expand=True, pady=10)

    colunas = ("nome", "telefone", "email")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
    for col in colunas:
        tabela.heading(col, text=col.capitalize())
    tabela.column("nome", width=180)
    tabela.column("telefone", width=120)
    tabela.column("email", width=180)

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=scrollbar.set)
    tabela.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    # Funções contatos
    def carregar_tabela():
        tabela.delete(*tabela.get_children())
        for idx, c in enumerate(contatos):
            tabela.insert("", "end", iid=idx, values=(c["nome"], c["telefone"], c["email"]))

    def limpar_form():
        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        tabela.selection_remove(tabela.selection())

    def inserir_contato():
        nome = entry_nome.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()
        if not nome or not telefone or not email:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        contatos.append({"nome": nome, "telefone": telefone, "email": email})
        carregar_tabela()
        limpar_form()
        messagebox.showinfo("Sucesso", "Contato inserido com sucesso.")

    def selecionar_contato(event):
        selected = tabela.selection()
        if selected:
            idx = int(selected[0])
            c = contatos[idx]
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, c["nome"])
            entry_telefone.delete(0, tk.END)
            entry_telefone.insert(0, c["telefone"])
            entry_email.delete(0, tk.END)
            entry_email.insert(0, c["email"])

    def atualizar_contato():
        selected = tabela.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um contato para atualizar.")
            return
        idx = int(selected[0])
        nome = entry_nome.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()
        if not nome or not telefone or not email:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        contatos[idx] = {"nome": nome, "telefone": telefone, "email": email}
        carregar_tabela()
        limpar_form()
        messagebox.showinfo("Sucesso", "Contato atualizado com sucesso.")

    def excluir_contato():
        selected = tabela.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um contato para excluir.")
            return
        idx = int(selected[0])
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este contato?"):
            contatos.pop(idx)
            carregar_tabela()
            limpar_form()
            messagebox.showinfo("Sucesso", "Contato excluído com sucesso.")

    tabela.bind("<<TreeviewSelect>>", selecionar_contato)

    # Botões contatos
    frame_botoes = tk.Frame(frame_contatos)
    frame_botoes.pack(fill="x", pady=5)

    btn_inserir = tk.Button(frame_botoes, text="➕ Inserir", bg="#28a745", fg="white", command=inserir_contato)
    btn_inserir.pack(side="left", padx=3)

    btn_atualizar = tk.Button(frame_botoes, text="✏️ Atualizar", bg="#007bff", fg="white", command=atualizar_contato)
    btn_atualizar.pack(side="left", padx=3)

    btn_excluir = tk.Button(frame_botoes, text="🗑️ Excluir", bg="#dc3545", fg="white", command=excluir_contato)
    btn_excluir.pack(side="left", padx=3)

    btn_limpar = tk.Button(frame_botoes, text="🧹 Limpar", command=limpar_form)
    btn_limpar.pack(side="right", padx=3)

    carregar_tabela()

    # === Frame direito: Chat Bot ===
    frame_chat = tk.Frame(janela, bg="#f4f6f8", bd=2, relief="groove")
    frame_chat.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame_chat, text="Chat de Suporte", bg="#007bff", fg="white", font=("Arial", 14, "bold"), pady=10).pack(fill="x")

    chat_log = scrolledtext.ScrolledText(frame_chat, state="disabled", wrap="word", font=("Arial", 11), bg="white")
    chat_log.pack(padx=10, pady=10, fill="both", expand=True)

    # Entrada e botão enviar
    frame_entry = tk.Frame(frame_chat)
    frame_entry.pack(fill="x", padx=10, pady=5)

    entry_msg = tk.Entry(frame_entry, font=("Arial", 12))
    entry_msg.pack(side="left", fill="x", expand=True, padx=(0,5), ipady=5)

    def inserir_msg_usuario():
        msg = entry_msg.get().strip()
        if not msg:
            return
        adicionar_msg(f"Você: {msg}\n")
        resposta_bot(msg)
        entry_msg.delete(0, tk.END)

    btn_enviar = tk.Button(frame_entry, text="Enviar", bg="#007bff", fg="white", command=inserir_msg_usuario)
    btn_enviar.pack(side="right")

    # Mensagens pré-definidas simples - resposta básica com palavras-chave
    respostas = {
        "horário": "Nosso horário de atendimento é de 8h às 18h, de segunda a sexta-feira.",
        "preço": "Os preços variam conforme o produto ou serviço. Posso te ajudar com algo específico?",
        "suporte": "Você pode abrir um chamado aqui mesmo ou ligar para o nosso suporte no telefone (11) 1234-5678.",
        "pagamento": "Aceitamos cartão, boleto e transferência bancária.",
        "entrega": "O prazo de entrega é de 3 a 7 dias úteis, dependendo da região.",
        "cancelar": "Para cancelar um pedido, entre em contato com o suporte o mais rápido possível.",
        "problema": "Lamento que esteja enfrentando problemas. Por favor, me informe detalhes para que eu possa ajudar.",
        "obrigado": "Disponha! Estamos aqui para ajudar no que for preciso.",
    }

    def resposta_bot(mensagem):
        msg_lower = mensagem.lower()
        resposta = "Desculpe, não entendi sua pergunta. Por favor, tente reformular."
        for chave, resp in respostas.items():
            if chave in msg_lower:
                resposta = resp
                break
        adicionar_msg(f"Bot: {resposta}\n")

    def adicionar_msg(texto):
        chat_log.config(state="normal")
        chat_log.insert(tk.END, texto)
        chat_log.see(tk.END)
        chat_log.config(state="disabled")

    # Mensagem inicial do bot
    adicionar_msg("Bot: Olá! Eu sou o assistente virtual de suporte. Como posso ajudar você hoje?\n")

# Exemplo de uso no menu:
# menu_suporte.add_command(label="📞 Contatos Suporte", command=contatos_suporte)
