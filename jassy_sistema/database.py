import sqlite3
import hashlib

def criar_tabela_usuarios():
    conn = sqlite3.connect('jassy_gestao.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def adicionar_usuario(usuario, senha):
    conn = sqlite3.connect('jassy_gestao.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, hash_senha(senha)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Usuário já existe
    finally:
        conn.close()

def verificar_credenciais(usuario, senha):
    conn = sqlite3.connect('jassy_gestao.db')
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado and resultado[0] == hash_senha(senha):
        return True
    return False

# Garante que a tabela de usuários exista ao iniciar o módulo
criar_tabela_usuarios()