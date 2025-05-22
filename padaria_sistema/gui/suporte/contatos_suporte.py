import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import csv

def contatos_suporte(janela):
    for widget in janela.winfo_children():
        if widget.winfo_class() != 'Menu':
            widget.destroy()

    janela.configure(bg="#e6f2ff")
    frame_principal = tk.Frame(janela, bg="#e6f2ff")
    frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

    tk.Label(frame_principal, text="📞 Contatos de Suporte", font=("Helvetica", 20, "bold"),
             bg="#e6f2ff", fg="#006699").pack(pady=10)

    frame_conteudo = tk.Frame(frame_principal, bg="#e6f2ff")
    frame_conteudo.pack(fill="both", expand=True)

    frame_esquerdo = tk.Frame(frame_conteudo, bg="#e6f2ff")
    frame_esquerdo.pack(side="left", fill="both", expand=True)

    # === Formulário Contatos ===
    frame_form = tk.LabelFrame(frame_esquerdo, text="Cadastro / Edição de Contato", bg="#e6f2ff", fg="#004d80",
                               font=("Helvetica", 12, "bold"))
    frame_form.pack(fill="x", padx=10, pady=5)

    labels = ["Nome:", "Telefone:", "Email:", "Cargo:", "Setor:"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(frame_form, text=label, bg="#e6f2ff", font=("Helvetica", 11)).grid(row=i, column=0, sticky="e", padx=5, pady=4)
        entry = tk.Entry(frame_form, width=35)
        entry.grid(row=i, column=1, padx=5, pady=4)
        entries[label[:-1].lower()] = entry

    # Campo Observações com ScrolledText
    tk.Label(frame_form, text="Observações:", bg="#e6f2ff", font=("Helvetica", 11)).grid(row=5, column=0, sticky="ne", padx=5, pady=4)
    txt_observacoes = scrolledtext.ScrolledText(frame_form, width=26, height=4, font=("Helvetica", 10))
    txt_observacoes.grid(row=5, column=1, padx=5, pady=4, sticky="w")

    # === Botões ===
    frame_botoes = tk.Frame(frame_form, bg="#e6f2ff")
    frame_botoes.grid(row=6, column=0, columnspan=2, pady=10)

    btn_inserir = tk.Button(frame_botoes, text="➕ Inserir", bg="#28a745", fg="white",
                            font=("Helvetica", 11))
    btn_inserir.pack(side="left", padx=5)

    btn_atualizar = tk.Button(frame_botoes, text="✏️ Atualizar", bg="#007bff", fg="white",
                              font=("Helvetica", 11))
    btn_atualizar.pack(side="left", padx=5)

    btn_excluir = tk.Button(frame_botoes, text="🗑️ Excluir", bg="#dc3545", fg="white",
                            font=("Helvetica", 11))
    btn_excluir.pack(side="left", padx=5)

    btn_limpar = tk.Button(frame_botoes, text="🧹 Limpar", font=("Helvetica", 11))
    btn_limpar.pack(side="left", padx=5)

    btn_exportar = tk.Button(frame_botoes, text="⬇️ Exportar CSV", bg="#17a2b8", fg="white", font=("Helvetica", 11))
    btn_exportar.pack(side="left", padx=5)

    btn_importar = tk.Button(frame_botoes, text="⬆️ Importar CSV", bg="#ffc107", fg="black", font=("Helvetica", 11))
    btn_importar.pack(side="left", padx=5)

    contatos = []

    # === Campo Pesquisa ===
    frame_pesquisa = tk.Frame(frame_esquerdo, bg="#e6f2ff")
    frame_pesquisa.pack(fill="x", padx=10, pady=(10,0))

    tk.Label(frame_pesquisa, text="🔍 Pesquisar:", bg="#e6f2ff", font=("Helvetica", 11)).pack(side="left")
    entry_pesquisa = tk.Entry(frame_pesquisa, width=30)
    entry_pesquisa.pack(side="left", padx=5)

    def filtrar_tabela(event=None):
        termo = entry_pesquisa.get().lower()
        tabela.delete(*tabela.get_children())
        for idx, c in enumerate(contatos):
            valores = " ".join([str(v).lower() for v in c.values()])
            if termo in valores:
                tabela.insert("", "end", iid=idx, values=(c["nome"], c["telefone"], c["email"], c["cargo"], c["setor"]))

    btn_pesquisar = tk.Button(frame_pesquisa, text="Pesquisar", command=filtrar_tabela)
    btn_pesquisar.pack(side="left", padx=5)

    btn_limpar_pesquisa = tk.Button(frame_pesquisa, text="Limpar Pesquisa", command=lambda: (entry_pesquisa.delete(0, tk.END), carregar_tabela()))
    btn_limpar_pesquisa.pack(side="left", padx=5)

    # === Tabela Contatos ===
    frame_tabela = tk.LabelFrame(frame_esquerdo, text="📋 Contatos Cadastrados", bg="#e6f2ff",
                                 fg="#004d80", font=("Helvetica", 12, "bold"))
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=5)

    colunas = ("nome", "telefone", "email", "cargo", "setor")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=12)
    for col in colunas:
        tabela.heading(col, text=col.capitalize())
        tabela.column(col, anchor="center", width=130)

    scroll_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll_y.set)

    tabela.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    scroll_y.grid(row=0, column=1, sticky="ns", pady=5)

    frame_tabela.grid_rowconfigure(0, weight=1)
    frame_tabela.grid_columnconfigure(0, weight=1)

    def carregar_tabela():
        tabela.delete(*tabela.get_children())
        for idx, c in enumerate(contatos):
            tabela.insert("", "end", iid=idx, values=(c["nome"], c["telefone"], c["email"], c["cargo"], c["setor"]))

    def limpar_form():
        for key in entries:
            entries[key].delete(0, tk.END)
        txt_observacoes.delete(1.0, tk.END)
        tabela.selection_remove(tabela.selection())
        entry_pesquisa.delete(0, tk.END)

    def validar_campos():
        if not entries["nome"].get().strip():
            messagebox.showwarning("Atenção", "O campo Nome é obrigatório.")
            return False
        if not entries["telefone"].get().strip():
            messagebox.showwarning("Atenção", "O campo Telefone é obrigatório.")
            return False
        if not entries["email"].get().strip():
            messagebox.showwarning("Atenção", "O campo Email é obrigatório.")
            return False
        return True

    def inserir_contato():
        if not validar_campos():
            return
        novo = {key: entries[key].get().strip() for key in entries}
        novo["observações"] = txt_observacoes.get(1.0, tk.END).strip()
        contatos.append(novo)
        carregar_tabela()
        limpar_form()
        messagebox.showinfo("Sucesso", "Contato inserido com sucesso.")

    def selecionar_contato(event):
        selected = tabela.selection()
        if selected:
            idx = int(selected[0])
            c = contatos[idx]
            for key in entries:
                entries[key].delete(0, tk.END)
                entries[key].insert(0, c.get(key, ""))
            txt_observacoes.delete(1.0, tk.END)
            txt_observacoes.insert(tk.END, c.get("observações", ""))

    def atualizar_contato():
        selected = tabela.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um contato para atualizar.")
            return
        if not validar_campos():
            return
        idx = int(selected[0])
        atualizado = {key: entries[key].get().strip() for key in entries}
        atualizado["observações"] = txt_observacoes.get(1.0, tk.END).strip()
        contatos[idx] = atualizado
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

    def exportar_csv():
        if not contatos:
            messagebox.showwarning("Aviso", "Não há contatos para exportar.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=["nome", "telefone", "email", "cargo", "setor", "observações"])
                    writer.writeheader()
                    for contato in contatos:
                        writer.writerow(contato)
                messagebox.showinfo("Sucesso", f"Contatos exportados para {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao exportar CSV:\n{e}")

    def importar_csv():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    contatos.clear()
                    for row in reader:
                        contatos.append(row)
                carregar_tabela()
                messagebox.showinfo("Sucesso", f"Contatos importados de {file_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao importar CSV:\n{e}")

    # ligar comandos aos botões
    btn_inserir.config(command=inserir_contato)
    btn_atualizar.config(command=atualizar_contato)
    btn_excluir.config(command=excluir_contato)
    btn_limpar.config(command=limpar_form)
    btn_exportar.config(command=exportar_csv)
    btn_importar.config(command=importar_csv)

    tabela.bind("<<TreeviewSelect>>", selecionar_contato)
    entry_pesquisa.bind("<Return>", lambda event: filtrar_tabela())
    carregar_tabela()

    # === Chatbot ===
    frame_chat = tk.Frame(frame_conteudo, bg="#f4f6f8", bd=2, relief="groove")
    frame_chat.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    tk.Label(frame_chat, text="💬 Chatbot de Suporte", bg="#007bff", fg="white",
             font=("Helvetica", 14, "bold")).pack(fill="x")

    chat_log = scrolledtext.ScrolledText(frame_chat, state="disabled", wrap="word",
                                         font=("Arial", 11), bg="white")
    chat_log.pack(padx=10, pady=10, fill="both", expand=True)

    frame_entry = tk.Frame(frame_chat)
    frame_entry.pack(fill="x", padx=10, pady=5)

    entry_msg = tk.Entry(frame_entry, font=("Arial", 12))
    entry_msg.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=5)

    respostas = {
    # Atendimento geral
    "horário": "Oi! Nosso atendimento é de segunda a sexta, das 8h às 18h. Estamos aqui para ajudar no que precisar!",
    "telefone": "Pode ligar pra gente no (11) 1234-5678 a qualquer momento dentro do nosso horário, tá bom?",
    "email": "Quer falar por e-mail? Envie para suporte@empresa.com.br, e a gente responde rapidinho.",
    "pagamento": "Aceitamos várias formas de pagamento, como cartão, Pix, boleto e transferência para facilitar sua vida.",
    "entrega": "A entrega costuma levar de 3 a 7 dias úteis, mas qualquer coisa, é só avisar que te atualizo!",
    "cancelamento": "Se precisar cancelar, fale com nosso time de suporte para que possamos te ajudar com rapidez e segurança.",
    "troca": "Trocas são feitas em até 7 dias após o recebimento do produto, com todo cuidado que você merece.",
    "reembolso": "O processo de reembolso leva até 5 dias úteis após a aprovação. Estamos aqui para facilitar pra você.",
    
    # TI e tecnologia
    "backup": "Fazer backup regularmente é o segredo para evitar dor de cabeça. Posso te ajudar a configurar isso se quiser.",
    "segurança": "A segurança dos seus dados é fundamental. Usamos ferramentas avançadas para proteger tudo.",
    "software": "Se estiver enfrentando problemas com o software, conta comigo para te orientar na atualização ou instalação.",
    "hardware": "Se seu computador ou aparelho estiver com defeito, nosso time técnico está preparado para diagnosticar e ajudar.",
    "atualização": "Manter tudo atualizado evita muitos problemas. Quer que eu te lembre de quando fizer as atualizações?",
    "conectividade": "Problemas de internet são chatos, né? Tente reiniciar o roteador, mas se precisar, estamos aqui pra ajudar.",
    "antivírus": "Ter um antivírus atualizado é a melhor forma de proteger seu sistema. Quer dicas de qual usar?",
    "recuperação de dados": "Se perdeu arquivos importantes, temos serviços para tentar recuperar seus dados. Não se preocupe!",
    "configuração": "Vai configurar algum equipamento novo? Posso te ajudar passo a passo para que tudo funcione direitinho.",
    "senha wifi": "Esqueceu a senha do Wi-Fi? Sem problemas, é só entrar em contato que te ajudamos a recuperar.",
    "suporte remoto": "Sabia que podemos te ajudar sem sair de casa? Nosso suporte remoto é rápido e prático.",
    
    # Perguntas frequentes ampliadas
    "cancelar pedido": "Quer cancelar seu pedido? Me diga o número e vamos resolver isso rápido pra você.",
    "rastreamento": "Para rastrear seu pedido, basta acessar o link que enviamos no e-mail ou me passar o código para eu ajudar.",
    "troca produto": "Se o produto veio com defeito ou não gostou, você pode solicitar a troca em até 7 dias após receber.",
    "garantia": "Os produtos têm garantia de 12 meses. Se precisar acionar, fale com nosso suporte que te orientamos.",
    "nota fiscal": "Quer a nota fiscal? Normalmente enviamos por e-mail após o pedido ser confirmado, mas posso reenviar para você.",
    "problema pagamento": "Se houve algum problema no pagamento, verifique seu banco ou cartão e nos avise para ajudarmos.",
    "desconto": "Quer saber sobre promoções e descontos? Fique ligado no nosso site e redes sociais para não perder nada.",
    "produtos": "Tem dúvida sobre algum produto? Posso te passar todas as informações e especificações que precisar.",
    "assistência técnica": "Oferecemos assistência técnica especializada para resolver qualquer problema com seus equipamentos.",
    "atendimento presencial": "Atendimento presencial disponível em nossa loja física, confira o endereço e horários conosco.",
    "meu cadastro": "Precisa atualizar seus dados cadastrais? Posso te ajudar a fazer isso de forma simples e rápida.",
    "como comprar": "Se tiver dúvidas de como realizar uma compra, posso te guiar pelo processo passo a passo.",
    "forma envio": "Enviamos por transportadoras confiáveis e também temos opções de retirada na loja.",
    "pedido atrasado": "Se seu pedido está atrasado, me informe o número para que eu possa verificar e te dar uma resposta.",
    "problema login": "Esqueceu a senha ou não consegue acessar sua conta? Posso te ajudar a recuperar o acesso.",
    "cancelar assinatura": "Quer cancelar sua assinatura? Me avise que te explico o processo e confirmo tudo para você.",
    "reinstalar software": "Precisa reinstalar algum software? Posso te guiar para fazer isso do jeito correto.",
    "limpeza sistema": "Quer dicas para deixar seu computador mais rápido? Posso passar algumas recomendações para limpeza e manutenção.",
    "erro sistema": "Está enfrentando algum erro no sistema? Me fale o que aparece para que eu possa ajudar a resolver.",
    "formatar pc": "Se precisar formatar seu PC, podemos ajudar a fazer backup e reinstalar tudo com segurança.",
    "instalar impressora": "Quer ajuda para instalar uma impressora? Vou te guiar para fazer isso sem dor de cabeça.",
    "configurar email": "Precisa configurar seu e-mail em algum dispositivo? Posso te ajudar com isso também.",
    "usar nuvem": "Quer saber como usar serviços de nuvem para guardar seus arquivos? Posso explicar e indicar boas opções.",
    "criptografia": "Quer proteger seus dados com criptografia? Posso te explicar o que é e como usar.",
    "suporte mobile": "Problemas com seu celular ou tablet? Nosso suporte também cobre dispositivos móveis.",
    "backup automático": "Quer configurar backups automáticos? Posso te ajudar a automatizar esse processo para você não esquecer.",
    "rede wifi": "Precisa configurar sua rede Wi-Fi ou melhorar o sinal? Fale comigo que te dou algumas dicas eficazes.",
    "instalar antivírus": "Quer ajuda para instalar um antivírus confiável? Tenho várias recomendações e posso ajudar na instalação.",
    "trocar senha": "Quer trocar sua senha por segurança? Vou te explicar o passo a passo para fazer isso.",
    "limpar cache": "Quer deixar seu dispositivo mais rápido limpando cache? Posso te ensinar a fazer isso facilmente.",
    "atualizar driver": "Precisa atualizar os drivers do seu hardware? Posso orientar como fazer sem riscos.",
    "recuperar senha": "Esqueceu sua senha? Não se preocupe, posso ajudar a recuperar o acesso ao seu sistema.",
    "problema login": "Está com dificuldades para entrar na conta? Vamos resolver isso juntos, é rapidinho!",
    "assistência remota": "Quer que a gente acesse seu computador remotamente para ajudar? É seguro e eficiente.",
    "backup na nuvem": "Quer fazer backup na nuvem para garantir a segurança dos seus dados? Posso ajudar a configurar.",
    }


    def responder():
        msg = entry_msg.get().strip()
        if not msg:
            return
        chat_log.config(state="normal")
        chat_log.insert(tk.END, f"Você: {msg}\n")
        msg_lower = msg.lower()
        resposta = "Desculpe, não entendi sua pergunta. Tente algo como 'horário', 'email' ou 'telefone'."
        for chave in respostas:
            if chave in msg_lower:
                resposta = respostas[chave]
                break
        chat_log.insert(tk.END, f"Bot: {resposta}\n\n")
        chat_log.config(state="disabled")
        chat_log.see(tk.END)
        entry_msg.delete(0, tk.END)

    btn_enviar = tk.Button(frame_entry, text="Enviar", bg="#007bff", fg="white",
                           font=("Helvetica", 11), command=responder)
    btn_enviar.pack(side="right")

    entry_msg.bind("<Return>", lambda event: responder())

def main():
    root = tk.Tk()
    root.title("Sistema de Suporte")
    root.geometry("1000x650")

    # Menu simples para chamar contatos_suporte
    menubar = tk.Menu(root)
    menu_geral = tk.Menu(menubar, tearoff=0)
    menu_geral.add_command(label="Contatos de Suporte", command=lambda: contatos_suporte(root))
    menu_geral.add_separator()
    menu_geral.add_command(label="Sair", command=root.quit)
    menubar.add_cascade(label="Menu", menu=menu_geral)
    root.config(menu=menubar)

    contatos_suporte(root)
    root.mainloop()

if __name__ == "__main__":
    main()
