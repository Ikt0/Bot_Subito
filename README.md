Questo script automatizza il monitoraggio degli annunci su Subito.it, controllando periodicamente nuovi articoli in base a criteri specifici e notificando l'utente quando viene trovato un nuovo articolo o se ci sono aggiornamenti di prezzo.

Funzionalità
Web Scraping: Estrazione dati da Subito.it con BeautifulSoup.
Memorizzazione Dati: Salvataggio dati in un database SQLite.
Notifiche: Avvisi all'utente quando vengono trovati nuovi articoli o cambiamenti di prezzo.
Interfaccia a Linea di Comando: Pulizia della linea di comando e stampa di un logo ad ogni iterazione.
Avvisi Sonori: Riproduzione di un suono quando un articolo che soddisfa i criteri viene trovato.
Requisiti
Python 3.x
Librerie Python: Requests, BeautifulSoup4, SQLite3, Playsound
File di configurazione (config_subito.py) con la seguente struttura:
python
Copia codice
config = {
    "url_ricerca": "TUA_URL_DI_RICERCA",
    "max_prezzo": PREZZO_MASSIMO,
    "intervallo_ricerca": INTERVALLO_IN_SECONDI
}
Installazione
Installa le librerie richieste:
bash
Copia codice
pip install requests beautifulsoup4 playsound
Assicurati di avere config_subito.py con i parametri corretti.
Posiziona il file cash.mp3 nella stessa directory dello script per le notifiche sonore.
Utilizzo
Esegui lo script:
bash
Copia codice
python script_name.py
Lo script eseguirà le seguenti operazioni:

Pulisce la linea di comando e stampa il logo.
Recupera gli annunci dalla URL fornita.
Analizza il contenuto HTML per estrarre i dettagli degli articoli.
Controlla se ci sono nuovi articoli o aggiornamenti.
Memorizza i risultati in un database SQLite.
Notifica l'utente in base al prezzo e alla disponibilità degli articoli.
Lo script continuerà a funzionare indefinitamente, controllando nuovi annunci all'intervallo specificato.

Schema del Database
Il database SQLite (subito.db) contiene una tabella andamento con la seguente struttura:

sql
Copia codice
CREATE TABLE IF NOT EXISTS andamento (
    item_number INTEGER PRIMARY KEY AUTOINCREMENT,
    prezzo INT,
    titolo VARCHAR(50),
    descrizione VARCHAR(500),
    status VARCHAR(50),
    is_sold VARCHAR(50),
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
Personalizzazione
URL: Modifica la URL di ricerca nel file config_subito.py per mirare ad annunci diversi.
Limite di Prezzo: Regola max_prezzo nel file di configurazione per impostare il prezzo massimo desiderato.
Intervallo di Ricerca: Modifica intervallo_ricerca nel file di configurazione per impostare la frequenza di controllo dei nuovi annunci.