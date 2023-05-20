import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from filtro_butter import IIR_filtter
import time

plt.style.use(['science', 'notebook', 'grid'])

# probar el filtro
def main():
    b = False #True si queres ver los diagramas de Bode

    # Crear señal de prueba
    Fs = 150
    t = np.arange(0, 40, 1 / (Fs))
    step = np.ones(len(t))

    f_max = 15

    # Filtros de distintos ordenes y distintas frecuencias de corte
    filtro_1 = [IIR_filtter(orden=1, fc=i, fs=Fs) for i in range(1, f_max,)]
    filtro_2 = [IIR_filtter(orden=2, fc=i, fs=Fs) for i in range(1, f_max)]
    filtro_3 = [IIR_filtter(orden=3, fc=i, fs=Fs) for i in range(1, f_max)]
    filtro_4 = [IIR_filtter(orden=4, fc=i, fs=Fs) for i in range(1, f_max)]

    # inicializar vectores de salida
    filtered_signal_1 = np.zeros((len(filtro_1), len(t)))
    filtered_signal_2 = np.zeros((len(filtro_2), len(t)))
    filtered_signal_3 = np.zeros((len(filtro_3), len(t)))
    filtered_signal_4 = np.zeros((len(filtro_4), len(t)))

    # filtrado de seniales
    for n in range(len(step)):
        for i in range(len(filtro_1)):
            filtered_signal_1[i][n] = filtro_1[i].filter(step[n])
            filtered_signal_2[i][n] = filtro_2[i].filter(step[n])
            filtered_signal_3[i][n] = filtro_3[i].filter(step[n])
            filtered_signal_4[i][n] = filtro_4[i].filter(step[n])
    
    # Busqueda de tiempo caracteristico (tiempo en el que el riple es menor que el e)
    e = 0.0001    #defino el epsilon del valor 'estable'
    t1, t2, t3, t4 = np.zeros(len(filtro_1)), np.zeros(len(filtro_2)), np.zeros(len(filtro_3)), np.zeros(len(filtro_4))

    # calcular la derivada de las seniales
    num_filas = filtered_signal_1.shape[0]  # Obtener el número de filas en la matriz
    derivada_1 = np.zeros_like(filtered_signal_1) # Crear una matriz vacía del mismo tamaño que filtered_signal_1
    derivada_2 = np.zeros_like(filtered_signal_2)
    derivada_3 = np.zeros_like(filtered_signal_3)
    derivada_4 = np.zeros_like(filtered_signal_4)

    for i in range(num_filas):
        derivada_1[i,:] = np.gradient(filtered_signal_1[i,:], t)
        derivada_2[i,:] = np.gradient(filtered_signal_2[i,:], t)
        derivada_3[i,:] = np.gradient(filtered_signal_3[i,:], t)
        derivada_4[i,:] = np.gradient(filtered_signal_4[i,:], t)
    
    # Buscar el tiempo caracteristico
    for i in range(len(filtro_1)):
        for n in range(len(t)):
            if(abs(filtered_signal_1[i][n] - 1) < e):
                if (abs(derivada_1[i][n]) < e):
                    t1[i] = t[n]
                    break
        for n in range(len(t)):
            if(abs(filtered_signal_2[i][n] - 1) < e):
                if (abs(derivada_2[i][n]) < e):
                    t2[i] = t[n]
                    break
        for n in range(len(t)):
            if(abs(filtered_signal_3[i][n] - 1) < e):
                if (abs(derivada_3[i][n]) < e):
                    t3[i] = t[n]
                    break
        for n in range(len(t)):
            if(abs(filtered_signal_4[i][n] - 1) < e):
                if (abs(derivada_4[i][n]) < e):
                    t4[i] = t[n]
                    break
    
    #imprimir el valor de los tiempos caracteristicos:
    print("t1: ", t1)
    print("t2: ", t2)
    print("t3: ", t3)
    print("t4: ", t4)

    #hacer un grafico en 3D del orden, frecuencia y tiempo caracteristico con matplot
    # Crear una malla 2D para X e Y
    X, Y = np.meshgrid(range(1, f_max), [1, 2, 3, 4])
    # Usar Z para definir la altura de cada punto en la trama
    Z = np.array([t1, t2, t3, t4])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #hace el plot 3D en formato de una superficie continua
    ax.plot_surface(Y, X, Z, cmap='coolwarm')
    ax.set_xlabel('Orden')
    ax.set_ylabel('Frecuencia de corte')
    ax.set_zlabel('Tiempo caracteristico')

    #creamos curvas de nivel para los deferentes ordenes
    plt.figure()
    # print(Z[0][])
    cm = plt.cm.get_cmap('viridis')
    plt.plot(np.arange(1, f_max, 1), Z[0], 'o', color=cm(1/4), label='Orden 1')
    plt.plot(np.arange(1, f_max, 1), Z[0], color=cm(1/4))
    plt.plot(np.arange(1, f_max, 1), Z[1], 'D', color=cm(2/4), label='Orden 2')
    plt.plot(np.arange(1, f_max, 1), Z[1], color=cm(2/4))
    plt.plot(np.arange(1, f_max, 1), Z[2], '^', color=cm(3/4), label='Orden 3')
    plt.plot(np.arange(1, f_max, 1), Z[2], color=cm(3/4))
    plt.plot(np.arange(1, f_max, 1), Z[3], 's', color=cm(4/4), label='Orden 4')
    plt.plot(np.arange(1, f_max, 1), Z[3], color=cm(4/4))

    plt.legend(fontsize = 14)
    plt.xlabel('f. corte [Hz]')
    plt.ylabel('t. carac. [s]')
    plt.savefig('Lock in/caractec filtro.png', dpi=300, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    main()