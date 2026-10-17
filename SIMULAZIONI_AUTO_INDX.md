# Simulazioni dello slicing automatico INDX

60 slicing reali nel motore FFF: 5 montaggi, 3 modalita, altezze richieste 0,10 e 0,40 mm, geometrie 20 x 20 x 8 e 20 x 2 x 8 mm. **Tutte passate: 967 asserzioni.** Regressioni GCodeWriter/CombinedInfill/UsedLayerTools: **467 asserzioni in 38 test**, passate. IndxChecks: 275 asserzioni in 11 test, passate.

La proposta viene calcolata dalla stessa funzione di Orca. Il test applica la regola GUI min(altezza richiesta, limite dei tool usati), esporta il G-code e lo analizza con GCodeProcessor, che alimenta l'anteprima. Verifica tool di pareti/infill, spessori positivi entro i rispettivi limiti, altezza finale e somma degli intervalli Z per il riempimento combinato.

## Risultati misurati nel G-code

Tabella per il parallelepipedo 20 x 20 x 8 mm con richiesta iniziale di 0,40 mm. Tutte le 60 combinazioni, inclusa la geometria sottile e la richiesta fine di 0,10 mm, sono nel [JSON dei risultati](SIMULAZIONI_AUTO_INDX.json). Lo spessore massimo infill dipende anche dalla geometria: non e obbligato a raggiungere il limite dell'ugello.

| Ugelli montati (mm) | Modalita | Ugello pareti / infill | Layer applicato | Max pareti nel G-code | Max infill nel G-code |
|---|---|---|---|---|---|
| 0.6, 0.4, 0.6, 0.8 | Dettaglio | 0.4 / 0.8 | 0.28 | 0.28 | 0.56 |
| 0.6, 0.4, 0.6, 0.8 | Equilibrato | 0.6 / 0.8 | 0.4 | 0.4 | 0.4 |
| 0.6, 0.4, 0.6, 0.8 | Veloce | 0.8 / 0.8 | 0.4 | 0.4 | 0.4 |
| 0.2, 0.4, 0.6, 0.8, 1 | Dettaglio | 0.2 / 1 | 0.14 | 0.14 | 0.7 |
| 0.2, 0.4, 0.6, 0.8, 1 | Equilibrato | 0.6 / 1 | 0.4 | 0.4 | 0.4 |
| 0.2, 0.4, 0.6, 0.8, 1 | Veloce | 1 / 1 | 0.4 | 0.4 | 0.4 |
| 0.4 | Dettaglio | 0.4 / 0.4 | 0.28 | 0.28 | 0.28 |
| 0.4 | Equilibrato | 0.4 / 0.4 | 0.28 | 0.28 | 0.28 |
| 0.4 | Veloce | 0.4 / 0.4 | 0.28 | 0.28 | 0.28 |
| 0.2, 0.8 | Dettaglio | 0.2 / 0.8 | 0.14 | 0.14 | 0.56 |
| 0.2, 0.8 | Equilibrato | 0.2 / 0.8 | 0.14 | 0.14 | 0.56 |
| 0.2, 0.8 | Veloce | 0.8 / 0.8 | 0.4 | 0.4 | 0.4 |
| 0.2, 0.4, 0.4, 0.6, 0.6, 0.8, 1, 1.2 | Dettaglio | 0.2 / 1.2 | 0.14 | 0.14 | 0.84 |
| 0.2, 0.4, 0.4, 0.6, 0.6, 0.8, 1, 1.2 | Equilibrato | 0.6 / 1.2 | 0.4 | 0.4 | 0.8 |
| 0.2, 0.4, 0.4, 0.6, 0.6, 0.8, 1, 1.2 | Veloce | 1.2 / 1.2 | 0.4 | 0.4 | 0.8 |

## Interfaccia e riproduzione

Nella GUI Windows installata il passaggio Veloce > Equilibrato e stato eseguito premendo solo la modalita: slicing e metriche aggiornati senza premere Ricalcola. Il pulsante Scegli come stampare e stato rimosso dalla home. Nessun invio alla macchina.

Il test riproducibile e in tests/fff_print/test_fill.cpp nella patch, tag [IndxSimulation]. Compilare Release e avviare fff_print_tests con quel filtro. La matrice e un test parametrizzato con 60 combinazioni, non 60 test Catch distinti. Le regressioni separate coprono anche tool usati per supporti e conteggi fino a 64.

I risultati usano profili PLA sintetici del test; nella matrice torre e supporti sono disabilitati. I diametri fino a 1,2 mm verificano il limite software, senza dichiarare disponibilita fisica degli ugelli INDX. Queste prove non misurano qualita, portata reale, PA o affidabilita meccanica. Il workflow GitHub verifica il pacchetto Python; la compilazione e gli slicing C++ sono stati eseguiti localmente.
