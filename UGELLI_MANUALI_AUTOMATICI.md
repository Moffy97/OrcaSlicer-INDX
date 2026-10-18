# Ugelli: Automatico / Manuale

La sezione Ugelli nella pagina principale mostra un campo diametro in mm e una scelta Standard / CHT per ogni tool, con numero variabile di tool.

- **Automatico** importa numero, diametri e tipi confermati in KlipperScreen. Senza una dichiarazione disponibile conserva gli ultimi valori; non inventa il montaggio fisico. I campi restano in sola lettura. Il passaggio ad Automatico ripristina la lettura dalla macchina.
- **Manuale** permette di cambiare diametro (0,10–2,00 mm) e Standard/CHT direttamente nel profilo Orca. Confermare il diametro con Invio, con le frecce oppure uscendo dal campo. La sincronizzazione non sovrascrive questi ugelli. La preferenza e conservata per profilo stampante.
- Questa scelta e indipendente da **Mappatura Automatico / Manuale** nella sezione Filamenti. Le associazioni manuali vengono conservate quando si cambia un ugello.
- **+ / - in Ugelli:** in Manuale aggiungono un tool da 0,4 mm Standard o rimuovono l'ultimo tool. Il minimo e uno; il massimo software e 64. Rimuovere un tool mantiene i filamenti e riporta a T0 le sue assegnazioni del piatto corrente: controllare le assegnazioni e rislicerare. Le altre piastre richiedono verifica prima dello slicing.
- **+ / - in Filamenti:** aggiungono un filamento al progetto o rimuovono l'ultimo, con la gestione nativa Orca delle assegnazioni al modello. Non modificano il numero di ugelli. Aggiungere un tool crea anche lo slot minimo necessario se manca.

La modifica manuale riguarda Orca: non cambia il montaggio dichiarato sul touch, i dock o il firmware. Prima di inviare una stampa i controlli confrontano il progetto con la stampante. Per un montaggio gestito dal touch usare Automatico. Cambiare gli ugelli richiede di rislicerare; PA, flow e portata misurati restano legati a filamento, tool, diametro e tipo corrispondenti. CHT aumenta solo le stime generiche, senza attestare una portata misurata.

Verifica software: compilazione Windows Release, modifica diretta del tipo Standard/CHT e del diametro, lettura dei valori aggiornati anche nella mappatura filamenti e aggiunta/rimozione degli ugelli. Il progetto di prova salvato con due tool e stato escluso dall'avvio; ripristinati i quattro tool. I nuovi pulsanti filamenti richiamano le operazioni native Orca: la prova interattiva finale e affidata all'utente, come richiesto. Nessuna stampa fisica, movimento o riscaldamento.
