# OrcaSlicer INDX - SV08 Max preview

Integrazione sperimentale tra una build personalizzata di **OrcaSlicer** e **KlipperScreen** per una Sovol SV08 Max convertita a Bondtech INDX.

**Target attuale: SV08 Max + INDX, quattro tool passivi, un solo feeder e riscaldatore fisico.** Il supporto ad altre stampanti e un obiettivo futuro, non una compatibilita gia verificata. Il progetto non e una release ufficiale OrcaSlicer, Bondtech, Sovol o KlipperScreen.

## Funzioni

- Libreria separata dei propri filamenti, con UUID stabile, nomi modificabili, marca, materiale e colore.
- Temperature ugello/piano, PA, flow ratio e massimo flusso volumetrico richiamabili senza reinserire i valori.
- Archivio calibrazioni per **filamento + tool + diametro + Standard/CHT**. Tornando alla stessa combinazione, i risultati vengono recuperati.
- Pulsante **Ugelli**: diametro indipendente per ciascun tool, da 0,10 a 2,00 mm nelle impostazioni software; la disponibilita fisica degli ugelli INDX e separata.
- Stima CHT modificabile per i profili generici: fattore iniziale 1,30. Il massimo flusso misurato prevale sempre sulla stima. Il diametro non viene usato come un moltiplicatore quadratico della capacita di fusione.
- Pulsante **INDX**: catalogo Orca standard/personale, importazione persistente dei profili e assegnazione T0-T3 al progetto. Salvataggio della libreria in background con Orca aperto.
- Test visivi PA, flow e massimo flusso dal touchscreen. La cella di carico non misura questi risultati.
- Combinazione riempimento INDX: l'ugello del riempimento puo depositare uno strato alto quanto la somma degli strati parete accorpati, entro il proprio limite di altezza. Per esempio, due strati parete da 0,20 mm corrispondono a un riempimento da 0,40 mm. Le intersezioni geometriche e le zone solide restano gestite da Orca.
- G-code adattato al feeder e al riscaldatore condivisi: PA sull'extruder fisico, nessun preriscaldamento degli ugelli parcheggiati.

## Stato e limiti

Anteprima software da testare e perfezionare sulla SV08 Max. Compilazione Windows Release e prove automatiche locali disponibili; la sincronizzazione e stata verificata con un server Moonraker simulato. I nuovi pannelli richiedono ancora verifica GTK sulla macchina e collaudo fisico di stampa. Non vengono forniti risultati di calibrazione inventati.

**Nessuna procedura di questo repository esegue flash, convalida pinout, certifica quote dock o abilita automaticamente movimenti.** Homing, pulizia, aggancio, offset e collegamenti devono essere verificati sulla singola macchina. Le macro di commissioning devono bloccare i test finche la macchina non e collaudata.

## Contenuto

| File | Utilizzo |
|---|---|
| `OrcaSlicer-INDX.patch` | Modifiche rispetto al commit ufficiale indicato in `UPSTREAM.json` |
| `prepare_source.py` | Scarica il sorgente ufficiale a quel commit e applica la patch |
| `touchscreen.zip` | Sorgenti dei pannelli, test Python e basi legacy esplicitamente non calibrate |
| `install_klipperscreen.py` | Installazione locale dei pannelli con backup; nessun accesso SSH incluso |
| `test_profiles.py` | Verifiche isolate di libreria, tipi di ugello e generatori di test |
| `PROMPTS.md` | Prompt riutilizzabili per modificare Orca e KlipperScreen |
| `Guida_OrcaSlicer_INDX_SV08Max.pdf` | Guida italiana al funzionamento e al collaudo |
| `LICENSE` | AGPL-3.0, mantenuta dal progetto OrcaSlicer |

## Preparare il sorgente Orca

Richiede Python 3 e Git. In una cartella di lavoro nuova:

```text
python prepare_source.py
```

Il programma crea `upstream-orca`, verifica il commit e applica la patch. Non modifica un checkout preesistente e non installa toolchain o firmware. La compilazione richiede le dipendenze e il compilatore descritti nella documentazione ufficiale OrcaSlicer. Su Windows usare una toolchain C++ completa e una build Release. Compilare anche `fff_print_tests` ed eseguirlo con filtro `[INDX]` e `[GCodeWriter]`.

## Preparare KlipperScreen

Sul computer che esegue KlipperScreen, dopo aver trasferito questa cartella:

```text
python3 test_profiles.py
python3 install_klipperscreen.py --klipperscreen-dir /home/USER/KlipperScreen --config-dir /home/USER/printer_data/config
```

Sostituire USER con l'utente reale. L'installatore crea un backup e compila la sintassi dei moduli. Non verifica pinout, non avvia test fisici e non riavvia servizi senza `--restart`. Prima del riavvio verificare dipendenze GTK e configurazione menu. Il vecchio pannello PA deve essere conservato nel backup per ripristino.

I test fisici richiedono le macro gia collaudate `_INDX_SETUP`, `_INDX_REQUIRE_COMMISSIONED`, `INDX_PRINT_START`, `INDX_PRINT_END` e `CHANGE_TOOL`. L'installatore non le inventa o sostituisce.

## Uso

1. Aprire la build INDX con un profilo stampante INDX a quattro tool e con impostazioni personali salvate.
2. In **Ugelli**, dichiarare quelli realmente montati. Standard/CHT e una scelta indipendente dal materiale dell'ugello e dalla variante di estrusore interna di Orca.
3. Nel pulsante **INDX**, configurare Moonraker con clic destro. Usare un indirizzo della propria stampante: il repository non contiene credenziali o indirizzi personali.
4. Sul touchscreen sincronizzare il catalogo, creare il filamento da una base appropriata, impostare colore/temperature e salvarlo con un nome riconoscibile.
5. A macchina collaudata, stampare e valutare i test. Salvare i risultati nel profilo. Per il massimo flusso si conserva il 90% dell'ultima fascia scelta senza difetti.
6. Sincronizzare INDX in Orca per applicare i tool al progetto, salvarlo e rislicera. La sincronizzazione dei dati non modifica un G-code gia esportato.

Quando si cambiano diametro o tipo, le calibrazioni precedenti restano archiviate ma non vengono applicate alla nuova combinazione. Gli aumenti CHT sono stime di partenza: non attestano una prestazione fisica della SV08 Max.

Dal pulsante **Ugelli**, il cambio hardware adatta automaticamente altezza strato e primo strato in un processo INDX separato, conservando gli altri parametri. Il limite prudente e il minore dei limiti dei quattro tool configurati (70% del diametro): un ugello da 0,20 mm limita lo strato a 0,14 mm. Questo vale anche se quel tool non e ancora assegnato a un oggetto. Tornando a ugelli piu grandi si ripristinano le altezze richieste, se non sono state cambiate manualmente. Il riempimento combinato usa invece il limite del proprio tool. Dopo il cambio salvare e rielaborare lo slicing.

## Riferimenti

- [Sorgente e documentazione OrcaSlicer](https://github.com/OrcaSlicer/OrcaSlicer)
- [Calibrazioni Orca](https://github.com/OrcaSlicer/OrcaSlicer/wiki/Calibration)
- [Bondtech INDX](https://www.bondtech.se/indx-by-bondtech/)
- [Studio Bondtech sulla portata CHT](https://www.bondtech.se/intranet/white-paper-max-flow-rate/)
- [KlipperScreen](https://github.com/KlipperScreen/KlipperScreen)

Lo studio CHT riguarda un hardware specifico: non e una misura di questa conversione. I valori calibrati del proprio filamento e ugello hanno priorita.
