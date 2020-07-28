# -*- coding: utf-8 -*-
"""Comdig2020_Waveformer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LOzaMXPoj_Jcd5tu_hOnTY-pcsIjD5_N

Simular un conformador de forma de onda que cumpla el criterio de ortonormalidad. Analice la respuesta en el tiempo de la salida del conformador. Explique el criterio que emplea para elegir los distintos parámetros.
Se prefiere que el archivo de entrega sea del tipo notebook donde se realicen todas las explicaciones junto con el código.

-----
*Para realizar esta consigna se utilizará el ejemplo 3.9, ubicado en la página 106 del libro Principles of Digital Communication: A top-down approach - Bixio Rimoldi. En este ejemplo se simula un Single-shot PSK, que toma los valores positivos para T y $f_c$ y valores enteros positivos para 'm'.
Las señales tienen la forma*

$w_i (t) = \sqrt{\frac{2\epsilon}{T}}cos(2\pi f_c t+ \frac{2\pi}{m}i)$
con $t \in [0,T]$ e $i = 0,...,m-1$

*Asumiendo que $2\pi f_c T$ es un entero, $\| w_i ² \| = \epsilon$ para todo $i$, lo que nos asegura que todas las $w_i (t)$ estén normalizadas, independientemente de su fase inicial.*

*Mediante la identidad trigonométrica $cos(\alpha + \beta) = cos(\alpha)cos(\beta)-sin(\alpha)sin(\beta)$ la ecuacuión anterior puede reescribirse como sigue:*

$w_i (t) = c_{i,1} \phi_1 (t) + c_{i,2} \phi_2 (t)$

donde:

$c_{i,1} = \sqrt{\epsilon}\cos(\frac{2\pi i}{m}),$
$\;\;\;\phi_1 (t) = \sqrt{\frac{2}{T}}cos(2\pi f_c t)$

$c_{i,2} = \sqrt{\epsilon}\sin(\frac{2\pi i}{m}),$
$\;\;\;\phi_2 (t) = -\sqrt{\frac{2}{T}} sin(2\pi f_c t)$

*Las funciones $\phi_1 (t)$ y $\phi_2 (t)$ están normalizadas y, como $2\pi f_c T$ es un número entero, son ortogonales entre ellas. Por lo tanto, el código asociado a $w_i (t)$ es:*

$c_i = \sqrt{\epsilon}\; \binom{cos(2\pi i/m)}{sin(2\pi i/m)}$

-----
*En este caso se utiliza un $\epsilon$ (costo energético) genérico para el cálculo de los valores. A medida que este valor aumente, se aumentará la amplitud, por lo que habrá más separación entre los símbolos de la constelación, disminuyendo así la probabilidad de error.*

*También se utiliza un $m = 2$ para simplificar los cálculos.*
"""

import numpy as np
import matplotlib.pyplot as plt

muestras = 10000                                #Cantidad de muestras
señal_codificada = [0 for _ in range(muestras)] #Señal codificada (discreta)
codigos = [1, 2]                                #Codificación de los mensajes
m = 2                                           #Cardinalidad (tamaño del alfabeto)
e = 5                                           #Costo energético

#Crea la señal codificada con 1 ó 2
for i in range(muestras):
  señal_codificada[i] = np.random.choice(codigos)

#------------------------Waveformer------------------------#
f = 2                         #Frecuencia
T = 1/f                       #Periodo
w = [0 for _ in range(m)]     #Señal continua
c_i = [0 for _ in range(2*m)] #Codigo
phi_i = [0, 0]                #Funciones normalizadas

#Valores que toman las funciones trigonométricas
values_phi = np.arange(0,2*np.pi*f,0.1) 

#Cálculo de las señales
phi_i[0] = np.sqrt(2/T) * np.cos(values_phi)
phi_i[1] = -(np.sqrt(2/T) * np.sin(values_phi))

#Cálculo de los códigos
c_i[0] = np.sqrt(e) * np.cos(2 * np.pi * 0/m)
c_i[1] = np.sqrt(e) * np.sin(2 * np.pi * 0/m)
c_i[2] = np.sqrt(e) * np.cos(2 * np.pi * 1/m)
c_i[3] = np.sqrt(e) * np.sin(2 * np.pi * 1/m)

#Cálculo de w_i
w[0] = c_i[0] * phi_i[0] + c_i[1] * phi_i[1]
w[1] = c_i[2] * phi_i[0] + c_i[3] * phi_i[1]

signal = [0 for _ in range(muestras)]

for y in range(muestras):
  if señal_codificada[y] == 1:
    signal[y] = señal_codificada[y]*w[0]
  else:
    signal[y] = señal_codificada[y]*w[1]

#Muestra dos de las señales generadas
plt.title("Salida waveformer")
plt.xlabel("t")
plt.ylabel("signal")
plt.plot(values_phi, signal[0], alpha = 0.5, color='g')
plt.plot(values_phi, signal[1], alpha = 0.5, color='r')
plt.show()

"""*En la figura superior se muestran 2 de las 10000 muestras pasadas al waveformer. Como se puede observar, ambas tienen diferente amplitud y son ortogonales entre sí, permitiendo su decodificación en el receptor.*"""