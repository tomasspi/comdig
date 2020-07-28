"""
UNC - FCEFyN - Comunicaciones digitales
Año 2020
Piñero, Tomás Santiago

Detección MAP y ML binario
"""

"""
PUNTO 1.- Grafique en una misma figura las probabilidades condicionales P(Y|H) para
H=0 y H=1 del Ejemplo 2.4 del libro. Elija parámetros para la función de
densidad de Poisson y saque conclusiones.
"""
import math as m
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

prob = [0.5, 0.5]   #Equiprobable
C = [0, 1]          #0 -> LED Off, 1 -> LED On

muestras = 10000
mu = [0 for i in range(muestras)]
signal = [0 for i in range(muestras)]

#---- Generación de muestras de 0 y 1 equiprobables
for i in range(muestras):
    s = np.random.uniform(0,1)
    if s < prob[0]:
        mu[i] = C[0]
    else:
        mu[i] = C[1]
#-----

#----- canal
lambda0 = 5
lambda1 = 10

cero = np.random.poisson(lambda0, muestras)
uno = np.random.poisson(lambda1, muestras)

for s in range(muestras):
    if mu[s] == 0:
        signal[s] = mu[s] + cero[s]
    else:
        signal[s] = mu[s] + uno[s]
#-----

bins = np.linspace(0, 30, 75)

plt.title("Probabilidades condicionales")
plt.xlabel("Lambda")
plt.ylabel("Frecuencia")
plt.hist(cero, bins, alpha = 0.5, color = 'r', label = 'P(Y|0)')
plt.hist(uno, bins, alpha = 0.5, color = 'g', label = 'P(Y|1)')
#plt.hist(signal, bins, alpha = 0.5, color = 'b', label = 'salida')
plt.legend(loc = 'best')
plt.show()
plt.clf()

"""------
Se pudo concluir que cuando lambda1 >> lambda0 no existe una intersección
entre los histogramas de las funciones, por lo que se podría detectar las
señales sin error simplemente utilizando los valores de lambda.
También que para este caso particular el threshold está ubicado alrededor
del valor 7, por lo que en la detección, el valor recibido será 0 si el valor
recibido es menor a 7 y 1 si es mayor.
------"""

"""
PUNTO 2.- Genere una distribución de Poisson y realice su histograma
"""
plt.title("Hisograma Poisson señal de salida")
plt.xlabel("Valores")
plt.ylabel("Frecuencia")
plt.hist(signal, bins, alpha = 0.5, color = 'b', label = 'salida')
plt.show()
plt.clf()

"""
PUNTO 3.- Determine las regiones de decisión MAP y ML. Para el caso MAP,
proponga una distribución de probabilidad de las hipótesis.
"""
#Se calcula el threshold
likelihood = prob[0]/prob[1]
ln = np.log(likelihood)

#MAP (si es equiprobable, se convierte en ML)
threshold = ((lambda1-lambda0) + ln) / np.log(lambda1/lambda0)

print("Threshold: ", threshold)

"""
Punto 4.- Estime estadísticamente la probabilidad error y realice una gráfica de
probabilidad de error vs SNR[dB]
"""
recibido = np.where(signal >= threshold, 1, 0)

error = np.sum(abs(recibido[1:muestras]-mu[1:muestras])/2)

print("Proabilidad de error estadístico: ", error/muestras)

"""
Para lograr un cálculo correcto de la relación ruido-señal, se
dejará fija la distribución de la hipótesis H = 0 y se variará el
lambda1 de acuerdo a distintos valores de SNRdB.
"""
def testings():

    #Genera valores de SNRdB de 0 a 30
    SNRdB = [i for i in range(6)]

    #Genera para el error estadistico
    ep  = [0 for a in range(len(SNRdB))]

    #En este caso, al ser equiprobables, la potencia queda
    #reducida a la media de los valores.
    mu_int = list(map(int, mu))
    mu_int = [x * x for x in mu_int]

    suma_cuadrado_muestras = np.sum(mu_int)

    potencia_signal = np.mean(suma_cuadrado_muestras)

    #Para cada señal, añade ruido, la decodifica y vuelve a
    #calcular los errores
    for t in range(len(SNRdB)):

        #La varianza es igual a la potenia del ruido, pot lo
        #tanto la varianza lambda será:
        lambdat = int(potencia_signal/(10**(SNRdB[t]/10)))

        #Genera distribución de Poisson con el lambda
        #calculado
        nu = np.random.poisson(lambdat,muestras)

        sig_test = [0 for _ in range(muestras)]

        if mu == 0:
            sig_test[t] = mu[t] + cero[t]
        else:
            sig_test[t] = mu[t] + nu[t]

        thres = ((lambdat-lambda0) + ln) / np.log(lambdat/lambda0)

        #Detecta la señal
        detected = np.where(sig_test >= thres, 1, 0)

        ep[t] = float(np.sum(abs(detected[1:muestras]-mu[1:muestras])/2))
        ep[t] = float(ep[t] / muestras)


    plt.title("BER vs SNR[dB]")
    plt.xlabel("SNR")
    plt.ylabel("Error")
    plt.yscale('log')
    plt.plot(SNRdB, ep, 'g')
    plt.show()

testings()

"""
Los resultados están incorrectos, ya que a mayor SNRdB debe
existir menos ruido en la señal, evento que no se observa en la
gráfica realizada.
Si se muestran los BER, se puede observar que estos se mantienen
constantes para los distintos lambdas generados, lo cual es
incorrecto ya que al aumentar el SNRdB, el BER debe disminuir.
"""
