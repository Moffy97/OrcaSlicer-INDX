# Profili per ugello e altezza layer

I profili hanno nomi come **INDX - Ugello 0.40 - Layer 0.12**. Il diametro è quello per cui la base è stata predisposta; il layer è l'altezza richiesta. Dettaglio, Equilibrato e Veloce restano le modalità separate di ottimizzazione dei tool.

| Ugello | Altezze layer in mm |
| --- | --- |
| 0,20 mm | 0,06 · 0,08 · 0,10 · 0,12 · 0,14 |
| 0,40 mm | 0,10 · 0,12 · 0,14 · 0,16 · 0,20 · 0,24 · 0,28 |
| 0,60 mm | 0,16 · 0,20 · 0,24 · 0,28 · 0,30 · 0,32 · 0,36 · 0,40 · 0,42 |
| 0,80 mm | 0,20 · 0,24 · 0,28 · 0,30 · 0,32 · 0,36 · 0,40 · 0,42 · 0,48 · 0,56 |

Sull'installazione verificata sono predisposte le 26 combinazioni per i diametri dichiarati in Orca: 0,40 / 0,60 / 0,80 mm. Lo 0,20 non è stato dichiarato montato: i suoi cinque profili sono nel pacchetto scaricabile per quando verrà configurato. Il pacchetto **profili-ugello-layer.zip** contiene tutte le 31 basi JSON; estrarre e importare quelle adatte alla propria configurazione. `profili-ugello-layer.json` elenca le combinazioni. Resta anche la base Collaudo prudente.

Il profilo di processo **non cambia l'hardware né il tool del modello**. Scegliere il tool corrispondente. Le larghezze sono proporzionali all'ugello effettivo; PA, temperature e portata provengono dal filamento. Auto slicing optimization può distribuire pareti e riempimento su diametri diversi: l'altezza effettiva viene ridotta se uno degli ugelli realmente usati impone un limite inferiore. Un ugello fine montato ma inutilizzato non limita la stampa. Queste basi rispettano il limite software attuale del 70% del diametro e conservano i limiti Performance da verificare sul montaggio reale.

I confronti automatici riusano varianti Dettaglio, Equilibrato e Veloce **nel progetto**, senza creare un nuovo processo utente per ogni codice. Le alternative di materiale e le varianti Z adattata sono etichettate. Salvare il 3MF per conservarle; per una propria base permanente usare Salva con nome.

Le vecchie copie con nomi a codice sono archiviate con backup. Restano i processi personali precedenti e una copia nominata Progetto attuale che conserva i parametri del lavoro aperto. Profili delle altre stampanti, filamenti e calibrazioni personali non vengono rimossi.


