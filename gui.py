from tkinter import *
from tkinter import ttk
from tkinter.ttk import Progressbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from rectangulo import Rectangulo
from gastrippackingrotacion import run
from utils import dibujar_solucion


def set_up_main():
    # Titulo
    pantalla.title('SPP - Algoritmos Genéticos')

    # Ícono
    pantalla.iconphoto(False, PhotoImage(file="icon.png"))

    # Color de fondo
    pantalla.configure(bg=bgcolor)

    # Dimensiones de la pantalla
    w = 350
    h = 385
    ws = pantalla.winfo_screenwidth()
    hs = pantalla.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    pantalla.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # No permitir que se redimensione
    pantalla.resizable(0, 0)


def set_up_resultado(resultado):
    resultado.iconphoto(False, PhotoImage(file="icon.png"))

    resultado.configure(bg=bgcolor)

    resultado.state('zoomed')
    resultado.resizable(0, 0)


def get_info_instancia(file):
    # Obtengo los colores para representar a los rectangulos
    def get_colores():
        a = open('colores.txt', 'r')
        c = [x for x in a.read().split()]
        a.close()
        return c

    # Leo el archivo file y obtengo W y los rectangulos
    archivo = open(file, 'r')
    contenido = [int(x) for x in archivo.read().split()]
    ancho = contenido[0]
    r = []
    colores = get_colores()
    index_colores = 0
    for j in range(1, len(contenido)):
        if j % 2 != 0:
            r.append(Rectangulo(contenido[j], contenido[j + 1], colores[index_colores]))
            index_colores += 1
    archivo.close()
    return r, ancho


def ejecutar():
    progressLabel.grid(row=10, column=0)
    progress.grid(row=10, column=1)
    rectangulos, w = get_info_instancia('instancias/' + combo.get() + '.txt')
    historial_mejores_fitness = []
    historial_mejores_soluciones = []
    for i in range(iteraciones.get()):
        mejor_fitness, mejor_solucion = run(rectangulos, w, rotar.get(), tamano_poblacion.get(), pm.get(), pc.get(),
                                            generaciones.get())
        historial_mejores_fitness.append(mejor_fitness)
        historial_mejores_soluciones.append(mejor_solucion)
        progress['value'] = (i + 1) / iteraciones.get() * 100
        pantalla.update_idletasks()

    mejor_fitness = min(historial_mejores_fitness)
    mejor_solucion = historial_mejores_soluciones[historial_mejores_fitness.index(mejor_fitness)]

    peor_fitness = max(historial_mejores_fitness)
    peor_solucion = historial_mejores_soluciones[historial_mejores_fitness.index(peor_fitness)]

    promedio_fitness = sum(historial_mejores_fitness) / len(historial_mejores_fitness)

    progress['value'] = 0

    resultado = Toplevel()
    resultado.grab_set()
    set_up_resultado(resultado)

    Label(resultado, text='Promedio fitness: ' + str(promedio_fitness), bg=bgcolor, fg=fontcolor, font=titulos).pack(
        pady=20)

    mejor_grafico = FigureCanvasTkAgg(
        dibujar_solucion(mejor_solucion, 'Mejor solucion', rectangulos, w, bgcolor, fontcolor),
        resultado)
    mejor_grafico.draw()
    mejor_grafico.get_tk_widget().pack(side=LEFT)

    peor_grafico = FigureCanvasTkAgg(
        dibujar_solucion(peor_solucion, 'Peor solucion', rectangulos, w, bgcolor, fontcolor),
        resultado)
    peor_grafico.draw()
    peor_grafico.get_tk_widget().pack(side=RIGHT)

    resultado.mainloop()


# Guia de colores y fuentes
bgcolor = '#2C2F33'
buttoncolor = '#7289DA'
fontcolor = '#FFFFFF'
titulos = ('Helvetica', 12)
labels = ('Helvetica', 10)

# Puesta a punto de la pantalla
pantalla = Tk()
set_up_main()

# Variables
combo = ttk.Combobox(pantalla, state='readonly')
rotar = BooleanVar()
pm = DoubleVar()
pc = DoubleVar()
generaciones = IntVar()
tamano_poblacion = IntVar()
iteraciones = IntVar()
progress = Progressbar(pantalla, orient=HORIZONTAL, length=100, mode='determinate')

# Setear valores por defecto
pm.set(0.1)
pc.set(0.65)
generaciones.set(5000)
tamano_poblacion.set(50)
iteraciones.set(10)
progress['value'] = 0

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

progressLabel = Label(pantalla, text='Progreso', bg=bgcolor, fg=fontcolor, font=labels)

Button(pantalla, text="Ejecutar", width=35,
       background=buttoncolor, fg=fontcolor, font=labels, command=ejecutar).grid(pady=30, padx=30, row=9, column=0,
                                                                                 columnspan=2, sticky=S + N + E + W)

pantalla.mainloop()
