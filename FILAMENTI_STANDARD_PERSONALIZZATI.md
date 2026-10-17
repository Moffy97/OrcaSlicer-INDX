# Colori automatici e profili standard o personalizzati

## Sul touch

1. Aprire **INDX → Filamenti**, scegliere il tool, la libreria di basi, marca, materiale e profilo. Temperatura ugello, piano, flow e portata vengono dalla base Orca scelta, non da una tabella universale per il solo nome PLA/PETG.
2. Toccare il campione per scegliere il colore. La selezione su un profilo già assegnato salva subito solo il colore; non salva altri campi eventualmente modificati. Su una nuova base il colore rimane in bozza fino all'assegnazione.
3. **Usa valori standard:** salva e assegna una copia senza test, usando i valori originali della base e il colore scelto. Eventuali modifiche manuali nei campi non vengono trattate come valori stock. Nessuna calibrazione viene inventata.
4. **Salva personalizzato:** conserva le modifiche, chiede il nome e assegna il profilo. Si possono quindi eseguire PA, flow e portata e salvare i risultati. Partendo da uno standard viene creata un'identità separata, conservando lo standard per il riutilizzo.

Se si avvia una calibrazione da uno standard, al salvataggio del risultato viene creata una copia personalizzata. I risultati rimangono specifici per filamento, tool, diametro e tipo di ugello. La sola scelta standard non rende verificati PA, flow o portata.

![Filamenti sul touch con dati di prova](studio-indx_filaments.png)

## In Orca

**INDX → Config tool → Colore del tool** mostra un campione senza codice o nome del colore: selezionare Tn e toccare il campione per aprire la palette nativa. Questo comando modifica il colore nel progetto Orca. La sincronizzazione automatica richiesta è dalla stampante verso Orca; non modifica la libreria stampante quando si sceglie un colore locale in Orca.

![Campione colore in Orca](orca-colore-tool.png)

Con Orca aperto e collegato, i profili assegnati dalla stampante aggiornano automaticamente i relativi slot del progetto: colore, temperature, valori di base e risultati di calibrazione ancora validi. La lettura avviene normalmente ogni 15 secondi, oltre ai tempi di rete. Slicing/esportazione, profili non salvati e finestre modali rimandano l'applicazione. Le copie generate modificate localmente richiedono confronto con **Sincronizza filamenti nel progetto**, invece di essere sovrascritte.

Le assegnazioni dei tool occupano i primi slot corrispondenti; eventuali slot aggiuntivi non assegnati dalla stampante vengono conservati. Il progetto aggiornato richiede un nuovo slicing prima della stampa: un G-code già esportato non viene modificato o inviato automaticamente. Una successiva modifica sul touchscreen torna ad applicare i valori del profilo della stampante anche se il colore del progetto era stato cambiato localmente in Orca.

![Prova di aggiornamento automatico, dati simulati](sync-filamenti-automatico.png)

## Verifiche

- GTK reale isolato: scelta/annullamento colore, aggiornamento immediato del record assegnato senza salvare temperature ancora in bozza, stock ripreso dalla base, copia personalizzata separata e identità stabile.
- Layout con pulsanti KlippyGtk reali, font 32 px, barre titolo/laterali, 4 e 12 tool a 1024×600 e 1280×800.
- Orca Windows Release con server Moonraker su loopback, senza connessione alla stampante: quattro assegnazioni applicate automaticamente; modifica simulata a colore e temperatura ricevuta senza premere Sincronizza. Il 3MF salvato contiene il nuovo colore in tutti i quattro slot e temperatura 220 °C.
- 356 asserzioni in 15 test IndxChecks e 1177 asserzioni in 6 test FFF INDX superati. Nessun movimento, riscaldamento o flash.
- Il controllo clang-tidy locale non è stato eseguito: lo script di progetto non riconosce il runtime Python portatile come installazione Python di sistema. La compilazione Release e i test sopra sono verificati separatamente.

I dati delle immagini e del test a 220 °C sono simulati e non prescrivono una temperatura per il filamento reale. I valori stock dipendono dalla base effettivamente scelta e restano da verificare sulla propria macchina.
