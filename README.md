# OrcaSlicer INDX - SV08 Max

Versione sperimentale di OrcaSlicer con integrazione KlipperScreen per una Sovol SV08 Max convertita a Bondtech INDX. Tool configurabili, un solo feeder e riscaldatore fisico. Il collaudo di stampa con il kit montato resta da completare.

## Download e guida

Apri la [release](https://github.com/Moffy97/OrcaSlicer-INDX/releases/tag/v0.3.1-preview.20261018) e scorri fino ad **Assets**:

- [Installer Windows x64](https://github.com/Moffy97/OrcaSlicer-INDX/releases/download/v0.3.1-preview.20261018/OrcaSlicer-INDX-SV08Max-0.3.1-preview-Setup-x64.exe): programma, profili iniziali, guida e collegamento nel menu Start.
- [Versione portatile ZIP](https://github.com/Moffy97/OrcaSlicer-INDX/releases/download/v0.3.1-preview.20261018/OrcaSlicer-INDX-Windows-x64-0.3.1-preview.zip): estrarre tutto e aprire Avvia-Orca-INDX.cmd. Installer e ZIP contengono la stessa versione aggiornata.
- [Plugin KlipperScreen SV08 Max](https://github.com/Moffy97/OrcaSlicer-INDX/releases/download/v0.3.1-preview.20261018/KlipperScreen-INDX-SV08Max-plugin.zip) e [istruzioni di installazione e rollback](PLUGIN_KLIPPERSCREEN_SV08MAX.md).
- [Profili scaricabili](PROFILI_DOWNLOAD.md).
- [Guida completa illustrata](Guida_completa_INDX_Orca_KlipperScreen.pdf).

[Note installer Windows](WINDOWS_INSTALLER.md). La [versione Generic](https://github.com/Moffy97/OrcaSlicer-INDX-Generic) ha repository, download e guide Italiano/English separati, senza integrazioni automatiche personalizzate.

## Interfaccia e uso

La barra laterale raggruppa gli ugelli in schede con numero tool, diametro in mm e Standard/CHT. La selezione Automatico/Manuale e distinta dalla mappatura dei filamenti. I pulsanti + e - gestiscono separatamente numero di ugelli e filamenti; ogni filamento mostra il tool assegnato. I selettori evidenziano la modalita attiva.

1. Parti dal profilo SV08 Max INDX incluso e verifica gli ugelli reali. Il profilo pubblico iniziale usa 0,4 / 0,4 / 0,6 / 0,8 mm, non i dati personali di una stampante.
2. Configura la connessione nella sezione stampante di Orca. In Automatico ricevi i tool dichiarati e confermati su KlipperScreen; in Manuale modifichi il profilo locale. Il firmware e il touchscreen non vengono riconfigurati dai pulsanti locali.
3. Crea o richiama un filamento, scegli colore e parametri, quindi assegnalo al tool desiderato. La libreria distingue filamenti standard e personalizzati e conserva le calibrazioni per filamento, tool, diametro e tipo ugello.
4. Apri INDX Auto Slice accanto a Elabora piatto. Dettaglio, Equilibrato e Veloce valutano prima le combinazioni con una preselezione logica, poi eseguono fino a cinque slicing finalisti per modalita/materiale. Le schede mostrano tempi nativi, layer totali, consumo, cambi tool e conteggio delle varianti valutate/slicerate. Pareti e superfici conservano il colore primario; il riempimento puo usare altri colori dello stesso materiale. Conferma il risultato per aprire la sua anteprima memorizzata senza ripetere lo slicing.
5. Controlla l'anteprima; modificare il modello o i parametri invalida i risultati memorizzati. I dati sincronizzati non cambiano un G-code gia esportato.

I layer vengono limitati dagli ugelli usati nel piatto corrente, inclusi supporti e assegnazioni per parte o altezza. Un tool montato ma inutilizzato non limita il progetto. Il riempimento combinato puo sommare piu layer parete entro il limite del proprio ugello. Le stime CHT non sostituiscono una misura di portata.

## KlipperScreen

Il plugin offre libreria filamenti, selettori marca/materiale/colore, temperature, PA, flow e portata massima, tool/dock e offset, bozze e backup. La sincronizzazione filamenti e colori funziona nei due sensi con Orca nella configurazione predisposta. La cella di carico non misura automaticamente PA, flow o portata: le calibrazioni richiedono valutazione del risultato.

Segui [la procedura del plugin](PLUGIN_KLIPPERSCREEN_SV08MAX.md). Il pacchetto richiede KlipperScreen e la conversione INDX gia configurati, con `_INDX_SETUP`, `_INDX_REQUIRE_COMMISSIONED`, `INDX_PRINT_START`, `INDX_PRINT_END` e `CHANGE_TOOL`. Non installa firmware, pinout o macro di movimento. L'installazione crea un backup e supporta rollback.

## Documentazione di riferimento

- [Ugelli Automatico/Manuale](UGELLI_MANUALI_AUTOMATICI.md)
- [Filamenti standard e personalizzati](FILAMENTI_STANDARD_PERSONALIZZATI.md)
- [Profili per diametro e altezza layer](PROFILI_ORDINATI.md)
- [Compatibilita materiali, condizioni e fonti](COMPATIBILITA_MATERIALI.md)
- [Prompt per modificare Orca e KlipperScreen](PROMPTS.md)
- [Tema e panoramica Mainsail](mainsail-indx.zip)

Le schermate di prova, i risultati simulati e le guide duplicate sono stati rimossi dal ramo corrente. Restano i test automatici di manutenzione e la guida completa. La cronologia Git conserva le revisioni precedenti.

## Sorgente e verifiche

`UPSTREAM.json` indica il commit ufficiale Orca; `OrcaSlicer-INDX.patch` contiene le modifiche e `python prepare_source.py` ricostruisce il sorgente in una nuova cartella. Compilare Release con la toolchain ufficiale Orca. La patch corrisponde alla build 0.3.1 di installer e ZIP portatile; le versioni precedenti restano nei propri tag. `windows-installer.iss` contiene la ricetta di installazione.

Per verificare il pacchetto Python: `python verify.py` e `python install_sv08max.py --check`. I test isolati di profili, aggiornamento e rollback restano nel repository; non eseguono il collaudo fisico della stampante. Homing, pulizia, dock, offset e collegamenti vanno verificati sulla singola macchina prima di abilitare i movimenti della conversione.

Progetto comunitario non ufficiale OrcaSlicer, Bondtech, Sovol o KlipperScreen. Licenza AGPL-3.0; sorgente corrispondente e licenza sono inclusi nei pacchetti.
