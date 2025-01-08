import redis
conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=0,decode_responses=True)
baseDatosRedis = redis.Redis(connection_pool=conexionRedis)

baseDatosRedis.flushdb()
# Meter registros
baseDatosRedis.set('libro_1', 'Quijote')
baseDatosRedis.set('libro_2', 'Hamlet', ex=100)

#Obtener el valor de la clave "libro_1" pero en binario:
print(baseDatosRedis.get("libro_1"))
#Obtener el valor de la clave "libro_1" pero en String
#baseDatosRedis.get("libro_1").decode("utf-8")
#Obtener el valor de la clave "libro_2" que al tener tiempo de vida estará ya vacía
print(baseDatosRedis.get("libro_2"))
#Actualizar un valor 
baseDatosRedis.set("libro_1","El señor de los anillos")
#Para eliminar claves-valor de la base de datos:
baseDatosRedis.delete("libro_1")
baseDatosRedis.delete("libro_2")
#Para obtener todas las claves de una base de datos redis:
claves = baseDatosRedis.keys()
#Si queremos mostrar la información de todas las claves:
for clave in claves:
 	print('Clave:', clave , ' y Valor: ', baseDatosRedis.get(clave))
baseDatosRedis.set("libro_1","Quijote")
baseDatosRedis.set("libro_2","Hamlet")
baseDatosRedis.set("libro_3","Otelo")
baseDatosRedis.set("comic_1","Mortadelo y Filemón")
baseDatosRedis.set("comic_2","Superman")

print("Los Libros:")
for clave in baseDatosRedis.scan_iter('libro*'):
   print(clave)
  
print("Los Comics:")   
for clave in baseDatosRedis.scan_iter('comic*'):
   print(clave)
#Podemos guardar archivos JSON en nuestra base de datos Redis:
res1 = baseDatosRedis.json().set("usuarios:1", "$", {"nombre": "Jorge", "apellido": "Baron", "edad": 37})
res2 = baseDatosRedis.json().set("usuarios:2", "$", {"nombre": "Lucía", "apellido": "Benitez", "edad": 24})
#O podemos guardar un array de datos en json:
baseDatosRedis.json().set("usuarios_array", "$", [])
res3 = baseDatosRedis.json().arrappend("usuarios_array", "$", {"nombre": "Pepe", "apellido": "Sanchez", "edad": 45})
res4 = baseDatosRedis.json().arrappend("usuarios_array", "$", {"nombre": "Calisto", "apellido": "Melibea", "edad": 67})
#Podemos tener listas en redis también:
#Añadimos a la lista:
baseDatosRedis.lpush("usuarios:hobbies", "futbol:1") 
baseDatosRedis.lpush("usuarios:hobbies", "tenis:2")
baseDatosRedis.lpush("usuarios:hobbies", "rugby:2") 
#Obtener todos los elementos:
print(baseDatosRedis.lrange("usuarios:hobbies",0,-1))
#Obtener el primer elemento y eliminarlo:
baseDatosRedis.rpop("usuarios:hobbies")
