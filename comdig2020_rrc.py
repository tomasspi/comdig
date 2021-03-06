# -*- coding: utf-8 -*-
"""Comdig2020_RRC.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dp76jhKtw33DrR0k0rez5dOmX6o5Y_4I

---
**UNC -- FCEFyN -- ComDig -- 2020**

**Piñero, Tomás Santiago**

---

**Root-raised cosine (raiz cuadrada de coseno alzado, RRC)**

Esta actividad consiste en replicar la figura 5.7 (pág. 172 del libro PDC Bixio Rimoldi), que utiliza la respuesta al impulso del RRC como *waveformer*, siendo ésta:

$\psi(t) = \frac{4 \beta}{\pi \sqrt{T}} \frac{cos[(1+ \beta) \pi \frac{t}{T}] + \frac{(1 - \beta) \pi}{4 \beta} sinc[(1 - \beta) \frac{t}{T}]}{1 - (4 \beta \frac{t}{T})^2}$

que es la anti-transformada de Fourier de la señal RRC.

Las figuras a replicar son las siguientes:

![fig5-7](https://drive.google.com/uc?id=18eujegUqGuEoWwKbi2YPFgLQBaSTa95-)

Donde: 

*   La *Fig. a* muestra la secuencia la respuesta al impulso de RRC de $s_i \psi (t -iT)$, con $i = 0, 1, 2, 3$ y símbolos ($s_i \in \pm 1$) 
*   La *Fig. b* muestra la suma de las señales mostradas en 'a'
*   $\beta = 0.5 \land T = 10$
"""

import scipy
import numpy as np
import matplotlib.pyplot as plt
from   random import choice
from   scipy.signal import find_peaks

muestras = 30  #tamaño de la salida
beta = 0.9    #roll-off
T = 10        #periodo
f = 100       #frecuencia de muestreo

bits = [0 for _ in range(muestras)] #Señal con simbolos s_i

for i in range(muestras):
  bits[i] = choice([-1, 1])

signals = [0 for _ in range(muestras)] #Señales a la entrada del waveformer

#Se define un función que realiza el cálculo del RRC
def rrcos(t):
  #Primer factor de la ecuación  
  constante = (4 * beta)/(np.pi * np.sqrt(T))
  
  #Numerador del segundo factor de la ecucación
  numerador = np.cos((1 + beta) * np.pi * (t/T)) \
              + (((1 - beta) * np.pi)/(4 * beta)) \
              * np.sinc((1 - beta)*(t/T))
  
  #Denominador del segundo factor de la ecucación                       
  denominador = 1 - ((4 * beta) *(t/T))**2

  #Cálculo de la función RRC
  rrcos = constante * (numerador/denominador)
  return rrcos

rrc_signals = [0 for _ in range(muestras)]  #Arreglo para las señales RRC
t = np.arange(-5*T, (len(bits)+2)*T, 1/f)   #Intervalo de tiempo a observar

for i in range(muestras):
  rrc_signals[i] = rrcos(t - i*T)        #Calcula cada RRC con su desfasaje
  signals[i] = bits[i] * rrc_signals[i]  #Convoluciona el símbolo con la señal \
                                         #RRC correspondiente

#Muestra las cuatro señales
plt.title("Entradas al waveformer (Fig. a)")
plt.xlabel("t")
plt.ylabel("signal")
plt.xlim(-50, 70)
plt.plot(t, signals[0], color='r')
plt.plot(t, signals[1], color='g')
plt.plot(t, signals[2], color='b')
plt.plot(t, signals[3], color='y')
plt.show()

suma = 0
for i in range(muestras):
  suma += signals[i]  #Suma las señales del punto anterior

#Muestra la suma realizada
plt.title("Salida del waveformer (Fig. b)")
plt.xlabel("t")
plt.ylabel("sum-signal")
plt.plot(t, suma, color='g')
plt.show()

"""---
**Receptor**

En esta sección se replicará la figura 5.8 (pág. 173 del libro PDC Bixio Rimoldi) en la que se utiliza un filtro apareado en el lado del receptor.

![fig5-8](https://drive.google.com/uc?id=1PcHkFyQ25uTthVYR3_YAbX5yi2Qwa_sI)

Donde:

*   La *Fig. a* muestra la respuesta al impulso del filtro apareado a la entrada $s_i \psi (t - iT)$. Dicha respuesta es de la forma $s_i R_\psi (t - iT)$, con $i = 0, 1, 2, 3$
*   La *Fig. b* muestra la señal $y(t)$ (sin ruido)
*   $\beta = 0.5 \land T = 10$
"""

R = [0 for _ in range(muestras)]  #Filtro apareado
y = [0 for _ in range(muestras)]  #Salidas al filtro apareado
Y = [0 for _ in range(muestras)]  #Integral de las salidas

def receptor(signal):
  for i in range(muestras):
    R = rrcos(-t + i*T) #Filtro apareado
    y[i] = signal * R   #Salidas
    Y[i] = scipy.integrate.simps(y[i])/100 #Integra la señal

receptor(suma)

#Muestra la suma realizada
plt.title("Respuesta al impulso (Fig. a)")
plt.xlabel("t")
plt.ylabel("signal")
plt.xlim(-50, 70)
plt.plot(t, y[0], color='r')
plt.plot(t, y[1], color='g')
plt.plot(t, y[2], color='b')
plt.plot(t, y[3], color='y')
plt.show()

"""---

**Diagrama de ojo**

A continuación se grafica el diagrama de ojo de la señal que llega al receptor (*suma*), que en este caso, es la que se observa a la salida del *waveformer*.

El diagrama de ojo consiste en tomar muestras de la señal transmitida y mostrarlas en un intervalo $t \in [-T,T]$. Esto permite analizar el ruido, la existencia de interferencia entre símbolos (ISI) y el desfase que se encuentran presentes en la señal mostrada.

El siguiente código fuente para graficarlo se puede encontrar [aquí](https://dspillustrations.com/pages/posts/misc/eye-diagram-examples.html)
"""

def diagrama_ojo(xt):
    samples_perT = f*T
    samples_perWindow = 2*f*T
    parts = []
    startInd = 2*samples_perT   # ignore some transient effects at beginning of signal
    
    for k in range(int(len(xt)/samples_perT) - 6):
        parts.append(xt[startInd + k*samples_perT + np.arange(samples_perWindow)])
    parts = np.array(parts).T

    t_part = np.arange(-T, T, 1/f)
    plt.plot(t_part, parts, 'g')

diagrama_ojo(suma)

"""En la figura anterior existe ISI, ya que "la altura" del ojo no está concentrada en un punto.

Por otro lado, cambiando los valores de beta (roll-off), se pudo deducir que a medida que se lo aumenta, la ISI disminuye y la probabilidad de detectar erróneamente un símbolo disminuye.

---

**Diagrama de dispersión**

A continuación se muestra el diagrama de dispersión de la señal decodificada. Como este caso no presenta ruido, el diagrama consiste únicamente de dos puntos: uno que corresponde al símbolo -1, y el otro al símbolo 1. 

Cabe mencionar que no son únicamente 2 valores los que se muestran, sino una cantidad total *muestras*. Si se añadiera ruido a la señal, se observarían más puntos en el diagrama.
"""

plt.title("Diagrama de dispersión")
plt.xlabel("símbolos")
plt.scatter(Y, np.zeros(muestras), marker='x', color='g')

"""El siguiente código agrega un canal AWGN de acuerdo a un valor de SNRdB dado.

Primero se calcula la potencia de la señal y luego la del ruido dado el SNRdB.
Finalmente se genera un ruido con media 0 y varianza según el SNR calculado y se lo suma a la señal obtenida a la salida del *waveformer*.
"""

snr_db = 30 #SNRdB
#Calcula la potencia de la señal y la convierte a dB
signal_pow = suma ** 2              
sig_avg = np.mean(signal_pow)       
sig_avg_db = 10 * np.log10(sig_avg) 

#Calcula el ruido de acuerdo al SNRdB
noise_db = sig_avg - snr_db
noise_avg_pow = 10 ** (noise_db / 10)
noise_media = 0

#Crea el ruido
noise = np.random.normal(noise_media, np.sqrt(noise_avg_pow), len(signal_pow))

signal_and_noise = suma + noise #Añade el ruido a la señal

diagrama_ojo(signal_and_noise)

"""El diagrama de ojo se puede observar que el ruido afecta considerablemente a la señal transmitida, generando más ISI."""

plt.title('Señal con ruido')
plt.xlabel('t')
plt.plot(t, signal_and_noise, 'r')

plt.title("Diagrama de dispersión")
plt.xlabel("símbolos")
plt.scatter(Y, np.zeros(muestras), marker='o', color='g')
print(Y[:10])

"""En el diagrama de dispesión se nota levemente la influencia del ruido, como se mencionó anteriormente. 

Para una mejor observación de este fenómeno, se imprimieron 10 valores de la señal recibida, donde se nota que los valores difieren en décimas debido a la influencia del ruido ingresado.
"""