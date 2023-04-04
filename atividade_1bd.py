# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error, OperationalError
import sys
import os

def conectarBanco():
    conexao = None
    banco = 'unoesc.db'
   
    print(f"SQLite Versão: {sqlite3.version}\n")
   
    path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(path, banco)
    
    print(f'Banco de dados: [{full_path}]\n')
    if not os.path.isfile(full_path):
        continuar = input(f'Banco de dados não encontrado, deseja cliá-lo? \nSe sim então o banco será criado no diretório onde o programa está sendo executado [{os.getcwd()}]! [S/N]: ')
        
        if continuar.upper() != 'S':
            raise sqlite3.DatabaseError('Banco de dados não encontrado!')
           
    conexao = sqlite3.connect(full_path)
    
    return conexao

def criar_tabela(conexao):
    cursor = conexao.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS alunos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT
                    )
                    
                    """)
    conexao.commit()

    if cursor:
        cursor.close()

def imprimirDados(conexao):
    cursor = conexao.execute('SELECT * FROM alunos')
       
    alunos = cursor.fetchall()
    print('\n', alunos, '\n')
 
    for aluno in alunos:
        print(aluno)
    print()

    if cursor:
        cursor.close()


def incluirUmRegistro(conexao):
    comando = 'INSERT INTO alunos (id, nome) VALUES(?, ?)'
    
    cursor = conexao.cursor()
    cursor.execute(comando, (None, 'Vanessa'))
    
    conexao.commit()
    
    if cursor:
        cursor.close()
        
def incluirVariosRegistros(conexao):
    comando = 'INSERT INTO alunos (id, nome) VALUES(?, ?)'
    pessoas = [
        (None, 'Zé das Couves'),
        (None, 'Maria das Dores')
        ]
    
    cursor = conexao.cursor()
    cursor.executemany(comando, pessoas)
    
    conexao.commit()
    
    if cursor:
        cursor.close()
        
def menu(conexao):
    opcao = 1
    while opcao != 5:
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')

        print('--------------')
        print('MENU DE OPÇÕES')
        print('--------------')
        print('1. Incluir dados')
        print('2. Alterar dados')
        print('3. Excluir dados')
        print('4. Listar dados')
        print('5. Sair')

        # Tratamento de erros no caso de entrada alfanumérica no input()
        try:
            opcao = int(input('\nOpção [1-5]: '))
        except ValueError:
                opcao = 0
        if opcao == 1:
            #Incluir(conexao)
        elif opcao == 2:
            #Alterar(conexao)
        elif opcao == 3:
            #Excluir(conexao)
        elif opcao == 4:
            #Listar(conexao)
        elif opcao != 5:
            print('Opção inválida, tente novamente')
    
        print()
    
print('\nEncerrando o programa...')
    sleep(2)

if __name__ == '__main__':
    conn = None
    
    try:
        conn = conectarBanco()
        criar_tabela(conn)
        
        #incluirUmRegistro(conn)
        #incluirVariosRegistros(conn)
        imprimirDados(conn)
    except OperationalError as e:
        print('Erro operacional:', e)
    except sqlite3.DatabaseError as e:
        print('Erro database:', e)
    except Error as e:
        print('Erro SQLite3:', e)
    except Exception as e:
        print('Erro durante a execução o sistema!')
        print(e)
    finally:
        # Não mostra o traceback
        raise SystemExit()
        
        if conn:
            print('Liberando conexão...')
            conn.commit()
            conn.close()
            print('Encerrando...')
    
        
