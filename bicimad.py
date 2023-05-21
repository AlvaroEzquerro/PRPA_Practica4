from pyspark import SparkContext
from datetime import datetime
import json #Sirve para leer el formato en el qeu estan las bases de datos


def mapper(line): #Funcion para extraer los datos de cada una de las lineas del archivo anterior
    '''
    user_age:
        0: No se ha podido determinar el rango de edad del usuario
        1: El usuario tiene entre 0 y 16 años
        2: El usuario tiene entre 17 y 18 años
        3: El usuario tiene entre 19 y 26 años
        4: El usuario tiene entre 27 y 40 años
        5: El usuario tiene entre 41 y 65 años
        6: El usuario tiene 66 años o más

    user_type:
        0: No se ha podido determinar el tipo de usuario
        1: Usuario anual (poseedor de un pase anual)
        2: Usuario ocasional
        3: Trabajador de la empresa
    '''
    data = json.loads(line)
    user_type = data['user_type']
    user_age = data['ageRange']
    user_day_code = data['user_day_code']
    start_station = data['idunplug_station']
    end_station = data['idplug_station']
    duration = data['travel_time']
    date = datetime.strptime(data["unplug_hourTime"]['$date'][:-4], '%Y-%m-%dT%H:%M:%S.000+')
    return user_type, user_day_code, start_station, end_station, duration, date, user_age
'''
Indices:
    0-user_type
    1-user_day_code
    2-start_station
    3-end_station
    4-time
    5-date
    6-user_age
    
'''
user_types = {0:'Sin datos', 1:'Usuario anual', 2:'Usuario ocasional',\
              3:'Trabajador de empresa'}
user_ages = {0: 'Sin datos',\
             1: '<17',\
             2: '17-18',\
             3: '19-26',\
             4: '27-40',\
             5: '41-65',\
             6: '>65'}
    
def rutas_ordenadas(rdd):
    rutas_ordenadas = rdd.map(lambda x: ((x[2], x[3]),1)).\
        reduceByKey(lambda x, y: x+y).\
        sortBy(lambda x: x[1], ascending = False)     
    return rutas_ordenadas

def estaciones_ordenadas(rdd):
    Estaciones = rdd.flatMap(lambda x: [(x[2], 1), (x[3], 1)]).\
        reduceByKey(lambda x, y: x+y).\
        sortBy(lambda x: x[1], ascending = False)
    estacioneS = rdd.flatMap(lambda x: [(x[2], 1), (x[3], 1)]).\
        reduceByKey(lambda x, y: x+y).\
        sortBy(lambda x: x[1], ascending = True)
    return Estaciones, estacioneS

def horas_ordenadas(rdd):
    horas = rdd.map(lambda x: (x[5].hour, 1)).\
        reduceByKey(lambda x, y: x+y).\
        sortBy(lambda x: x[1], ascending = False)
    total = horas.map(lambda x: x[1]).sum() #total de viajes
    horas = horas.map(lambda x: (x[0], x[1]*100/total)) #cambio el total por porcentajes
    return horas

def tipos_ordenados(rdd):
    tipos = rdd.map(lambda x: (user_types[x[0]], 1)).\
        reduceByKey(lambda x, y: x+y).\
        sortBy(lambda x: x[1], ascending = False)
    total = tipos.map(lambda x: x[1]).sum() #total de viajes
    tipos = tipos.map(lambda x: (x[0], x[1]*100/total)) #cambio el total por porcentajes
    return tipos

def edades_ordenadas(rdd):
    edades = rdd.map(lambda x: (user_ages[x[0]], 1)).\
        reduceByKey(lambda x, y: x+y).\
        sortBy(lambda x: x[1], ascending = False)
    total = edades.map(lambda x: x[1]).sum() #total de viajes
    edades = edades.map(lambda x: (x[0], x[1]*100/total)) #cambio el total por porcentajes
    return edades

def main():
    with SparkContext() as sc:
        sc.setLogLevel("ERROR")
        
        rdd_base = sc.textFile('sample_10e4.json') #Aqui leemos el archivo .json
        rdd = rdd_base.map(mapper) #Aplicamos la funcion anterior a todo el archivo
        n = 5
        
        print('------------------------------1-------------------------------')
        
        rutas = rutas_ordenadas(rdd)
        print('Las', n, 'rutas mas repetidas son:')
        print(rutas.map(lambda x: x[0]).take(n))
        print('realizadas cada una este numero de veces:')
        print(rutas.map(lambda x: x[1]).take(n))
        print('Además, las siguientes rutas solo se realizan una vez:')
        #print(rutas.filter(lambda x: x[1] == 1).map(lambda x: x[0]).collect())
        
        print('------------------------------2-------------------------------')
        
        Estaciones, estacioneS = estaciones_ordenadas(rdd)
        print('Estas son las', n, 'estaciones más transitadas:')
        print(Estaciones.map(lambda x: x[0]).take(n))
        print('con este numero de usos cada una:')
        print(Estaciones.map(lambda x: x[1]).take(n))
        print('Además, estas son las', n, ' estaciones menos transitadas:')
        print(estacioneS.map(lambda x: x[0]).take(n))
        print('con este numero de usos cada una:')
        print(estacioneS.map(lambda x: x[1]).take(n))
        
        print('------------------------------3-------------------------------')
        
        horas = horas_ordenadas(rdd)
        print('Las horas ordenadas en cuanto a mayor uso son:')
        print(horas.map(lambda x: x[0]).collect())
        print('con porcentajes:')
        print(horas.map(lambda x: x[1]).collect())
        
        print('------------------------------4-------------------------------')
        
        
        
        print('------------------------------5-------------------------------')
        
        edades = edades_ordenadas(rdd)
        print('Las edades de los usuarios ordenadas en cuanto a más uso son:')
        print(edades.map(lambda x: x[0]).collect())
        print('con porcentajes:')
        print(edades.map(lambda x: x[1]).collect())
        
        print('------------------------------6-------------------------------')
        
        
        
if __name__ == '__main__':
    main()
