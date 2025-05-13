import sqlite3
import re
from tkinter import messagebox

class Backend:
    def ativar_db(self):
        self.conn = sqlite3.connect("Alunos_cadastrados")
        self.cursor = self.conn.cursor()
        print("Banco de dados: Ativo")

    def desativar_db(self):
        self.conn.close()
        print("Banco de dados: Desativado")

    def tabela_db(self):
        self.ativar_db()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Alunos(
                Id_Aluno INTEGER PRIMARY KEY,
                Nome TEXT NOT NULL,
                Email TEXT NOT NULL,
                Telefone INTEGER NOT NULL,
                Cpf INTEGER NOT NULL,
                Senha TEXT NOT NULL,
                Confirmar_senha TEXT NOT NULL
            );
        """)
        self.conn.commit()
        self.desativar_db()

    def validar_nome(self, nome):
        return re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome) is not None

    def validar_cpf(self, cpf):
        return cpf.isdigit() and len(cpf) == 11

    def validar_telefone(self, telefone):
        return telefone.isdigit() and len(telefone) == 11

    def validar_senha(self, senha, confirma_senha):
        return senha == confirma_senha
