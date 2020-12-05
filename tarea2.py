import numpy as np
import random as rd
import pandas as pd
import os.path
from os import path


def sumatoria(lens):
    """
    Calcula la suma de los puestos que se encuentran 
    entre los puestos de origen y destino
    @param arg :  [lens] largos de cada puesto entre origen y destino
    @return :  [number] suma de los largos de cada puesto entre origen y destino
    """
    total = 0

    #print("a sumar (len):",lens)

    for i in lens:
        total = total + i

    #print("sumat:",total)
    return total

def calcular_distancia(pos_a, pos_b, lens):
    """
    Calcula la distancia entre el puesto de origen y destino
    @param arg :  [pos_a] posicion de origen; [pos_b] posicion de destino; [lens] largos de cada puesto entre origen y destino
    @return :  [number] suma de la distancia entre origen y destino
    """
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

def adquirir_datos(nombre):
    """
    Funcion de lectura, usa la funcion normal de open() y la libreria de pandas usando csv para sacar 
    los vectores y matrices, los cuales los deja en el formato adecuado apra ser usados en el resto del algoritmo.
    @param arg :  [nombre] nombre del archivo de entrada
    @return :  [n] cantidad de tiendas, [l] array que contiene cuanto mide cada tienda, [f_weight] matriz de pesos que representa cuantas personas pasan de la tienda x a la y
    """
    f=open(nombre,'r')
    n=int(f.readline())
    #n=pd.read_csv(nombre,header=None,nrows=1,engine='python')
    l=pd.read_csv(nombre,header=None,skiprows=1,nrows=1,engine='python')
    l=pd.DataFrame.to_numpy(l)
    l=l[0]
    f_weight=pd.read_csv(nombre,header=None,skiprows=2,engine='python')
    f_weight=pd.DataFrame.to_numpy(f_weight)
    f.close()
    return n,l,f_weight

def funcion_objetivo(n,vsee,f_weight,seed):
    """
    Hace la sumatoria donde se saca el valor de la solucion  
    puestos
    @param [n] tamaño del array, [vsee] valor del seed dependiendo del l, [f_weight] matriz de pesos, [seed] index que representa donde estan posicionados los lugares
    @return :  una funcion que retorna un valor solucion.
    """
    return np.sum([calcular_distancia(x,y,vsee)*f_weight[seed[x]][seed[y]] for x in range(len(l)) for y in range(x+1,len(l))])


def neighborhood(n,f_weight,l,it,k,resultados):
    """
    Esta funcion encuentra la solucion minima dentro de k neighbors, los cuales son inicializados por un seed random 
    puestos
    @param [n] tamaño del array, [l] array inicial, [f_weight] matriz de pesos, [it] cantidad de iteraciones, [k] cantidad de neighbors,[resultados] archivo de escritura
    @return :  [seed_sol],[best_sol] seed_sol es el index de la mejor solucion encontrada, best_sol es la mejor solucion.
    """
    print("Elementos: ", n)
    resultados.write("Elementos: ")
    resultados.write(str(n))
    resultados.write("\n")
    print("Vecindarios: ", k)
    resultados.write("Vecindarios: ")
    resultados.write(str(k))
    resultados.write("\n")
    print("Iteraciones: ", it)
    resultados.write("Iteraciones: ")
    resultados.write(str(it))
    resultados.write("\n\n")
    print()

    best_sol=1000000
    seed_sol= np.ones(n)

    for x in range(k):
        print("VECINDARIO ", x+1)
        resultados.write("VECINDARIO ")
        resultados.write(str(x+1))
        resultados.write("\n")
        seed=encontrar_seed(n)
        print("Seed: ",seed)
        resultados.write("Seed: ")
        resultados.write(str(seed))
        resultados.write("\n")

        print("Realizando busqueda local...")
        resultados.write("Realizando busqueda local...\n")

        [seed_local,best_sol_local]=local_search(seed,it,n,l,f_weight,resultados)

        print("Seed local: ",seed_local)
        resultados.write("Seed local: ")
        resultados.write(str(seed_local))
        resultados.write("\n")
        print("Solucion local: ",best_sol_local)
        resultados.write("Solucion local: ")
        resultados.write(str(best_sol_local))
        resultados.write("\n")

        if best_sol > best_sol_local:
            best_sol = best_sol_local
            seed_sol=seed_local
        print()
        resultados.write("\n")
    return seed_sol,best_sol


def stochastic_iteration(n,seed):
    """
    Hace un swap de dos items del array
    @param [n] tamaño del array, [seed] index de la solucion
    @return :  [seed] index modificado
    """
    x=rd.randint(0,n-1)
    y=rd.randint(0,n-1)
    while y == x:
        y=rd.randint(0,n-1)
    seed[x],seed[y]=seed[y],seed[x]
    return seed

def local_search(seed,it,n,l,f_weight,resultados):
    """
    Hace un search iterativo random dentro del espacio de busqueda, los movimientos son swap de items dentro del array
    y se encarga de encontrar la solucion minima local.
    @param [n] tamaño del array, [l] array inicial, [f_weight] matriz de pesos, [it] cantidad de iteraciones, [seed] index de la solucion, [resultados] archivo de escritura
    @return :  [seed_sol],[sol_local] seed_sol es el index de la mejor solucion encontrada, sol_local es la mejor solucion local.
    """
    sol_local=1000000 
    seed_sol=seed
    for x in range(it):
        print("Iteracion ", x+1)
        resultados.write("Iteracion ")
        resultados.write(str(x+1))
        resultados.write("\n")
        
        sol=funcion_objetivo(n,valor_seed(seed,l),f_weight,seed)

        print("(Seed) solucion local: ", sol_local)
        resultados.write("(Seed) solucion local: ")
        resultados.write(str(sol_local))
        resultados.write("\n")
        print("(Seed) solucion encontrada: ", sol)
        resultados.write("(Seed) solucion encontrada: ")
        resultados.write(str(sol))
        resultados.write("\n")

        if sol_local > sol:
            sol_local=sol
            seed_sol=seed
        seed=stochastic_iteration(n,seed)
    return seed_sol,sol_local  

def encontrar_seed(n):
    """
    re-ordena de forma random la posicion del array inicial, para sacar la primera solucion
    @param arg :  [n] tamaño del array
    @return :  [seed] index representativo de la posicion de los items en el array
    """
    seed=[x for x in range(n)] 
    np.random.shuffle(seed)
    return seed

def valor_seed(seed,l):
    """
    Asigna el valor pertinente a la posicion del seed
    @param arg :  [seed] array con los index de posicion,[l] array inicial
    @return :  [[l[x] for x in seed]] funcion que crea un array insertando los valores correspondientes de l usando las posiciones de seed
    """    
    return [l[x] for x in seed]



if __name__ == '__main__':
    """
    Funcion main
    """

    #config---------------------------------------------------------------------
    it=50
    k=20
    nombre='QAP_sko56_04_n'
    #nombre='test123.txt'
    #----------------------------------------------------------------------------
    resultados=open("resultados.txt","w")

    [n,l,f_weight]=adquirir_datos(nombre)
    [seed,vsol]=neighborhood(n,f_weight,l,it,k,resultados)
    
    print("Mejor resultado\n")
    resultados.write("Mejor resultado\n\n")
    print("Index solución: ",seed)
    resultados.write("Index solución: ")
    resultados.write(str(seed))
    resultados.write("\n")
    print("Valor solución: ",vsol)
    resultados.write("Valor solución: ")
    resultados.write(str(vsol))
    resultados.write("\n")

    resultados.close()

