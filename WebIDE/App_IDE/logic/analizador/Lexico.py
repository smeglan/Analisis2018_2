'''
Created on 26/01/2019

@author: Sebastian
'''

import ply.lex as lex
import re
import codecs
import os
import sys
#from ply.example.ansic.clex import reserved, reserved_map
#from test.test_decimal import file
#from lib2to3.tests.data.infinite_recursion import FILE

reservadas =['VAR',
          'INT',
          'FLOAT',
          'BOOLEAN',
          'STRING',
          'LISTA',
          'IF',
          'THEN',
          'ELSE',
          'ENDIF',
          'CASEOF',
          'DEFAULT',
          'ENDCASE',
          'FOR',
          'TO',
          'INC',
          'DO',
          'DOWNTO',
          'ENDFOR',
          'WHILE',
          'ENDWHILE',
          'REPEAT',
          'UNTIL',
          'PROCEDURA',
          'IN',
          'OUT',
          'FUNCTION',
          'RETURN',
          'CONST',
          'CALL',
          'TRUE',
          'FALSE',
          'ADD',
          'REMOVE',
          'SIZE',
          'FIND',
          'INDEX',
          'CONTAINS',
          'PRINT'
]


tokens = reservadas+['ID',
          'Numero',
          'String',
          'Coma',
          'PuntoComa',
          'Punto',
          'ParentesisIzquierdo', 
          'ParentesisDerecho', 
          'Suma', 
          'Resta', 
          'Multiplicacion',
          'Division',
          'Modulo',
          'Potencia',
          'Menor',
          'Mayor',
          'MenorIgual',
          'MayorIgual',
          'Igual',
          'Diferente',
          'Y',
          'O',
          'No',
          'vAsignacion',
          'InicioF',
          'FinalF',
          'Condicion_caso',
          'CorcheteIzquierdo',
          'CorcheteDerecho'
]

#tokens = tokens + list(reservadas.values())

t_ignore = '\t'
t_Suma = r'\+'
t_Resta = r'\-'
t_Multiplicacion = r'\*'
t_Division = r'/'
t_vAsignacion = r'<-'
t_Coma = r','
t_PuntoComa = r';'
t_Punto = r'\.'
t_ParentesisIzquierdo = r'\('
t_ParentesisDerecho = r'\)'
t_Modulo = r'mod'
t_Potencia = r'exp'
t_Menor = r'<'
t_Mayor = r'>'
t_MenorIgual = r'<='
t_MayorIgual = r'>='
t_Igual = r'='
t_Diferente = r'<>'
t_Y = r'and'
t_O = r'or'
t_No = r'not'
t_InicioF = r'\{'
t_FinalF = r'\}'
t_Condicion_caso = r'\:'
t_CorcheteIzquierdo = r'\['
t_CorcheteDerecho = r'\]'


def t_ID(t):
    r'[a-zA-z_][a-zA-z0-9_]*'
    if t.value.upper() in reservadas:
        t.value = t.value.upper()
        t.type = t.value
        
    return t

def t_String(t):
    r'["][a-zA-z0-9_]*["]'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno +=len(t.value)
    
def t_ccode_nonspace(t):
    r'\s+'
    pass

def t_COMMENT(t):
    r'\#.*'
    pass

def t_Numero(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print ("caracter no valido '%s'" % t.value[0])
    t.lexer.skip(1)
    
#def buscarFicheros(directorio):
#    ficheros = []
#    numArchivo = ''
#    respuesta = False
#    cont = 1
    
#    for base, dirs, files in os.walk(directorio):
#        ficheros.append(files)
        
#    for file in files:
#        print (str(cont)+". "+file)
#        cont = cont + 1
        
#    while respuesta == False:
#        numArchivo = 1
#        for file in files:
#            if file == files[int(numArchivo)-1]:
#                respuesta = True
#                break
            
#    print("Has escogido \" %s\" \n" %files[int(numArchivo)-1])
    
#    return files[int(numArchivo)-1]


#directorio = 'C:/Users/usuario/Downloads/ProyectoAnalisis/test/'
#archivo = buscarFicheros(directorio)
#test = directorio + archivo
#fp = codecs.open(test, "r", "utf-8")
#cadena = fp.read()
#fp.close()

analizador = lex.lex()

#analizador.input(cadena)

#while True:
#    tok = analizador.token()
#    if not tok : break
#    print (tok)


