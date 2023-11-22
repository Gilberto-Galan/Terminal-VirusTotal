import requests
API_KEY = '7924abb6c3182a773c997a0cc2336169c82b9a5e48a990c411d0dd5aadde6f9c'


def scan_file(file_path):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'

    try:
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file)}
            params = {'apikey': API_KEY}

            response = requests.post(url, files=files, params=params)
            result = response.json()

            print(result)  # Imprime la respuesta para diagnosticar

            if 'response_code' in result and result['response_code'] == 1:
                print("Escaneo exitoso. ID del escaneo:", result['scan_id'])
                return result['scan_id']
            else:
                print("Error en el escaneo:", result.get(
                    'verbose_msg', 'No se proporcionó un mensaje de error.'))
                return None
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no fue encontrado.")
        return None
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return None


def scan_url(url):
    url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    params = {'apikey': API_KEY, 'url': url}

    response = requests.post(url, params=params)
    result = response.json()

    if result['response_code'] == 1:
        print("Escaneo exitoso. ID del escaneo:", result['scan_id'])
        return result['scan_id']
    else:
        print("Error en el escaneo:", result['verbose_msg'])
        return None
    

