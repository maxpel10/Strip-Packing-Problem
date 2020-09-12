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


def crear_poblacion_inicial(tamano_permutacion):
    # Crea la poblacion tomando permutaciones de randoms
    return [list(np.random.permutation(range(tamano_permutacion))) for _ in range(tamano_poblacion)]


def generar_rectangulos(cantidad):
    # Genero la cantidad de rectangulos pasados por parámetro
    return [Rectangulo() for _ in range(cantidad)]


def calcular_niveles(individuo):
    # Variables a utilizar para calcular la altura del individuo
    niveles = []
    nivel_actual = []
    ancho_nivel_actual = 0

    # Acomodo los rectangulos en niveles
    for j in individuo:
        # Si el rectángulo cabe en el nivel actual lo agrego
        if ancho_nivel_actual + rectangulos[int(j)].w <= W:
            nivel_actual.append(rectangulos[int(j)].h)
            ancho_nivel_actual += rectangulos[int(j)].w
        # Guardo el nivel anterior  y creo uno nuevo con el nuevo rectángulo
        else:
            niveles.append(nivel_actual)
            nivel_actual = [rectangulos[int(j)].h]
            ancho_nivel_actual = rectangulos[int(j)].w

    # Agrego el ultimo nivel
    niveles.append(nivel_actual)
    # Sumo las alturas máximas de los niveles
    altura = sum([max(h) for h in niveles])

    return niveles, altura


def altura_individuo(individuo):
    _, altura = calcular_niveles(individuo)
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
    # Realizo el pmx para crear los nuevos individuos
    h1 = pmx(list(p1), list(p2))
    h2 = pmx(list(p2), list(p1))

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


def mutar_poblacion_aleatoriamente():
    # Aplico mutación aleatoria
    return list(map(lambda x: x if random.uniform(0, 1) > pm else mutar_individuo(x), poblacion))


def get_coordenadas(ancho, alto, x_inicial, y_inicial):
    x = [x_inicial, x_inicial + ancho, x_inicial + ancho, x_inicial, x_inicial]
    y = [y_inicial, y_inicial, y_inicial + alto, y_inicial + alto, y_inicial]
    return x, y


def dibujar_solucion(individuo, titulo):
    niveles, altura = calcular_niveles(individuo)
    nro_individuo = 0
    x = 0
    y = 0
    fig = plt.figure(1, figsize=(5, 5), dpi=90)
    grafico = fig.add_subplot()
    for nivel in niveles:
        for _ in nivel:
            rectagulo = rectangulos[individuo[nro_individuo]]
            coordenadas_x, coordenadas_y = get_coordenadas(rectagulo.w, rectagulo.h, x, y)
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
poblacion = crear_poblacion_inicial(cantidad_rectangulos)

# Calcular fitness de la población inicial
fitness = calcular_fitness()

# Calculo el mejor fitness de la población inicial
mejor_fitness = min(fitness)
mejor_solucion_inicial = poblacion[fitness.index(min(fitness))]
print('Mejor fitness inicial: ', mejor_fitness, ', Individuo: ', mejor_solucion_inicial)
dibujar_solucion(mejor_solucion_inicial, "Mejor solución inicial")

# Lo agrego al historial
historial_mejores_fitness.append(mejor_fitness)

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
    poblacion = np.array(nueva_poblacion)

    # Aplico la mutación
    poblacion = mutar_poblacion_aleatoriamente()

    # Calculo el fitness de la poblacion
    fitness = calcular_fitness()
    # Calculo el mejor fitness de la población
    mejor_fitness = min(fitness)
    # Lo agrego al historial
    historial_mejores_fitness.append(mejor_fitness)

mejor_solucion = poblacion[fitness.index(min(fitness))]
print('Mejor fitness final: ', mejor_fitness, ', Individuo:', list(mejor_solucion))
dibujar_solucion(mejor_solucion, "Mejor solución")

# Genero un gráfico del progreso
plt.plot(historial_mejores_fitness)
plt.xlabel('Generacion')
plt.ylabel('Mejor fitness (altura)')
plt.show()
