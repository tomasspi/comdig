"""
UNC - FCEFyN - Comunicaciones digitales
Año 2020
Piñero, Tomás Santiago

Modelado de fuente, transmisor y canal
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools as it

"""
PUNTO 1.-  Implementar en software una fuente de mensajes de cardinalidad 2 y 4
equiprobable. Extender la fuente de mensaje a una de probabilidad parametrizable
(no necesariamente equiprobable)
"""

#Parámetros
muestras = 10000                    #Cantidad de muestras
cardinalidad = 2                    #Cardinalidad de los mensajes
equiprobable = 0                    #Son equiprobables? 1 -> si, 0 -> no
p = 1/cardinalidad                  #De serlo, se asina la probabilidad de c/u
prob2 = [0.8, 0.2]                  #De no serlo, se asignan aca
prob4 = [0.2, 0.4, 0.1, 0.3]
mensajes = []                       #Mensajes a enviar
mu = [0 for i in range(muestras)]   #Muestras para el histograma

#Función para corroborar que la suma de las probabilidades sea 1
def check_prob(probabilidades):
    suma = list(it.accumulate(probabilidades))
    print("Checkenado probabilidades de cardinalidad " + str(len(suma)) +"...")
    if(suma[len(suma)-1] != 1):
        print("Probabilidades fuera de rango.")
        raise SystemExit(0)
    else: print("Done.")

if equiprobable:
    check_prob(prob2)
    check_prob(prob4)

#En caso de no tener mensajes definidos, los genera automáticamente
for m in range(cardinalidad):
    mensajes.append(m)

for i in range(muestras):
    if cardinalidad == 2:
        s = np.random.uniform(0,1)
        if equiprobable:
            if s < p:
                mu[i] = mensajes[0]
            else:
                mu[i] = mensajes[1]
        else:
            if s > prob2[0]:
                mu[i] = mensajes[0]
            else:
                mu[i] = mensajes[1]
    elif cardinalidad == 4:
        t = np.random.uniform(0,1)
        if equiprobable:
            if t < p:
                mu[i] = mensajes[0]
            elif p <= t and t < 2*p:
                mu[i] = mensajes[1]
            elif 2*p <= t and t < 3*p:
                mu[i] = mensajes[2]
            else:
                mu[i] = mensajes[3]
        else:
            suma = list(it.accumulate(prob4)) #Lista con los valores P acumulados
            if 0 <= t and t < suma[0]:
                mu[i] = mensajes[0]
            elif suma[0] <= t and t < suma[1]:
                mu[i] = mensajes[1]
            elif suma[1] <= t and t < suma[2]:
                mu[i] = mensajes[2]
            else:
                mu[i] = mensajes[3]

"""
--- FIN PUNTO 1 ---
"""

"""
PUNTO 2.- Argumentar ecuación.

El canal requiere un alfabeto de entrada (X), uno de salida (Y) y
la probabilidad de que ocurra una salida dada la entrada.

Al no tener memoria, la salida (Y) no depende de la entrada (X)
anterior, por lo que la probabilidad de que suceda una salida (Y) dado una
entrada (X) es la multiplicación de las probabilidades de cada variable
independiente.

--- FIN PUNTO 2 ---
"""

"""
PUNTO 3.- Implementar el modelo del canal del ejemplo 2.3.
Ejemplo 2.3 (AWGN) canal que agrega ruido blanco (gaussiano)
"""

media = 0
varianza = 0.5
#Crea un array[muestras] con media 0 y desviacion 1
noise = np.random.normal(media,varianza,muestras)

signal = mu + noise

print("\nSeñal sin ruido:")
print(mu[0:10])

print("\nSeñal con ruido:")
print(signal[0:10])


"""
--- FIN PUNTO 3 ---
"""

"""
PUNTO 4.- Modelar el transmisor para C = {+1, -1,+3, -3} y
C = {(1,1),(1,-1),(-1,-1),(-1,1)}. El mensaje de entrada al transmisor es
H={1, 2, 3, 4}
"""
C1 = [1, -1, 3, -3]
C2 = [(1,1), (1,-1), (-1,-1), (-1,1)]
H  = [1, 2, 3, 4]

def codificar(codigo, hipotesis):
    #Copio los C y la H para generar la señal a enviar
    code_copy = codigo.copy()
    hipotesis = H.copy()
    señal = []
    print("\nCodificación:\n")
    #Selecciona una una H y una C y realiza el mapeo
    for r in range(len(hipotesis)):
        seleccion_hipotesis = np.random.choice(hipotesis,1)
        index = np.random.randint(len(code_copy))

        hipotesis.remove(seleccion_hipotesis)
        seleccion_code = code_copy[index]

        señal.append(seleccion_code)
        print("C = " +str(seleccion_code)+" -> H = "+str(seleccion_hipotesis))
        del code_copy[index]

    print("\nSeñal: "+str(señal))

codificar(C1, H)
codificar(C2, H)

"""
--- FIN PUNTO 4 ---
"""

bins = 50

plt.title("Histograma Mensajes")
plt.xlabel("Mensajes")
plt.ylabel("Frecuencia")
plt.hist(mu, bins, alpha = 0.5, color = 'red', ec = 'black')
plt.show()
plt.clf()

plt.title("Histograma Ruido")
plt.xlabel("Ruido")
plt.ylabel("Frecuencia")
plt.hist(noise, bins, alpha = 0.5, color = 'green', ec = 'black')
plt.show()
plt.clf()

plt.title("Histograma Señal")
plt.xlabel("Valores")
plt.ylabel("Frecuencia")
plt.hist(signal, bins, alpha = 0.5, color = 'blue', ec = 'black')
plt.show()
plt.clf()
