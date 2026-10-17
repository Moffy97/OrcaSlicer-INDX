# Prompt riutilizzabili - OrcaSlicer INDX / KlipperScreen

Questi prompt descrivono il comportamento richiesto. Non sostituiscono la lettura del codice e delle guide ufficiali. Target attuale: SV08 Max INDX; altre stampanti richiedono un progetto di compatibilita separato.

## 1. Modificare e compilare OrcaSlicer

```text
Lavora sul repository OrcaSlicer INDX e leggi README.md, UPSTREAM.json,
docs/HLSD/INDX.md e gli AGENTS.md applicabili. Ricostruisci il sorgente con
prepare_source.py in una nuova directory, senza sovrascrivere checkout esistenti.

Target: Sovol SV08 Max convertita a INDX, quattro tool passivi e un unico
feeder/riscaldatore. Mantieni la compatibilita dei progetti e non alterare il
comportamento delle stampanti che non attivano l'integrazione INDX.

Mantieni i pulsanti INDX e Ugelli. Ogni tool deve avere diametro indipendente,
tipo Standard/CHT e fattore CHT modificabile. Il fattore riguarda solo una stima
del massimo flusso dei profili generici: non deve moltiplicare flow ratio o PA,
ne sovrascrivere un massimo flusso gia calibrato. Non dedurre la portata dal
quadrato del diametro. Non confondere Standard/CHT con materiale dell'ugello o
con la variante interna di estrusore di Orca.

La libreria filamenti deve conservare UUID stabili, nomi modificabili, marca,
materiale, colore, temperature e calibrazioni per filamento/tool/diametro/tipo.
Cambiare combinazione deve escludere i vecchi valori senza cancellarli; tornando
alla combinazione originale devono essere recuperati. I generici e i personali
calibrati devono restare distinguibili. Importa tutti i profili Orca disponibili
e personali come basi; escludi i profili generati per evitare ricorsioni.

Salva i profili nella libreria utente di Orca. Non sovrascrivere modifiche non
salvate. Il salvataggio in background non deve riassegnare silenziosamente i
filamenti del progetto. La sincronizzazione esplicita applica T0-T3, colori e
mappatura. Un G-code gia esportato richiede nuova elaborazione.

Per la combinazione riempimento usa l'ugello realmente assegnato a quella zona,
il suo limite di altezza e la somma delle altezze dei layer accorpati. Pareti
da 0,20 mm e due layer combinati devono produrre infill da 0,40 mm. Verifica
anche tre layer da 0,20 mm, limiti insufficienti, zone solide e mappatura tool.
Non cambiare le quote globali dei perimetri per simulare la compensazione.

Verifica PA sul solo extruder fisico, azzeramento del PA quando disabilitato,
temperature solo sul tool attivo e assenza di preriscaldamento dei passivi.
Compila Release, esegui test mirati della pipeline e una prova GUI con dati
isolati e server Moonraker locale simulato. Non inserire risultati fittizi nei
profili reali, non inviare stampe e non cambiare firmware. Consegna build,
patch riproducibile, licenze, esiti dei test e limiti ancora da verificare.
```

## 2. Integrare o modificare KlipperScreen

```text
Integra i pannelli KlipperScreen di questo repository sulla SV08 Max INDX.
Prima leggi i moduli in touchscreen.zip e la documentazione ufficiale della
versione KlipperScreen installata. Verifica accesso, servizi, spazio, versione
Python/GTK, struttura delle configurazioni e macro esistenti in sola lettura.
Non richiedere password in chat e non salvarle nei sorgenti o nei log.

Crea un backup datato dei pannelli, menu e JSON esistenti. Esegui le prove in
una directory temporanea, con profili fittizi confinati a quella directory.
Verifica realmente i costruttori GTK prima di sostituire i pannelli attivi.

Mantieni I miei filamenti calibrati come elenco principale, distinto dalle
basi generiche Orca e dai profili ancora da calibrare. Consenti nome, marca,
prodotto, materiale, colore con selettore e HEX, temperature ugello/piano,
flow ratio e massimo flusso. La selezione di un profilo gia provato deve
richiamarne i valori per il tool e ugello montati senza reinserimenti.

Leggi dal catalogo Orca la configurazione reale dei quattro tool. Non fissare
0,4/0,4/0,6/0,8 nel comportamento dei pannelli. Mantieni l'archivio calibrazioni
con chiave tool/diametro/Standard-CHT: escludi valori incompatibili e recuperali
quando si rimonta lo stesso ugello. Non segnare una stima CHT come calibrata.

Mantieni test PA a righe, flow a campioni e massimo flusso a fasce crescenti.
I risultati si scelgono visivamente; la cella di carico non li misura. Usa
geometria, volume estruso e velocita coerenti col diametro configurato. Salva
il risultato solo sul filamento/tool/configurazione corretti. Per il massimo
flusso conserva un margine dichiarato; non chiamare massimo un test che non
ha raggiunto difetti o il cui limite superiore e stato scelto arbitrariamente.

Tutti i test fisici devono essere bloccati se geometry_verified o
cleaning_verified sono falsi. Usa le macro INDX esistenti e collaudate,
compresa la pulizia del nozzle prima delle tastature. Non inventare dock,
pinout, finecorsa, offset o quote Z. Non sbloccare i gate per superare un test.
Verifica che i pulsanti di assegnazione/sincronizzazione non muovano o scaldino
la stampante. Non usare la vecchia testa o il buffer rimossi dalla conversione.

Installa solo dopo i controlli software; verifica menu, pagina filamenti,
richiamo profili, sincronizzazione e stato servizi. Se la macchina non e
raggiungibile, consegna i file preparati e descrivi cosa non e stato installato.
Prima di flash o modifiche irreversibili verifica guide ufficiali, firmware,
pinout e rollback, poi chiedi conferma su un intervento concreto. Riporta
esattamente cio che e stato testato e prepara le istruzioni di ripristino.
```

## 3. Pubblicare una nuova anteprima

```text
Prepara una release sperimentale del progetto INDX. Prima verifica sorgente
base e patch, build, test della pipeline, test Python e sincronizzazione GUI
isolata. Controlla che documentazione e PDF descrivano lo stato reale.

Escludi credenziali, token, chiavi SSH, IP personali, profili con dati privati,
log, cache e risultati di calibrazione fittizi. Conserva licenze e riferimenti
upstream. Pubblica solo i file previsti e controlla il contenuto online.

Distingui la compatibilita SV08 Max in prova da quella futura con altre
stampanti. Non dichiarare collaudo fisico o calibrazione automatica se non
eseguiti. Non distribuire quote hardware non verificate come configurazione
pronta all'uso. Aggiorna changelog, istruzioni di ripristino e limiti noti.
```

Adattamento Z: al cambio ugello con Ugelli, riduci automaticamente layer e primo strato al limite prudente comune dei quattro tool (70% del diametro). Crea un processo separato, preserva gli altri parametri e ripristina le altezze richieste al ritorno a ugelli compatibili se non modificate manualmente. Prova 0,20 mm di ugello: layer 0,40 deve scendere a 0,14 mm; il riempimento combinato mantiene il limite del suo ugello.
