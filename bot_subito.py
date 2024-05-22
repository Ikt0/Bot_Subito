import json
import time
import requests
from playsound import playsound
from config_subito import config
from datetime import datetime
import sqlite3
from pathlib import os
from bs4 import BeautifulSoup

print("""
   _____       _     _ _          _           _     __   ___  
  / ____|     | |   (_) |        | |         | |   /_ | |__ \ 
 | (___  _   _| |__  _| |_ ___   | |__   ___ | |_   | |    ) |
  \___ \| | | | '_ \| | __/ _ \  | '_ \ / _ \| __|  | |   / / 
  ____) | |_| | |_) | | || (_) | | |_) | (_) | |_   | |_ / /_ 
 |_____/ \__,_|_.__/|_|\__\___/  |_.__/ \___/ \__|  |_(_)____|
 By Ikto                                                            
""")

url_ricerca = config.get("url_ricerca")
maxPrezzo = config.get("maxPrezzo")
intervallo_ricerca = config.get("intervallo_ricerca")

def esegui_ricerca():

    response = requests.get(url_ricerca)
    response_content = response.text

    html_content = BeautifulSoup(response_content, "html.parser")

    scripts = html_content.find_all("script")
    json_content = json.loads(scripts[27].text)

    results = []
    for i in range(len(json_content["props"]["pageProps"]["initialState"]["items"]["list"])):
        try:
            title = json_content["props"]["pageProps"]["initialState"]["items"]["list"][i]["item"]["subject"]
            desc = json_content["props"]["pageProps"]["initialState"]["items"]["list"][i]["item"]["body"]
            price = json_content["props"]["pageProps"]["initialState"]["items"]["list"][i]["item"]["features"]["/price"]["values"][0]["value"]
        except:
            print("Non è stato possibile estrarre i dati")

        try:
            is_sold = json_content['props']['pageProps']['initialState']['items']['list'][i]['item']['features']['/transaction_is_sold']['values'][0]['value']
        except:
            is_sold = "DISPONIBILE"

        if is_sold!="DISPONIBILE":
            is_sold = "VENDUTO"

        results.append({"title": title,"desc": desc,"price": price,"is_sold": is_sold})

    return results


conn = sqlite3.connect("subito.db")

def create_sqlite_database(filename):
    """ create a database connectionto an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        conn.executescript("""
CREATE TABLE IF NOT EXISTS andamento (
item_number INTEGER PRIMARY KEY AUTOINCREMENT,
prezzo INT,
titolo varchar(50),
descrizione varchar(50),
is_sold varchar(50),
data timestamp default CURRENT_TIMESTAMP
);""")
        # print(f"sqllite ver: {sqlite3.sqlite_version}")
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_sqlite_database("subito.db")

def GetTime():
    return str(datetime.now())[:16]


iterazioni = 0
old_prices = []
result_prices=[]

results_array=["title","desc","price","is_sold"]


while True:
    reserch_results = esegui_ricerca()
    if iterazioni >= 1:
        if set(result_prices) == set(old_prices):
            print(f"{GetTime()} Nessuna novità, ultimo prezzo: {reserch_results[0]['price']}, Titolo: {reserch_results[0]['title']}", end="\r")
            # conn.execute(f"INSERT INTO andamento (prezzo,titolo,descrizione,is_sold,data) VALUES({int(reserch_results[0]['price'].split(' ')[0])},'SAME','{reserch_results[0]['title']}','{reserch_results[0]['desc']}','{reserch_results[0]['is_sold']}')")
            # conn.commit()
        elif set(result_prices) != set(old_prices) and int(reserch_results[0]['price'].split(' ')[0]) <= config.get("maxPrezzo"):
            print(f"{GetTime()} Novità trovata!")
            print(f"{GetTime()} Nuovo Prezzo: {reserch_results[0]['price']}, Titolo: {reserch_results[0]['title']}, Descrizione: {reserch_results[0]['desc']}")
            # playsound(os.path.abspath("cash.mp3"))
            conn.execute(f"INSERT INTO andamento (prezzo, titolo, descrizione, is_sold, data) VALUES ({int(reserch_results[0]['price'].split(' ')[0])}, 'GOOD', '{reserch_results[0]['title']}', '{reserch_results[0]['desc']}', '{reserch_results[0]['is_sold']}')")
            conn.commit()
            old_prices = result_prices
        elif set(result_prices) != set(old_prices) and int(reserch_results[0]['price'].split(' ')[0]) > config.get("maxPrezzo"):
            print(f"{GetTime()} Novità trovata ma il prezzo è troppo alto!")
            print(f"{GetTime()} Prezzo: {reserch_results[0]['price']}, Titolo: {reserch_results[0]['title']}")
            # playsound(os.path.abspath("cash.mp3"))
            conn.execute(f"INSERT INTO andamento (prezzo, titolo, descrizione, is_sold, data) VALUES ({int(reserch_results[0]['price'].split(' ')[0])}, 'TOO_HIGH', '{reserch_results[0]['title']}', '{reserch_results[0]['desc']}', '{reserch_results[0]['is_sold']}')")
            conn.commit()
            old_prices = result_prices
    else:
        print(f"{GetTime()} Prima iterazione...")
        conn.execute(f"INSERT INTO andamento (prezzo,titolo,descrizione,is_sold,data) VALUES({int(reserch_results[0]['price'].split(' ')[0])},'SAME','{reserch_results[0]['title']}','{reserch_results[0]['desc']}','{reserch_results[0]['is_sold']}')")
        conn.commit()
    old_prices = result_prices
    time.sleep(intervallo_ricerca)
    iterazioni += 1
