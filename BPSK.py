"""
UNC - FCEFyN - Comunicaciones digitales
Año 2020
Piñero, Tomás Santiago

Simulador BPSK con canal Gausiano v1.0
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

#Parámetros
muestras = 10000                    #Cantidad de muestras
cardinalidad = 2                    #Cantidad de mensajes
prob = [0.5, 0.5]                   #De no serlo, se asignan aca
mensajes = [0, 1]                   #Mensajes a enviar
mu = [0 for i in range(muestras)]   #Muestras para el histograma
C = [-1, 1]                         #Códigos
señal = []                          #Señal a la salida del transmisor

#Función para corroborar que la suma de las probabilidades sea 1
def check_prob(probabilidades):
    suma = list(it.accumulate(probabilidades))
    print("Checkenado probabilidades de cardinalidad " + str(len(suma)) +"...")
    if(suma[len(suma)-1] != 1):
        print("Probabilidades fuera de rango.")
        raise SystemExit(0)
    else: print("Done.")

check_prob(prob)

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

"""----------
Transmisor
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
threshold = min(prob)/max(prob)
ln = np.log(threshold)

#MAP (si es equiprobable, se convierte en ML)
zeta = (varianza/(C[1]-C[0])) * ln + ((C[0]+C[1])/2)

#Señales detectadas
detectado = np.where(signal >= zeta, 1, 0);

errores = np.sum(abs((detectado[1:muestras]-señal[1:muestras]))/2)

print("Probabilidad de error: ", errores/muestras)

"""----------
Fin Receptor
"""
