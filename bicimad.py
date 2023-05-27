from pyspark import SparkContext
from datetime import datetime
import sys
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
    date = datetime.strptime(data["unplug_hourTime"], '%Y-%m-%dT%H:%M:%SZ')
    return user_type, user_day_code, start_station, end_station, duration, date, user_age
    # No sería más comodo devolver esto como un diccionario o un objeto?
    
    # Alvaro:
    # Piensa que se hace .map(mapper), entonces por cada dato creariamos un dict
'''
Indices:
    0-user_type
    1-user_day_code
    2-start_station
    3-end_station
    4-duration
    5-date
    6-user_age
    
'''
user_types = {0:'NaN', 6:'NaN', 7:'NaN', 1:'Usuario anual', 2:'Usuario ocasional',\
              3:'Trabajador de empresa'}
    
user_ages = {0: 'NaN',\
             1: '<17',\
             2: '17-18',\
             3: '19-26',\
             4: '27-40',\
             5: '41-65',\
             6: '>65'}


def to_listas(a):
    return [(a,1)]

def combinar_si_dentro_del_margen(listas, duracion, margen):
    b = True; i = 0
    while b and i < len(listas):
        media, num = listas[i][0] 
        if media - margen <= duracion <= media + margen:
            listas[i] = ( (media*num + duracion)/(num+1) , num+1)   # Recalculamos la media
            b = False
        i += 1
    if b: listas.append( (duracion, 1) )        # Si tarda mucho mas tiempo, lo consideramos a parte
    return listas

def clientes_habituales(rdd, margen):
    # Por anonimato, los IDs de cada persona solo duran un dia. Por eso, vamos a considerar a un cliente habitual si repite trayectos con el mismo horario y tienen mismo tipo
    # La idea es agrupar los que compartan salida, destino, hora de salida y grupo de edad, después comparar que tienen un tiempo de trayecto similar dentro del margen
    repeticiones_horario = rdd.map(lambda x: ((x[2],x[3], x[5].hour, x[6]) , x[4]) ).\
                           aggregateByKey(to_listas, lambda a, b : combinar_si_dentro_del_margen(a,b,margen)).\
                           flatMap(lambda x: x[1]).map(lambda x: x[1]).sort()
    return repeticiones_horario# Devuelve el numero de veces que se ha repetido cada trayecto por una misma persona                                                             



def pregunta1(rdd, n):
    
    def rutas_ordenadas(rdd):
        rutas_ordenadas = rdd.map(lambda x: ((x[2], x[3]),1)).\
            reduceByKey(lambda x, y: x+y).\
            sortBy(lambda x: x[1], ascending = False)     
        return rutas_ordenadas
    
    print('------------------------------1-------------------------------')
    
    rutas = rutas_ordenadas(rdd)
    print('Las', n, 'rutas mas repetidas son:')
    print(rutas.map(lambda x: x[0]).take(n))
    print('realizadas cada una este numero de veces:')
    print(rutas.map(lambda x: x[1]).take(n))

def pregunta2(rdd, n):

    def bicis_rotas(rdd):
        total = rdd.count()
        rotas = rdd.filter(lambda x: x[4]<60).count()
        return rotas, total, round(rotas/total, 4)
        
    print('------------------------------2-------------------------------')
    
    rotas, total, porciento = bicis_rotas(rdd)
    print('Este es el número de veces que alguien ha cogido una bici rota:')
    print(rotas)
    print('de un total de viajes de:')
    print(total, '('+str(porciento),'%)')
    
def pregunta3(rdd, n):
    
    def estaciones_ordenadas(rdd):
        Estaciones = rdd.flatMap(lambda x: [(x[2], 1), (x[3], 1)]).\
            reduceByKey(lambda x, y: x+y).\
            sortBy(lambda x: x[1], ascending = False)
        estacioneS = rdd.flatMap(lambda x: [(x[2], 1), (x[3], 1)]).\
            reduceByKey(lambda x, y: x+y).\
            sortBy(lambda x: x[1], ascending = True)
        return Estaciones, estacioneS
    
    print('------------------------------3-------------------------------')
    
    Estaciones, estacioneS = estaciones_ordenadas(rdd)
    print('Estas son las', n, 'estaciones más transitadas:')
    print(Estaciones.map(lambda x: x[0]).take(n))
    print('con este numero de usos cada una:')
    print(Estaciones.map(lambda x: x[1]).take(n))
    print('Además, estas son las', n, ' estaciones menos transitadas:')
    print(estacioneS.map(lambda x: x[0]).take(n))
    print('con este numero de usos cada una:')
    print(estacioneS.map(lambda x: x[1]).take(n))
    
def pregunta4(rdd, n):
    # Diferencia de llegada vs salida de cada estación
    def salidaVsEntrada(rdd):
        dif_por_estacion =  rdd.filter(lambda x: x[2]!=x[3]).\
                            flatMap(lambda x: [(x[2],-1),(x[3],1)]).\
                            reduceByKey(lambda x,y : x+y).\
                            sortBy(lambda x: x[1], ascending = False)
        return dif_por_estacion
    
    print('------------------------------4-------------------------------')
    
    bicis = salidaVsEntrada(rdd)
    print('Las estaciones con mayor superavit de bicicletas:')
    print(bicis.map(lambda x: x[0]).take(n))
    print('La cantidad de bicicletas que llegan superan a las que salen en:')
    print(bicis.map(lambda x: x[1]).take(n))
    
    print('Las estaciones con mayor déficit de bicicletas:')
    print(bicis.sortBy(lambda x: x[1], ascending = True).map(lambda x: x[0]).take(n))
    print('La cantidad de bicicletas que llegan superan a las que salen en:')
    print(bicis.sortBy(lambda x: x[1], ascending = True).map(lambda x: -x[1]).take(n))
    
    
def pregunta5(rdd, n):
    
    def horas_ordenadas(rdd):
        horas = rdd.map(lambda x: (x[5].hour, 1)).\
            reduceByKey(lambda x, y: x+y).\
            sortBy(lambda x: x[1], ascending = False)
        total = horas.map(lambda x: x[1]).sum() #total de viajes
        horas = horas.map(lambda x: (x[0], x[1]*100/total)) #cambio el total por porcentajes
        return horas
    
    print('------------------------------5-------------------------------')
    
    horas = horas_ordenadas(rdd)
    print('Las horas ordenadas en cuanto a mayor uso son:')
    print(horas.map(lambda x: x[0]).take(n))
    print('con porcentajes:')
    print(horas.map(lambda x: round(x[1], 4)).take(n))

def pregunta6(rdd, n):
    
    def edades_ordenadas(rdd):
        edades = rdd.map(lambda x: (user_ages[x[6]], 1)).\
            reduceByKey(lambda x, y: x+y).\
            sortBy(lambda x: x[1], ascending = False)
        total = edades.map(lambda x: x[1]).sum() #total de viajes
        edades = edades.map(lambda x: (x[0], x[1]*100/total)) #cambio el total por porcentajes
        return edades
    
    def tipos_ordenados(rdd):
        tipos = rdd.map(lambda x: (user_types[x[0]], 1)).\
            reduceByKey(lambda x, y: x+y).\
            sortBy(lambda x: x[1], ascending = False)
        total = tipos.map(lambda x: x[1]).sum() #total de viajes
        tipos = tipos.map(lambda x: (x[0], x[1]*100/total)) #cambio el total por porcentajes
        return tipos
    
    print('------------------------------6-------------------------------')
    
    edades = edades_ordenadas(rdd)
    print('Las edades de los usuarios ordenadas en cuanto a más uso son:')
    print(edades.map(lambda x: x[0]).collect())
    print('con porcentajes:')
    print(edades.map(lambda x: round(x[1], 4)).collect())
    
    tipos = tipos_ordenados(rdd)
    print('Los tipos de usuario ordenadas en cuanto a más uso son:')
    print(tipos.map(lambda x: x[0]).collect())
    print('con porcentajes:')
    print(tipos.map(lambda x: round(x[1], 4)).collect())
    

def main(dataset):
    with SparkContext() as sc:
        sc.setLogLevel("ERROR")
        
        rdd_base = sc.textFile(dataset) #Aqui leemos el archivo .json
        rdd = rdd_base.map(mapper) #Aplicamos la funcion anterior a todo el archivo
        n = 5
        
        pregunta1(rdd, n)
        
        pregunta2(rdd, n)
        
        pregunta3(rdd, n)
        
        pregunta5(rdd, n)
        
        pregunta6(rdd, n)    
        
        #pregunta7(rdd, n)
        
        
        
        
if __name__ == '__main__':
    if len(sys.argv)>1:
        dataset = sys.argv[1]
    main(dataset)
    #main('202103_movements.json')
