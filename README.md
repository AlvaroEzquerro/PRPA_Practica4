# Práctica 4
Entrega de la Práctica 4 de la asignatura de Programación Paralela realizada por:
- José Ignacio Alba Rodríguez
- Álvaro Ezquerro Pérez
- Alejandro Millán Arribas

La práctica consiste en el diseño e implementación de una solución a un problema de análisis de datos utlizando Spark sobre el dataset proporcionado por Ayuntamiento de Madrid del uso de sistema de bicicletas de préstamos BICIMAD. Nuestro objetivo es plantear diferentes cuestiones las cuales pretendemos resolver mediante el usa de las técnicas aprendidas en clase. 

##Dataset
El dataset sobre el que vamos a trabajar es el de BICIMAD. Todo lo referente a estos datos se puede encontrar en https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=d67921bb86e64610VgnVCM2000001f4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default
Los archivos son formato json y son de la siguiente forma:

-Tipo de usuario: cliente o personal de mantenimiento.
-Código de usuario.
-Número de la estación donde se desengacha la bicicleta.
-Número de la estación donde se enchancha la bicicleta.
-Número de la base de la que se desengancha la bicicleta.
-Número de la base en la que se engancha la bicicleta.
-Tiempor transcurrido entre el enganche y el desenganche de la bicicleta.
-Hora a la que se realiza el desenganche de la bicicleta.


A continuación, exponemos cada una de las problemáticas que nos hemos enfrentado y como hemos decidido abordarlas:

##1. ¿Cuáles son las estaciones más transitadas? ¿Y las menos?


##2. ¿Cuál es el trayecto más repetido? ¿Y el menos?


##3. ¿Cuál es la hora a la que hay mayor número de usuarios activos? ¿Sería conveniente aumentar el personal de mantenimiento a esas horas?

##4. ¿Hay un gran número de clientes habituales, o sería recomendable plantear sistemas de fidelización para aumentar dicho número?
