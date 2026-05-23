# Pubblicazione e Release

Regole per la generazione degli artefatti di pubblicazione e release per sessione.

---

## Pubblicazione (`public/`)

Artefatti tracciati da git, destinati alla condivisione pubblica.

### Contenuto

| Tipo | Formato | Contenuto |
|------|---------|-----------|
| PDF avventura | `.pdf` (lowres) | Documento principale + tutti i moduli |
| Stat block | `.pdf` | PDF unico con tutti gli stat block NPC/mostri homebrew (no generici) |
| Compendium | `.xml` | FightClub XML, solo NPC/mostri homebrew (no generici). Flag `--with-generic` per includere anche i generici. |
| Mappe e immagini | `.zip` | Tutte le mappe e immagini dell'avventura (versioni lowres) |

### Naming

```
public/
├── NomeAvventura_YYYYMMDD_lowres_it.pdf
├── NomeAvventura_YYYYMMDD_lowres_en.pdf
├── NomeAvventura_Statblocks_it.pdf
├── NomeAvventura_Statblocks_en.pdf
├── NomeAvventura_Compendium_it.xml
├── NomeAvventura_Compendium_en.xml
└── NomeAvventura_Maps_lowres.zip
```

### Procedura

Per ogni lingua nel `manifest.json`:

1. `python3 tech/fightclub/generate-statblocks.py <Avventura> [--lang <lang>]`
2. `python3 tech/create-pdf-adventure/create-pdf-adventure.py <Avventura> --lowres [--lang <lang>]`
3. `python3 tech/create-pdf-adventure/optimize-images.py <Avventura>`
4. Rimuovere vecchie versioni: `rm -f public/<Avventura>_*`
5. Copiare PDF avventura in `public/`
6. Creare ZIP mappe lowres
7. Copiare stat block PDF (solo homebrew) in `public/`
8. Copiare compendium XML in `public/`

### Cosa NON va nel PDF pubblicato

- Stat block di mostri generici (Skeleton, Giant Rat, Swarm of Rats, ecc.)
- Questi vanno in `tech/data/monsters/` e sono referenziati per nome + pagina MM nei moduli

---

## Release per sessione (`releases/`)

Artefatti di lavoro per una singola sessione di gioco. Non tracciati da git.

### Contenuto

| Tipo | Formato | Contenuto |
|------|---------|-----------|
| PDF sessione | `.pdf` | Documento principale + solo il modulo della sessione |
| Stat block sessione | `.pdf` | Tutti gli stat block necessari per la sessione, **compresi i mostri generici** |
| Mappe e immagini | `.zip` | Solo le mappe/immagini necessarie per quella sessione |

### Naming

```
releases/<Avventura>/
├── <Avventura>_YYYYMMDD_only-<NN>_doc.pdf
├── <Avventura>_session_<NN>_statblocks.pdf
└── <Avventura>_session_<NN>_maps.zip
```

### Procedura

1. `python3 tech/create-pdf-adventure/create-pdf-adventure.py <Avventura> --only doc,<NN>`
2. Generare PDF stat block con tutti i mostri/NPC del modulo (homebrew + generici)
3. Creare ZIP con mappe/immagini del modulo

### Lista mostri/NPC per modulo

Ogni modulo deve avere una sezione `## Nemici` (già prevista in adventure-template.md) che elenca tutti i mostri e NPC necessari per quel modulo, sia homebrew che generici. Questa lista è la fonte per generare la release di sessione.

---

## Mostri generici vs homebrew

| Tipo | Dove va lo stat block | Nel PDF pubblicato? | Nella release sessione? |
|------|----------------------|--------------------|-----------------------|
| Generico (MM standard, senza modifiche) | `tech/data/monsters/` | No | Sì |
| Homebrew (nome proprio o modifiche) | `adventures/<Avventura>/<lang>/characters/markdown/` | Sì | Sì |

**Esempi generici:** Skeleton, Giant Rat, Swarm of Rats, Dire Wolf, Owlbear, Wight, Wraith
**Esempi homebrew:** MON_RattoCorrotto (Giant Rat + Pack Tactics), MON_ChefMorticcio (Ghoul cuoco), MON_TeppistaCharmato (Cultista charmato)
