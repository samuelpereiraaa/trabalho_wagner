import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox
import re


class Backend():

    def ativar_db(self):
        self.conn = sqlite3.connect("Alunos_Cadastado.db")
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

    def limpar_campos_cadastro(self):
        self.cadastro_nome_aluno_entry.delete(0, END)
        self.cadastro_email_aluno_entry.delete(0, END)
        self.cadastro_telefone_aluno_entry.delete(0, END)
        self.cadastro_cpf_aluno_entry.delete(0, END)
        self.cadastro_senha_aluno_entry.delete(0, END)
        self.cadastro_confirma_senha_aluno_entry.delete(0, END)
    def limpar_campos_login(self):
        self.cpf_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)

    def validar_cpf(self, cpf):
        return cpf.isdigit() and len(cpf) == 11
    def validar_telefone(self, telefone):
        return telefone.isdigit() and len(telefone) == 11
    def validar_senha(self, senha, confirma_senha):
        return senha == confirma_senha
    def validar_nome(self, nome):
        # Aceita letras maiúsculas, minúsculas, acentuadas e espaços
        return re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome) is not None


    def cadastro_aluno(self):
        self.cadastro_nome_aluno = self.cadastro_nome_aluno_entry.get()
        self.cadastro_email_aluno = self.cadastro_email_aluno_entry.get()
        self.cadastro_telefone_aluno = self.cadastro_telefone_aluno_entry.get()
        self.cadastro_cpf_aluno = self.cadastro_cpf_aluno_entry.get()
        self.cadastro_senha_aluno = self.cadastro_senha_aluno_entry.get()
        self.cadastro_confirma_senha_aluno = self.cadastro_confirma_senha_aluno_entry.get()

        self.ativar_db()

        self.cursor.execute("""
            INSERT INTO Alunos(Nome, Email, Telefone, Cpf, Senha, Confirmar_senha)
            VALUES (?, ?, ?, ?, ?, ?)""", (self.cadastro_nome_aluno, self.cadastro_email_aluno, self.cadastro_telefone_aluno, self.cadastro_cpf_aluno, self.cadastro_senha_aluno, self.cadastro_confirma_senha_aluno))
        try:

            if self.cadastro_nome_aluno == "" or self.cadastro_email_aluno == "" or self.cadastro_telefone_aluno == "" or self.cadastro_cpf_aluno == "" or self.cadastro_senha_aluno == "" or self.cadastro_confirma_senha_aluno == "":
                messagebox.showerror(title="Sistema", message="Error \nPreencha todos os campos.")
	    elif not self.validar_nome(self.cadastro_nome_aluno):
                messagebox.showerror(title="Sistema", message="Error \nO nome deve conter apenas letras.")
            elif not self.validar_cpf(self.cadastro_cpf_aluno):
                messagebox.showerror(title="Sistema", message="Error \nInsira um cpf válido.")
            elif not self.validar_telefone(self.cadastro_telefone_aluno):
                messagebox.showerror(title="Sistema", message="Error \nInsira um telefone válido.")
            elif not self.cadastro_email_aluno.endswith("@gmail.com"):
                messagebox.showerror(title="Sistema", message="Error \nInsira um endereço gmail válido.")
            elif not self.validar_senha(self.cadastro_senha_aluno, self.cadastro_confirma_senha_aluno):
                messagebox.showerror(title="Sistema", message="Error \nSenhas não coincidem.")
            else:
                self.conn.commit()
                messagebox.showinfo(title="Sistema", message="Cadastro realizado com sucesso!")
                self.desativar_db()
                self.limpar_campos_cadastro()
        except Exception as e:
                messagebox.showerror(title="Sistema", message=f"Erro no cadastro:\n{e}")
                self.desativar_db()

    def login_aluno(self):
        self.cpf_login = self.cpf_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        print(self.cpf_login, self.senha_login)
        self.limpar_campos_login()

        self.ativar_db()

        self.cursor.execute("""SELECT * FROM Alunos WHERE(Cpf = ? AND Senha = ?)""", (self.cpf_login, self.senha_login))

        self.verifica_db = self.cursor.fetchone()

        try:
            if(self.cpf_login == "" or self.senha_login == ""):
                messagebox.showinfo(title="Sistema", message="Preencha os campos vazios.")
            elif(self.cpf_login in self.verifica_db and self.senha_login in self.verifica_db):
                messagebox.showinfo(title="Sistema", message="Login bem sucessido, bem vindo!")
                self.desativar_db()
                self.limpar_campos_login()
        except:
            messagebox.showerror(title="Sistema", message="Usuário não encontrado.\n Verifique seus dados.")
            self.desativar_db()


class App(ctk.CTk,Backend):
    def __init__(self):
        super().__init__()
        self.configuracao_da_janela()
        self.login()
        self.ativar_db()
        self.tabela_db()

    def configuracao_da_janela(self):
        self.geometry("400x400")
        self.title("Escola Pequenos Saberes")
        self.resizable(False, False)
    def login(self):
        self.title = ctk.CTkLabel(self, text="administrador".upper(), font=("Bungee Spice", 20))
        self.title.grid(row=0, column=0, pady=20, padx=120)

        self.frame_login = ctk.CTkFrame(self,width= 200, height=200)
        self.frame_login.place(x=45, y=90)

        self.lb_title = ctk.CTkLabel(self.frame_login, text="Escola Pequenos Saberes", font=("Special Gothic Expanded One", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        self.cpf_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="CPF", font=("Special Gothic Expanded One", 16), corner_radius=15, border_color="#000")
        self.cpf_login_entry.grid(row=1, column=0, padx=10, pady=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha", font=("Special Gothic Expanded One", 16), corner_radius=15,  border_color="#000", show="*")
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)

        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text="Login".upper(), font=("Special Gothic Expanded One", 14), fg_color="#000", hover_color="#FFF", corner_radius=15, command=self.login_aluno)
        self.btn_login.grid(row=3, column=0, padx=10, pady=10)

        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="#000", hover_color="#FFF", text="Cadastro".upper(), font=("Century Gothic bold", 14), corner_radius=15, command=self.cadastro)
        self.btn_cadastro.grid(row=4, column=0, padx=10, pady=10)

        self.exit = ctk.CTkButton(self.frame_login, width=300, fg_color="#F00", hover_color="#000", text="Sair".upper(), corner_radius=15, command=self.destroy)
        self.exit.grid(row=5, column=0, padx=10, pady=10)

    def cadastro(self):
        self.frame_login.place_forget()

        self.frame_cadastro = ctk.CTkFrame(self,width= 200, height=200) #Ajuste do frame do login
        self.frame_cadastro.place(x=45, y=60)

        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Cadastro", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=5)

        self.cadastro_nome_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Nome do Usuario:", font=("Century Gothic bold", 16), corner_radius=15, border_color="#000")
        self.cadastro_nome_aluno_entry.grid(row=1, column=0, padx=10, pady=5)

        self.cadastro_email_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Email do Usuario:", font=("Century Gothic bold", 16), corner_radius=15, border_color="#000")
        self.cadastro_email_aluno_entry.grid(row=2, column=0, padx=10, pady=5)

        self.cadastro_telefone_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Telefone do Usuario:", font=("Century Gothic bold", 16), corner_radius=15, border_color="#000")
        self.cadastro_telefone_aluno_entry.grid(row=3, column=0, padx=10, pady=5)

        self.cadastro_cpf_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="CPF do Usuario:", font=("Century Gothic bold", 16), corner_radius=15, border_color="#000")
        self.cadastro_cpf_aluno_entry.grid(row=4, column=0, padx=10, pady=5)


        self.cadastro_senha_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha do Usuario:", font=("Century Gothic bold", 16), corner_radius=15, show="*",  border_color="#000")
        self.cadastro_senha_aluno_entry.grid(row=5, column=0, padx=10, pady=5)

        self.cadastro_confirma_senha_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirme a senha do Usuario:", font=("Century Gothic bold", 16), corner_radius=15, show="*",  border_color="#000")
        self.cadastro_confirma_senha_aluno_entry.grid(row=6, column=0, padx=10, pady=5)

        self.btn_cadastrar = ctk.CTkButton(self.frame_cadastro, width=300, text="Cadastrar".upper(), font=("Century Gothic bold", 14), corner_radius=15, fg_color="#000", hover_color="#FFF", command=self.cadastro_aluno)
        self.btn_cadastrar.grid(row=7, column=0, padx=10, pady=5)

        self.btn_login_back = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar".upper(), font=("Century Gothic bold", 14), corner_radius=15, fg_color="#000", hover_color="#FFF", command=self.login)
        self.btn_login_back.grid(row=8, column=0, padx=10, pady=5)
    

if __name__ == "__main__":
    app = App()
    app.mainloop(),






