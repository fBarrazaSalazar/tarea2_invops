import numpy as np
import os.path
from os import path


"""
    Calcula la suma de los puestos que se encuentran 
    entre los puestos de origen y destino
    @param arg :  [lens] largos de cada puesto entre origen y destino
    @return :  [number] suma de los largos de cada puesto entre origen y destino
"""
def sumatoria(lens):
    total = 0

    #print("a sumar (len):",lens)

    for i in lens:
        total = total + i

    #print("sumat:",total)
    return total
"""
    Calcula la distancia entre el puesto de origen y destino
    @param arg :  [pos_a] posicion de origen; [pos_b] posicion de destino; [lens] largos de cada puesto entre origen y destino
    @return :  [number] suma de la distancia entre origen y destino
"""
def calcular_distancia(pos_a, pos_b, lens):
    start = pos_a
    end = pos_b-1

    #print("start:",start)
    #print("end:",end)
    
    #print("list:",lens)
    #print("pos_a:",lens[start-1])
    #print("pos_b:",lens[end+1])

    sumat = sumatoria(lens[start:end])

    total = (lens[pos_a-1]/2) + sumat + (lens[pos_b-1]/2)

    return total

"""
    Lee el archivo y retorna 1 array y 1 matriz , el array contiene el largo de cada puesto, y la matriz contiene cuantas personas pasaron entre 
    puestos
    @param nombre : nombre del archivo que con tiene los datos a parsear 
    @return :  [array],[matrix] suma de la distancia entre origen y destino
"""


def leer_archivo(nombre):
    i=0
    if not path.isfile(nombre):
        return "error"
    f= open(nombre,'r')
    while (True):
        linea=f.readline()
        if not linea:
            break
        elif i==1:
            line = [int(x.strip()) for x in linea.split(',')]
            f_size=np.array(line)
        else:
            if i==2:
                line = [int(x.strip()) for x in linea.split(',')]
                f_weight=np.array(line)
            else:
                line = [int(x.strip()) for x in linea.split(',')]
                f_weight=np.append(f_weight,[line],axis=0)
        i=i+1     
    return f_size,f_weight
"""
    re-ordena de forma random la posicion del array inicial, para sacar la primera solucion
    @param arg :  [n] tamaño del array
    @return :  [seed] index representativo de la posicion de los items en el array
"""
def encontrar_seed(n):
    seed=[x for x in range(n)] 
    np.random.shuffle(seed)
    return seed
"""
    Asigna el valor pertinente a la posicion del seed
    @param arg :  [seed] array con los index de posicion,[l] array inicial
    @return :  [[l[x] for x in seed]] funcion que crea un array insertando los valores correspondientes de l usando las posiciones de seed
"""    
def valor_solucion(seed,l):
    return [l[x] for x in seed]

"""
    Funcion main
"""

if __name__ == '__main__':
    n = 5
    l = [4,5,2,3,6]
    # pos_a = 2
    # pos_b = 5
    total = calcular_distancia(2,5,l)

    print(total)
