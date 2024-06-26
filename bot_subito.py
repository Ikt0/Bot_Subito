import json
import time
import requests
from playsound import playsound
#playsound 1.2.2
from config_subito import config
from datetime import datetime
import sqlite3
from bs4 import BeautifulSoup
import os
from visualizzazione_dati import data_graph

def print_logo():
    print("""
┏┓  ┓ •     ┳┓     ┓ ┏━
┗┓┓┏┣┓┓╋┏┓  ┣┫┏┓╋  ┃ ┗┓
┗┛┗┻┗┛┗┗┗┛  ┻┛┗┛┗  ┻•┗┛
by. Ikto
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
max_prezzo = config.get("max_prezzo")
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
            title = json_content["props"]["pageProps"]["initialState"]["items"]["list"][i]["item"]["subject"].replace("'","")
            try:
                desc = json_content["props"]["pageProps"]["initialState"]["items"]["list"][i]["item"]["body"].replace("'","")
            except:
                desc= "Descrizione non disponibile"
            try:
                price = json_content["props"]["pageProps"]["initialState"]["items"]["list"][i]["item"]["features"]["/price"]["values"][0]["value"]
            except:
                price = "0 €"
        except:
            print("Non è stato possibile estrarre i dati")

        try:
            is_sold = json_content['props']['pageProps']['initialState']['items']['list'][i]['item']['features']['/transaction_status']['values'][0]['value']
        except:
            is_sold = "Disponibile"

        if is_sold!="Disponibile":
            is_sold = "Venduto"

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
descrizione varchar(1000),
status varchar(50),
is_sold varchar(50),
data timestamp default CURRENT_TIMESTAMP
);""")
        # print(f"sqllite ver: {sqlite3.sqlite_version}")
        if config.get("clear_database_on_startup").lower()=="true":
            conn.execute("""DELETE FROM andamento""")
            conn.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_sqlite_database("subito.db")

def get_time():
    return str(datetime.now())[:16]

def plot_data():
    try:
        cur = conn.cursor()
        cur.execute("""SELECT item_number,prezzo FROM andamento""")

        risultato=cur.fetchall()

        data_graph(risultato)
    except:
        print("Plotting non disponibile")


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
            print(f"{get_time()} Nessuna novità\n-----\nUltimo articolo:\n-----")
            print(f"Titolo:\n{reserch_results[0]['title']}\n-----")
            print(f"Prezzo:\n{latest_price}\n-----")
            print(f"Descrizione:\n{reserch_results[0]['desc'].replace("'","")}\n-----")
            print(f"Disponibilità:\n{reserch_results[0]['is_sold']}\n-----")
            # conn.execute(f"INSERT INTO andamento (prezzo,titolo,descrizione,is_sold,data) VALUES({int(latest_price.split(' ')[0])},'SAME','{reserch_results[0]['title']}','{reserch_results[0]['desc'].replace("'","")}','{reserch_results[0]['is_sold']}')")
            # conn.commit()
            # for elem in reserch_results:
            #     print(elem["title"],elem["price"],elem["is_sold"])
            # print("__________________________________________________________")
            # print(latest_price,old_price)
            if config.get("plot_data").lower()=="true":
                plot_data()#da commentare per non creare un diagramma dei prezzi
                
        elif latest_price != old_price and int(latest_price.split(' ')[0]) <= config.get("max_prezzo"):
            restart_graphics()
            print(f"Titolo:\n{reserch_results[0]['title']}\n-----")
            print(f"Prezzo:\n{latest_price}\n-----")
            print(f"Descrizione:\n{reserch_results[0]['desc'].replace("'","")}\n-----")
            print(f"Disponibilità:\n{reserch_results[0]['is_sold']}\n-----")
            playsound("cash.mp3")
            conn.execute(f"INSERT INTO andamento (prezzo, titolo, descrizione, is_sold, status, data) VALUES ({int(latest_price.split(' ')[0])}, '{reserch_results[0]['title']}', '{reserch_results[0]['desc'].replace("'","")}', '{reserch_results[0]['is_sold']}', 'GOOD', '{get_time()}')")
            conn.commit()
            old_price = latest_price
        elif latest_price != old_price and int(latest_price.split(' ')[0]) > config.get("max_prezzo"):
            restart_graphics()
            print(f"{get_time()} Novità trovata ma il prezzo è troppo alto!\n-----")
            print(f"Titolo:\n{reserch_results[0]['title']}\n-----")
            print(f"Prezzo:\n{latest_price}\n-----")
            print(f"Descrizione:\n{reserch_results[0]['desc'].replace("'","")}\n-----")
            print(f"Disponibilità:\n{reserch_results[0]['is_sold']}\n-----")
            playsound("cash.mp3")
            conn.execute(f"INSERT INTO andamento (prezzo, titolo, descrizione, is_sold, status, data) VALUES ({int(latest_price.split(' ')[0])}, '{reserch_results[0]['title']}', '{reserch_results[0]['desc'].replace("'","")}', '{reserch_results[0]['is_sold']}', 'TOO_HIGH', '{get_time()}')")
            conn.commit()
            old_price = latest_price
    else:
        print(f"{get_time()} Prima iterazione, attendi {intervallo_ricerca} secondi...")
        conn.execute(f"INSERT INTO andamento (prezzo, titolo, descrizione, is_sold, status, data) VALUES ({int(latest_price.split(' ')[0])}, '{reserch_results[0]['title']}', '{reserch_results[0]['desc']}', '{reserch_results[0]['is_sold']}', 'SAME', '{get_time()}')")
        conn.commit()
    old_price = reserch_results[0]["price"]
    iterazioni += 1
    time.sleep(intervallo_ricerca)
