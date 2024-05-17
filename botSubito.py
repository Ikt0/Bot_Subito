import time
import requests
from playsound import playsound
from configSubitoBot import config
from datetime import datetime

url = config.get("urlRicerca")
stringa_ricerca=config.get("stringaRicerca")
intervallo=config.get("intervalloRicerca")
# print(f"Testo da ricercare {stringa_ricerca}")
response = requests.get(url)
response_content = response.text
def GetTime():
    return str(datetime.now())[:16]

result_prices=[]

def EseguiRicerca():
    start_index=0
    numero_risultati=0
    while True:
        found_result_index = response_content.lower().find(stringa_ricerca.lower(), start_index)
        # print(f"found_result_index {found_result_index}")
        if found_result_index == -1:
            # print("---------------")
            # print("FINE RICERCA")
            # print("Sono stati trovati", numero_risultati, "risultati")
            # print(result_prices)
            break
        else:
            numero_risultati += 1
        start_index = found_result_index + len(stringa_ricerca)
        # print(f"start_index {start_index}")
        snippet_start = found_result_index
        # print(response_content[snippet_start+len(stringa_ricerca)+2:snippet_start+len(stringa_ricerca)+10])
        result_to_append=(response_content[snippet_start+len(stringa_ricerca)+2:snippet_start+len(stringa_ricerca)+10])
        # print(result_to_append.replace('\xa0', ' ').split(" ")[0])
        result_prices.append(result_to_append.replace('\xa0', ' ').split(" ")[0])


iterazioni = 0
old_prices=[]
while True:
    EseguiRicerca()
    if iterazioni >=1:
        if  result_prices == old_prices:
            print(f"{GetTime()} Nessuna novità...")
        elif result_prices[0]>=300:
            print(f"{GetTime()} Novità trovata!")
            print(f"{GetTime()} Nuovo Prezzo",result_prices[0])
            playsound("cash.mp3")
    else:
        print(f"{GetTime()} Prima iterazione...")
    # print(f"{GetTime()} Prezzi trovati precedentemente {old_prices}")
    # print(f"{GetTime()} Nuovi prezzi {result_prices}")
    old_prices=result_prices
    result_prices=[]
    time.sleep(intervallo)
    iterazioni+=1