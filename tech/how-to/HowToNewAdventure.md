# How-To: Creare una Nuova Avventura

Guida passo-passo per creare una nuova avventura dal template.

## Prerequisiti

```bash
bash tech/scripts/setup.sh
```

---

## Passo 1 — Scaffolding

```bash
bash tech/scripts/new-adventure.sh NomeMiaAvventura
```

Crea `adventures/NomeMiaAvventura/` con la struttura standard e `releases/NomeMiaAvventura/`.

---

## Passo 2 — Metadati base (wizard)

```bash
python3 tech/scripts/adventure-wizard.py NomeMiaAvventura
```

Il wizard chiede interattivamente: sistema, livello, durata, struttura (lineare/sandbox/mista), tono, saga (se applicabile), descrizione breve. Rilanciabile: salta i campi già compilati.

---

## Passo 3 — Rinomina i moduli

Il template crea `01_NomeModulo/` come placeholder. Rinominare secondo il contenuto reale:

```bash
mv adventures/NomeMiaAvventura/01_NomeModulo adventures/NomeMiaAvventura/01_NomePrimoModulo
mv adventures/NomeMiaAvventura/01_NomePrimoModulo/NomeMiaAvventura_Modulo01.md \
   adventures/NomeMiaAvventura/01_NomePrimoModulo/NomePrimoModulo.md
```

Per aggiungere altri moduli, copiare la struttura:

```bash
cp -r adventures/NomeMiaAvventura/01_NomePrimoModulo adventures/NomeMiaAvventura/02_NomeSecondoModulo
```

---

## Passo 4 — Aggiungi NPC

**Modalità wizard** (consigliata per NPC principali):
```bash
python3 tech/scripts/new-npc.py NomeMiaAvventura
```

**Modalità template** (per NPC secondari da riempire a mano):
```bash
python3 tech/scripts/new-npc.py NomeMiaAvventura --template
```

Rinominare il placeholder `personaggi/NPC_NomePersonaggio.md.placeholder` o eliminarlo se non serve.

---

## Passo 5 — Scrivi il contenuto

File da compilare in ordine consigliato:

1. `NomeMiaAvventura.md` — lore, introduzione, plot, NPC principali, struttura
2. `mappe/MappaGenerale.md` — luoghi, connessioni, distanze
3. `NN_NomeModulo/NomeModulo.md` — ogni modulo
4. `personaggi/NPC_*.md` — schede NPC
5. `PlanBook.md` — stato lavoro, todo, problemi aperti

---

## Passo 6 — Verifica

```bash
python3 tech/scripts/check-adventure.py NomeMiaAvventura
```

Iterare fino a zero errori. I warning sono accettabili.

---

## Passo 7 — Release (quando pronta)

```bash
bash tech/scripts/release.sh NomeMiaAvventura 0.1
```

Output in `releases/NomeMiaAvventura/`.
