import psutil
import subprocess
import asyncio
import imaplib



def terminar_proceso_por_nombre(nombre_proceso):
    for proceso in psutil.process_iter():
        try:
            if proceso.name() == nombre_proceso:
                terminar_proceso_por_pid(proceso.pid)
                return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as ex:
            print(f"No se puede acceder al proceso: {ex.name}")
    print(f"No se encontró ningún proceso con el nombre: {nombre_proceso}")

def terminar_proceso_por_pid(pid):
    try:
        proceso = psutil.Process(pid)
        proceso.terminate()
        print(f"El proceso {pid} ha sido eliminado")

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        print(f"No se puede acceder al proceso: {e.name}")
    except psutil.TimeoutExpired:
        print(f"El proceso {pid} no ha terminado a tiempo")

def  ejecutar_programa_sincrono():
    try:
        subprocess.run(['calc.exe',])

    except subprocess.CalledProcessError as e:
        print(e.output)

async def ejecutar_programa_asincrono():
    try:
        await asyncio.create_subprocess_exec("calc.exe")
    except subprocess.CalledProcessError as e:
        print(e.output)

def comunicacion_entre_servidores():
    try:
        servidor ="test.rebex.net"
        puerto = 143
        usuario = "demo"
        password = "password"

        mail = imaplib.IMAP4(servidor, puerto)
        print("\nConexión establecida con el servidor IMAP.")


        mail.login(usuario, password)
        print("Has iniciado sesión correctamente.")

        status, carpetas = mail.list()
        if status == 'OK':
            print("\nCarpetas en el correo:")
            for carpeta in carpetas:
                print(carpeta.decode())
        else:
            print("No se puede obtener la lista de carpetas.")

        status, mensajes= mail.select("INBOX", readonly=True)
        if status == 'OK':
            print("\nBandeja de entrada 'INBOX' seleccionada correctamente.")
        else:
            print("No se puede seleccionar la bandeja de entrada.")

        mail.close()
        mail.logout()
        print("Se ha desconectado del servidor IMAP.")

    except imaplib.IMAP4.error as e:
        print(f"Error en la conexión IMAP: {e}")

async def main():
    # FUNCION SÍNCRONA
    print("\nInicio de la función síncrona:")
    ejecutar_programa_sincrono()
    print("Fin de la función síncrona")

    # FUNCION ASÍNCRONA
    print("\nInicio de la función asincrona:")
    await ejecutar_programa_asincrono()
    print("Fin de la función asincrona")

 

if __name__ == "__main__":
    while True:
        print("\n            ----- Menú -----")
        print("1 - Mostrar TODA la lista de los procesos en ejecución")
        print("2 - Eliminar un proceso en ejecución")
        print("3 - Ejecución Síncrona y Asíncrona de Tareas")
        print("4 - Comunicación entre procesos")
        print("5 - Salir")
        
        opcion = int(input("Introduce una opción: "))

        if opcion == 1:
            try:
                for proceso in psutil.process_iter():
                    try:
                        nombre_proceso = proceso.name()
                        id_proceso = proceso.pid
                        prioridad = proceso.nice()
                        directorio_actual = proceso.cwd()

                        print("\n Información del proceso: ")
                        print(f"Nombre del proceso: {nombre_proceso}")
                        print(f"ID del proceso: {id_proceso}")
                        print(f"Prioridad del proceso: {prioridad}")
                        print(f"Directorio actual del proceso: {directorio_actual}")
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as ex:
                        print(f"No se puede acceder al proceso: {ex}")
            except Exception as ex:
                print(f"Error al obtener los procesos: {ex}")
        
        elif opcion == 2:
            respuesta = input("\n¿Desea eliminar un proceso? (s/n): ")
            if respuesta.lower() == 's':
                pid_o_nombre = input("\nIntroduce el PID o el nombre del proceso a eliminar: ")

                if pid_o_nombre.isdigit():
                    pid = int(pid_o_nombre)
                    terminar_proceso_por_pid(pid)
                else:
                    terminar_proceso_por_nombre(pid_o_nombre)
            else:
                print("No se ha eliminado ningún proceso.")

        elif opcion == 3:
            asyncio.run(main())  
        elif opcion==4:
            comunicacion_entre_servidores()
        elif opcion == 5:
            print("Adiós")
            break
        else:
            print("Opción no válida")