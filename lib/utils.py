import matplotlib.pyplot as plt
from lib.rectangulo import Rectangulo
from lib.strip_pack import calcular_niveles


# Función para graficar un individuo
def dibujar_solucion(individuo, titulo, rectangulos, W, bgcolor, textcolor):
    # Función para obtener las coordenadas absolutas del rectangulo
    def get_coordenadas(ancho, alto, x_inicial, y_inicial):
        x_r = [x_inicial, x_inicial + ancho, x_inicial + ancho, x_inicial, x_inicial]
        y_r = [y_inicial, y_inicial, y_inicial + alto, y_inicial + alto, y_inicial]
        return x_r, y_r

    # Obtengo la información sobre la ubicación de los rectángulos
    niveles, altura = calcular_niveles(individuo, rectangulos, W)

    # Lleva el índice del rectángulo a graficar
    nro_individuo = 0

    # Lleva el índice del punto del eje x en el que está ubicado el lapiz
    x = 0

    # Lleva el índice del punto del eje y en el que está ubicado el lapiz
    y = 0

    # Seteo el gráfico
    fig = plt.figure(figsize=(6, 6), dpi=100)
    fig.patch.set_facecolor(bgcolor)
    axis = fig.gca()

    # Mantener proporciones de eje x e y
    axis.set_aspect('equal', 'box')

    # Cambiar color de los ejes
    axis.spines['right'].set_color(textcolor)
    axis.spines['left'].set_color(textcolor)
    axis.spines['bottom'].set_color(textcolor)
    axis.spines['top'].set_color(textcolor)
    axis.xaxis.label.set_color(textcolor)
    axis.yaxis.label.set_color(textcolor)
    axis.tick_params(axis='x', colors=textcolor)
    axis.tick_params(axis='y', colors=textcolor)

    # Setear los labels de los ejes
    plt.xlabel('Ancho', color=textcolor)
    plt.ylabel('Alto', color=textcolor)

    # Definir los límites de los ejes
    plt.xlim(0, W)
    plt.ylim(0, 35)

    # Darle un titulo al gráfico
    plt.title(titulo, color=textcolor)

    # Dibujo los rectángulos según el nivel al que pertenecen
    for nivel in niveles:
        for _ in nivel:
            # Obtengo el rectangulo
            rectagulo = rectangulos[individuo[nro_individuo][0]]

            # Seteo el ancho y el alto según si tiene la rotación activada o no
            w = rectagulo.w if not individuo[nro_individuo][1] else rectagulo.h
            h = rectagulo.h if not individuo[nro_individuo][1] else rectagulo.w

            # Obtengo las coordenadas absolutas del rectángulo
            coordenadas_x, coordenadas_y = get_coordenadas(w, h, x, y)

            # Dibujo el rectángulo
            axis.fill(coordenadas_x, coordenadas_y, facecolor=rectagulo.color, edgecolor="#000000")

            # Actualizo el índice del número de individuo
            nro_individuo += 1

            # Actualizo el punto del eje x en donde se va a graficar el siguiente rectángulo
            x += w

        # Ubico el indicador en el punto 0 del eje x
        x = 0

        # Ubico el indicador y en el punto maximo que se ha dibujado en el eje y
        y += max(nivel)

    # Retorno el gráfico
    return fig


# Funcion para obtener W y los rectangulos desde un archivo de texto
def get_info_instancia(file):
    # Obtengo los colores para representar a los rectangulos
    def get_colores():
        a = open('resources/colores.txt', 'r')
        c = [x for x in a.read().split()]
        a.close()
        return c

    # Abro el archivo
    archivo = open(file, 'r')

    # Guardo la información del archivo en una lista
    contenido = [int(x) for x in archivo.read().split()]

    # Obtengo el ancho máximo
    ancho = contenido[0]

    # Obtengo los rectángulos
    r = []
    colores = get_colores()
    index_colores = 0
    for j in range(1, len(contenido)):
        if j % 2 != 0:
            r.append(Rectangulo(contenido[j], contenido[j + 1], colores[index_colores]))
            index_colores += 1

    # Cierro el archivo
    archivo.close()

    # Retorno los rectángulos y el ancho máximo
    return r, ancho
