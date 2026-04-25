import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#%%%%%%%%%% Constantes
k = 1.3806e-23 # [J/K] Constante del Boltzmann
q = 1.60223e-19 # [C] Carga del electrón
T = 300 # [K] Temperatura de trabajo
Vth = k*T/q # [V] Tensión térmica


#%%%%%%%%%%  Lectura del archivo
archivo_transferencia = "./simulaciones/sim1/ICandIBvsVBE.txt"

# Lectura del archivo salteando la primera fila ya que esa tiene los nombres de las columnas
data=np.loadtxt(archivo_transferencia, skiprows=1)

## Asignación de datos
VBE = data[:,0]; # Acá elegir la columna que represente los datos de tensión VBE
IB = data[:,1 ]; # Acá elegir la columna que represente los datos de corriente IB
IC = data[:,2]; # Acá elegir la columna que represente los datos de corriente IC
logIC = np.log(np.abs(IC)); # Tomar el logaritmo natural del valor absoluto de la corriente

#%%%%%%%%%% Gráficos de los datos
# Graficar los datos en escala lineal

mili = 1000 # Hay que multiplicar por 1e3 la corriente para pasarla a mA

plt.figure()
plt.plot(VBE,mili*IB)
plt.plot(VBE,mili*IC)
plt.grid()
legends = list()
legends.append('Simulación $I_{B}$')
legends.append('Simulación $I_{C}$')
plt.legend(legends)
plt.ylabel('Corriente [mA]');
plt.xlabel('Tensión [V]');


#%%%%%%%%%% Graficar los datos en escala semilog 
plt.figure()
plt.grid(True, which="both", ls="-")
plt.semilogy(VBE,np.abs(mili*IB),'-b') # Hay que tomar el valor abosulto de la corriente ya que el logaritmo no admite valores negativos
plt.semilogy(VBE,np.abs(mili*IC),'-r') # Hay que tomar el valor abosulto de la corriente ya que el logaritmo no admite valores negativos
plt.ylabel('Corriente [mA]');
plt.xlabel('Tensión VBE [V]');
#plt.ylim([1e-15, 1]) #Esto permite controlar los límites del eje y


# %%%%%%%%  Ajuste de IC vs VBE para obtener el parámetro IS

# Hay que elegir los puntos a ajustar con una recta
# Seleccionar vMin y vMax para elegir un rango de puntos a ajustar por una recta
# Este debe ser el rango de tensiones donde la curva en escala semilog se parece a una recta
vMin = 0.25 # Valor mínimo del rango (en volts)
vMax = 0.5 # Valor máximo del rango (en volts)

# Me quedo con los puntos entre vMin y vMax
indicesAjuste = np.where((VBE > vMin) & (VBE < vMax))

# Tomo los datos en el intervalo elegido
VBE_ajuste = VBE[indicesAjuste]
IC_ajuste = IC[indicesAjuste]
logIC_ajuste = logIC[indicesAjuste]

# Ajusto una recta a esos puntos
coefAjuste = np.polyfit(VBE_ajuste, logIC_ajuste, deg=1) # Ajusto una recta y obtengo los coeficientes

# Calculo la corriente del TBJ usando los parámetros ajustados y el modelo exponencial
logIS = coefAjuste[1]
IS = np.exp(logIS) # Corriente de saturación en inversa
Vth_ajuste = 1/coefAjuste[0] # Tensión térmica
IC_ajustada = -IS*np.exp(-VBE/Vth); # Obtengo la corriente del diodo utilizando el modelo exponencial y los parametros ajustados

print('Ajuste de IS = ', str(IS), 'A')
print('Ajuste de Vth = ', str(Vth_ajuste), 'V')



# %%%%%%%%%%%%%%%%%%%%%% Crea la figura y el eje

fig, ax = plt.subplots()

# Graficamos usando semilogaritmo en el eje Y
ax.semilogy(VBE, np.abs(mili * IB), label='$I_B$')
ax.semilogy(VBE, np.abs(mili * IC), label='$I_C$: datos de simulación')
ax.semilogy(VBE_ajuste, np.abs(mili * IC_ajuste), label='Datos elegidos para el ajuste')
ax.semilogy(
    VBE,
    np.abs(mili * IC_ajustada),
    label=f'Curva ajustada: $I_S$ = {IS:.3} A, $Vth$ = {Vth_ajuste:.3} V',
    linestyle='--'
)

# Límites, labels y deduplicación de leyenda
ax.set_ylim(bottom=1e-8)
ax.set_xlabel('Tensión $V_{BE}$ [V]')
ax.set_ylabel('Corriente [mA]')
ax.legend(['$I_B$', '$I_C$: datos de simulación', 'Datos elegidos para el ajuste de $I_C$', f'Curva ajustada: $I_S$ = {IS:.3} A, $Vth$ = {Vth_ajuste:.3} V'])

# Configura manualmente los minor ticks en el eje Y para la escala logarítmica
# Esto fuerza a que se muestren los ticks menores y, por ende, la grilla asociada
ax.yaxis.set_minor_locator(ticker.LogLocator(base=10, subs=np.arange(1, 10), numticks=100))

# Activa la grilla para los ticks mayores y menores con estilos diferenciados
ax.grid(which='major', linestyle='--', linewidth=0.5)
ax.grid(which='minor', linestyle='--', linewidth=0.3)

plt.show()




#Parte 2

# %%%%%%%%%%%%%%%%%
# Lectura del archivo
archivo_salida = './simulaciones/sim2/ICvsVCE.txt'

# Lectura del archivo salteando la primera fila ya que esa tiene los nombres de las columnas
data=np.loadtxt(archivo_salida, skiprows=1)

## Asignación de datos
VCE = data[:, 0]; # Acá elegir la columna que represente los datos de tensión VCE
IC_salida = data[:, 1]; # Acá elegir la columna que represente los datos de corriente IC

# %%%%%%%%%%%%%%% 
## Ajuste de IC vs VCE para obtener el parámetro VA

# Hay que elegir los puntos a ajustar con una recta.
# Seleccionar vMin y vMax para elegir un rango de puntos a ajustar por una recta
# Este debe ser el rango de tensiones donde la curva en escala semilog se parece a una recta
vMin = 0 # Valor mínimo del rango (en volts)
vMax = 4 # Valor máximo del rango (en volts)

# Me quedo con los puntos entre vMin y vMax
indicesAjuste_VA = np.where((VCE > vMin) & (VCE < vMax))

# Tomo los datos en el intervalo elegido
VCE_ajuste = VCE[indicesAjuste_VA]
IC_ajuste_VA = IC_salida[indicesAjuste_VA]

# Ajusto una recta a esos puntos
coefAjuste_VA = np.polyfit(VCE_ajuste, IC_ajuste_VA, deg=1) # Ajusto una recta y obtengo los coeficientes

# Calculo el parámetro beta del TBJ usando los parámetros ajustados y el modelo exponencial
IC0 = coefAjuste_VA[1]
VA = -IC0/coefAjuste_VA[0]
IC_ajustada_VA = IC0*(1-VCE/VA); # Obtengo la corriente utilizando el modelo exponencial y los parametros ajustados

print('Ajuste de VA = ', str(VA))



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%

plt.figure()
plt.plot(VCE,mili*IC_salida, label='Datos de simulación')
plt.plot(VCE_ajuste, mili*IC_ajuste_VA, label= 'Datos elegidos para el ajuste')
plt.plot(VCE, mili*IC_ajustada_VA, label='Curva ajustada', linestyle='--')
#plt.ylim(bottom=1e-15)
#plt.xlim(right=0)
plt.grid()
plt.ylabel('Corriente $I_C$ [mA]');
plt.xlabel('Tensión $V_{CE}$ [V]');
plt.legend([f'Datos de simulación, $VCEsat$ = 0.25 V','Datos elegidos para el ajuste', f'Datos del ajuste: $V_A$ = {VA:.2f} V'])
#Acá hay que poner el valor que corresponde a la tensión VCEsat por inspección




# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Cargar los archivos para la simulación en temperatura
archivo_sinRE = './ICpolarizacion_sinRE_vsT.txt'
archivo_conRE = './ICpolarizacion_conRE_vsT.txt'

datos_sinRE = np.loadtxt(archivo_sinRE, skiprows=1)
datos_conRE = np.loadtxt(archivo_conRE,skiprows=1)

# Seleccionar las columnas correspondientes
IC_sinRE = datos_sinRE['IC']  # Reemplazar 'IC' por el nombre real de la columna de IC en este archivo
T = datos_sinRE['T']          # Reemplazar 'T' por el nombre real de la columna de T
IC_conRE = datos_conRE['IC']  # Reemplazar 'IC' por el nombre real de la columna de IC en este archivo

# Graficar ambos conjuntos de datos
plt.figure()
plt.plot(T, IC_sinRE*mili, label="IC sin RE")
plt.plot(T, IC_conRE*mili, label="IC con RE")
plt.grid()
plt.ylabel('Corriente $I_C$ [mA]');
plt.xlabel('Temperatura [$\circ$C]');
plt.legend([f'$I_C$ sin $R_E$', '$I_C$ con $R_E$'])
plt.show()





















