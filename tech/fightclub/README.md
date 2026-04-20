# FightClub 5e XML — Formato e Utilizzo

## Cos'è FightClub 5e

**Fight Club 5e** e **Game Master 5e** sono app iOS/Android di Lion's Den per gestire personaggi e sessioni D&D 5e. Sono tra le app più usate dai DM per consultare stat block di mostri e NPC durante il gioco.

Le app supportano l'import di contenuti homebrew tramite file **XML** con un formato specifico. Questo permette di avere i propri NPC custom disponibili nell'app con la stessa interfaccia dei mostri ufficiali.

## A cosa serve nel progetto

Convertire le schede NPC markdown del progetto (`characters/NPC_*.md`) in file XML importabili in FightClub/Game Master 5e. Così il DM ha gli NPC homebrew disponibili sull'iPad/telefono durante la sessione, senza dover consultare i file markdown.

## Come si usa un file XML in FightClub

1. Genera il file XML (manualmente o con lo script `npc-to-fightclub.py` — da creare)
2. Trasferisci il file `.xml` sul dispositivo (AirDrop, email, cloud, cavo)
3. In FightClub 5e: **Settings → Import → seleziona il file XML**
4. I mostri/NPC appaiono nella sezione Compendium dell'app

---

## Il formato XML

### Struttura base

Ogni file XML è un "compendium" che contiene uno o più mostri:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<compendium version="5" auto_indent="NO">
    <monster>
        <!-- dati del mostro -->
    </monster>
    <!-- altri mostri opzionali -->
</compendium>
```

### Tag di un `<monster>`

| tag | obbligatorio | contenuto | esempio |
|-----|-------------|-----------|---------|
| `<name>` | sì | nome | `Korex` |
| `<size>` | sì | T/S/M/L/H/G | `M` |
| `<type>` | sì | tipo (sottotipo) | `humanoid (elf)` |
| `<alignment>` | sì | allineamento in inglese | `chaotic evil` |
| `<ac>` | sì | CA, opzionalmente con fonte | `13 (leather armor)` |
| `<hp>` | sì | PF totali (formula opzionale) | `52 (8d8+16)` |
| `<speed>` | sì | velocità in ft | `40 ft.` |
| `<str>` `<dex>` `<con>` `<int>` `<wis>` `<cha>` | sì | punteggio (solo numero) | `16` |
| `<save>` | no | tiri salvezza | `Dex +5, Cha +4` |
| `<skill>` | no | abilità | `Stealth +5, Perception +3` |
| `<vulnerable>` | no | vulnerabilità danni | `fire` |
| `<resist>` | no | resistenze danni | `bludgeoning` |
| `<immune>` | no | immunità danni | `poison` |
| `<conditionImmune>` | no | immunità condizioni | `poisoned` |
| `<senses>` | no | sensi | `darkvision 60 ft., passive Perception 13` |
| `<languages>` | no | lingue | `Common, Elvish` |
| `<cr>` | sì | challenge rating | `3` |
| `<description>` | no | testo descrittivo per il DM | testo libero |
| `<environment>` | no | ambienti tipici | `underdark, urban` |

### Tratti, azioni, reazioni

Capacità passive, azioni e reazioni usano tag dedicati, ciascuno con `<name>` e `<text>`:

```xml
<trait>
    <name>Cunning Action</name>
    <text>Korex can Dash or Disengage as a bonus action.</text>
</trait>

<action>
    <name>Rancid Knife</name>
    <text>Melee Weapon Attack: +5 to hit, reach 5 ft., one target.
    Hit: 7 (2d4+3) piercing damage plus 7 (2d6) poison damage.
    The target is poisoned until the start of Korex's next turn.</text>
    <attack>Rancid Knife|+5|2d4+3</attack>
</action>

<reaction>
    <name>Nome Reazione</name>
    <text>Descrizione della reazione.</text>
</reaction>

<legendary>
    <name>Nome Azione Leggendaria</name>
    <text>Descrizione.</text>
</legendary>
```

### Tag `<attack>` (opzionale, dentro `<action>`)

Permette a FightClub di calcolare automaticamente i tiri. Formato:

```
Nome|+bonus_attacco|formula_danni
```

Esempio: `Rancid Knife|+5|2d4+3`

Se l'attacco ha danni aggiuntivi (es. veleno), descriverli nel `<text>` — il tag `<attack>` gestisce solo il danno primario.

---

## Esempio completo: Korex

```xml
<?xml version="1.0" encoding="UTF-8"?>
<compendium version="5" auto_indent="NO">
    <monster>
        <name>Korex</name>
        <size>M</size>
        <type>humanoid (elf)</type>
        <alignment>chaotic evil</alignment>
        <ac>13</ac>
        <hp>52</hp>
        <speed>40 ft.</speed>
        <str>13</str>
        <dex>16</dex>
        <con>14</con>
        <int>8</int>
        <wis>12</wis>
        <cha>15</cha>
        <skill>Perception +3, Performance +4, Stealth +5</skill>
        <immune>poison</immune>
        <conditionImmune>poisoned</conditionImmune>
        <senses>darkvision 60 ft., passive Perception 13</senses>
        <languages>Common, Elvish</languages>
        <cr>3</cr>
        <trait>
            <name>Cunning Action</name>
            <text>Korex can Dash or Disengage as a bonus action.</text>
        </trait>
        <action>
            <name>Rancid Knife</name>
            <text>Melee Weapon Attack: +5 to hit, reach 5 ft., one target. Hit: 7 (2d4+3) piercing damage plus 7 (2d6) poison damage. The target is poisoned until the start of Korex's next turn.</text>
            <attack>Rancid Knife|+5|2d4+3</attack>
        </action>
        <action>
            <name>Magic Flute</name>
            <text>Korex plays his magic flute, targeting one creature he can see within 120 ft. The target must make a DC 12 Wisdom saving throw. On a failure, the target takes 14 (4d6) psychic damage and is charmed until the start of Korex's next turn. On a success, the target takes half damage and is not charmed.</text>
        </action>
        <description>Elf bard, chaotic evil. Charmer and manipulator who fights from distance, charms enemies, and sends minions forward. Flees when cornered.</description>
    </monster>
</compendium>
```

---

## Validazione

Lo schema XSD per validare i file è in `tech/data/compendium/compendium.xsd`.

```bash
xmllint --noout --schema tech/data/compendium/compendium.xsd mio_file.xml
```

I file XML di esempio dei mostri ufficiali sono in `tech/data/compendium/Sources/`.

---

## Fonti

| fonte | tipo | URL |
|-------|------|-----|
| kinkofer/FightClub5eXML | Repo GitHub (733 ⭐, MIT) — file XML di tutte le fonti ufficiali D&D 5e | [github.com/kinkofer/FightClub5eXML](https://github.com/kinkofer/FightClub5eXML) |
| Sources/README.md | Documentazione del formato XML e del sistema di merge | [Sources/README.md](https://github.com/kinkofer/FightClub5eXML/blob/main/Sources/README.md) |
| Utilities/compendium.xsd | Schema XSD per validazione XML | nel repo kinkofer |
| Moonlington/5eTtoFC5 | Tool conversione 5eTools → FightClub XML | [github.com/Moonlington/5eTtoFC5](https://github.com/Moonlington/5eTtoFC5) |
| matteraByte/5eDataParser | Parser/converter XML, JSON, markdown per stat block 5e | [github.com/matteraByte/5eDataParser](https://github.com/matteraByte/5eDataParser) |
| vidalvanbergen/CompendiumEditor | Editor GUI per creare/modificare XML FightClub | [github.com/vidalvanbergen/CompendiumEditor](https://github.com/vidalvanbergen/CompendiumEditor) |

La struttura dei tag è stata ricavata dallo schema XSD e dai file XML di esempio nel repo kinkofer (directory `Sources/`). L'esempio di Korex è stato scritto a mano seguendo il formato dei mostri ufficiali presenti nel repo.

---

## TODO

- [ ] Creare `tech/fightclub/npc-to-fightclub.py` — converte `NPC_*.md` → XML FightClub
- [ ] Testare validazione con `xmllint` + `tech/data/compendium/compendium.xsd`
- [ ] Testare import in FightClub 5e su dispositivo reale

### Miglioramenti PDF/PNG stat block

- [ ] Parametro `--width N` per controllare la grandezza della scheda (default 400px)
- [ ] Parametro `--layout portrait|landscape` + più schede per pagina (affiancate orizzontalmente o verticalmente)
- [ ] Parametro `--image <file.png>` per aggiungere un'immagine/ritratto nella scheda
- [ ] Parametro `--brief` per versione compatta: solo stats, attacchi e tratti — senza descrizione, motivazioni, note
