from pyspark import SparkContext
import json #Sirve para leer el formato en el qeu estan las bases de datos


sc = SparkContext()

rdd_base = sc.textFile('sample_10e3.json') #Aqui leemos el archivo .json

def mapper(line): #Funcion para extraer los datos de cada una de las lineas del archivo anterior
    data = json.loads(line)
    user_type = data['user_type']
    user_day_code = data['user_day_code']
    start_station = data['idunplug_station']
    end_station = data['idplug_station']
    time = data['travel_time']
    return user_type, user_day_code, start_station, end_station, time

rdd = rdd_base.map(mapper) #Aplicamos la funcion anterior a todo el archivo

rdd.take(3)



