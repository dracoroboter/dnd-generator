# Biblioteca Analisi Narrative

Questa directory contiene le analisi strutturali di opere narrative famose, scomposte secondo il vocabolario degli stereotipi (`narrative-stereotypes.yaml`) e validate contro la grammatica (`narrative-grammar.yaml`).

Ogni file è un'analisi YAML di un'opera. Servono come "corpus di training" per la grammatica narrativa.

## Stato

| Opera | File | Esito |
|-------|------|-------|
| Star Wars — A New Hope (test minimale) | `star-wars-a-new-hope.yaml` | completa |
| Star Wars — Original Trilogy (campagna 3 archi) | `star-wars-original-trilogy.yaml` | completa |
| Game of Thrones — Stagioni 1-4 (sandbox multi-party) | `game-of-thrones-s1-4.yaml` | completa |
| Harry Potter — Saga Completa (campagna 7 archi) | `harry-potter-saga.yaml` | completa |

| Le Caverne d'Acciaio — Asimov (modulo investigativo) | `caves-of-steel-asimov.yaml` | completa (parziale — focus mystery) |

## Come aggiungere un'analisi

Usare l'agente `@meta-narratore` con il comando `analizza [opera]`.
