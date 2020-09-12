import random
import numpy as np
import time
import matplotlib.pyplot as plt


# Clase que representa a los rectangulos
class Rectangulo:
    def __init__(self, w=-1, h=-1):
        if w == -1 and h == -1:
            # Al ancho le asigno un random entero entre 10 y 50
            self.w = random.randint(10, 50)

            # A la altura le asigno un random entero entre 10 y 75
            self.h = random.randint(10, 75)

        else:
            # Al ancho le asigno un random entero entre 10 y 50
            self.w = w

            # A la altura le asigno un random entero entre 10 y 75
            self.h = h

        # Le asigno un color
        def r():
            return random.randint(0, 255)

        self.color = ('#%02X%02X%02X' % (r(), r(), r()))


def crear_poblacion_inicial(tamano_poblacion, tamano_permutacion):
    # Crea la poblacion tomando permutaciones de randoms
    return [list(np.random.permutation(range(tamano_permutacion))) for _ in range(tamano_poblacion)]


def generar_rectangulos(cantidad):
    # Genero la cantidad de rectangulos pasados por parámetro
    return [Rectangulo() for _ in range(cantidad)]


def calcular_niveles(individuo, rectangulos, W):
    # Variables a utilizar para calcular la altura del individuo
    niveles = []
    nivel_actual = []
    ancho_nivel_actual = 0

    # Acomodo los rectangulos en niveles
    for i in individuo:
        # Si el rectángulo cabe en el nivel actual lo agrego
        if ancho_nivel_actual + rectangulos[int(i)].w <= W:
            nivel_actual.append(rectangulos[int(i)].h)
            ancho_nivel_actual += rectangulos[int(i)].w
        # Guardo el nivel anterior  y creo uno nuevo con el nuevo rectángulo
        else:
            niveles.append(nivel_actual)
            nivel_actual = [rectangulos[int(i)].h]
            ancho_nivel_actual = rectangulos[int(i)].w

    # Agrego el ultimo nivel
    niveles.append(nivel_actual)
    # Sumo las alturas máximas de los niveles
    altura = sum([max(h) for h in niveles])

    return niveles, altura


def altura_individuo(individuo, rectangulos, W):
    _, altura = calcular_niveles(individuo, rectangulos, W)
    return altura


def calcular_fitness(poblacion, rectangulos, W):
    # Calculo las alturas de toda la poblacion
    return list(map(lambda x: altura_individuo(x, rectangulos, W), poblacion))


def seleccionar_individuo_por_competicion(poblacion, fitness, tamano_poblacion):
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


def crossover(padre_1, padre_2):
    # Realizo el pmx para crear los nuevos individuos
    hijo_1 = pmx(list(padre_1), list(padre_2))
    hijo_2 = pmx(list(padre_2), list(padre_1))

    return hijo_1, hijo_2


def pmx(padre_1, padre_2):
    tamano_cromosoma = len(padre_1)

    # Calculo los puntos de corte
    primer_punto = random.randint(1, tamano_cromosoma - 2)
    segundo_punto = random.randint(primer_punto + 1, tamano_cromosoma - 1)

    # Obtengo la lista entre los puntos de corte del padre_1
    lista_intermedia_1 = padre_1[primer_punto:segundo_punto]
    # Obtengo la lista entre los puntos de corte del padre_2
    lista_intermedia_2 = padre_2[primer_punto:segundo_punto]

    # Paso los elementos intermedios del padre_1 al hijo y el resto de los elementos los pongo en -1
    hijo = [-1] * primer_punto + lista_intermedia_1 + [-1] * (tamano_cromosoma - segundo_punto)

    # Guardo los mapeos
    mapeo = []
    for i in range(segundo_punto - primer_punto):
        if lista_intermedia_2[i] not in hijo:
            mapeo.append((lista_intermedia_2[i], lista_intermedia_1[i]))

    # Relleno el hijo con los mapeos
    for x in mapeo:
        m1 = x[0]
        m2 = x[1]
        while hijo[padre_2.index(m2)] != -1:
            m2 = hijo[padre_2.index(m2)]
        hijo[padre_2.index(m2)] = m1

    # Relleno los elementos del hijo que todavía están en -1
    for i in range(tamano_cromosoma):
        if hijo[i] == -1:
            hijo[i] = padre_2[i]

    return np.array(hijo)


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

    return x


def mutar_poblacion_aleatoriamente(poblacion, pm):
    # Aplico mutación aleatoria
    return list(map(lambda x: x if random.uniform(0, 1) > pm else mutar_individuo(x), poblacion))


def getCoordenadas(ancho, alto, x_inicial, y_inicial):
    x = [x_inicial, x_inicial + ancho, x_inicial + ancho, x_inicial, x_inicial]
    y = [y_inicial, y_inicial, y_inicial + alto, y_inicial + alto, y_inicial]
    return x, y


def dibujar_solucion(individuo, rectangulos, W, titulo):
    niveles, altura = calcular_niveles(individuo, rectangulos, W)
    nro_individuo = 0
    x = 0
    y = 0
    fig = plt.figure(1, figsize=(5, 5), dpi=90)
    grafico = fig.add_subplot()
    for nivel in niveles:
        for _ in nivel:
            rectagulo = rectangulos[individuo[nro_individuo]]
            coordenadas_x, coordenadas_y = getCoordenadas(rectagulo.w, rectagulo.h, x, y)
            grafico.plot(coordenadas_x, coordenadas_y, color=rectagulo.color)
            nro_individuo += 1
            x += rectagulo.w
        x = 0
        y += max(nivel)
    plt.xlabel('Ancho')
    plt.ylabel('Alto')
    plt.xlim(0, W)
    plt.ylim(0, altura + 1)
    plt.title(titulo)
    plt.show()


random.seed(int(round(time.time() * 1000)))

# Descomentar para que genere rectangulos aleatorios
cantidad_rectangulos = 20
rectangulos = generar_rectangulos(cantidad_rectangulos)

# Descomentar para que genere 10 rectangulos fijos
# cantidad_rectangulos = 10
# rectangulos = [Rectangulo(57, 28), Rectangulo(39, 31), Rectangulo(66, 28), Rectangulo(52, 11), Rectangulo(60, 26),
#                Rectangulo(13, 26), Rectangulo(13, 21), Rectangulo(72, 36), Rectangulo(27, 18), Rectangulo(43, 48)]

# Descomentar para que genere 20 rectangulos fijos
# cantidad_rectangulos = 20
# rectangulos = [Rectangulo(57, 28), Rectangulo(39, 31), Rectangulo(66, 28), Rectangulo(52, 11), Rectangulo(60, 26),
#                Rectangulo(13, 26), Rectangulo(13, 21), Rectangulo(72, 36), Rectangulo(27, 18), Rectangulo(43, 48),
#                Rectangulo(57, 28), Rectangulo(39, 31), Rectangulo(66, 28), Rectangulo(52, 11), Rectangulo(60, 26),
#                Rectangulo(13, 26), Rectangulo(13, 21), Rectangulo(72, 36), Rectangulo(27, 18), Rectangulo(43, 48)]

# Ajusto parámetros
W = 100
tamano_poblacion = 50
max_generaciones = 10000
pm = 0.1
pc = 0.65
historial_mejores_fitness = []

# Crear la población inicial
poblacion = crear_poblacion_inicial(tamano_poblacion, cantidad_rectangulos)

# Calcular fitness de la población inicial
fitness = calcular_fitness(poblacion, rectangulos, W)

# Calculo el mejor fitness de la población inicial
mejor_fitness = min(fitness)
mejor_solucion_inicial = poblacion[fitness.index(min(fitness))]
print('Mejor fitness inicial: ', mejor_fitness, ', Individuo: ', mejor_solucion_inicial)
dibujar_solucion(mejor_solucion_inicial, rectangulos, W, "Mejor solución inicial")

# Lo agrego al historial
historial_mejores_fitness.append(mejor_fitness)

# Algoritmo genético
for generacion in range(max_generaciones):

    # Creo una lista para almacenar la nueva poblacion
    nueva_poblacion = []

    # Creo la nueva poblacion generando dos hijos a la vez
    for i in range(int(tamano_poblacion / 2)):
        padre_1 = seleccionar_individuo_por_competicion(poblacion, fitness, tamano_poblacion)
        padre_2 = seleccionar_individuo_por_competicion(poblacion, fitness, tamano_poblacion)
        if random.uniform(0, 1) <= pc:
            hijo_1, hijo_2 = crossover(padre_1, padre_2)
        else:
            hijo_1, hijo_2 = padre_1, padre_2
        nueva_poblacion.append(hijo_1)
        nueva_poblacion.append(hijo_2)

    # Reemplazo la vieja población por una nueva
    poblacion = np.array(nueva_poblacion)

    # Aplico la mutación
    poblacion = mutar_poblacion_aleatoriamente(poblacion, pm)

    # Calculo el fitness de la poblacion
    fitness = calcular_fitness(poblacion, rectangulos, W)
    # Calculo el mejor fitness de la población
    mejor_fitness = min(fitness)
    # Lo agrego al historial
    historial_mejores_fitness.append(mejor_fitness)

mejor_solucion = poblacion[fitness.index(min(fitness))]
print('Mejor fitness final: ', mejor_fitness, ', Individuo:', mejor_solucion)
dibujar_solucion(mejor_solucion, rectangulos, W, "Mejor solución")

# Genero un gráfico del progreso
plt.plot(historial_mejores_fitness)
plt.xlabel('Generacion')
plt.ylabel('Mejor fitness (altura)')
plt.show()
