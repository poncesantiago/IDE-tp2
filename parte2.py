import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
mili = 1000 # Hay que multiplicar por 1e3 la corriente para pasarla a mA


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Cargar los archivos para la simulación en temperatura
archivo_sinRE = './simulaciones/sim3/cirSinRE.txt'
archivo_conRE = './simulaciones/sim3/cirConRE.txt'

datos_sinRE = np.loadtxt(archivo_sinRE, skiprows=1)
datos_conRE = np.loadtxt(archivo_conRE,skiprows=1)

# Seleccionar las columnas correspondientes
IC_sinRE = datos_sinRE[:,1]  # Reemplazar 'IC' por el nombre real de la columna de IC en este archivo
T = datos_sinRE[:,0]          # Reemplazar 'T' por el nombre real de la columna de T
IC_conRE = datos_conRE[:,1]  # Reemplazar 'IC' por el nombre real de la columna de IC en este archivo

# Graficar ambos conjuntos de datos
plt.figure()
plt.plot(T, IC_sinRE*mili, label="IC sin RE")
plt.plot(T, IC_conRE*mili, label="IC con RE")
plt.grid()
plt.ylabel('Corriente $I_C$ [mA]');
plt.xlabel('Temperatura [$\circ$C]');
plt.legend([f'$I_C$ sin $R_E$', '$I_C$ con $R_E$'])
plt.show()




