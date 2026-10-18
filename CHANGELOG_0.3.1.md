# 0.3.1 preview — 18 October 2026

## SV08 Max / Italiano

- Confronto congiunto di assegnazioni ugelli, altezza layer e riempimento combinato; pareti e superfici mantengono materiale e colore primari. Altri colori dello stesso materiale sono ammessi nel riempimento.
- Ottimizzazione automatica indipendente dall'altezza manuale della barra laterale; rispetta i limiti degli ugelli effettivamente usati, la portata dei filamenti e lo scopo scelto.
- Limite software dello 0,8 mm portato a 0,64 mm. Ricerca anche 0,30/0,60 mm e stampa con un solo ugello 0,8 mm. Il limite software non certifica la qualita fisica di stampa.
- Griglia Z dichiarata nelle note macchina: `INDX_Z_STEP`. Per il solo profilo SV08 Max verificato: 0,001875 mm. Nessuna griglia SV08 Max imposta al profilo Generic.
- Corretto il controllo che considerava un piccolo ugello inizialmente assegnato ma poi inutilizzato.
- Risultati delle tre modalita memorizzati; confermare apre l'anteprima senza ripetere lo slicing. Gestione delle varianti non valide senza perdere il miglior risultato valido.
- Numero totale layer nelle schede, nella conferma e nel riepilogo manuale, ricavato dal risultato nativo.

## Generic / English

The Generic edition remains a basic manual INDX starting profile, without the custom SV08 Max automatic synchronization/Auto Slice workflow enabled. It shares the updated slicing engine, active-nozzle validation and 0.8 mm software layer ceiling. Configure your own machine, macros, tool count, nozzle sizes and validated limits; no SV08 Max Z grid is assumed.

Both installers and portable ZIPs contain the same application DLL. Updates preserve an existing `dati` directory. Existing custom machine profiles may retain their own explicit maximum layer height; review those limits yourself. No firmware, printer motion or heating is performed by installation.

## Validation and limits

15,094 assertions in 49 focused native test cases passed. Native G-code tests verified layer counts, actual tool changes, primary exterior color, single-nozzle 0.8 mm at 0.60 mm (84 layers) and 0.639375 mm (79 layers), and combined infill. On the white test part, the faster valid result changed from 53 min 37 s to 37 min 15 s with zero tool changes. These are model/profile-specific estimates, not a performance guarantee.

The optimizer searches a discrete set of valid candidates and selects by native estimated time, with tool-change count and filament as tie breakers. It does not prove a global optimum, simulate mechanical strength or replace physical commissioning. INDX hardware print validation remains pending. The 8 s tool-change estimate remains provisional until measured.

Source is distributed as the full patch against the exact upstream revision in UPSTREAM.json, with prepare_source.py and the upstream license. No personal profiles, printer addresses, logs or temporary slicing projects are included.

## Fast logical preselection

The planner first scores all eligible nozzle/Z/infill combinations using model-instance bounding boxes, shell thickness, path lengths, filament volumetric limits and provisional tool-change overhead. It then runs at most five diverse native finalists per mode/material, instead of slicing every theoretical candidate. The cards distinguish logical candidates from completed native slices. Final times/grams are native estimates; screening scores are never displayed as measured results.

This is a heuristic shortlist, not an exhaustive optimum. Bounding boxes do not describe internal geometry, cooling, supports or every travel, so a discarded candidate can be faster. Preserve native validation and inspect the selected G-code.

Native regression on the current 50 mm white part with structural purpose: 40 logical candidates screened, 10 native jobs instead of 40 (75% fewer jobs), same best result: 1 h 35 min 6 s, 238 layers, zero tool changes. Reduction is in job count, not a promise of 75% less wall-clock time for every model.
