import redis
import json

# Conexion a la BBDD
conexionRedis = redis.ConnectionPool(host='localhost', port=6379, db=1,decode_responses=True)
client = redis.Redis(connection_pool=conexionRedis)

# Limpiamos la bbdd para posibles errores
client.flushdb()

# Funciones menu
def mostrar_menu():
    print("\n--- Menú de Ejercicios ---")
    print("1-18. Ejercicios")
    print("0. Salir")
    
def menu():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Selecciona una opción: "))
            if opcion == 0:
                ejecutar_opcion(opcion)
                break
            ejecutar_opcion(opcion)
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")

# Seccion de ejercicios --------------------------------------------------------------
def ejecutar_opcion(opcion):
    if opcion == 1:
        # 1. Crear registros clave-valor
        print("EJERCICIO 1 --------------------------------------------- ")

        client.set("sensor1", "activo")
        client.set("sensor2", "inactivo")
        print("Registros creados.")
        
    elif opcion == 2:
        # 2. Obtener y mostrar el número de claves registradas
        print("EJERCICIO 2 --------------------------------------------- ")

        num_keys = len(client.keys())
        print(f"Número de claves registradas: {num_keys}")

    elif opcion == 3:
        # 3. Obtener y mostrar un registro en base a una clave
        print("EJERCICIO 3 --------------------------------------------- ")

        value = client.get("sensor1")
        print(f"Registro obtenido: sensor1 -> {value}")

    elif opcion == 4:
        # 4. Actualizar el valor de una clave y mostrar el nuevo valor
        print("EJERCICIO 4 --------------------------------------------- ")

        client.set("sensor1", "inactivo")
        updated_value = client.get("sensor1")
        print(f"Registro actualizado: sensor1 -> {updated_value}")

    elif opcion == 5:
        # 5. Eliminar una clave-valor y mostrar la clave y el valor eliminado
        print("EJERCICIO 5 --------------------------------------------- ")

        deleted_value = client.get("sensor2")
        client.delete("sensor2")
        print(f"Registro eliminado: sensor2 -> {deleted_value}")

    elif opcion == 6:
        # 6. Obtener y mostrar todas las claves guardadas
        print("EJERCICIO 6 --------------------------------------------- ")

        all_keys = client.keys()
        print(f"Todas las claves: {all_keys}")

    elif opcion == 7:
        # 7. Obtener y mostrar todos los valores guardados
        print("EJERCICIO 7 --------------------------------------------- ")

        # Obtener todas las claves
        all_keys = client.keys()

        # Mostrar cada valor asociado a cada clave
        print("Valores almacenados en Redis:")
        for key in all_keys:
            value = client.get(key)  # Obtén el valor asociado a cada clave
            print(f"Clave: {key}, Valor: {value}")

    elif opcion == 8:
        # 8. Obtener registros con un patrón (*)
        print("EJERCICIO 8 --------------------------------------------- ")

        keys_with_pattern = client.keys("sensor*")
        print(f"Claves con patrón 'sensor*': {keys_with_pattern}")

    elif opcion == 9:
        # 9. Obtener registros con un patrón ([] - rangos)
        print("EJERCICIO 9 --------------------------------------------- ")

        keys_with_range = client.keys("sensor[1-3]")
        print(f"Claves con patrón 'sensor[1-3]': {keys_with_range}")

    elif opcion == 10:
        # 10. Obtener registros con un patrón (? - un solo carácter)
        print("EJERCICIO 10 --------------------------------------------- ")

        keys_with_single_char = client.keys("sensor?")
        print(f"Claves con patrón 'sensor?': {keys_with_single_char}")

    elif opcion == 11:
        # 11. Filtrar registros por un valor específico
        print("EJERCICIO 11 --------------------------------------------- ")

        filtered_records = {key: client.get(key) for key in client.keys() if client.get(key) == "inactivo"}
        print(f"Registros filtrados por valor 'inactivo': {filtered_records}")

    elif opcion == 12:
        # 12. Actualizar una serie de registros por un filtro
        print("EJERCICIO 12 --------------------------------------------- ")

        for key in client.keys():
            value = client.get(key)
            if value == "inactivo":
                client.set(key, "revisar")
        print("Registros actualizados.")

    elif opcion == 13:
        # 13. Eliminar una serie de registros en base a un filtro
        print("EJERCICIO 13 --------------------------------------------- ")

        for key in client.keys():
            if client.get(key) == "revisar":
                client.delete(key)
        print("Registros eliminados con filtro.")

    elif opcion == 14:
        # 14. Crear una estructura en JSON
        print("EJERCICIO 14 --------------------------------------------- ")

        data = {"id": 1, "status": "activo", "location": "zona norte"}
        client.set("sensor_json", json.dumps(data))
        print(f"Estructura JSON creada: {data}")

    elif opcion == 15:
        # 15. Filtrar por atributo en JSON
        print("EJERCICIO 15 --------------------------------------------- ")
        filtered_json = {}
        for key in client.keys():
            try:
                json_data = json.loads(client.get(key))
                if json_data.get("status") == "activo":
                    filtered_json[key] = json_data
            except json.JSONDecodeError:
                continue
        print(f"JSON filtrados por 'status=activo': {filtered_json}")

    elif opcion == 16:
        # 16. Crear una lista en Redis
        print("EJERCICIO 16 --------------------------------------------- ")

        client.delete("lista_sensores")  # Borrar si existe
        client.rpush("lista_sensores", "sensor1", "sensor2", "sensor3")
        print("Lista creada en Redis.")

    elif opcion == 17:
        # 17. Obtener elementos de una lista con un filtro
        print("EJERCICIO 17 --------------------------------------------- ")

        lista = client.lrange("lista_sensores", 0, -1)
        filtered_list = [item for item in lista if "2" in item]
        print(f"Elementos filtrados en la lista: {filtered_list}")

    elif opcion == 18:
        # 18. Usar otros tipos de datos en Redis (Set y Hash)
        print("EJERCICIO 18 --------------------------------------------- ")

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

    elif opcion == 0:
        print("Saliendo del programa. ¡Hasta luego!")
    else:
        print("Opción no válida. Por favor, elige una opción entre 0 y 18.")

# Ejecutar el menú
menu()




