# Práctica 4
Entrega de la Práctica 4 de la asignatura de Programación Paralela realizada por:
- José Ignacio Alba Rodríguez
- Álvaro Ezquerro Pérez
- Alejandro Millán Arribas

La práctica consiste en el diseño e implementación de una solución a un problema de análisis de datos utlizando Spark sobre el dataset proporcionado por Ayuntamiento de Madrid del uso de sistema de bicicletas de préstamos BICIMAD. 

La entrega consta principalmente de dos archivos:
- bicimad.py: donde hemos implementado la solución en Python, utilizando la herramienta Spark.
- BiciMAD.pdf: donde se encuentra una explicación extendida de la problemática planteada, así como la solución propuesta y el análisis de los resultados con las conclusiones correspondientes.
- EjecucionesCluster.png: se encuentra el registro de varias ejecuciones en el cluster cada una de ellas sobre un distinto número de archvivos.

## EJECUCIÓN
Para ejecutar el programa bicimad.py sobre los archivos que se deseen hay que utilizar el comando:

**python3 bicimad.py 'archivo1.json' 'archivo2.json' ... 'archivon.json'**


Nosotros nos hemos planteado intentar diseñar un plan de mejora para la eficiencia del servicio BiciMAD basándonos en algunas cuestiones de las cuales nos parece fundamental su estudio e intento de mejora. Estas cuestiones son:

Las cuestiones que nos hemos planteado son las siguientes:
1. Determinar los trayectos más realizados y los menos.
2. Calcular la cantidad de bicicletas rotas.
3. Calcular cuáles son las estaciones más utilizadas y las que menos.
4. Determinar la necesidad de transferencia de cada estación
5. Estimar la hora punta de uso.
6. Calcular los porcentajes de uso en función del rango de edad y el tipo de usuario.

Los datos que hemos utilizado son los correspondientes a los meses de enero a junio de 2021 que se pueden encontrar en la página web del Ayuntamiento de Madrid, indicada en el archivo BiciMAD.pdf. Sin embargo, no hemos podido subirlos a este repositorio porque superaban la capacidad permitida por github.
