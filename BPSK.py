"""
UNC - FCEFyN - Comunicaciones digitales
Año 2020
Piñero, Tomás Santiago

Simulador BPSK con canal Gausiano v1.0
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import scipy.stats as st

#Parámetros
muestras = 10000                    #Cantidad de muestras
cardinalidad = 2                    #Cantidad de mensajes
prob = [0.7, 0.3]                   #Probabilidades
mensajes = [0, 1]                   #Mensajes a enviar
mu = [0 for i in range(muestras)]   #Muestras para el histograma
C = [-1, 1]                         #Códigos: ¡C[0] < C[1]!
señal = []                          #Señal codificada

#Función para corroborar que la suma de las probabilidades sea 1
#Acumula en 'suma' los valores de 'prob'. Si 'suma' es mayor a uno,
#está mal cargado.
def check_prob(probabilidades):
    suma = list(it.accumulate(probabilidades))
    print("Checkenado probabilidades de cardinalidad " + str(len(suma)) +"...")
    if(suma[len(suma)-1] != 1):
        print("Probabilidades fuera de rango.")
        raise SystemExit(0)
    else: print("Done.")

check_prob(prob)

"""----------
Transmisor
"""

"""----------
Fuente
"""
#En caso de no tener mensajes definidos, los genera automáticamente
if len(mensajes) == 0:
    for m in range(cardinalidad):
        mensajes.append(m)
"""----------
Fin Fuente
"""
#Funcion que realiza la codificación de mensajes
def codificar(codigo, hipotesis):
    #Copio los C y la H para generar la señal a enviar
    code_copy = codigo.copy()
    hipotesis = mensajes.copy()
    print("\nCodificación:\n")
    #Selecciona una una H y un C y realiza el mapeo
    for r in range(len(hipotesis)):
        seleccion_hipotesis = hipotesis[r]
        seleccion_code = code_copy[r]

        señal.append(int(seleccion_code))
        print("C = " +str(seleccion_code)+" -> H = "+str(seleccion_hipotesis))

    print("\nSeñal: "+str(señal))

#Codificación de los mensajes a enviar
codificar(C, mensajes)

#Genera la cantidad de muestras según probabilidades
for i in range(muestras):
    s = np.random.uniform(0,1)
    if s < prob[0]:
        mu[i] = señal[0]
    else:
        mu[i] = señal[1]
"""----------
Fin Transmisor
"""

"""----------
Canal
"""
media = 0
varianza = 0.5
#Crea un array[muestras] según los parámetros
noise = np.random.normal(media,varianza,muestras)

signal = mu + noise
"""----------
Fin Canal
"""

#Función a la salida del canal
bins = 50
plt.title("Histograma de la señal")
plt.xlabel("Valores")
plt.ylabel("Frecuencia")
plt.hist(signal, bins, alpha = 0.5, color = 'green', ec = 'black')
plt.show()
plt.clf()

"""----------
Receptor
"""
#Se calcula el threshold
threshold = prob[0]/prob[1]
ln = np.log(threshold)

#MAP (si es equiprobable, se convierte en ML)
theta = (varianza/(C[1]-C[0])) * ln + ((C[0]+C[1])/2)

#Señales detectadas
detectado = np.where(signal >= theta, 1, -1);

errores = np.sum(abs((detectado[1:muestras]-mu[1:muestras]))/2)

print("mu: ", mu[1:10])
print("de: ", detectado[1:10])

print("zeta: ", theta)

print("Probabilidad de error estadístico: ", errores/muestras)

#Error utilizando función Q
perror = prob[0] * st.norm.sf((theta-C[0])/varianza)
perror += prob[1] * st.norm.sf((C[1]-theta)/varianza)

print("Probabilidad de error analítico: ", perror)

plt.plot(perror)

"""----------
Fin Receptor
"""

#Crea una señal de ruido con los parámetros del arreglo
#'varianzas' y una señal de salida prueba, para ver los
#efectos de las mismas
def testings():
    #Crea un array de varianzas des 0.2 a 0.8 con salto 0.1
    varianzas = np.arange(0.3, 0.9, 0.1)
    ep  = [0 for a in range(len(varianzas))]
    eq = [0 for a in range(len(varianzas))]

    #Para cada señal, añade ruido, la decodifica y vuelve a
    #calcular los errores
    for t in range(len(varianzas)):

        n = np.random.normal(media, varianzas[t], muestras)
        sig_test = mu + n

        zeta = (varianzas[t]/(C[1]-C[0])) * np.log(prob[0]/prob[1])
        zeta += ((C[0]+C[1])/2)

        #Detecta la señal
        detected = np.where(sig_test >= zeta, 1, -1)

        ep[t] = np.sum(abs((detected[1:muestras]-mu[1:muestras]))/2)
        ep[t] = ep[t] / muestras

        eq[t] = prob[0] * st.norm.sf((zeta-C[0])/varianzas[t])
        eq[t] += prob[1] * st.norm.sf((C[1]-zeta)/varianzas[t])

    #Plotea los dos tipos de errores calculados
    plt.title("Error estadístico vs Error analítico")
    plt.xlabel("Varianza")
    plt.ylabel("Error")
    plt.yscale('log')
    plt.plot(varianzas, ep, 'r', alpha = 0.5, label = 'estadístico')
    plt.plot(varianzas, eq, 'b', alpha = 0.5, label = 'analítico')
    plt.legend(loc = 'best')
    plt.show()

testings()
