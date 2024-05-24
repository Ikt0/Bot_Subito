
## Panoramica

Il Subito.it Price Tracker è uno script basato su Python progettato per monitorare i prezzi dei prodotti su Subito.it. Esegue controlli periodici su un URL specificato, estrae i dati sugli articoli elencati e memorizza questi dati in un database SQLite. Inoltre, fornisce notifiche e visualizzazioni basate sui dati raccolti.

## Funzionalità

Recupero Dati Automatico: Recupera periodicamente i dati da Subito.it.
Monitoraggio Prezzi: Traccia i prezzi e notifica quando un prodotto soddisfa le condizioni specificate.
Memorizzazione in Database: Memorizza i dati degli articoli in un database SQLite.
Visualizzazione Grafica: Traccia le tendenze dei prezzi nel tempo.
Notifiche Personalizzate: Riproduce un suono e stampa informazioni nella console quando vengono soddisfatte determinate condizioni.
## Relase 1.5

![preview](https://i.ibb.co/1sP6P6y/Screenshot-2024-05-24-224730.png)
## Come configurare il bot

#### config_subito.py

Modifica questo file per gestire le configurazioni del bot

"url_ricerca":"Url di ricerca di un articolo su Subito.it elencato per più recente",
"intervallo_ricerca":int in secondi d'aggiornamento tra una richiesta e un altra (consigliati 20 secondi),
"max_prezzo": int Il massimo del prezzo desiderato,
"clear_database_on_startup":"Booleano per resettare o meno il database all'avvio del bot",
"plot_data":"Apre un plotter per visualizzare l'andamento dei prezzi durante l'esecuzione del bot"

#### Avviare il bot

Il file bot_subito.py apre il terminale che chiede all'utente se ha intenzione di installare le dipendenze e successivamente avvia il bot.

## Installare dipendenze senza utilizzare bot_subito.py

pip install -r requirements.txt
## Attenzione

Poiché il progetto si concentra esclusivamente sul monitoraggio dei prezzi e sull'analisi dei dati estratti da Subito.it tramite web scraping, non è prevista l'implementazione di un'interfaccia web che consenta agli utenti di inserire direttamente i propri dati. Di conseguenza, le query al database non sono parametrizzate.
## Autore

- [@Ikto](https://www.github.com/ikt0)