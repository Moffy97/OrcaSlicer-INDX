# Autoslicing: separazione ABS e PLA

La politica automatica usa il tipo materiale e il colore del filamento principale scelto nella pagina di ottimizzazione. Le tre modalita selezionano solo tool dello stesso tipo e colore. Un altro colore dello stesso tipo puo essere proposto per infill soltanto dopo una riduzione misurata del tempo e una scelta finale esplicita. Nessun risparmio o conferma rende candidati tipi diversi.

## Verifica riproducibile

Compilare Release con BUILD_TESTS=ON. Eseguire `libslic3r_tests "[IndxChecks]"` e `fff_print_tests "[INDX]"`.

- Regole: **401 asserzioni, 18 casi**, superati. ABS/PLA esclusi in entrambe le direzioni, per Dettaglio, Equilibrato e Veloce, anche con ugello alternativo maggiore. Altro colore PLA proposto mantenendo pareti e superfici originali.
- Motore e G-code: **1198 asserzioni, 7 casi**, superati. Caso di regressione con materiali ABS/PLA/PLA/PLA e ugelli 0,6/0,4/0,6/0,8 mm: assegnazione ABS per pareti e PLA per infill respinta; dopo selezione PLA, slicing nativo e analisi di ogni movimento estruso nelle tre modalita confermano che T0 ABS non viene estruso. Anche un override locale che reintroduce ABS viene respinto.
- Gli altri test INDX di limiti layer, infill combinato, mappature e numero variabile di tool restano verdi.

Il controllo e nella validazione nativa INDX: gli slot caricati ma non usati non bloccano il modello. I filamenti dedicati ai supporti mantengono la gestione separata. Nessuna stampa fisica eseguita.

L’analisi clang-tidy locale non e stata eseguita: lo script di progetto non riconosce il runtime Python portatile e segnala «Missing: Python 3». La compilazione Release e i test sopra sono completati.
