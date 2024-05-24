@echo off
setlocal

:ASK
echo Vuoi installare le dipendenze? (s/n)
set /p input=
if /i "%input%"=="s" goto INSTALL
if /i "%input%"=="n" goto RUN
echo Risposta non valida. Per favore inserisci 's' per Si o 'n' per No.
goto ASK

:INSTALL
echo Installazione delle dipendenze...
pip install requests
pip install playsound==1.2.2
pip install beautifulsoup4
pip install db-sqlite3
goto RUN

:RUN
echo Avvio di bot_subito.py...
python bot_subito.py

endlocal