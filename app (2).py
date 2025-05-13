import customtkinter as ctk
from tkinter import END, messagebox
from backend import Backend

class App(ctk.CTk, Backend):
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
        self.frame_login = ctk.CTkFrame(self, width=300, height=300)
        self.frame_login.place(x=45, y=90)

        self.cpf_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="CPF")
        self.cpf_login_entry.grid(row=0, column=0, padx=10, pady=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha", show="*")
        self.senha_login_entry.grid(row=1, column=0, padx=10, pady=10)

        self.btn_login = ctk.CTkButton(self.frame_login, text="LOGIN", command=self.login_aluno)
        self.btn_login.grid(row=2, column=0, padx=10, pady=10)

        self.btn_cadastro = ctk.CTkButton(self.frame_login, text="CADASTRO", command=self.cadastro)
        self.btn_cadastro.grid(row=3, column=0, padx=10, pady=10)

    def cadastro(self):
        self.frame_login.place_forget()
        self.frame_cadastro = ctk.CTkFrame(self, width=300, height=400)
        self.frame_cadastro.place(x=45, y=60)

        self.cadastro_nome_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Nome")
        self.cadastro_nome_aluno_entry.grid(row=0, column=0, padx=10, pady=5)

        self.cadastro_email_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Email")
        self.cadastro_email_aluno_entry.grid(row=1, column=0, padx=10, pady=5)

        self.cadastro_telefone_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Telefone")
        self.cadastro_telefone_aluno_entry.grid(row=2, column=0, padx=10, pady=5)

        self.cadastro_cpf_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="CPF")
        self.cadastro_cpf_aluno_entry.grid(row=3, column=0, padx=10, pady=5)

        self.cadastro_senha_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha", show="*")
        self.cadastro_senha_aluno_entry.grid(row=4, column=0, padx=10, pady=5)

        self.cadastro_confirma_senha_aluno_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirmar Senha", show="*")
        self.cadastro_confirma_senha_aluno_entry.grid(row=5, column=0, padx=10, pady=5)

        self.btn_cadastrar = ctk.CTkButton(self.frame_cadastro, text="Cadastrar", command=self.cadastro_aluno)
        self.btn_cadastrar.grid(row=6, column=0, padx=10, pady=5)

        self.btn_voltar = ctk.CTkButton(self.frame_cadastro, text="Voltar", command=self.voltar_login)
        self.btn_voltar.grid(row=7, column=0, padx=10, pady=5)

    def voltar_login(self):
        self.frame_cadastro.place_forget()
        self.login()

    def cadastro_aluno(self):
        nome = self.cadastro_nome_aluno_entry.get()
        email = self.cadastro_email_aluno_entry.get()
        telefone = self.cadastro_telefone_aluno_entry.get()
        cpf = self.cadastro_cpf_aluno_entry.get()
        senha = self.cadastro_senha_aluno_entry.get()
        confirma = self.cadastro_confirma_senha_aluno_entry.get()

        if not all([nome, email, telefone, cpf, senha, confirma]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
        elif not self.validar_nome(nome):
            messagebox.showerror("Erro", "Nome inválido.")
        elif not self.validar_cpf(cpf):
            messagebox.showerror("Erro", "CPF inválido.")
        elif not self.validar_telefone(telefone):
            messagebox.showerror("Erro", "Telefone inválido.")
        elif not email.endswith("@gmail.com"):
            messagebox.showerror("Erro", "Use um email @gmail.com.")
        elif not self.validar_senha(senha, confirma):
            messagebox.showerror("Erro", "Senhas não coincidem.")
        else:
            try:
                self.ativar_db()
                self.cursor.execute("""
                    INSERT INTO Alunos (Nome, Email, Telefone, Cpf, Senha, Confirmar_senha)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (nome, email, telefone, cpf, senha, confirma))
                self.conn.commit()
                self.desativar_db()
                messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
                self.voltar_login()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro no cadastro: {e}")
                self.desativar_db()

    def login_aluno(self):
        cpf = self.cpf_login_entry.get()
        senha = self.senha_login_entry.get()

        if not cpf or not senha:
            messagebox.showinfo("Erro", "Preencha os campos.")
            return

        try:
            self.ativar_db()
            self.cursor.execute("SELECT * FROM Alunos WHERE Cpf=? AND Senha=?", (cpf, senha))
            resultado = self.cursor.fetchone()
            if resultado:
                messagebox.showinfo("Sucesso", "Login bem-sucedido.")
            else:
                messagebox.showerror("Erro", "CPF ou senha incorretos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer login: {e}")
        finally:
            self.desativar_db()
