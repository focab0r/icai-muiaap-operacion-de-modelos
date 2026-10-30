import requests
import json
from dotenv import load_dotenv
import os


PLACE = "MADRID, CIUDAD UNIVERSITARIA"
FECHAINISTR = "2019-10-01T00:00:00UTC"
FECHAFINSTR = "2019-10-30T23:59:59UTC"


if __name__ == "__main__":

    load_dotenv(".env")
    api_key = os.getenv("api_key")
    if api_key == None or api_key == "MY_API_KEY":
        Exception("[X] ERROR: Please add the api_key to the env")

    # First API
    headers = {"api_key": api_key}

    url_link = "https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones"

    r = requests.get(url_link, headers=headers)             # Get the URL that contains the "indicativo"
    if r.status_code != 200:
        Exception(f"[X] ERROR: Error code {r.status}")
    r_parsed = json.loads(r.content)
    url_stations = r_parsed["datos"]

    r = requests.get(url_stations, headers=headers)         # Get the "indicativo"
    if r.status_code != 200:
        Exception(f"[X] ERROR: Error code {r.status}")
    r_parsed = json.loads(r.content.decode('latin-1'))


    indicativo = 0
    for elem in r_parsed:
        if elem['nombre'] == PLACE:
            indicativo  = elem['indicativo']
            break


    # Second API

    print(f"[+] Indicativo: {indicativo}")
    print(f"[*] fechaIniStr: {FECHAINISTR}")
    print(f"[*] fechaFinStr: {FECHAFINSTR}")

    url_meteo = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{FECHAINISTR}/fechafin/{FECHAFINSTR}/estacion/{indicativo}"

    r = requests.get(url_meteo, headers=headers)            # Get the URL that contains the meteo data
    if r.status_code != 200:
        Exception(f"[X] ERROR: Error code {r.status}")
    r_parsed = json.loads(r.content)
    url_meteo_station = r_parsed["datos"]

    r = requests.get(url_meteo_station, headers=headers)    # Get meteo data
    r_parsed = json.loads(r.content.decode('latin-1'))

    print(f"[+] Printing meteo for {PLACE}...")
    for elem in r_parsed:
        print(elem)

    print("[+++] Done")