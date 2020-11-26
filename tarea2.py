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



def leer_archivo(nombre):
    """
    Lee el archivo y retorna 1 array y 1 matriz , el array contiene el largo de cada puesto, y la matriz contiene cuantas personas pasaron entre 
    puestos
    @param nombre : nombre del archivo que con tiene los datos a parsear 
    @return :  [array],[matrix] suma de la distancia entre origen y destino
    """
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

def adquirir_datos(nombre):
    """
    Es una mosntruosidad pero no sabia como cambiar el otro leer, asi que es asi como funciona ahora
    uso csv y os para sacar los datos y transformarlos.
    """
    f=open(nombre,'r')
    n=int(f.readline(1))
    #n=pd.read_csv(nombre,header=None,nrows=1,engine='python')
    l=pd.read_csv(nombre,header=None,skiprows=1,nrows=1,engine='python')
    l=pd.DataFrame.to_numpy(l)
    l=l[0]
    f_weight=pd.read_csv(nombre,header=None,skiprows=2,engine='python')
    f_weight=pd.DataFrame.to_numpy(f_weight)
    return n,l,f_weight

def funcion_objetivo(n,vsee,f_weight,seed):
    """
    Hace la sumatoria donde se saca el valor de la solucion  
    puestos
    @param [n] tamaño del array, [vsee] valor del seed dependiendo del l, [f_weight] matriz de pesos, [seed] index que representa donde estan posicionados los lugares
    @return :  una funcion que retorna un valor solucion.
    """
    return np.sum([calcular_distancia(x,y,vsee)*f_weight[seed[x]][seed[y]] for x in range(len(l)) for y in range(x+1,len(l))])


def neighborhood(n,f_weight,l,it,k):
    """
    Esta funcion encuentra la solucion minima dentro de k neighbors, los cuales son inicializados por un seed random 
    puestos
    @param [n] tamaño del array, [l] array inicial, [f_weight] matriz de pesos, [it] cantidad de iteraciones, [k] cantidad de neighbors
    @return :  [seed_sol],[best_sol] seed_sol es el index de la mejor solucion encontrada, best_sol es la mejor solucion.
    """
    best_sol=1000000
    seed_sol= np.ones(n)
    for x in range(k):
        seed=encontrar_seed(n)
        [seed_local,best_sol_local]=local_search(seed,it,n,l,f_weight)
        if best_sol > best_sol_local:
            best_sol = best_sol_local
            seed_sol=seed_local
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

def local_search(seed,it,n,l,f_weight):
    """
    Hace un search iterativo random dentro del espacio de busqueda, los movimientos son swap de items dentro del array
    y se encarga de encontrar la solucion minima local.
    @param [n] tamaño del array, [l] array inicial, [f_weight] matriz de pesos, [it] cantidad de iteraciones, [seed] index de la solucion
    @return :  [seed_sol],[sol_local] seed_sol es el index de la mejor solucion encontrada, sol_local es la mejor solucion local.
    """
    sol_local=1000000 
    seed_sol=seed
    for x in range(it):
        sol=funcion_objetivo(n,valor_seed(seed,l),f_weight,seed)  
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
    it=10
    k=5
    nombre='S8.txt'
    #----------------------------------------------------------------------------
    [n,l,f_weight]=adquirir_datos(nombre)
    [seed,vsol]=neighborhood(n,f_weight,l,it,k)
    print("\nMejor resultado\n")
    print("Index solución: ",seed)
    print("Valor solución: ",vsol)

