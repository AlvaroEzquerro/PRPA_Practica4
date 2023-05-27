# Práctica 4
Entrega de la Práctica 4 de la asignatura de Programación Paralela realizada por:
- José Ignacio Alba Rodríguez
- Álvaro Ezquerro Pérez
- Alejandro Millán Arribas

La práctica consiste en el diseño e implementación de una solución a un problema de análisis de datos utlizando Spark sobre el dataset proporcionado por Ayuntamiento de Madrid del uso de sistema de bicicletas de préstamos BICIMAD. 

La entrega consta principalmente de dos archivos:
- bicimad.py: donde hemos implementado la solución en Python, utilizando la herramienta Spark.
- BiciMAD.pdf: donde se encuentra una explicación extendida de la problemática planteada, así como la solución propuesta y el análisis de los resultados con las conclusiones correspondientes.

Nosotros nos hemos planteado intentar diseñar un plan de mejora para la eficiencia del servicio BiciMAD basándonos en algunas cuestiones de las cuales nos parece fundamental su estudio e intento de mejora. Estas cuestiones son:

1. Los trayectos más realizados y los que menos.
2. Optimizar las estaciones que hay, es decir, ver cuales son las menos utilizadas y las más. 
3. Determinar la hora punta de uso.
4. ¿Hay un gran número de clientes habituales, o sería recomendable plantear sistemas de fidelización para aumentar dicho número?
5. Porcentajes de uso dependiendo del rango de edad y el tipo de usuario.
6. Cantidad de bicicletas rotas, es decir, cuyo viaje consta de un tiempo bajo (<60 seg)
