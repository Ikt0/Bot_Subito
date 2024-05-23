import json
import time
import requests
from playsound import playsound
from config_subito import config
from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup
import os

def print_logo():
    print("""
┏┓  ┓ •     ┳┓     ┓ ┏━
┗┓┓┏┣┓┓╋┏┓  ┣┫┏┓╋  ┃ ┗┓
┗┛┗┻┗┛┗┗┗┛  ┻┛┗┛┗  ┻•┗┛
""")
#tmplr
    
def clear_CMD():
    try:
        os.system('cls')
        pass
    except:
        print("Error running command")
        pass

def restart_graphics():
    clear_CMD()
    print_logo()

restart_graphics()

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
descrizione varchar(500),
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
old_price = []
latest_price=[]

results_array=["title","desc","price","is_sold"]


while True:
    try:
        reserch_results = esegui_ricerca()
        latest_price=reserch_results[0]["price"]
    except:
        print("Impossibile effettuare la ricerca")
    if iterazioni >= 1:
        if latest_price == old_price:
            restart_graphics()
            print(f"{GetTime()} Nessuna novità, ultimo prezzo: {latest_price}, Titolo: {reserch_results[0]['title']}", end="\r")
            # conn.execute(f"INSERT INTO andamento (prezzo,titolo,descrizione,is_sold,data) VALUES({int(latest_price.split(' ')[0])},'SAME','{reserch_results[0]['title']}','{reserch_results[0]['desc']}','{reserch_results[0]['is_sold']}')")
            # conn.commit()
            # for elem in reserch_results:
            #     print(elem["title"],elem["price"],elem["is_sold"])
            # print("__________________________________________________________")
            # print(latest_price,old_price)
        elif latest_price != old_price and int(latest_price.split(' ')[0]) <= config.get("maxPrezzo"):
            restart_graphics()
            print(f"{GetTime()} Novità trovata!")
            print(f"{GetTime()} Nuovo Prezzo: {latest_price}, Titolo: {reserch_results[0]['title']}, Descrizione: {reserch_results[0]['desc']}")
            playsound("cash.mp3")
            conn.execute(f"INSERT INTO andamento (prezzo, titolo, descrizione, is_sold, data) VALUES ({int(latest_price.split(' ')[0])}, 'GOOD', '{reserch_results[0]['title']}', '{reserch_results[0]['desc']}', '{reserch_results[0]['is_sold']}')")
            conn.commit()
            old_price = latest_price
        elif latest_price != old_price and int(latest_price.split(' ')[0]) > config.get("maxPrezzo"):
            restart_graphics()
            print(f"{GetTime()} Novità trovata ma il prezzo è troppo alto!")
            print(f"{GetTime()} Prezzo: {latest_price}, Titolo: {reserch_results[0]['title']}")
            playsound("cash.mp3")
            conn.execute(f"INSERT INTO andamento (prezzo, titolo, descrizione, is_sold, data) VALUES ({int(latest_price.split(' ')[0])}, 'TOO_HIGH', '{reserch_results[0]['title']}', '{reserch_results[0]['desc']}', '{reserch_results[0]['is_sold']}')")
            conn.commit()
            old_price = latest_price
    else:
        print(f"{GetTime()} Prima iterazione...")
        conn.execute(f"INSERT INTO andamento (prezzo,titolo,descrizione,is_sold,data) VALUES({int(latest_price.split(' ')[0])},'SAME','{reserch_results[0]['title']}','{reserch_results[0]['desc']}','{reserch_results[0]['is_sold']}')")
        conn.commit()
    old_price = reserch_results[0]["price"]
    iterazioni += 1
    time.sleep(intervallo_ricerca)
