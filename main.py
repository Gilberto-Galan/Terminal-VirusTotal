import requests
from openpyxl import Workbook
import os


from Modulos.modulo2 import  plot_results 
from Modulos.modulo1 import scan_url, scan_file



def export_to_excel(scan_id, result):
    workbook = Workbook()
    sheet = workbook.active

    sheet.title = 'Results'
    sheet['A1'] = 'Antivirus'
    sheet['B1'] = 'Resultado'

    for index, (antivirus, verdict) in enumerate(result['scans'].items(), start=2):
        sheet[f'A{index}'] = antivirus
        sheet[f'B{index}'] = verdict['result']

    
    ruta_guardado_excel = os.path.join('Registro en XLS', f'results_{scan_id}.xlsx')
    workbook.save(ruta_guardado_excel)
    print(f"Resultados guardados en results_{scan_id}.xlsx")

def get_report(scan_id):
    url = f'https://www.virustotal.com/vtapi/v2/file/report'
    params = {'apikey': API_KEY, 'resource': scan_id}

    response = requests.get(url, params=params)
    result = response.json()

    if result['response_code'] == 1:
        print("Resultados del escaneo:")
        for antivirus, verdict in result['scans'].items():
            print(f"{antivirus}: {verdict['result']}")

        positives = result['positives']
        if positives > 0:
            print(
                f"¡Alerta! Este archivo ha sido detectado por {positives} motores antivirus.")
        else:
            print(
                "El archivo no ha sido detectado como malicioso por ningún motor antivirus.")

        export_to_excel(scan_id, result)
    else:
        print("Error al obtener el informe:", result['verbose_msg'])


# Ruta a escanear el archivo
ruta_a_escanear = ' '


# Lectura de la API-Key en el archivo
nombre_archivo = "API-Key\\API-Key.txt"

try:
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read()

    # Se utiliza la API-Key de VirusTotal
    API_KEY = str(contenido)

except FileNotFoundError:
    print(f"El archivo '{nombre_archivo}' no se encontró.")
except Exception as e:
    print(f"Ocurrió un error: {e}")



menu = True
while menu:
        opcion = input("Selecciona una opción: \n1)Escanear archivo \n2)Escanear URL \n3)Ver gráfica \n")

        if opcion == '1':
            archivo_a_escanear = ruta_a_escanear  # Reemplaza con la ruta de tu archivo
            scan_id = scan_file(archivo_a_escanear)
        elif opcion == '2':
            url_a_escanear = input("Ingresa la URL a escanear: ")
            scan_id = scan_url(url_a_escanear)
        elif opcion == '3':
            plot_results(int(input("Ingrese la cantidad de motores que detectaron el archivo: ")),
                         int(input("Ingrese la cantidad de motores que no detectaron el archivo: ")),
                         export_image=True)
        else:
            print("Opción no válida.")
            exit()

        if opcion in ('1', '2'):
            # Espera un tiempo razonable para que se complete el escaneo
            input("Presiona Enter después de esperar un tiempo razonable...")

            # Obtén el informe utilizando el ID del escaneo
            get_report(scan_id)

        again = int(input("Desea hacer otro scan\n1. Si\n2. No\nIngrese una opcion: "))
        if again !=1:
            menu=False



