'''
Created on 18/04/2019

@author: Sebastian
'''
import re

#Prepara el algoritmo transformandolo en una lista de lineas.
def prepare_algor(algorithm):
    algoritmo = []
    i = 0
    for c in algorithm._split_lines():
        algoritmo[i] = c
        i=i+1
    return algoritmo

#Obtiene el nombre del algoritmo.
def get_algor_name(algorithm):
    cadena = algorithm[0]
    cadena = re.sub(r"\s+", "", cadena) 
    corte = 0
    if cadena.find("PROCEDURA")>-1:
        corte = 9
    elif cadena.find("FUNCTION")>-1:
        corte = 8
    cadena = cadena[corte:len(cadena)]
    name = cadena[0:cadena.find("(")]
    return name
#Determina si un algoritmo es recursivo o no.
def is_recursive(algorithm):
    count = 0
    name = get_algor_name(algorithm)
    for line in algorithm:
        if(line.find(name)>-1):
            count = count+1
        if(count>1):
            return True
    return False
#Busca la cantidad de instrucciones de un tipo.
def search_intruction(algorithm, instruction):
    lineas = []
    for i in range(0, len(algorithm)):
        cadena = re.sub(r"\s+", "", algorithm[i]) 
        if cadena.find(instruction) == 0:
            lineas.append(i) 
    return lineas#posiciones en el algoritmo

#Determina el nombre y el tipo de variable.
def determine_enter_values(algorithm):
    values = {}
    encabezado = algorithm[0]
    encabezado = encabezado[encabezado.find("("):len(encabezado)]
    encabezado.replace(")","")
    encabezado.replace("{","")
    encabezado.replace(",","")
    cadena = encabezado.split()
    for i in range(0, len(cadena)-1, 2):
        values[cadena[i+1]] = cadena[i]
    return values

#Determina la complejidad de algoritmos sin ciclos.
def constant_algor(algorithm):    
    count = 0
    for line in algorithm:
        if line.find("endif") != -1 or line.find("endfor") != -1 or line.find("endwhile") != -1 or line.find("endcase") != -1:
            count = count + 1
    return count-1
    
#Determina la complejidad de algoritmos que solo contengan ciclos for
def only_for(algorithm, lines):
    values = determine_enter_values(algorithm)
    palabras = []
    i = 0
    complejidad = 0
    for val in values.keys():
        if values[val]=='INT':
            palabras[i] = val
    for line in lines:
        for p in palabras:
            if line.find(p)!=-1:
                complejidad = complejidad+1
    if complejidad == 0:
        constant = constant_algor(algorithm)
        return constant
    
#Determina si el algoritmo tiene loops y busca complejidades conocidas.
def determine_loops(algorithm):
    complejidad = -1
    if not is_recursive(algorithm):
        has_for = search_intruction(algorithm, "for")
        has_while = search_intruction(algorithm, "while")
        has_until = search_intruction(algorithm, "until")
        if(len(has_until)>0):
            for line in has_until:
                has_while.append(line)
        if len(has_for)==0 and has_while==0:
            complejidad = constant_algor(algorithm)
        elif len(has_for)>0 and has_while == 0:
            only_for(algorithm, has_for)
        elif len(has_for)==0 and has_while > 0:
            return 2
        else:
            return 3
    else:
        return complejidad


    
        