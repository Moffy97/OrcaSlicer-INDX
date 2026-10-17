# Preview 0.3.0 - interfaccia diretta e configurazione dalla stampante

## Un solo punto di inserimento

In KlipperScreen aprire INDX. I pulsanti **Tool e dock, Filamenti, PA, Flow, Portata, Collaudo, Tool attivo** cambiano il contenuto della stessa area. Le schede T0, T1 e successive selezionano il tool da modificare. Standard/CHT e direzione dock sono interruttori diretti.

In Orca il pulsante **INDX** apre uno spazio unico con tre pulsanti di selezione: **Info INDX**, **Config tool**, **Auto slicing optimization**. Non c'e un secondo editor connessione INDX: viene usata la connessione della stampante configurata nella sezione superiore di Orca. Le connessioni della preview precedente restano utilizzabili durante la migrazione.

## Aggiungere tool, dock e offset

1. In **Tool e dock**, ricaricare la configurazione e aumentare **Numero tool**. Il limite software e 1-64; non e una capacita fisica certificata.
2. Selezionare ogni nuova scheda Tn. Impostare diametro, Standard/CHT, fattore CHT, Dock X, Dock Y e offset X/Y/Z. Le quote nuove restano vuote finche non vengono inserite; non si generano dock da un passo presunto.
3. Verificare direzione dock, corsia libera Y, distanza ingresso e Z-hop. **Leggi posizione attuale per il dock** legge X/Y senza muovere e richiede assi referenziati.
4. **Salva bozza senza applicare** conserva dati anche incompleti. **Verifica e salva configurazione** richiede dati completi, macchina libera, target termici spenti, quote entro i limiti del profilo e corsia ad almeno 26 mm sul lato esterno ai dock. Non amplia le corse.
5. Il salvataggio modifica il file utente `indx/indx.cfg`, aggiunge i comandi Tn mancanti, conserva un backup e invalida il precedente collaudo. Non cambia i file ufficiali del meccanismo, non muove assi e non esegue flash.
6. **Riavvia Klipper per caricare** richiede macchina ferma e riscaldatori spenti. La riga di stato distingue salvato e caricato. Il profilo manutenzione non attiva INDX: il caricamento reale richiede il profilo INDX con testa e cella presenti.
7. Dopo le misure reali, selezionare la dichiarazione dell'operatore e usare **Conferma dock misurati: abilita test**. I test di aggancio/parcheggio richiedono la conferma del movimento e usano le macro esistenti.
8. In **Collaudo**, completare in ordine i primi sei passaggi fisici: collegamenti, dock, aggancio, pulizia, Z, XY. Solo dopo si puo dichiarare il collaudo per la stampa in Tool e dock. La stampa di prova e il settimo passaggio, da verificare dopo averla eseguita.

Gli offset sono i valori assoluti Klipper del tool, non incrementi. Sono registrati una sola volta per revisione tramite `SAVE_VARIABLE`; i riavvii successivi non cancellano le calibrazioni ufficiali fatte dopo. Il global Z offset resta separato. Le vecchie varianti filamento/calibrazione restano archiviate; rimuovendo tool occorre riassegnare le funzioni dei vecchi progetti.

## Sincronizzazione con Orca

Orca importa automaticamente numero, diametri, Standard/CHT e fattore CHT dalla dichiarazione confermata del touchscreen, circa ogni 15 secondi oltre alla rete. Attende durante modifiche non salvate ai profili, slicing/export e finestre modali. Risposte incomplete, offline o di una connessione precedente non ridimensionano il profilo. Le copie precedenti del profilo stampante sono conservate in `indx-profile-backups`.

In **Config tool**, **Sincronizza filamenti nel progetto** importa le assegnazioni nel piatto corrente e i parametri del profilo personale: colore, temperature, PA, flow e portata. Chiede conferma se una copia generata e stata modificata localmente. Salvare il progetto e rislicera dopo i cambi; il G-code gia esportato non cambia.

## Filamenti e calibrazioni

La libreria stampante separa profili personali e basi generiche. Le calibrazioni sono legate a filamento, tool, diametro, Standard/CHT e condizioni del test. **Verificato** indica un test visivo/manuale salvato con condizioni corrispondenti; **stimato**, **da calibrare** e **da rifare** restano distinti. Rinominare o cambiare colore conserva l'identita; modificare temperatura, materiale/prodotto o flow puo invalidare i test dipendenti.

PA, flow e portata richiedono il test corrispondente completato prima del salvataggio. La scelta del campione e visiva: la cella non misura automaticamente PA o qualita del flusso. Il massimo flusso salva il 90% dell'ultima fascia scelta senza difetti. Le stime CHT generiche non sono misure della macchina.

## Controlli e multidiametro

**Controlla il piatto corrente** legge uno stato nuovo e confronta i tool effettivamente usati. Tool montati ma inutilizzati non impongono il limite di layer. L'invio INDX controllato resta limitato al piatto corrente tramite stampante fisica Moonraker; offline slicing/export sono disponibili, ma un file esportato separatamente non e certificato dal controllo.

In **Auto slicing optimization**, i selettori **Dettaglio, Equilibrato, Veloce** applicano una proposta in un processo separato. Materiali diversi e override locali richiedono assegnazioni manuali. Pareti da 0,20 mm e infill da 0,80 mm possono usare base 0,14 mm e accorpamento infill 0,56 mm dove la geometria lo consente. L'altezza segue i tool usati; non aumenta una richiesta piu fine. In anteprima usare Altezza strato e le proprieta del movimento selezionato.

## Backup e guide

`indx-machine-backup-*` conserva i file geometrici precedenti; `indx-profile-backups` conserva profili e dati; `indx-screen-backup-*` conserva software e menu. Il rollback software dell'installatore mantiene i dati filamento/calibrazione attuali. Non ripristina automaticamente una vecchia geometria o un collaudo fisico.

Guida completa illustrata: [Guida_completa_INDX_Orca_KlipperScreen.pdf](Guida_completa_INDX_Orca_KlipperScreen.pdf). Risultati: [TEST_PREVIEW_03.md](TEST_PREVIEW_03.md). I limiti e le quote non vengono misurati automaticamente.


## Ottimizzazione automatica: filamenti identici e pareti fini

La proposta legge i preset e la mappatura attuali del piatto. Se sono presenti almeno tanti filamenti quanti i tool, tutti dello stesso tipo e colore, una mappatura predefinita vuota, tutta sul primo tool o gestita da una modalita automatica Orca viene completata automaticamente: filamento 1 su T0, filamento 2 su T1 e cosi via. Una mappatura personalizzata non predefinita viene preservata.

Dettaglio sceglie l'ugello piu fine e richiede pareti da 0,4 mm o meno. Con T0=0,6, T1=0,4, T2=0,6 e T3=0,8, propone T1 per pareti e superfici. Dettaglio usa comunque il maggiore ugello per infill. Equilibrato sceglie il maggiore fino a 0,6 mm per pareti e superfici e il maggiore disponibile per infill. Con questo montaggio: Dettaglio 0,4/0,8 ed Equilibrato 0,6/0,8. Uno 0,2 associato prevale sullo 0,4 per Dettaglio. Tutti i tool diventano disponibili alla scelta; non viene imposto di usare ugelli equivalenti, aggiungendo cambi inutili.

Se manca il filamento per un ugello fine montato, la proposta lo segnala anziche sostituirlo con uno 0,6 e chiamarlo Dettaglio. Materiali/colori diversi non vengono rimappati automaticamente. Il software non dichiara carichi fisici o calibrazioni per effetto della proposta. Salva il progetto e rislicera.


## Veloce: ugello maggiore per tutte le funzioni proposte

Veloce assegna pareti, superfici e riempimento al maggiore ugello disponibile tra i filamenti associati. Con 0,6/0,4/0,6/0,8 usa T3 da 0,8 per tutte queste funzioni. Dettaglio resta 0,4/0,8 ed Equilibrato 0,6/0,8. I supporti e le parti dipinte mantengono le assegnazioni esplicite esistenti. Il limite Z continua a dipendere dai tool effettivamente usati e non aumenta una richiesta di layer piu fine.


## Workspace INDX e slicing nella stessa pagina

I tre pulsanti principali sono Info INDX, Config tool e Auto slicing optimization. La home presenta solo le informazioni INDX; non contiene risultati di slicing o parametri di calibrazione. Config tool mostra il montaggio ricevuto dal touchscreen e conserva il comando di sincronizzazione filamenti senza la tabella delle calibrazioni.

In Auto slicing optimization scegli Dettaglio, Equilibrato o Veloce: il cambio di modalita applica la proposta e avvia il motore nativo Orca senza chiudere la finestra o cambiare pagina. La stessa area mostra avanzamento, assegnazioni, tempo stimato, materiale e cambi tool. Rilanciare la stessa proposta riusa il processo; un profilo modificato non viene sovrascritto.

Il cambio modalita nasconde i risultati precedenti. Il nuovo calcolo parte automaticamente nella stessa pagina; Ricalcola resta disponibile per ripetere una prova o recuperare dopo un errore. Piatto cambiato o risultato invalidato nascondono le metriche. Eventuali errori nativi restano nelle notifiche Orca e il pannello invita a correggere e riprovare. Nessuna stampa viene avviata dal pulsante di slicing.
