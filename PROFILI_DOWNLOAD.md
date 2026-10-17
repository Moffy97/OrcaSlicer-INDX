# Download e profili INDX

ORCASLICER INDX — Windows x64, preview sperimentale

Estrarre TUTTO lo ZIP in una cartella scrivibile, poi aprire Avvia-Orca-INDX.cmd.
Il launcher usa solo la cartella dati accanto al programma, senza modificare i profili dell'Orca gia installato.
Piatto vuoto all'avvio, nessun progetto personale o indirizzo stampante incluso.

Profili inclusi:
- Sovol SV08 MAX INDX 4T - DA COLLAUDARE: 0,4 / 0,4 / 0,6 / 0,8 mm. Richiede il pacchetto KlipperScreen INDX e la configurazione/macro della conversione SV08 Max gia installata e collaudata. La connessione si imposta sulla propria macchina. Nessuna calibrazione e preconfermata.
- INDX - Generica semplice - DA CONFIGURARE: solo slicing e cambio tool Bondtech. Senza sync automatica, Auto slice o plugin KlipperScreen personalizzato. Quote 200x200x200 di ESEMPIO; sostituire quote, limiti, avvio, homing e pulizia con quelli della propria stampante. Installare e collaudare prima le macro ufficiali INDX. Il profilo non configura elettronica, dock o firmware.
- PLA standard: valori di partenza, NON calibrati.

Per importare in un'installazione esistente: File > Importa > Importa configurazioni, selezionando i cinque JSON in profili.
Il profilo generico conserva il marcatore INDX_BASIC_PROFILE: rimuoverlo abilita le funzioni complete riservate all'integrazione touch. Il marcatore INDX_PRINT_START in un commento abilita soltanto l'output per feeder/riscaldatore condiviso; non e una chiamata macro.
Non e una release ufficiale OrcaSlicer o Bondtech. Collaudo fisico INDX ancora da eseguire.

Fonti e sorgente corrispondente: https://github.com/Moffy97/OrcaSlicer-INDX
Macro e istruzioni Bondtech: https://github.com/BondtechAB/INDX#slicer-setup


[Releases: download Windows e plugin SV08 Max](https://github.com/Moffy97/OrcaSlicer-INDX/releases)
