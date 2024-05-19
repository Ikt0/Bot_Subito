import time
import requests
from playsound import playsound
from configSubitoBot import config
from datetime import datetime

print("""
   _____       _     _ _          ____        _     __   ___  
  / ____|     | |   (_) |        |  _ \      | |   /_ | / _ \ 
 | (___  _   _| |__  _| |_ ___   | |_) | ___ | |_   | || | | |
  \___ \| | | | '_ \| | __/ _ \  |  _ < / _ \| __|  | || | | |
  ____) | |_| | |_) | | || (_) | | |_) | (_) | |_   | || |_| |
 |_____/ \__,_|_.__/|_|\__\___/  |____/ \___/ \__|  |_(_)___/ 
 By Ikto                                                            
                                                              
""")

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
            print(f"{GetTime()} Nessuna novità...",end="\r")
        elif result_prices[0]>=config.get("maxPrezzo"):
            print(f"{GetTime()} Novità trovata!")
            print(f"{GetTime()} Nuovo Prezzo",result_prices[0])
            playsound("cash.mp3")
        elif result_prices[0]<config.get("maxPrezzo"):
            print(f"{GetTime()} Novità trovata ma il prezzo è troppo alto!")
            print(f"{GetTime()} Prezzo:",result_prices[0])
            playsound("cash.mp3")  
    else:
        print(f"{GetTime()} Prima iterazione...",end="\r")
    # print(f"{GetTime()} Prezzi trovati precedentemente {old_prices}")
    # print(f"{GetTime()} Nuovi prezzi {result_prices}")
    old_prices=result_prices
    result_prices=[]
    time.sleep(intervallo)
    iterazioni+=1