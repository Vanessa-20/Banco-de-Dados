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

def imprimirDados(conexao):
    cursor = conexao.execute('SELECT * FROM alunos')
       
    alunos = cursor.fetchall()
    print('\n', alunos, '\n')
 
    for aluno in alunos:
        print(aluno)
    print()
        
conn = conectarBanco()
if conn:
    print('Pronto para realizar operações no BD')
    imprimirDados(conn)
    conn.commit()
    conn.close()
        
else:
    print('Sem conexão')
            
print('Encerrando...')

