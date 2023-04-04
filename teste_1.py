# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error, OperationalError
import os
from time import sleep
from IPython import get_ipython


def conectarBanco():
    conexao = None
    banco = 'unoesc1.db'
   
    print(f'SQLite Versão: {sqlite3.version}\n')
   
    path = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(path, banco)
    print(f'Banco de dados: [{full_path}]\n')
    
    if not os.path.isfile(full_path):
        continuar = input(f'Banco de dados não encontrado, deseja cliá-lo? \nSe sim então o banco será criado no diretório onde o programa está sendo executado [{os.getcwd()}]! [S/N]: ')
        
        if continuar.upper() != 'S':
            raise sqlite3.DatabaseError('Banco de dados não encontrado!')
           
    conexao = sqlite3.connect(full_path)
    print('BD aberto com sucesso!')
    
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
        
def exibir_cabecalho(mensagem):
    mensagem = f'Rotina de {mensagem} de dados'

    print('\n' + '-' * len(mensagem))
    print(mensagem)
    print('-' * len(mensagem), '\n')

    id = input('ID (0 para voltar): ')

    return id


def mostrar_registro(registro):
    print('\n===================')
    print('Registro')
    print('--------')
    print('ID:', registro[0])
    print('Nome:', registro[1])
    print('===================')


def tabela_vazia(conexao):
    cursor = conexao.cursor()
    cursor.execute('SELECT count(*) FROM alunos')
    resultado = cursor.fetchall()
    cursor.close()
    print(resultado)
    return resultado[0][0] == 0


def verificar_registro_existe(conexao, id):
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM alunos WHERE id=?', (id,))
    resultado = cursor.fetchone()
    cursor.close()

    return resultado 

def pausa():
    input('\nPressione <ENTER> para continuar')

def listar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    cursor = conexao.cursor()

    print('\n----------------------')
    print('Listagem dos Registros')
    print('----------------------\n')

    cursor.execute('SELECT * FROM alunos')
    registros = cursor.fetchall()

    for registro in registros:
        print('ID:', registro[0])
        print('Nome:', registro[1])
        print('-----')

    pausa()

    cursor.close()

def incluir(conexao):
    id = exibir_cabecalho('inclusão')
    if int(id) == 0:
        return

    if verificar_registro_existe(conexao, id):
        print('\nID já existe!')
        sleep(2)
    else:
        nome = input('\nNome: ')

        confirma = input('\nConfirma a inclusão [S/N]? ').upper()
        if confirma == 'S':
            comando = f'INSERT INTO alunos VALUES({id}, "{nome}")'

            # Cria um ID automaticamente (autoincremento)
            # comando = f'INSERT INTO alunos(nome) VALUES("{nome}")'

            cursor = conexao.cursor()
            cursor.execute(comando)
            conexao.commit()
            cursor.close()

def alterar(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    id = exibir_cabecalho('alteração')
    if int(id) == 0:
        return

    resultado = verificar_registro_existe(conexao, id)

    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)

        nome = input('\nNome: ')

        confirma = input('\nConfirma a alteração [S/N]? ').upper()
        if confirma == 'S':
            cursor = conexao.cursor()
            cursor.execute('UPDATE alunos SET nome=? WHERE id=?', (nome, id))
            conexao.commit()
            cursor.close()

def excluir(conexao):
    if tabela_vazia(conexao):
        print('\n*** TABELA VAZIA ***')
        pausa()
        return

    id = exibir_cabecalho('exclusão')
    if int(id) == 0:
        return

    resultado = verificar_registro_existe(conexao, id)

    if not resultado:
        print('\nID não existe!')
        sleep(2)
    else:
        mostrar_registro(resultado)

        confirma = input('\nConfirma a exclusão [S/N]? ').upper()
        if confirma == 'S':
            cursor = conexao.cursor()
            cursor.execute('DELETE FROM alunos WHERE id=?', (id, ))
            conexao.commit()
            cursor.close()

def menu(conexao):
    opcao = 1
    while opcao != 5:
        # if 'SPY_PYTHONPATH' in os.environ:
        #     get_ipython().magic('clear')
        # else:
        #     os.system('cls' if os.name == 'nt' else 'clear')

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
            incluir(conexao)
        elif opcao == 2:
            alterar(conexao)
        elif opcao == 3:
            excluir(conexao)
        elif opcao == 4:
            listar(conexao)
        elif opcao != 5:
            print('Opção inválida, tente novamente')
            sleep(2)

        print()

    return opcao
        
if __name__ == '__main__':
    conn = None

    while True:
        try:
            conn = conectarBanco()
            criar_tabela(conn)

            if menu(conn) == 5:
                break
        except OperationalError as e:
            # Possibilidade de se recuperar do erro
            print('Erro operacional:', e)
        except sqlite3.DatabaseError as e:
            print('Erro database:', e)
            raise SystemExit()
        except Error as e:
            print('Erro SQLite3:', e)
            raise SystemExit()
        except Exception as e:
            print('Erro durante a execução do sistema!')
            print(e)
        finally:
            if conn:
                print('Liberando a conexão...')
                conn.commit()
                conn.close()

    print('Encerrando..')

def listar(conexao):
    cursor = conexao.execute('SELECT * from alunos')

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
        # if 'SPY_PYTHONPATH' in os.environ:
        #     get_ipython().magic('clear')
        # else:
        #     os.system('cls' if os.name == 'nt' else 'clear')

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
            pass
            #Incluir(conexao)
        elif opcao == 2:
            pass
            #Alterar(conexao)
        elif opcao == 3:
            pass
            #Excluir(conexao)
        elif opcao == 4:
            listar(conexao)
            input('Pressione uma tecla para continuar...')
        elif opcao != 5:
            print('Opção inválida, tente novamente')
            sleep(2)
    
        print()

if __name__ == '__main__':
    conn = None
    
    try:
        conn = conectarBanco()
        criar_tabela(conn)
        
        #incluirUmRegistro(conn)
        incluirVariosRegistros(conn)
        
        #tebela_vazia(conn)
        menu(conn)
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