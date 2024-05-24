import matplotlib.pyplot as plt
import sqlite3


def data_graph():

    conn = sqlite3.connect("subito.db")
    cur = conn.cursor()
    cur.execute("""SELECT item_number,prezzo FROM andamento""")

    risultato=cur.fetchall()

    x=[]
    y=[]
    elements=risultato
    for elem in elements:
        x.append(elem[0])
        y.append(elem[1])


    # plotting the points 
    plt.plot(x, y)

    # naming the x axis
    plt.xlabel('# Rilevamento')
    # naming the y axis
    plt.ylabel('Prezzo')

    # giving a title to my graph
    plt.title('Vsiualizzazione prezzi')

    # function to show the plot
    plt.show()