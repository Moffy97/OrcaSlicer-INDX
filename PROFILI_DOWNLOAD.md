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


### Automatic Z and infill grouping

Normal slicing preserves the sidebar layer height. INDX Auto Slice chooses a common layer height independently for each mode and purpose, using active nozzles only. It compares feasible infill grouping boundaries and a half-nozzle candidate with native slicing: time includes tool changes and filament volumetric limits remain active. Surface quality and physical shell thickness follow the selected purpose. The 0.8 mm nozzle ceiling is 0.64 mm; 0.30 mm walls with 0.60 mm infill are included when feasible. Grouping remains local to geometry; solid layers and transitions may require more frequent infill.

Verified motor resolution can be stored as `INDX_Z_STEP=<millimetres>` in printer notes. The SV08 Max profile uses 0.001875 mm, derived from retained Klipper settings: rotation distance 40, ratio 80:12, 200 full steps and 16 microsteps. Other printers must use their own verified mechanics; absent metadata leaves heights unquantized. Microstep size is command resolution, not a claim of physical positioning accuracy.


Automatic optimization jointly enumerates the available wall, solid-surface and sparse-infill tool assignments allowed by each mode. Walls and surfaces retain the primary material and color; sparse infill may use other colors of the same polymer. The search evaluates nozzle-dependent Z candidates for every assignment, including single-tool printing and infill grouping transitions. Conditional material alternatives remain separate and require approval. Native slicing ranks completed valid trials by total time, including tool changes; near ties use fewer changes, then lower filament weight. The comparison shows valid and rejected trial counts, caches each winning mode, and preserves the usual sidebar height for ordinary slicing. This is a discrete candidate search, not a proof of globally optimal layer heights or mechanical strength. Physical commissioning remains necessary.
