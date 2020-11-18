import numpy as np

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
    Funcion main
"""
if __name__ == '__main__':
    n = 5
    l = [4,5,2,3,6]
    # pos_a = 2
    # pos_b = 5

    total = calcular_distancia(2,5,l)

    print(total)