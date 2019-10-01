from scipy.stats import poisson
import numpy as np
import math
import random
import scipy.spatial.distance as dist

# Uso una distribución de Poisson para el número de puntos en cada cubo.
# Puedo hacerlo con una función, pero si hay algún 0, el ruído tendrá valor 0
#
distP = np.array([4, 4, 6, 5, 3, 4, 8, 8, 7, 5])
#distP = poisson.rvs(4, size=10)

# Calculamos una semilla diferente para cada cubo.
#
def calculateSeed(cube):
    seed = (541 * cube[0] + 79 * cube[1] + 31 * cube[2]) % 4294967296
    return seed

# Devolvemos el número de puntos por cubo.
#
def pointNumber(seed):
    global distP

    random.seed(seed)
    index = random.randrange(10)

    return(distP[index])

# Genero un punto 3d con coordenadas en el rango 0-1
# Les añado las del cubo para poder calcular la distancia al punto
# original, ya que las coordenadas de éste no están en el rango 0-1
#
def generatePoint(seed,cube):
    #random.seed(seed)

    pointX = random.uniform(0, 1) + cube[0]
    pointY = random.uniform(0, 1) + cube[1]
    pointZ = random.uniform(0, 1) + cube[2]

    return(np.array([pointX,pointY,pointZ]))

# Worley 3d con cubos.
# Referencias :
#   https://thebookofshaders.com/12/
#   http://www.rhythmiccanvas.com/research/papers/worley.pdf
#   https://github.com/bhickey/worley/blob/master/worley.c
#   https://www.kdnuggets.com/2017/08/comparing-distance-measurements-python-scipy.html
def worley3D(punto):
    minimo = 1000

    # Generamos todos los cubos que rodean al del punto. Las coordenadas del cubo al que éste
    # pertenece son las del punto sin decimales. a partir de ahí montamos bucles -1...+1
    for cx in range(math.floor(punto[0] - 1), math.floor(punto[0] + 2)):
        for cy in range(math.floor(punto[1] - 1), math.floor(punto[1] + 2)):
            for cz in range(math.floor(punto[2] - 1), math.floor(punto[2] + 2)):
                cube = np.array([cx, cy, cz])

                # El número de puntos en el cubo vendrá dado por una distribución de Poisson.
                #
                seed = calculateSeed(cube)
                points = pointNumber(seed)
                if points <= 1:
                    return 0
                coords = np.zeros((points, 3))

                distancias = np.zeros(points)
                coords = np.zeros((points, 3))

                # Cálculo de las distancias a los puntos de cada cubo.
                distancias = np.zeros(points)
                for cont in range(points):
                    coords[cont] = generatePoint(seed, cube)
                    # Podemos usar los diferentes cálculos de distancia del módulo
                    # para obtener resultados visuales distintos.
                    #
                    #distancias[cont] = dist.chebyshev(punto, coords[cont])
                    #distancias[cont] = dist.canberra(punto, coords[cont])
                    #distancias[cont] = dist.cosine(punto, coords[cont])
                    #distancias[cont] = dist.cityblock(punto, coords[cont])
                    distancias[cont] = dist.euclidean(punto, coords[cont])

                # Las ordeno y me quedo con la nueva mínima, que es el valor que devuelvo.
                distancias.sort()
                if distancias[1] < minimo:
                    minimo = distancias[1]

    return(np.clip(minimo, 0, 1))

if __name__ == '__main__':
    punto = np.array([1.2,3.4,5.6])
    print(worley3D(punto))
    punto = np.array([1.3, 3.5, 5.7])
    print(worley3D(punto))
    punto = np.array([1.4, 3.6, 5.8])
    print(worley3D(punto))