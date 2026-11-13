# Rapporto di collaudo — v0.1.0

**13 novembre 2026.** Risultati osservati, non una certificazione generale di autonomia o sicurezza.

## Installazione e importazione

- Mac Apple Silicon, Node 24.22.1.
- Paperclip ufficiale **2026.1106.0**, commit server `d69631b01b9c658f80bf8bed389863dce82643e1`.
- Servizio sulla porta locale 3188: stato `ok`, modalità `local_trusted`, esposizione `private`.
- Anteprima riconosce cinque ruoli Codex, tre skill, un progetto fittizio e un'attività iniziale.
- Importazione riuscita: cinque agenti in pausa. Verificati adattatore, cartella di lavoro, timeout, bypass disabilitato, avvii automatici disabilitati e budget per agente.
- Lo schema 6 genera un avviso sulle date e sui collegamenti avanzati delle attività: la demo non contiene questa cronologia.
- Due primi tentativi con selezione automatica del runner hanno lasciato squadre incomplete: sono state archiviate. Il pacchetto ora seleziona esplicitamente l'adattatore legacy e documenta che gli errori upstream possono lasciare importazioni parziali.

## Prova reale con Codex

Il controllo dell'ambiente ha avuto esito positivo. Successivamente un'esecuzione manuale dell'agente Sviluppo ha letto il solo file fittizio `site.html`, restituendo:

```text
Title: Officina Aurora — laboratorio dimostrativo
Numero di H1: 1
Meta description: presente
REGIA_DEMO_OK
```

Stato finale del server: `succeeded`. Il risultato coincide con il controllo indipendente del file. Dopo la prova l'agente è stato rimesso in pausa, il messaggio temporaneo di collaudo azzerato e l'avvio manuale nuovamente disabilitato. Interfaccia finale: **0 in esecuzione, 5 in pausa, 0 errori**.

Questo dimostra una singola esecuzione circoscritta Paperclip → Codex → file locale → risultato. Non dimostra un ciclo autonomo completo di più agenti, la presenza dell'intero catalogo ECC/SEO in ogni ambiente o un audit completo di sicurezza e SEO.

## Test e interfaccia

- **10 test Python superati**: file del pacchetto, rifiuto di collegamenti simbolici e file inattesi, URL locali, cartella dedicata, anteprima senza importazione, protezione dai duplicati, versione non compatibile, configurazione insicura e verifica della pausa dopo importazione.
- Revisione indipendente del codice: nessun problema alto o critico rilevato.
- Demo aperta in Chrome: la scelta SEO aggiorna correttamente dettaglio e selezione. Controllo visivo desktop superato; vista mobile non collaudata separatamente.
- Centro Codex rigenerato con scheda dedicata, terzo kit, skill personale, demo, guida, repository, release e indirizzo locale.
- Clic reale dal catalogo alla dashboard Paperclip riuscito. Test esistenti del collegamento alla chat e del caso senza destinazione superati. Nessun messaggio inviato o conversazione trasferita automaticamente.
- Catalogo personale, schermate locali e dati privati esclusi dal pacchetto pubblico.

## Spazio osservato

Al termine della prova: circa **2,3 GiB** per il runtime Paperclip e **404 MiB** per i dati dell'istanza. La cache del gestore pacchetti è aggiuntiva e può essere condivisa. I sorgenti del pacchetto sono nell'ordine di 100 KiB, prima della cronologia Git.

Non sono quote rigide né garanzie sulla crescita futura. Nessun peso di modello scaricato e nessun servizio di avvio automatico installato. Per usare la dashboard serve il processo Paperclip attivo; si arresta con Ctrl+C.

## Italiano e limiti

Demo, squadra, istruzioni, guida e README sono in italiano. Per le prossime esecuzioni le istruzioni richiedono rapporti in italiano. L'interfaccia Paperclip 2026.1106.0 resta in inglese: nelle impostazioni generali e del profilo verificate non compare un selettore di lingua. Non è stata modificata la distribuzione compilata di Paperclip.

Il budget si basa sui costi registrati. Un'esecuzione con abbonamento può mostrare zero dollari pur consumando quota dell'account. Il parallelismo è limitato per agente, non per azienda. L'indirizzo locale del sito non isola i file accessibili al runtime. Questa è una prima integrazione collaudata, non una distribuzione multiutente già consolidata.
