"""
UNC - FCEFyN - Comunicaciones digitales
Año 2020
Piñero, Tomás Santiago

Densidad de probabilidad de vector Gausiano
"""

# from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mn

"""
Graficar la función de densidad de probabilidad de un vector de variables
aleatorias gausianas.
"""

muestras = 10000
media = 0
varianza = 0.5

X = np.random.normal(media, varianza, muestras)

y = mn.pdf(x,media, varianza)




"""
Graficar la densidad de probabilidad de probabilidad para distintas medias.
"""

"""
Graficar el efecto del ruido en constelaciones de dos dimensiones
"""



def getGauss(sigma):
  ##genero una campana gaussiana centrada en 1, 1 con imagen en z
  x = np.arange(0, 2, 0.01)
  y = np.arange(0, 2, 0.01)
  x, y = np.meshgrid(x, y)
  xy = np.column_stack([x.flat, y.flat])#.flat es un iterador que recorre un array
  #parametros de la normal#
  mu = np.array([1 , 1])
  #sigma = np.array([.3, .3])
  covariance = np.diag(sigma**2)
  #obtengo la normal en matriz#
  z = multivariate_normal.pdf(xy, mean=mu, cov=covariance)
  z = z.reshape(x.shape)
  return z

fig = plt.figure(figsize=(12,5))
ax = fig.gca(projection='3d')

#esto va a contener el DOMINIO#
X = np.arange(0, 2, 0.01)
Y = np.arange(0, 2, 0.01)
X, Y = np.meshgrid(X, Y)
#imagen del dominio#
Z = np.zeros((200, 200), dtype = float)

pepe = np.zeros((200, 200), dtype = float) #aca tenemos la mini imagen a colocar del dominio#

var = np.array([.3, .3])

pepe = getGauss(var)

for i in range(200):
  for j in range (200):
    Z [i] [j] = Z [i] [j] + pepe [i] [j]

surf = ax.plot_surface(X, Y, Z, cmap=cm.rainbow)
plt.show()
