# Verifica materiali per ruolo

La matrice corrente e descritta in [COMPATIBILITA_MATERIALI.md](COMPATIBILITA_MATERIALI.md), con dati e fonti ufficiali datate. I risultati seguenti sono software, senza una stampa fisica.

## Regole e slicing

Compilare Release con BUILD_TESTS=ON. Eseguire `libslic3r_tests "[IndxChecks]"` e `fff_print_tests "[INDX],[GCodeWriter]"`.

- **468 asserzioni, 21 casi IndxChecks**, superati: regole direzionali per modello/interfaccia, origine delle fonti, coppie rigido/flessibile condizionali, nessuna estensione automatica a CF/GF, conservazione delle pareti, alternative solo se misurate e accettate, sincronizzazione e conflitti.
- **1481 asserzioni, 42 casi di slicing/G-code**, superati: limiti layer, infill combinato, mappature, numero variabile di tool e gestione del feeder condiviso; assegnazioni ABS/PLA respinte anche tramite override locali.
- Quattro modelli con sporgenza vengono realmente slicerati con interfacce PLA/PETG, PETG/PLA, PLA/PVA e PETG/BVOH. La verifica dei movimenti del G-code trova il secondo materiale nell’interfaccia e il principale nelle pareti e nel riempimento; nessun falso avviso INDX di modello misto. Il PETG/PLA generico non richiede di marcare globalmente il filamento come supporto.
- PETG/TPU e ammesso nel modello secondo la regola condizionale, ma respinto se proposto come interfaccia da staccare. Un filamento dedicato ai supporti assegnato al riempimento non aggira il controllo.

Nel progetto di prova PLA con ABS inutilizzato, il confronto nativo produce: Dettaglio 1h38m12s /41,4g/242 cambi; Equilibrato 1h36m54s /45,5g/242; Veloce 1h8m23s /38,0g/0. Sono stime Orca, non tempi fisici. La precedente esportazione del progetto conferma solo T1/T3 (slot 2/4), nessuna selezione T0 ABS, e avvio con il tool PLA.

## Limiti delle verifiche

L’analisi clang-tidy non e completata: riconosciuto il Python portatile, lo script richiede un’installazione Visual Studio registrata e non riconosce la toolchain C++ portatile usata dalla build Release. La compilazione e i test sopra sono completati; non viene dichiarato un risultato clang-tidy.

Adesione, temperature effettive, rimozione dei supporti, compatibilita del grado e qualita di stampa richiedono il collaudo fisico INDX. Le coppie ignote o condizionali nei supporti conservano il proprio avviso; i controlli termici e geometrici non sono disabilitati.


La regressione della copia filamento riaperta distingue il colore predefinito del preset dal colore effettivo dello slot. Il confronto conserva la protezione di temperatura, flow, PA e note; le modifiche al colore dello slot restano richieste di sincronizzazione.
