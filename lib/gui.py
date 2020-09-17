import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from lib.strip_pack import obtener_resultados
from lib.utils import dibujar_solucion, get_info_instancia


def set_up_principal(pantalla):
    # Titulo
    pantalla.title('SPP - Algoritmos Genéticos')

    # Ícono
    pantalla.iconphoto(False, PhotoImage(file="resources/icon.png"))

    # Color de fondo
    pantalla.configure(bg=bgcolor)

    # Dimensiones de la pantalla
    w = 350
    h = 385

    # Ubicación de la pantalla
    ws = pantalla.winfo_screenwidth()
    hs = pantalla.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    pantalla.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # No permitir que se redimensione
    pantalla.resizable(0, 0)


def pantalla_principal():
    # Puesta a punto de la pantalla
    pantalla = Tk()
    set_up_principal(pantalla)

    # Variables
    combo = ttk.Combobox(pantalla, state='readonly')
    rotar = BooleanVar()
    pm = DoubleVar()
    pc = DoubleVar()
    generaciones = IntVar()
    tamano_poblacion = IntVar()
    iteraciones = IntVar()
    progreso = Progressbar(pantalla, orient=HORIZONTAL, length=100, mode='determinate')

    # Setear valores por defecto
    pm.set(0.05)
    pc.set(0.65)
    generaciones.set(1000)
    tamano_poblacion.set(50)
    iteraciones.set(20)
    rotar.set(True)
    progreso['value'] = 0

    # Widgets de la pantalla
    Label(pantalla, text='Ajustar parámetros', bg=bgcolor, fg=fontcolor, font=titulos).grid(pady=10, padx=10, row=0,
                                                                                            column=0)
    Label(pantalla, text='Instancia', bg=bgcolor, fg=fontcolor, font=labels).grid(row=2, column=0)

    combo['values'] = ['spp9a', 'spp9b', 'spp10', 'spp11', 'spp12', 'spp13']
    combo.set('spp9a')
    combo.grid(row=2, column=1)

    Label(pantalla, text='Pm', bg=bgcolor, fg=fontcolor, font=labels).grid(pady=10, row=3, column=0)
    Label(pantalla, text='Pc', bg=bgcolor, fg=fontcolor, font=labels).grid(row=3, column=1)

    Entry(pantalla, width=5, textvariable=pm).grid(row=4, column=0)
    Entry(pantalla, width=5, textvariable=pc).grid(row=4, column=1)

    Label(pantalla, text='Generaciones', bg=bgcolor, fg=fontcolor, font=labels).grid(row=5, column=0)
    Label(pantalla, text='Tamaño de poblacion', bg=bgcolor, fg=fontcolor, font=labels).grid(pady=10, row=5, column=1)

    Entry(pantalla, width=5, textvariable=generaciones).grid(row=6, column=0)
    Entry(pantalla, width=5, textvariable=tamano_poblacion).grid(row=6, column=1)

    Label(pantalla, text='Iteraciones', bg=bgcolor, fg=fontcolor, font=labels).grid(pady=10, row=7, column=0)
    Entry(pantalla, width=5, textvariable=iteraciones).grid(row=8, column=0)

    Checkbutton(pantalla, text="Rotacion", variable=rotar, bg=bgcolor, fg=fontcolor, selectcolor=bgcolor,
                activebackground=bgcolor, activeforeground=fontcolor, font=labels).grid(row=8, column=1,
                                                                                        sticky=W)

    progreso_label = Label(pantalla, text='Progreso', bg=bgcolor, fg=fontcolor, font=labels)

    Button(pantalla, text="Ejecutar", width=35, background=buttoncolor, fg=fontcolor, font=labels,
           command=lambda: ejecutar(iteraciones.get(), rotar.get(), tamano_poblacion.get(), combo.get(), pm.get(),
                                    pc.get(), generaciones.get(), progreso_label, progreso, pantalla)).grid(pady=30,
                                                                                                            padx=30,
                                                                                                            row=9,
                                                                                                            column=0,
                                                                                                            columnspan=2)
    # Ejecuto la pantalla
    pantalla.mainloop()


def set_up_resultado(pantalla):
    # Ícono
    pantalla.iconphoto(False, PhotoImage(file="resources/icon.png"))

    # Color de fondo
    pantalla.configure(bg=bgcolor)

    # Ubicación de la pantalla
    pantalla.state('zoomed')

    # No permitir que se redimensione
    pantalla.resizable(0, 0)


def pantalla_resultados(mejor_fitness, mejor_solucion, peor_fitness, peor_solucion, media_fitness, mediana_fitness,
                        desviacion_fitness, tiempo_transcurrido, rectangulos, w, rotar, tamano_poblacion, combo, pm, pc,
                        generaciones, iteraciones):
    # Puesta a punto de la pantalla
    pantalla = Toplevel()
    pantalla.grab_set()
    set_up_resultado(pantalla)

    # Widgets de la pantalla

    Label(pantalla, text="Resultados", bg=bgcolor, fg=fontcolor, font=titulo_grande).pack(pady=20, side=TOP)
    Label(pantalla, text="Instancia: " + combo, bg=bgcolor, fg=fontcolor, font=labels).pack(side=TOP)
    Label(pantalla, text="Rotar: " + str(rotar), bg=bgcolor, fg=fontcolor, font=labels).pack(side=TOP)
    Label(pantalla, text="pm: " + str(pm), bg=bgcolor, fg=fontcolor, font=labels).pack(side=TOP)
    Label(pantalla, text="pc: " + str(pc), bg=bgcolor, fg=fontcolor, font=labels).pack(side=TOP)
    Label(pantalla, text="Generaciones: " + str(generaciones), bg=bgcolor, fg=fontcolor, font=labels).pack(side=TOP)
    Label(pantalla, text="Tamaño población: " + str(tamano_poblacion), bg=bgcolor, fg=fontcolor, font=labels).pack(
        side=TOP)
    Label(pantalla, text="Iteraciones: " + str(iteraciones), bg=bgcolor, fg=fontcolor, font=labels).pack(
        side=TOP)

    mejor_grafico = FigureCanvasTkAgg(
        dibujar_solucion(mejor_solucion, 'Mejor solucion (' + str(mejor_fitness) + ')', rectangulos, w, bgcolor,
                         fontcolor, rotar),
        pantalla)
    mejor_grafico.draw()
    mejor_grafico.get_tk_widget().pack(side=LEFT)

    peor_grafico = FigureCanvasTkAgg(
        dibujar_solucion(peor_solucion, 'Peor solucion (' + str(peor_fitness) + ')',
                         rectangulos, w, bgcolor, fontcolor, rotar), pantalla)
    peor_grafico.draw()
    peor_grafico.get_tk_widget().pack(side=RIGHT)

    Label(pantalla, bg=bgcolor, fg=fontcolor, font=labels).pack(pady=20, side=BOTTOM)
    Label(pantalla, text='Desviación: ' + str(round(desviacion_fitness, 2)), bg=bgcolor, fg=fontcolor,
          font=labels).pack(side=BOTTOM)
    Label(pantalla, text='Mediana: ' + str(mediana_fitness), bg=bgcolor, fg=fontcolor, font=labels).pack(side=BOTTOM)
    Label(pantalla, text='Valor medio: ' + str(round(media_fitness, 2)), bg=bgcolor, fg=fontcolor, font=labels).pack(
        side=BOTTOM)

    Label(pantalla, text='Tiempo transcurrido: ' + str(round(tiempo_transcurrido, 2)) + ' seg', bg=bgcolor,
          fg=fontcolor, font=labels).pack(side=BOTTOM)

    # Ejecutar pantalla
    pantalla.mainloop()


def ejecutar(iteraciones, rotar, tamano_poblacion, combo, pm, pc, generaciones, progreso_label, progreso, pantalla):
    # Hago aparecer la barra de progreso
    progreso_label.grid(row=10, column=0)
    progreso.grid(row=10, column=1)

    # Obtengo los rectángulos de la instancia a ejecutar
    rectangulos, w = get_info_instancia('resources/spp_instances/' + combo + '.txt')

    # Guardo el tiempo actual
    t0 = time.clock()

    # Obtengo los resultados de la ejecucion
    mejor_fitness, mejor_solucion, peor_fitness, peor_solucion, media_fitness, mediana_fitness, desviacion_fitness, = obtener_resultados(
        rectangulos, w,
        iteraciones,
        rotar,
        tamano_poblacion,
        pm, pc,
        generaciones,
        progreso,
        pantalla)

    # Guardo el tiempo transcurrido
    t1 = time.clock() - t0

    # Reseteo la barra de progreso
    progreso['value'] = 0

    # Muestro los resultados
    pantalla_resultados(mejor_fitness, mejor_solucion, peor_fitness, peor_solucion, media_fitness, mediana_fitness,
                        desviacion_fitness, t1, rectangulos, w, rotar, tamano_poblacion, combo, pm, pc, generaciones,
                        iteraciones)


# Guia de colores y fuentes
bgcolor = '#2C2F33'
buttoncolor = '#7289DA'
fontcolor = '#FFFFFF'
titulo_grande = ('Helvetica', 20)
titulos = ('Helvetica', 12)
labels = ('Helvetica', 10)
