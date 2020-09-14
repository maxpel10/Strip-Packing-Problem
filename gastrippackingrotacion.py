import random
import numpy as np
import time
import matplotlib.pyplot as plt
from utils import calcular_niveles


def run(rectangulos, W, rotar, tamano_poblacion, pm, pc, max_generaciones):
    def crear_poblacion_inicial():
        # Crea la poblacion tomando permutaciones de randoms
        rotacion = []
        if rotar:
            for j in range(len(rectangulos)):
                rotacion.append(bool(random.getrandbits(1)))
        else:
            rotacion = [False] * len(rectangulos)
        return list(map(lambda x: corregir_rotacion(x) if rotar else x,
                        [list(zip(np.random.permutation(range(len(rectangulos))), rotacion)) for _ in
                         range(tamano_poblacion)]))

    def corregir_rotacion(individuo):
        for j in range(len(individuo)):
            if individuo[j][1] and rectangulos[individuo[j][0]].h > W:
                individuo[j] = (individuo[j][0], False)
        return individuo

    def altura_individuo(individuo):
        _, altura = calcular_niveles(individuo, rectangulos, W)
        return altura

    def calcular_fitness():
        # Calculo las alturas de toda la poblacion
        return list(map(lambda x: altura_individuo(x), poblacion))

    def seleccionar_individuo_por_competicion():
        # Elijo a individuos para que compitan
        peleador_1 = random.randint(0, tamano_poblacion - 1)
        peleador_2 = random.randint(0, tamano_poblacion - 1)

        # Obtengo el fitness de cada uno
        peleador_1_fitness = fitness[peleador_1]
        peleador_2_fitness = fitness[peleador_2]

        # Identifico el peleador con menor fitness
        if peleador_1_fitness <= peleador_2_fitness:
            ganador = peleador_1
        else:
            ganador = peleador_2

        # Retorno el cromosoma del ganador
        return poblacion[ganador]

    def crossover(p1, p2):
        # Tomo la primer componente de cada elemento del padre, es decir, el elemento correspondiente a la permutacion
        p1_permutacion = [j[0] for j in p1]
        p2_permutacion = [j[0] for j in p2]

        # Realizo el pmx sobre las permutaciones
        h1_permutacion = pmx(p1_permutacion, p2_permutacion)
        h2_permutacion = pmx(p2_permutacion, p1_permutacion)

        # Tomo la segunda componente de cada elemento del padre, es decir, el elemento correspondiente a la rotacion
        p1_rotacion = [j[1] for j in p1]
        p2_rotacion = [j[1] for j in p2]

        if rotar:
            # Realizo el crossover correspondiente a la rotación
            h1_rotacion = crossover_rotacion(p1_rotacion, p2_rotacion)
            h2_rotacion = crossover_rotacion(p2_rotacion, p1_rotacion)

            # Armo los nuevos individuos
            h1 = corregir_rotacion(list(zip(h1_permutacion, h1_rotacion)))
            h2 = corregir_rotacion(list(zip(h2_permutacion, h2_rotacion)))
        else:
            # Armo los nuevos individuos
            h1 = corregir_rotacion(list(zip(h1_permutacion, [False] * len(p1))))
            h2 = corregir_rotacion(list(zip(h2_permutacion, [False] * len(p1))))

        return h1, h2

    def pmx(p1, p2):
        tamano_cromosoma = len(p1)

        # Calculo los puntos de corte
        primer_punto = random.randint(1, tamano_cromosoma - 2)
        segundo_punto = random.randint(primer_punto + 1, tamano_cromosoma - 1)

        # Obtengo la lista entre los puntos de corte del p1
        lista_intermedia_1 = p1[primer_punto:segundo_punto]
        # Obtengo la lista entre los puntos de corte del p2
        lista_intermedia_2 = p2[primer_punto:segundo_punto]

        # Paso los elementos intermedios del p1 al hijo y el resto de los elementos los pongo en -1
        hijo = [-1] * primer_punto + lista_intermedia_1 + [-1] * (tamano_cromosoma - segundo_punto)

        # Guardo los mapeos
        mapeo = []
        for j in range(segundo_punto - primer_punto):
            if lista_intermedia_2[j] not in hijo:
                mapeo.append((lista_intermedia_2[j], lista_intermedia_1[j]))

        # Relleno el hijo con los mapeos
        for x in mapeo:
            m1 = x[0]
            m2 = x[1]
            while hijo[p2.index(m2)] != -1:
                m2 = hijo[p2.index(m2)]
            hijo[p2.index(m2)] = m1

        # Relleno los elementos del hijo que todavía están en -1
        for j in range(tamano_cromosoma):
            if hijo[j] == -1:
                hijo[j] = p2[j]

        return hijo

    def crossover_rotacion(p1, p2):
        # Calculo el punto de corte
        punto = random.randint(0, len(p1))
        return p1[0:punto] + p2[punto:]

    def mutar_individuo(x):
        # Elijo aleatoriamente dos puntos
        indice_1 = random.randint(0, len(x) - 1)
        indice_2 = random.randint(0, len(x) - 1)

        # Guardo los genes en ese punto
        gen_1 = x[indice_1]
        gen_2 = x[indice_2]

        # Intercambio genes
        x[indice_1] = gen_2
        x[indice_2] = gen_1

        return corregir_rotacion(x) if rotar else x

    def mutar_poblacion_aleatoriamente():
        # Aplico mutación aleatoria
        return list(map(lambda x: x if random.uniform(0, 1) > pm else mutar_individuo(x), poblacion))

    # Generar una semilla que dependa del tiempo asi produzco
    # independencia en la secuencia de numeros aleatorios utilizados
    random.seed(int(round(time.time() * 1000)))

    historial_mejores_fitness = []
    historial_mejores_individuos = []

    # Crear la población inicial
    poblacion = crear_poblacion_inicial()

    # Calcular fitness de la población inicial
    fitness = calcular_fitness()

    # Calculo el mejor fitness de la población inicial
    mejor_fitness = min(fitness)
    mejor_solucion_inicial = poblacion[fitness.index(mejor_fitness)]

    # Lo agrego al historial
    historial_mejores_fitness.append(mejor_fitness)
    historial_mejores_individuos.append(mejor_solucion_inicial)

    # Algoritmo genético
    for generacion in range(max_generaciones):

        # Creo una lista para almacenar la nueva poblacion
        nueva_poblacion = []

        # Creo la nueva poblacion generando dos hijos a la vez
        for i in range(int(tamano_poblacion / 2)):
            padre_1 = seleccionar_individuo_por_competicion()
            padre_2 = seleccionar_individuo_por_competicion()
            if random.uniform(0, 1) <= pc:
                hijo_1, hijo_2 = crossover(padre_1, padre_2)
            else:
                hijo_1, hijo_2 = padre_1, padre_2
            nueva_poblacion.append(hijo_1)
            nueva_poblacion.append(hijo_2)

        # Reemplazo la vieja población por una nueva
        poblacion = nueva_poblacion

        # Aplico la mutación
        poblacion = mutar_poblacion_aleatoriamente()

        # Calculo el fitness de la poblacion
        fitness = calcular_fitness()

        # Calculo el mejor fitness de la población actual
        mejor_fitness = min(fitness)
        mejor_solucion_inicial = poblacion[fitness.index(mejor_fitness)]

        # Lo agrego al historial
        historial_mejores_fitness.append(mejor_fitness)
        historial_mejores_individuos.append(mejor_solucion_inicial)

    mejor_fitness = min(historial_mejores_fitness)
    mejor_solucion = historial_mejores_individuos[historial_mejores_fitness.index(mejor_fitness)]
    print('Mejor fitness: ', mejor_fitness, ', Individuo:', mejor_solucion)

    return mejor_fitness, mejor_solucion

    # Genero un gráfico del progreso
    plt.plot(historial_mejores_fitness)
    plt.xlabel('Generacion')
    plt.ylabel('Mejor fitness (altura)')
    plt.show()
