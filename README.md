# Codex Regia

**Una squadra pronta per usare Codex dentro Paperclip, con collegamenti a Codex Engineering Kit e Codex SEO.**

[English](README.en.md) · [Guida italiana](docs/GUIDA-IT.md) · [Demo interattiva](examples/index.html) · [Collaudo](docs/VERIFICATION.md) · [Paperclip originale](https://github.com/paperclipai/paperclip)

Cinque ruoli, tre skill, un progetto fittizio e un importatore locale. Gli agenti vengono importati **in pausa**: l'importazione non avvia un'azienda autonoma.

## La squadra

| Ruolo | Compito |
|---|---|
| Coordinamento | Definisce obiettivi, criteri di accettazione e prove |
| Sviluppo | Realizza modifiche e test riproducibili |
| Qualità | Controlla risultati e regressioni |
| Sicurezza | Esamina i rischi nel progetto autorizzato |
| SEO | Analizza contenuti e ricerca, dichiarando i limiti |

Le skill incluse sono `regia-workflow`, `ecc-bridge` e `seo-bridge`. Le ultime due verificano che i kit completi siano disponibili nell'ambiente dell'agente prima di usarli: **non li installano né li duplicano**. Kit separati: [Codex Engineering Kit](https://github.com/DennisResponsa/codex-engineering-kit) e [Codex SEO](https://github.com/DennisResponsa/codex-seo).

## Prova la demo

Scarica il repository e apri `examples/index.html`. È una pagina interattiva in italiano, senza server, tracker o AI avviate. Seleziona i ruoli per esplorare responsabilità e risultati attesi. La pagina non simula risultati di esecuzioni mai avvenute.

## Avvia la regia vera

Servono Node.js 24.11 o successivo, Python 3.10 o successivo e Codex CLI installato e autenticato. Versione Paperclip collaudata: **2026.1106.0**.

```sh
git clone https://github.com/DennisResponsa/codex-regia.git
cd codex-regia
python3 scripts/regia.py check
python3 -m unittest discover -s tests -v
```

Avvia Paperclip in un terminale, senza installare un servizio automatico:

```sh
PORT=3188 npx --yes paperclipai@2026.1106.0 onboard \
  --data-dir "$HOME/.local/share/codex-regia/instance" \
  --bind loopback --yes --no-install-service
```

Da un altro terminale, nella cartella del repository:

```sh
python3 scripts/regia.py preview --workspace examples
python3 scripts/regia.py import --workspace examples
```

Apri **http://127.0.0.1:3188**: troverai `Codex Regia Demo`, cinque agenti in pausa, tre skill, un progetto e un'attività iniziale non assegnata. L'importatore verifica la configurazione ricevuta dal server e rifiuta duplicati con lo stesso nome.

Per fermare il server premi Ctrl+C nel suo terminale. Per riaprire un'installazione già configurata:

```sh
npx --yes paperclipai@2026.1106.0 run \
  --data-dir "$HOME/.local/share/codex-regia/instance"
```

## Il primo incarico

Configura il workspace dimostrativo, riattiva **un solo agente** e abilita il suo avvio manuale. Lascia disabilitati timer, avvii su assegnazione e automazioni. Una prova utile: leggere `site.html` e riportare titolo, numero di H1 e presenza della descrizione. Controlla il risultato e rimetti l'agente in pausa. “Resume all” non sostituisce la configurazione di ambito e permessi.

Il pacchetto seleziona esplicitamente l'adattatore `legacy`: nella versione collaudata il percorso d'importazione con runner nativo rifiuta il campo che disabilita il bypass delle protezioni. Il bypass rimane disabilitato; Paperclip gestisce l'esecuzione.

## Italiano

Demo, nomi dei ruoli, istruzioni della squadra, guida e README sono in italiano. Anche i rapporti degli agenti devono essere prodotti in italiano, salvo richiesta diversa. **L'interfaccia Paperclip della versione installata rimane in inglese**: la verifica di impostazioni generali e profilo non ha mostrato un selettore della lingua. Comandi, identificatori e licenze conservano la forma originale. Non dichiariamo una traduzione completa dell'app upstream.

## Limiti da conoscere

- Codex normalmente comunica con OpenAI: una regia locale non è un modello offline.
- La pagina web è limitata a questo computer. Questo non isola automaticamente tutti i file e la rete accessibili agli agenti: contano i permessi del runtime.
- Timeout di 180 secondi e massimo un'esecuzione **per agente**; non è un limite globale per tutta la squadra.
- Budget iniziale di 500 centesimi di dollaro per agente al mese, basato sui consumi registrati da Paperclip. Non garantisce il limite della fattura OpenAI né della quota abbonamento; i consumi in corso possono superarlo.
- Non è implementata una quota rigida del disco. Runtime, database, log e cache possono crescere. Le misure della prova sono nel rapporto di collaudo.
- Nessun servizio di avvio automatico, attività ricorrente o progetto cliente viene installato dall'importatore.
- L'importazione upstream può lasciare una squadra parziale in caso di errore. Verificarla e archiviarla prima di riprovare: nessun tentativo automatico.
- Lo schema 6 omette cronologia avanzata, date e legami tra attività: l'avviso upstream è atteso perché la demo non contiene questi dati.
- Un test di collegamento riuscito non dimostra che ogni possibile squadra, skill o incarico sia stato collaudato.

## Sviluppo e attribuzione

`team.json` contiene la configurazione; `company/.paperclip.yaml` ne è la rappresentazione importabile. Il controllo rifiuta divergenze. Dopo ogni modifica esegui i test.

È un progetto d'integrazione indipendente di DennisResponsa, **non** una distribuzione ufficiale OpenAI o Paperclip. Istruzioni e demo originali sono MIT. Attribuzioni in [NOTICE](NOTICE.md). Il Centro Codex privato, le chat, i file dei clienti e le credenziali non fanno parte di questo repository.
