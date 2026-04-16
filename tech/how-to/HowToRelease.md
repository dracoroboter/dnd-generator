# How-To: Creare una Release

Guida passo-passo per generare una release (PDF + ZIP) di un'avventura.

## Prerequisiti

Esegui il setup una volta sola:

```bash
bash tech/scripts/setup.sh
```

Installa automaticamente: `pandoc`, `wkhtmltopdf`, `zip`.

## Struttura attesa dell'avventura

Lo script si aspetta che l'avventura sia in `adventures/<NomeAvventura>/` con questa struttura:

```
adventures/<NomeAvventura>/
├── README.md          ← non incluso nel PDF
├── AdventureBook.md   ← non incluso nel PDF
├── PlanBook.md        ← non incluso nel PDF
├── *.md               ← convertiti in PDF
├── */*.md             ← convertiti in PDF (moduli nelle subdirectory)
├── mappe/*.png|svg    ← copiati nella release
└── personaggi/*.png|jpg ← copiati nella release
```

Opzionale: `cover.png` nella root dell'avventura viene copiata nella release.

## Comando

Dalla root del progetto (`~/dungeonandragon`):

```bash
bash tech/scripts/release.sh <NomeAvventura> <versione>
```

Esempio:

```bash
bash tech/scripts/release.sh AvventuraDiProva 1.0
```

## Output

Lo script genera:

```
releases/<NomeAvventura>/<NomeAvventura>_v<versione>_<data>.zip
```

Il ZIP contiene:
```
pdf/          ← tutti i .md convertiti in PDF
mappe/        ← immagini delle mappe
personaggi/   ← artwork dei personaggi
RELEASE.txt   ← nome avventura, versione, data
```

## Troubleshooting

**`WARN: conversione fallita per ...`** — il file MD ha un problema di sintassi o un link non risolvibile. Aprire il file e verificare i link interni.

**`directory non trovata`** — il nome dell'avventura non corrisponde a nessuna directory in `adventures/`. Verificare maiuscole/minuscole (PascalCase).
