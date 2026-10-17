# INDX 0.2.0-preview: controllo macchina e calibrazioni

Questa preview estende l'integrazione SV08 Max. Le verifiche software non attestano quote dei dock, cablaggi, offset o qualita di stampa. Il numero di tool e configurabile; non vengono create automaticamente posizioni fisiche.

## Numero di tool e ugelli

Numero di tool, diametri, Standard/CHT e fattore stimato CHT si impostano una sola volta su **KlipperScreen > I miei filamenti > Conferma ugelli montati sulla stampante**. Orca importa automaticamente la dichiarazione confermata con la connessione INDX attiva e un profilo INDX selezionato. Il ciclo di lettura e di circa 15 secondi, oltre al tempo di rete; premere **INDX** esegue anche l'importazione esplicita prima di leggere i filamenti.

Il pulsante **Ugelli** mostra la configurazione ricevuta dalla stampante. L'editor locale resta disponibile per preparare un profilo offline quando non e raggiungibile una dichiarazione confermata; alla successiva connessione la dichiarazione del touchscreen prevale. Il limite software e 1-64, non una promessa di capacita fisica della SV08 Max.

L'importazione aggiorna il profilo stampante e i limiti di altezza layer, conserva una copia precedente in `indx-profile-backups`. Attende finche sono presenti modifiche non salvate nei profili, slicing/export attivi o finestre modali. Una risposta offline, incompleta o non confermata non riduce il numero di tool. La risposta di una connessione o di un profilo precedente viene scartata. Dopo un cambiamento occorre rifare lo slicing; il G-code gia esportato non cambia.

Riducendo il numero di tool le varianti di calibrazione e le assegnazioni archiviate non vengono eliminate: tornando alla stessa combinazione si recuperano i dati ancora validi. Le funzioni del progetto che usano tool rimossi vanno riassegnate.

Le macro della macchina devono dichiarare lo stesso `TOOL_POSITIONS.tool_count` e avere le posizioni reali di tutti i dock, secondo la [guida Bondtech INDX](https://github.com/BondtechAB/INDX). I pannelli e Orca non aggiungono queste posizioni nel firmware.

### Esempio: aggiungere T4 e T5 a una macchina con quattro tool

1. Configurare i due nuovi dock nelle macro, con coordinate reali e `tool_count` pari a 6; collaudare aggancio, parcheggio e offset.
2. Sul touchscreen aprire **I miei filamenti > Conferma ugelli montati sulla stampante**, impostare 6 e dichiarare diametro e Standard/CHT di tutti i tool.
3. Con Orca aperto e collegato alla macchina, attendere l'aggiornamento automatico. In alternativa premere **INDX**. Non reinserire numero o ugelli in Orca.
4. Assegnare sul touchscreen i filamenti anche a T4 e T5; premere **INDX** in Orca per importarli, poi **Controlla** e rifare lo slicing.

I dati di T0-T3 restano conservati. I nuovi tool richiedono le proprie calibrazioni. Aggiungere righe in Orca o sul touchscreen non crea dock e non collauda la macchina.

## Controllo del piatto

**Controlla** legge da Moonraker lo stato di Klipper, occupazione della macchina, flag del collaudo geometria/pulizia, tool count, dichiarazione del montaggio, assegnazioni e libreria. Risolve le mappature filamento/tool del piatto e controlla solo i tool usati: un ugello montato ma inutilizzato non impone il limite di layer ne un confronto del diametro per quella stampa.

Per ogni filamento usato confronta UUID, colore, temperature, PA, flow e portata con il profilo personale salvato. Differenze, dati incompleti, montaggio non confermato, macchina occupata/offline o collaudo mancante bloccano l'invio INDX. Le calibrazioni mancanti o stimate vengono segnalate; non vengono presentate come misure verificate. Il confronto del montaggio e una dichiarazione dell'operatore, non un sensore di riconoscimento del diametro.

Durante l'aggiornamento del progetto viene ricalcolato anche un report locale con l'ultima lettura della stampante, valido al massimo 60 secondi. Il pulsante e l'invio richiedono una lettura nuova. Si puo preparare lo slicing ed esportare un file locale offline. L'invio INDX supportato e quello del **piatto corrente** tramite stampante fisica Moonraker / invio G-code legacy; la destinazione deve corrispondere all'indirizzo della connessione INDX, inclusa la porta. L'invio multipiatto e le altre interfacce di upload richiedono un'estensione dedicata; non costituiscono un controllo di tutti i piatti. Un G-code esportato separatamente non viene certificato da questo controllo.

## Stati delle calibrazioni

| Stato | Significato | Uso |
|---|---|---|
| Verificato | Test visivo/manuale salvato con condizioni corrispondenti | Il valore viene richiamato per la combinazione corretta |
| Stimato | Valore di base o stima CHT senza test corrispondente | Resta una base da verificare |
| Da calibrare | Nessun PA valido per la combinazione | Non viene inventato un PA misurato |
| Da rifare | Vecchio risultato con condizioni diverse o provenienza incompleta | Il valore resta nello storico e non viene applicato come misura valida |

Il salvataggio registra data, metodo e condizioni: tool/diametro/tipo ugello, temperatura, piano, materiale, marca/prodotto e flow effettivo quando rilevante. Cambiare nome o colore conserva l'identita; cambiare condizioni del filamento puo rendere il test da rifare. Cambiare flow invalida PA e massimo flusso che dipendevano dal flow precedente. I numeri legacy senza condizioni complete non vengono promossi a risultati verificati. Le date dipendono dall'orologio del computer che esegue KlipperScreen.

PA, flow e massimo flusso richiedono il completamento del file di test corrispondente prima del salvataggio dal pannello. Il risultato resta scelto dall'utente osservando il campione: la cella non misura automaticamente PA o qualita del flusso.

## Proposte e anteprima

**Proponi** offre dettaglio, equilibrato e veloce. Il dettaglio usa l'ugello minore; l'equilibrato propone pareti fini e infill con ugello maggiore; il veloce preferisce il maggiore ugello pareti disponibile fino a 0,4 mm e l'ugello maggiore per l'infill. La scelta rispetta la mappatura filamento/tool. Materiali diversi richiedono assegnazioni manuali. Supporti e pittura restano espliciti. Gli override locali di pareti/superfici/infill vanno risolti prima di applicare la proposta globale. La conferma crea un processo separato, senza sovrascrivere il processo originale.

L'altezza comune viene ricalcolata dopo l'applicazione usando i tool effettivamente usati. I tempi e il numero di cambi si valutano dopo il nuovo slicing: non viene inventato un risparmio prima di elaborare il modello.

Nell'anteprima sequenziale aprire le proprieta del movimento selezionato. Oltre ad altezza e larghezza effettive, compaiono tool/ugello dichiarati nel progetto e numero di intervalli Z accorpati. Il conteggio usa le quote reali del percorso, anche con altezze variabili; se la somma non corrisponde, mostra un valore non disponibile. Per la colorazione del volume depositato usare **Altezza strato**.

## Collaudo guidato e protezione dei dati

La pagina touchscreen **Collaudo INDX** registra collegamenti, dock, agganci, pulizia, Z, XY e stampa di collaudo, in ordine. Un prerequisito non piu verificato invalida i passaggi successivi; una diversa configurazione ugelli richiede una nuova checklist. Legge anche i flag reali delle macro. La checklist documenta verifiche manuali e non abilita i flag di movimento.

**Tool configurati** offre una lista variabile per l'aggancio/parcheggio manuale. Verifica collaudo, macchina libera, montaggio confermato, tool count e presenza delle macro richieste; il movimento passa dalla conferma standard KlipperScreen. Se una macro non e configurata, non viene sostituita con una sequenza inventata. I vecchi menu di commissioning specifici della macchina restano disponibili.

La libreria stampante rimane la sorgente dei profili personali. Orca non sovrascrive in background le copie generate modificate localmente: nella sincronizzazione esplicita mostra le differenze e consente di annullare. Confermando, sostituisce i valori della copia generata con quelli della libreria; salva prima un backup nella cartella `indx-profile-backups` dei dati Orca. Non e una fusione automatica delle modifiche fatte contemporaneamente sui due dispositivi.

Il touchscreen conserva le versioni precedenti dei file dati modificati nella propria cartella `indx-profile-backups`. L'installatore verifica checksum e protocolli e supporta:

```sh
python3 install_klipperscreen.py --check
python3 install_klipperscreen.py --klipperscreen-dir /home/USER/KlipperScreen --config-dir /home/USER/printer_data/config
python3 install_klipperscreen.py --klipperscreen-dir /home/USER/KlipperScreen --config-dir /home/USER/printer_data/config --rollback PERCORSO_BACKUP
```

Sostituire i percorsi con quelli reali. `--restart` e opzionale e riavvia solo KlipperScreen. Il rollback ripristina codice/menu, preservando filamenti e calibrazioni attuali. La versione e visibile nel controllo Orca e nella pagina Collaudo del touchscreen. `VERSION.json` dichiara i protocolli del pacchetto.

## Verifiche ripetibili

`python verify.py` controlla hash, protocolli, stati calibrazione, conteggi tool, checklist e installazione/rollback in directory temporanee. Il workflow GitHub esegue le stesse prove Python. La patch include i test C++ `IndxChecks` e `UsedLayerTools`, oltre alle regressioni di infill combinato e G-code INDX. Le prove GTK sullo SPI-XI e il collaudo di stampa sono verifiche distinte.

Risultati eseguiti: [TEST_PREVIEW_02.md](TEST_PREVIEW_02.md).
