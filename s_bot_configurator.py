from config_subito import config

# config={
#     "url_ricerca":"https://www.subito.it/annunci-italia/vendita/usato/?q=steam+deck&from=recentsearches",
#     "intervallo_ricerca":20,
#     "max_prezzo":300
# }
while True:
    user_input=input(f"Cosa hai intenzione di configurare?\n1)url_ricerca\n2)intervallo_ricerca\n3)max_prezzo\n")
    match user_input:
        case "1":
            input("Inserisci l'url_ricerca desiderato: ")
            print("Settato url_ricerca")
            break
        case "2":
            input("Inserisci l'url_ricerca desiderato: ")
            print("Settato intervallo_ricerca")
            break
        case "3":
            input("Inserisci l'url_ricerca desiderato: ")
            print("Settato max_prezzo")
            break
        case _:
            print("Non è stato inserito un valore corretto: ")