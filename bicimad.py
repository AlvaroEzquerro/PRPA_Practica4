from pyspark import SparkContext
import json #Sirve para leer el formato en el qeu estan las bases de datos


def mapper(line): #Funcion para extraer los datos de cada una de las lineas del archivo anterior
    data = json.loads(line)
    user_type = data['user_type']
    user_day_code = data['user_day_code']
    start_station = data['idunplug_station']
    end_station = data['idplug_station']
    time = data['travel_time']
    return user_type, user_day_code, start_station, end_station, time

def ruta_mas_repetida(rdd):
    ruta, veces = rdd.map(lambda x: ((x[2], x[3]),1)).\
        reduceByKey(lambda x, y: x+y).\
        sortBy(lambda x: x[1], ascending = False).first()       
    return ruta, veces

def rutas_hechas_1_vez(rdd):
    pass

def main():
    with SparkContext() as sc:
        sc.setLogLevel("ERROR")
        
        rdd_base = sc.textFile('sample_10e3.json') #Aqui leemos el archivo .json
        rdd = rdd_base.map(mapper) #Aplicamos la funcion anterior a todo el archivo
        ruta, veces = ruta_mas_repetida(rdd)
        print('La ruta mas repetida es:', ruta)
        print('Realizada', veces, 'veces')

if __name__ == '__main__':
    main()
