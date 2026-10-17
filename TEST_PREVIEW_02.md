# Verifiche preview 0.2.0

Eseguite il 17 ottobre 2026. Nessuna stampa fisica, movimento o flash effettuato per queste verifiche.

| Prova | Risultato |
|---|---|
| C++ `IndxChecks`, ordine casuale | 195 asserzioni, 6 casi superati |
| C++ `GCodeWriter`, `CombinedInfill`, `UsedLayerTools`, ordine casuale | 467 asserzioni, 38 casi superati |
| Protocollo, catalogo, libreria, condizioni delle calibrazioni | Superati su Windows/Python 3.12 e SPI-XI/Python 3.9.2 |
| Conteggi 1/2/4/8/12/64 | Dichiarazione, archivio, richiamo e rimozione/ripristino verificati; mappatura/limite Z verificati in C++ |
| Separazione catalogo e montaggio fisico | La risposta Orca non sovrascrive la dichiarazione della stampante |
| Installazione, aggiornamento ripetuto e rollback | Superati in directory temporanee su Windows e SPI-XI; dati calibrazione successivi al backup conservati |
| GTK 3 sullo SPI-XI | Costruzione e attivazione dei 6 pannelli con 1/2/4/8/12 tool; dialoghi montaggio annullabili senza modificare i dati |
| Installazione sullo SPI-XI | 9 moduli installati verificati rispetto ai sorgenti provati; backup di codice/config/dati; riavvio del solo KlipperScreen |
| Stato Klipper dopo aggiornamento touchscreen | Ready; processo Klipper invariato; collaudo geometria/pulizia non abilitato dall'installazione |
| Interfaccia Orca con Moonraker simulato | Sincronizzazione e controllo coerente dei soli T0/T1 usati; differenza di diametro T0 segnalata con invio bloccato |
| Dialogo Ugelli in Orca | Passaggio da 4 a 8 tool applicato e salvato nel profilo stampante isolato |

Le immagini seguenti usano dati esplicitamente denominati TEST SIMULATO, in una directory separata dai profili personali. Il controllo verde non attesta il collaudo della stampante reale.

![Controllo coerente dei soli tool usati, con dati simulati](controllo-simulato.png)

![Diametro diverso dichiarato dalla macchina simulata: invio bloccato](controllo-diametro-incoerente.png)

![Otto tool configurabili nel dialogo Ugelli](ugelli-otto-tool.png)

La suite FFF emette anche diagnostica su opzioni/risorse opzionali dei fixture; tutte le asserzioni richieste sono superate. Il controllo clang-tidy previsto dal progetto e stato avviato ma il suo wrapper richiede un'installazione Visual Studio registrata, assente nell'ambiente con toolchain MSVC portabile: non si dichiara quel controllo superato.

Il workflow GitHub verifica il pacchetto Python e gli hash. Non compila Orca e non sostituisce le prove GTK o il collaudo della conversione. La prova multidiametro 0,20/0,80 precedente resta disponibile in [PROVA_MULTIDIAMETRO.md](PROVA_MULTIDIAMETRO.md).

## Importazione automatica degli ugelli

Il protocollo C++ verifica la dichiarazione completa per 1/2/4/6/8/64 tool, default del fattore CHT, risposte offline e non confermate e rifiuto di numero/indici/diametri/tipi non validi. Numero, diametri e Standard/CHT del touchscreen sono la sorgente del montaggio in Orca.

Prova GUI isolata: una dichiarazione simulata di sei tool e stata importata dal ciclo automatico, senza usare l'editor Ugelli. Il profilo salvato contiene i sei diametri attesi e il riepilogo mostra T4 da 0,40 mm CHT. La copia precedente del profilo stampante e presente nella cartella di backup. Nessun dato della stampante reale modificato per la prova.

![Sei tool importati automaticamente, incluso T4 CHT](sync-ugelli-automatica.png)

Verificata anche la riduzione automatica da sei a due tool e il cambio T0 da 0,20 a 0,30 mm, senza reinserimento nell'editor Orca. Le assegnazioni a tool rimossi richiedono verifica e riassegnazione prima di usare progetti precedenti.
