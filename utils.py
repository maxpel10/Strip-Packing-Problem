import matplotlib
import matplotlib.pyplot as plt


def calcular_niveles(individuo, rectangulos, W):
    # Variables a utilizar para calcular la altura del individuo
    niveles = []
    nivel_actual = []
    ancho_nivel_actual = 0

    # Acomodo los rectangulos en niveles
    for j in individuo:
        w_j = rectangulos[int(j[0])].w if not j[1] else rectangulos[int(j[0])].h
        h_j = rectangulos[int(j[0])].h if not j[1] else rectangulos[int(j[0])].w
        # Si el rectángulo cabe en el nivel actual lo agrego
        if ancho_nivel_actual + w_j <= W:
            nivel_actual.append(h_j)
            ancho_nivel_actual += w_j
        # Guardo el nivel anterior  y creo uno nuevo con el nuevo rectángulo
        else:
            niveles.append(nivel_actual)
            nivel_actual = [h_j]
            ancho_nivel_actual = w_j

    # Agrego el ultimo nivel
    niveles.append(nivel_actual)
    # Sumo las alturas máximas de los niveles
    altura = sum([max(h) for h in niveles])

    return niveles, altura


def get_coordenadas(ancho, alto, x_inicial, y_inicial):
    x = [x_inicial, x_inicial + ancho, x_inicial + ancho, x_inicial, x_inicial]
    y = [y_inicial, y_inicial, y_inicial + alto, y_inicial + alto, y_inicial]
    return x, y


def dibujar_solucion(individuo, titulo, rectangulos, W, bgcolor, textcolor):
    niveles, altura = calcular_niveles(individuo, rectangulos, W)
    nro_individuo = 0
    x = 0
    y = 0
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

    for nivel in niveles:
        for _ in nivel:
            rectagulo = rectangulos[individuo[nro_individuo][0]]
            w = rectagulo.w if not individuo[nro_individuo][1] else rectagulo.h
            h = rectagulo.h if not individuo[nro_individuo][1] else rectagulo.w
            coordenadas_x, coordenadas_y = get_coordenadas(w, h, x, y)
            axis.fill(coordenadas_x, coordenadas_y, facecolor=rectagulo.color, edgecolor="#000000")
            nro_individuo += 1
            x += w
        x = 0
        y += max(nivel)

    plt.xlabel('Ancho', color=textcolor)
    plt.ylabel('Alto', color=textcolor)
    plt.xlim(0, W)
    plt.ylim(0, 35)
    plt.title(titulo + ' (' + str(altura) + ')', color=textcolor)

    return fig
