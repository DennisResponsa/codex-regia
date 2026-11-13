# Codex Regia — guida pratica

Codex Regia prepara una squadra per Paperclip usando Codex. Non è un altro modello da scaricare: Paperclip organizza le attività, Codex svolge il lavoro.

## Cosa aprire

- `examples/index.html`: demo illustrativa, funziona anche senza Internet. Seleziona i cinque ruoli e leggi le responsabilità. Non avvia AI.
- `http://127.0.0.1:3188`: regia vera, disponibile quando Paperclip è avviato.
- `README.md`: installazione ripetibile e limiti verificati.

Nel Centro Codex privato la scheda **Codex Regia** raccoglie questi collegamenti. “Usa nella chat” torna alla conversazione di origine con una richiesta precompilata: non trasferisce automaticamente la chat a Paperclip e non avvia agenti.

## Procedura iniziale

1. Segui il Quick start nel README. Usa la cartella `examples` per la prima prova.
2. Controlla l'anteprima: cinque agenti, tre skill, un progetto e una attività.
3. Importa. Tutti gli agenti devono risultare in pausa.
4. Per il primo incarico attiva solo un agente e il relativo avvio manuale. I timer restano disattivati.
5. Controlla il risultato e i test. Riporta l'agente in pausa a fine prova.

Le skill bridge spiegano come usare ECC e Codex SEO **se presenti nel runtime dell'agente**. Vederli nel Centro Codex non dimostra che siano disponibili anche in ogni ambiente Paperclip. Quando mancano, il ruolo lo deve dichiarare.

## Spazio e costi

Il pacchetto pubblico è piccolo. L'installazione completa di Paperclip include database e dipendenze ed è molto più grande. Non scarica pesi Qwen. Non contiene un limite rigido allo spazio: la configurazione iniziale evita esecuzioni ricorrenti e il server si ferma chiudendo il processo con Ctrl+C. Prima di usarlo continuativamente va definita una politica di conservazione dei dati.

Il budget è espresso in centesimi di dollaro per agente, basato sui consumi registrati da Paperclip. Non è una garanzia sul conto OpenAI. La prova locale non rende Codex un modello offline.

## Pubblicazione

Solo repository, demo fittizia e release sono pubblici. Il Centro Codex con le chat e i progetti personali rimane sul computer. Conservare sempre l'attribuzione a Paperclip, ECC e alle rispettive licenze.

## Lingua

I materiali Codex Regia sono in italiano. La versione Paperclip 2026.1106.0 collaudata mantiene l’interfaccia in inglese; nelle impostazioni esaminate non è presente un selettore della lingua. Non modificare file compilati del runtime per tradurli.
