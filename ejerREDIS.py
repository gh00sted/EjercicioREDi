import redis
import json

conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=1,decode_responses=True)
client = redis.Redis(connection_pool=conexionRedis)
client.flushdb()

# 1. Crear registros clave-valor
print("EJERCICIO 1 --------------------- ")

client.set("sensor1", "activo")
client.set("sensor2", "inactivo")
print("Registros creados.")

# 2. Obtener y mostrar el número de claves registradas
print("EJERCICIO 2 --------------------- ")

num_keys = len(client.keys())
print(f"Número de claves registradas: {num_keys}")

# 3. Obtener y mostrar un registro en base a una clave
print("EJERCICIO 3 --------------------- ")

value = client.get("sensor1")
print(f"Registro obtenido: sensor1 -> {value}")

# 4. Actualizar el valor de una clave y mostrar el nuevo valor
client.set("sensor1", "inactivo")
updated_value = client.get("sensor1")
print(f"Registro actualizado: sensor1 -> {updated_value}")

# 5. Eliminar una clave-valor y mostrar la clave y el valor eliminado
deleted_value = client.get("sensor2")
client.delete("sensor2")
print(f"Registro eliminado: sensor2 -> {deleted_value}")

# 6. Obtener y mostrar todas las claves guardadas
all_keys = client.keys()
print(f"Todas las claves: {all_keys}")

# 7. Obtener y mostrar todos los valores guardados
# Obtener todas las claves
all_keys = client.keys()

# Mostrar cada valor asociado a cada clave
print("Valores almacenados en Redis:")
for key in all_keys:
    value = client.get(key)  # Obtén el valor asociado a cada clave
    print(f"Clave: {key}, Valor: {value}")

# 8. Obtener registros con un patrón (*)
keys_with_pattern = client.keys("sensor*")
print(f"Claves con patrón 'sensor*': {keys_with_pattern}")

# 9. Obtener registros con un patrón ([] - rangos)
keys_with_range = client.keys("sensor[1-3]")
print(f"Claves con patrón 'sensor[1-3]': {keys_with_range}")

# 10. Obtener registros con un patrón (? - un solo carácter)
keys_with_single_char = client.keys("sensor?")
print(f"Claves con patrón 'sensor?': {keys_with_single_char}")

# 11. Filtrar registros por un valor específico
filtered_records = {key: client.get(key) for key in client.keys() if client.get(key) == "inactivo"}
print(f"Registros filtrados por valor 'inactivo': {filtered_records}")

# 12. Actualizar una serie de registros por un filtro
for key in client.keys():
    value = client.get(key)
    if value == "inactivo":
        client.set(key, "revisar")
print("Registros actualizados.")

# 13. Eliminar una serie de registros en base a un filtro
for key in client.keys():
    if client.get(key) == "revisar":
        client.delete(key)
print("Registros eliminados con filtro.")

# 14. Crear una estructura en JSON
data = {"id": 1, "status": "activo", "location": "zona norte"}
client.set("sensor_json", json.dumps(data))
print(f"Estructura JSON creada: {data}")

# 15. Filtrar por atributo en JSON
filtered_json = {}
for key in client.keys():
    try:
        json_data = json.loads(client.get(key))
        if json_data.get("status") == "activo":
            filtered_json[key] = json_data
    except json.JSONDecodeError:
        continue
print(f"JSON filtrados por 'status=activo': {filtered_json}")

# 16. Crear una lista en Redis
client.delete("lista_sensores")  # Borrar si existe
client.rpush("lista_sensores", "sensor1", "sensor2", "sensor3")
print("Lista creada en Redis.")

# 17. Obtener elementos de una lista con un filtro
lista = client.lrange("lista_sensores", 0, -1)
filtered_list = [item for item in lista if "2" in item]
print(f"Elementos filtrados en la lista: {filtered_list}")

# 18. Usar otros tipos de datos en Redis (Set y Hash)
# Crear un Set
client.sadd("set_sensores", "sensorA", "sensorB", "sensorC")
print("Set creado:", client.smembers("set_sensores"))

# Crear un Hash
client.hset("hash_sensorA", mapping={"status": "activo", "zona": "central"})
print("Hash creado:", client.hgetall("hash_sensorA"))

# Obtener elementos del Set y del Hash
set_members = client.smembers("set_sensores")
hash_values = client.hgetall("hash_sensorA")
print(f"Elementos del Set: {set_members}")
print(f"Valores del Hash: {hash_values}")
