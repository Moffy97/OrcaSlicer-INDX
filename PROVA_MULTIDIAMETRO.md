# Prova di slicing multidiametro: pareti 0,20 mm e infill 0,80 mm

Prova software del 17 ottobre 2026 sulla build OrcaSlicer INDX per SV08 Max. Nessuna stampa fisica eseguita. Il risultato verifica slicing, anteprima e G-code; non certifica montaggio, offset, agganci o qualita di stampa.

![Layer 45 a Z 6,30 mm, colorato per altezza](anteprima-multidiametro.png)

## Impostazioni e risultato

Blocco 40 x 40 x 12 mm; riempimento rettilineo al 20%; mappatura manuale filamento 1 -> T0, filamento 2 -> T1. Pareti e superfici su T0 (ugello 0,20 mm), infill sparso su T1 (ugello 0,80 mm). Gli altri tool non sono usati.

| Controllo | Risultato |
| --- | --- |
| Altezza richiesta nel progetto | 0,40 mm, adattata automaticamente a 0,14 mm |
| Pareti | Solo T0, altezza massima 0,14 mm |
| Riempimento combinato | Solo T1, 18 gruppi da 0,56 mm = 4 x 0,14 mm |
| Layer 45 | Z 6,30 mm: pareti da 0,14 mm e infill da 0,56 mm terminano alla stessa quota |
| Chiusura del modello | 86 layer, Z finale 12,00 mm; ultimi layer circa 0,132 mm |
| Volume E/mm del combinato | Scarto massimo dal calcolo geometrico inferiore a 0,05%, compatibile con gli arrotondamenti del G-code |
| Accelerazioni | Pareti interne e travel a 3.000 mm/s2, entro i limiti macchina; avviso assente nel nuovo slicing |

Nelle transizioni alle zone solide, l'infill puo essere da 0,14 mm. La combinazione viene applicata dove la geometria lo permette. La legenda dell'anteprima arrotonda il valore minimo a 0,13 mm; il G-code riporta le altezze effettive.

## File e riproduzione

Scaricare [prova-multidiametro.zip](prova-multidiametro.zip) ed estrarlo in una cartella dedicata. Contiene modello STL, progetto 3MF, G-code esportato, anteprima, estratto del layer 45, misure JSON e verificatore Python.

1. Aprire `pareti02-infill08-verifica.3mf` nella build personalizzata di questo repository. Il progetto conserva la richiesta da 0,40 mm per verificare l'adattamento automatico.
2. Attendere l'aggiornamento del processo a 0,14 mm e controllare la mappatura manuale T0/T1, pareti su filamento 1, infill su filamento 2 e combinazione infill attiva.
3. Elaborare il piatto. In anteprima scegliere **Altezza strato** e isolare il layer 45 a Z 6,30 mm: contorno fine blu, infill spesso rosso.
4. Per analizzare il G-code incluso, eseguire `python verifica_gcode.py` nella cartella estratta. Il controllo usa soltanto la libreria standard Python e file locali, senza collegarsi alla stampante. Scrive `verifica-numerica.json` e `VERIFICA.md` nella stessa cartella: per conservarne gli originali, usare una copia della cartella.

La verifica controlla tool per funzione, altezza massima, quota Z reale durante l'estrusione e somma dei quattro layer per ogni gruppo. Controlla anche il volume E/mm usando larghezza, altezza, diametro filamento e flow ratio. Esclude risalite di viaggio e retrazioni.

Il primo export esplorativo aveva perso i ruoli e la combinazione a causa dei metadati del progetto CLI: non e incluso. I file pubblicati conservano esplicitamente gli override di processo e la mappatura del piatto. Il G-code e un artefatto di analisi; un collaudo fisico della conversione rimane separato.
