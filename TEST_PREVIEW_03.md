# Verifiche preview 0.3.0

Eseguite il 17 ottobre 2026. Nessun movimento, riscaldamento o flash eseguito sulla stampante reale per queste verifiche. La macchina resta nel profilo manutenzione.

| Prova | Risultato |
|---|---|
| Build Windows Release | Compilazione e collegamento della GUI riusciti |
| C++ IndxChecks | 195 asserzioni in 6 casi, ordine casuale |
| Regressioni GCodeWriter, CombinedInfill, UsedLayerTools | 467 asserzioni in 38 casi; pipeline invariata rispetto alla prova precedente |
| Python libreria/protocolli | Conteggi variabili, condizioni di calibrazione, storico e separazione tra catalogo e montaggio confermato |
| Editor macchina | 1/2/4/6/8/12/64 tool; controllo limiti e corsia, valori non validi, input con comandi respinto, macchina occupata, riscaldatori, revisione obsoleta e guasto rete |
| Dati e rollback | Backup, rollback di una transazione file interrotta, lettura delle sezioni Variables/variables, conservazione calibrazioni dopo aggiornamento software |
| Conferme fisiche | Richiedono revisione caricata, macro geometriche coerenti, testa/cella attive e i primi sei passaggi della checklist per il collaudo completo; nessuna conferma automatica |
| Offset persistenti | Modello Jinja provato nell'ambiente Kalico: applicazione una sola volta per revisione e nessuna sovrascrittura al riavvio dopo una calibrazione ufficiale |
| Orca GUI isolata | Tre pulsanti di selezione, nessun campo connessione INDX, lettura di sei tool con T4 CHT, cambio diretto delle pagine e report inline del piatto vuoto bloccato |
| GTK sullo SPI-XI | Costruzione/attivazione con 1/2/4/8/12 tool e visualizzazione delle sette pagine; aree scorrevoli espanse correttamente |
| Guida completa | 17 pagine renderizzate; controllo visivo di impaginazione e diagrammi |

Le schermate Orca usano dati TEST SIMULATO in una directory separata dai profili personali. Non rappresentano calibrazioni della stampante reale. Il wrapper clang-tidy richiede un'installazione Visual Studio registrata, assente nella toolchain portabile: quel controllo non e dichiarato superato. Il workflow GitHub controlla il pacchetto Python, non compila Orca e non sostituisce il collaudo fisico.

![Orca: selezione diretta, nessuna connessione duplicata](orca-workspace-03.png)

![Orca: filamenti simulati e risultato nella stessa pagina](orca-filaments-03.png)


![KlipperScreen: pulsanti diretti e geometria con quote simulate](klipperscreen-tools-03.png)
