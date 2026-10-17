# Plugin INDX Studio per KlipperScreen — SV08 Max

Pacchetto aggiuntivo per una SV08 Max con host Linux, KlipperScreen, Moonraker e conversione Bondtech INDX gia configurati. Include i pannelli, il tema touch, la libreria filamenti, la dichiarazione dei tool e il servizio di sincronizzazione bidirezionale in background. Non e un plugin ufficiale KlipperScreen o Bondtech.

Il pacchetto replica le funzioni software della preview SV08 Max, senza copiare filamenti personali, calibrazioni, quote dock, offset, indirizzi o password della macchina di sviluppo. Non installa firmware, pinout o macro di movimento e non abilita il commissioning.

## Installazione

Scaricare `KlipperScreen-INDX-SV08Max-plugin.zip` dalle Releases, estrarlo sull'host della stampante ed eseguire come utente della stampante:

```sh
python3 install_sv08max.py --check
python3 install_sv08max.py --install
```

I percorsi predefiniti sono `~/KlipperScreen` e `~/printer_data/config`. Se diversi, passarli con `--klipperscreen-dir` e `--config-dir`. Occorre una configurazione KlipperScreen esistente e l'accesso gia configurato a systemd tramite `sudo -n`. L'installatore non cambia i permessi sudo.

L'installazione verifica gli hash, compila la sintassi, salva i file/menu/tema/unit precedenti, aggiunge INDX al touch, abilita `indx-filament-sync.service` e riavvia soltanto KlipperScreen e il servizio dati. Durante la preparazione esegue prima il controllo e non invia G-code. La stampante deve essere inattiva prima dell'installazione.

## Configurazione iniziale

1. Collegare la build Orca INDX alla propria stampante dalla sezione Stampante.
2. Sul touch dichiarare tool, diametri e Standard/CHT in Tool e dock; impostare dock e offset reali solo dopo averli verificati.
3. Da Filamenti sincronizzare il catalogo Orca, scegliere marca/materiale/colore e assegnare i profili ai tool.
4. In Orca usare Ugelli Automatico per leggere il montaggio confermato. Colore e profilo assegnato si sincronizzano nei due sensi con le protezioni per conflitti, bozze e stampa attiva.
5. Salvare come Standard per usare valori di base, oppure eseguire e valutare le calibrazioni dopo il collaudo fisico.

Le procedure fisiche richiedono le macro di conversione verificate `_INDX_SETUP`, `_INDX_REQUIRE_COMMISSIONED`, `INDX_PRINT_START`, `INDX_PRINT_END`, `CHANGE_TOOL`. Il plugin non le inventa per una macchina sconosciuta: in loro assenza calibrazione e commissioning restano indisponibili/protetti. I pannelli non sostituiscono la configurazione Bondtech del firmware.

## Ripristino

L'installatore stampa la cartella backup. Per ripristinarla:

```sh
python3 install_sv08max.py --rollback /percorso/del/backup
```

Il ripristino conserva libreria filamenti e calibrazioni attuali. Non applica una configurazione firmware.

## Due profili diversi

Il profilo **SV08 Max completo** usa questo plugin e le funzioni Auto slice/sync. Il profilo **INDX generico semplice** non lo richiede, non sincronizza dati e non abilita l'ottimizzazione automatica. Per il generico usare la configurazione ufficiale INDX e adattare il profilo alla propria stampante.
