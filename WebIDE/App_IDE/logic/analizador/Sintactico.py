import ply.yacc as yacc
import os
import codecs
import re 
from .Lexico import tokens
from sys import stdin
from Semantico import *


class Node:
    def __init__(self):
        print("init node")
    def evaluate(self):
        return 0
    def execute(self):
        return 0

class programa(Node):
    def __init__(self, v1):
        self.v1 = v1

    def evaluate(self):
        return self.v1.evaluate()
    
    

class bloque(Node):
    def __init__(self, v1, v2, v3, v4):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4

    def evaluate(self):
        vt = self.v1.evaluate()
        vt = self.v2.evaluate()
        vt = self.v3.evaluate()
        vt = self.v4.evaluate()
        return None


class multiplicar(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if (self.op == '*'):
            return self.v1.evaluate() * self.v2.evaluate()
        elif(self.op == '/'):
            return self.v1.evaluate() / self.v2.evaluate()


class sumar(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if (self.op == '+'):
            return self.v1.evaluate() + self.v2.evaluate()
        elif(self.op == '-'):
            return self.v1.evaluate() - self.v2.evaluate()


class negar(Node):
    def __init__(self, op, v1):
        self.v1 = v1
        self.op = op

    def evaluate(self):
        return not self.v1.evaluate()


class relacion2(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if (self.op == 'Y'):
            return self.v1.evaluate() and self.v2.evaluate()
        elif(self.op == 'O'):
            return self.v1.evaluate() or self.v2.evaluate()


class relacion(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.op = op

    def evaluate(self):
        if (self.op == '='):
            return self.v1.evaluate() == self.v2.evaluate()
        elif(self.op == '<>'):
            return self.v1.evaluate() != self.v2.evaluate()
        elif(self.op == '> '):
            return self.v1.evaluate() >  self.v2.evaluate()
        elif(self.op == '< '):
            return self.v1.evaluate() <  self.v2.evaluate()
        elif(self.op == '>='):
            return self.v1.evaluate() >= self.v2.evaluate()
        elif(self.op == '<='):
            return self.v1.evaluate() <= self.v2.evaluate()


class sumaString(Node):
    def __init__(self, op, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        return str(self.v1.evaluate()) + str(self.v2.evaluate())


class imprimir(Node):
    def __init__(self, v1):
        self.v1 = v1

    def evaluate(self):
        print (self.v1.evaluate())
        return None


class asignar(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        if (VARIABLES['INT'[self.v1.evaluate()]] != None):
            VARIABLES['INT'[self.v1.evaluate()]] = self.v2.evaluate()
        elif(VARIABLES['STRING'[self.v1.evaluate()]] != None):
            VARIABLES['STRING'[self.v1.evaluate()]] = self.v2.evaluate()
        elif(VARIABLES['BOOLEAN'[self.v1.evaluate()]] != None):
            VARIABLES['BOOLEAN'[self.v1.evaluate()]] = self.v2.evaluate()
        return None


class tipoAsignar(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        VARIABLES[str(self.v1.evaluate())] = self.v2.evaluate()


class buscarConstanteInt(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        if (VARIABLES['INT'[self.v1.evaluate()]] == None or
            VARIABLES['STRING'[self.v1.evaluate()]] == None or
            VARIABLES['BOOLEAN'[self.v1.evaluate()]] == None or
            VARIABLES['LISTA'[self.v1.evaluate()]] == None or
            CONSTANTE['INTC'[self.v1.evaluate()]] == None or
            CONSTANTE['STRINGC'[self.v1.evaluate()]] == None or
            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] != None):

            CONSTANTE['INTC'[self.v1.evaluate()]] = self.v2
        else:
            return None


class buscarConstanteString(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        if (VARIABLES['INT'[self.v1.evaluate()]] == None or
            VARIABLES['STRING'[self.v1.evaluate()]] == None or
            VARIABLES['BOOLEAN'[self.v1.evaluate()]] == None or
            VARIABLES['LISTA'[self.v1.evaluate()]] == None or
            CONSTANTE['INTC'[self.v1.evaluate()]] == None or
            CONSTANTE['STRINGC'[self.v1.evaluate()]] == None or
            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] != None):

            CONSTANTE['STRINGC'[self.v1.evaluate()]] = self.v2


class buscarConstanteBooleanTrue(Node):
    def __init__(self, v1):
        self.v1 = v1

    def evaluate(self):
        if (VARIABLES['INT'[self.v1.evaluate()]] == None or
            VARIABLES['STRING'[self.v1.evaluate()]] == None or
            VARIABLES['BOOLEAN'[self.v1.evaluate()]] == None or
            VARIABLES['LISTA'[self.v1.evaluate()]] == None or
            CONSTANTE['INTC'[self.v1.evaluate()]] == None or
            CONSTANTE['STRINGC'[self.v1.evaluate()]] == None or
            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] == None):

            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] = True


class buscarConstanteBooleanFalse(Node):
    def __init__(self, v1):
        self.v1 = v1

    def evaluate(self):
        if (VARIABLES['INT'[self.v1.evaluate()]] == None or
            VARIABLES['STRING'[self.v1.evaluate()]] == None or
            VARIABLES['BOOLEAN'[self.v1.evaluate()]] == None or
            VARIABLES['LISTA'[self.v1.evaluate()]] == None or
            CONSTANTE['INTC'[self.v1.evaluate()]] == None or
            CONSTANTE['STRINGC'[self.v1.evaluate()]] == None or
            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] == None):

            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] = False

class buscarVariableInt(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        if (VARIABLES['INT'[self.v1.evaluate()]] == None or
            VARIABLES['STRING'[self.v1.evaluate()]] == None or
            VARIABLES['BOOLEAN'[self.v1.evaluate()]] == None or
            VARIABLES['LISTA'[self.v1.evaluate()]] == None or
            CONSTANTE['INTC'[self.v1.evaluate()]] == None or
            CONSTANTE['STRINGC'[self.v1.evaluate()]] == None or
            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] == None):

            CONSTANTE['INT'[self.v1.evaluate()]] = self.v2


class buscarVariableString(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        if (VARIABLES['INT'[self.v1.evaluate()]] == None or
            VARIABLES['STRING'[self.v1.evaluate()]] == None or
            VARIABLES['BOOLEAN'[self.v1.evaluate()]] == None or
            VARIABLES['LISTA'[self.v1.evaluate()]] == None or
            CONSTANTE['INTC'[self.v1.evaluate()]] == None or
            CONSTANTE['STRINGC'[self.v1.evaluate()]] == None or
            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] == None):

            CONSTANTE['STRING'[self.v1.evaluate()]] = self.v2


class buscarVariableBooleanTrue(Node):
    def __init__(self, v1):
        self.v1 = v1

    def evaluate(self):
        if (VARIABLES['INT'[self.v1.evaluate()]] == None or
            VARIABLES['STRING'[self.v1.evaluate()]] == None or
            VARIABLES['BOOLEAN'[self.v1.evaluate()]] == None or
            VARIABLES['LISTA'[self.v1.evaluate()]] == None or
            CONSTANTE['INTC'[self.v1.evaluate()]] == None or
            CONSTANTE['STRINGC'[self.v1.evaluate()]] == None or
            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] == None):

            CONSTANTE['BOOLEAN'[self.v1.evaluate()]] = True


class buscarVariableBooleanFalse(Node):
    def __init__(self, v1):
        self.v1 = v1

    def evaluate(self):
        if (VARIABLES['INT'[self.v1.evaluate()]] == None or
            VARIABLES['STRING'[self.v1.evaluate()]] == None or
            VARIABLES['BOOLEAN'[self.v1.evaluate()]] == None or
            VARIABLES['LISTA'[self.v1.evaluate()]] == None or
            CONSTANTE['INTC'[self.v1.evaluate()]] == None or
            CONSTANTE['STRINGC'[self.v1.evaluate()]] == None or
            CONSTANTE['BOOLEANC'[self.v1.evaluate()]] == None):

            CONSTANTE['BOOLEAN'[self.v1.evaluate()]] = False


class condicion(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        if (self.v1.evaluate()):
            return self.v2.evaluate()
        else:
            return None

class repetir(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        vt = self.v1.evaluate()
        while (self.v2.evaluate()):
            vt = self.v1.evaluate()
        else:
            return vt

class mientras(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        vt = None
        while (self.v1.evaluate()):
            vt = self.v1.evaluate()
        else:
            return vt






class contiene(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        if(self.v2.evaluate() in VARIABLES['LISTA'[self.v1.evaluate()]]):
            return True
        else:
            return False


class tam(Node):
    def __init__(self, v1):
        self.v1 = v1

    def evaluate(self):
        return len(VARIABLES['LISTA'[self.v1.evaluate()]])


class remover(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        VARIABLES['LISTA'[self.v1.evaluate()]].remove(self.v2.evaluate())
        return None

class adicionar(Node):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        VARIABLES['LISTA'[self.v1.evaluate()]].append(self.v2.evaluate())
        return None


precedence =(
    ('right', 'PRINT'),
    ('right','ID','CALL','InicioF','IF','WHILE', 'REPEAT'),
    ('right','PROCEDURA', 'FUNCTION'),
    ('right', 'INT', 'BOOLEAN', 'STRING', 'LISTA'),
    ('right', 'vAsignacion'),
    ('left', 'Y', 'O'),
    ('right', 'No'),
    ('left', 'Diferente', 'Igual'),
    ('left', 'Menor', 'Mayor', 'MenorIgual', 'MayorIgual'),
    ('left', 'Suma', 'Resta'),
    ('left', 'Multiplicacion', 'Division'),
    ('left', 'ParentesisIzquierdo', 'ParentesisDerecho')
    
    )


INT = {}
STRING = {}
BOOLEAN = {}
LISTA = {}
INTC = {}
STRINGC = {}
BOOLEANC = {}

VARIABLES = {
    'INT': INT,
    'STRING': STRING,
    'BOOLEAN': BOOLEAN,
    'LISTA': LISTA
    }
CONSTANTE = {
    'INTC': INTC,
    'STRINGC': STRINGC,
    'BOOLEANC': BOOLEANC
    }


def p_program(p):
    '''program : block'''
    p[0] = programa(p[1])
    
def p_block(p):
    '''block : constDecl varDecl procDecl statement'''
    p[0] = bloque(p[1], p[2], p[3], p[4])

def p_constDecl(p):
    '''constDecl : CONST constAssignmentList'''
    
    p[0] = p[2]

def p_constDeclempty(p):
    '''constDecl : empty'''
    p[0] = None
    
def p_constAssignmentList1(p):
    '''constAssignmentList : INT ID vAsignacion Numero'''
    p[0] = buscarConstanteInt(p[2], p[4])
    
def p_constAssignmentList2(p):
    '''constAssignmentList : STRING ID vAsignacion String'''
    p[0] = buscarConstanteString(p[2], p[4])

def p_constAssignmentList3(p):
    '''constAssignmentList : LISTA ID vAsignacion lista'''
    p[0] = buscarConstanteString(p[2], p[4])
    
def p_constAssignmentList4(p):
    '''constAssignmentList : BOOLEAN ID vAsignacion TRUE'''
    p[0] = buscarConstanteBooleanTrue(p[2])
    
def p_constAssignmentList5(p):
    '''constAssignmentList : BOOLEAN ID vAsignacion FALSE'''
    p[0] = buscarConstanteBooleanFalse(p[2])

def p_val1(p):
    '''val : Numero'''
    p[0] = p[1]
    
def p_val2(p):
    '''val : String'''
    p[0] = p[1]
    
def p_val3(p):
    '''val : TRUE'''
    p[0] = True
    
def p_val4(p):
    '''val : FALSE'''
    p[0] = False

def p_val5(p):
    '''val : empty'''
    p[0] = None
    
def p_lista(p):
    '''lista : CorcheteIzquierdo inLista CorcheteDerecho'''
    p[0] = p[2]

def p_inLista1(p):
    '''inLista : val'''
    p[0] = p[1]
    
def p_inLista2(p):
    '''inLista : propListaVal'''
    p[0] = p[1]
    
def p_inLista3(p):
    '''inLista : propListaValTF'''
    p[0] = p[1]
    
def p_propLista1(p):
    '''propLista : ID Punto ADD ParentesisIzquierdo val ParentesisDerecho'''
    p[0] = adicionar(p[1], p[5])
    
def p_propLista2(p):
    '''propLista : ID Punto REMOVE ParentesisIzquierdo val ParentesisDerecho'''
    p[0] = remover(p[1], p[5])
    
def p_propListaVal1(p):
    '''propListaVal : ID Punto SIZE ParentesisIzquierdo ParentesisDerecho'''
    p[0] = tam(p[1])
    
def p_propListaValTF(p):
    '''propListaValTF : ID Punto CONTAINS ParentesisIzquierdo val ParentesisDerecho'''
    p[0] = contiene(p[1], p[5])
    
def p_varDecl1(p):
    '''varDecl : INT ID vAsignacion Numero PuntoComa'''
    p[0] = buscarVariableInt(p[2], p[4])
    
def p_varDecl2(p):
    '''varDecl : STRING ID vAsignacion String PuntoComa'''
    print("test")
    p[0] = buscarVariableString(p[2], p[4])
    


def p_varDecl3(p):
    '''varDecl : BOOLEAN ID vAsignacion TRUE PuntoComa'''
    p[0] = buscarVariableBooleanTrue(p[2])

def p_varDecl4(p):
    '''varDecl : BOOLEAN ID vAsignacion FALSE PuntoComa'''
    p[0] = buscarVariableBooleanFalse(p[2])


def p_varDeclempty(p):
    '''varDecl : empty'''
    p[0] = None
    
#def p_procDecl1(p):
#    '''procDecl : procDecl FUNCTION ID ParentesisIzquierdo variable ParentesisDerecho block RETURN'''
#    p[0] = procDecl1(p[1], Id(p[3]), p[5], p[7], "procDecl1")
#    print ("procDecl 1")
    
def p_procDecl2(p):
    '''procDecl : procDecl PROCEDURA ID block'''
    p[0] = p[4]
    
def p_procDeclempty(p):
    '''procDecl : empty'''
    p[0] = None

    
#def p_variable1(p):
#    '''variable : INT ID'''
#    p[0] = variable1(Id(p[2]), "variable1")
#    print("variable 1")
    
#def p_variable2(p):
#    '''variable : STRING ID'''
#    p[0] = variable2(Id(p[2]), "variable2")
#    print("variable 2")

#def p_variable3(p):
#    '''variable : variable Coma variable'''
#    p[0] = variable3(p[1], p[3], "variable3")
#    print('variable 3')
    
#def p_variableempty(p):
 #   '''variable : empty'''
  #  p[0] = None

    
def p_statement1(p):
    '''statement : ID vAsignacion expression'''
    p[0] = asignar(p[1], p[3])
    
def p_statement2(p):
    '''statement : CALL ID'''
    p[0] = p[2]
    
def p_statement3(p):
    '''statement : InicioF statementList FinalF'''
    p[0] = p[2]

def p_statement4(p):
    '''statement : IF condition THEN statement ENDIF'''
    p[0] = condicion(p[2], p[4])

def p_statement5(p):
    '''statement : WHILE condition DO statement ENDWHILE'''
    p[0] = mientras(p[2], p[4])
    
def p_statement6(p):
    '''statement : REPEAT statement UNTIL ParentesisIzquierdo condition ParentesisDerecho'''
    p[0] = repetir(p[2], p[5])
    
def p_statement7(p):
    '''statement : propLista'''
    p[0] = p[1]
    
#def p_statement8(p):
#    '''statement : CALL ID ParentesisIzquierdo variable ParentesisDerecho'''
#    p[0] = statement8(Id(p[2]), "statement8")
#    print ("statement 8")
    
def p_statement9(p):
    '''statement : PRINT ParentesisIzquierdo print ParentesisDerecho'''
    p[0] = imprimir(p[3])
    
def p_statement10(p):
    '''statement : FOR ID TO ID DO statement ENDFOR'''
    p[0] = imprimir(p[3])

def p_print1(p):
    '''print : val'''
    p[0] = p[1]
    
def p_print2(p):
    '''print : ID'''
    p[0] = p[1]
    
def p_print3(p):
    '''print : print Suma print'''
    p[0] = sumaString(p[1], p[3])

def p_statementempty(p):
    '''statement : empty'''
    p[0] = None

def p_statementList1(p):
    '''statementList : statement'''
    p[0] = p[1]

def p_statementList2(p):
    '''statementList : statementList PuntoComa statement'''
    p[0] = None
    

def p_condition1(p):
    '''condition : expression relation expression'''
    p[0] = relacion(p[2], p[1], p[3])

def p_condition2(p):
    '''condition : condition relationRelation condition'''
    p[0] = relacion2(p[2], p[1], p[3])
    
def p_condition3(p):
    '''condition : No condition'''
    p[0] = negar(p[1], p[2])

def p_relationRelation1(p):
    '''relationRelation : Y'''
    p[0] = p[1]

def p_relationRelation2(p):
    '''relationRelation : O'''
    p[0] = p[1]

def p_relation1(p):
    '''relation : Igual'''
    p[0] = p[1]

def p_relation2(p):
    '''relation : Diferente'''
    p[0] = p[1]

def p_relation3(p):
    '''relation : Menor'''
    p[0] = p[1]

def p_relation4(p):
    '''relation : Mayor'''
    p[0] = p[1]

def p_relation5(p):
    '''relation : MenorIgual'''
    p[0] = p[1]

def p_relation6(p):
    '''relation : MayorIgual'''
    p[0] = p[1]

def p_expression1(p):
    '''expression : term'''
    p[0] = p[1]

def p_expression3(p):
    '''expression : expression addingOperator term'''
    p[0] = sumar(p[2], p[1], p[3])

def p_addingOperator1(p):
    '''addingOperator : Suma'''
    p[0] = p[1]

def p_addingOperator2(p):
    '''addingOperator : Resta'''
    p[0] = p[1]

def p_term1(p):
    '''term : factor'''
    p[0] = p[1]

def p_term2(p):
    '''term : term multiplyingOperator factor'''
    p[0] = multiplicar(p[2], p[1], p[3])
    
def p_multiplyingOperator1(p):
    '''multiplyingOperator : Multiplicacion'''
    p[0] = p[1]

def p_multiplyingOperator2(p):
    '''multiplyingOperator : Division'''
    p[0] = p[1]
    
def p_factor1(p):
    '''factor : ID'''
    p[0] = p[1]

def p_factor2(p):
    '''factor : Numero'''
    p[0] = p[1]

def p_factor3(p):
    '''factor : ParentesisIzquierdo expression ParentesisDerecho'''
    p[0] = p[2]

def p_empty(p):
    '''empty :'''
    pass

def p_error(p):
    print ("Error de sintaxis ", p)
    #print "Error en la linea "+str(p.lineno)
    
    
    
    
def buscarFicheros(directorio):
    ficheros = []
    numArchivo = ''
    respuesta = False
    cont = 1

    for base, dirs, files in os.walk(directorio):
        ficheros.append(files)

    for file in files:
        print (str(cont)+". "+file)
        cont = cont+1

    while respuesta == False:
        numArchivo = 1
        for file in files:
            if file == files[int(numArchivo)-1]:
                respuesta = True
                break

    print ("Has escogido \"%s\" \n" %files[int(numArchivo)-1])

    return files[int(numArchivo)-1]

directorio = 'C:\Users\Sebastian\Dropbox\Proyecto Analisis 2019\test'
archivo = buscarFicheros(directorio)
test = directorio+archivo
fp = codecs.open(test,"r","utf-8")
cadena = fp.read()
fp.close()

parser = yacc.yacc()
result = parser.parse(cadena)

#result.imprimir("")
#print (result.traducir())

#graphFile = open('graphviztrhee.vz', 'w')
#graphFile.write(result.traducir())
#graphFile.close()

print (result)