#!/usr/bin/env python3
"""
run-check.py — Esegue un comando e ne riporta l'esito in modo INEQUIVOCABILE.

Nasce per eliminare due frizioni ricorrenti quando si lavora da PowerShell -> wsl -> bash:
  1. `echo $?` per leggere l'exit code viene mangiato dall'escape di PowerShell.
  2. l'output di un sotto-comando si mescola a quello del comando principale e
     la coda (tail) mostra la riga sbagliata, facendo sembrare fallito ciò che
     non lo è (o viceversa).

Questo wrapper esegue il comando che gli passi, poi stampa SEMPRE come ULTIMA
riga un verdetto netto:  ESITO: OK (exit 0)  oppure  ESITO: FALLITO (exit N).
Così basta guardare l'ultima riga, senza interpretare output ambiguo.

Uso:
  python3 tech/scripts/run-check.py -- python3 tech/tests/test_regression.py
  python3 tech/scripts/run-check.py --quiet -- python3 tech/scripts/check-adventure.py IlReSpezzato

Opzioni:
  --quiet   non ristampa l'output del comando, mostra solo il verdetto finale
            (e le ultime righe in caso di fallimento).
  --tail N  in caso di fallimento, mostra le ultime N righe dell'output (default 15).
  --        separatore: tutto ciò che segue è il comando da eseguire.
"""
import sys
import subprocess


def main(argv):
    quiet = False
    tail_n = 15
    # parsing minimale prima del separatore --
    if "--" not in argv:
        print("Uso: python3 tech/scripts/run-check.py [--quiet] [--tail N] -- <comando>")
        return 2
    sep = argv.index("--")
    opts = argv[:sep]
    cmd = argv[sep + 1:]
    if not cmd:
        print("Nessun comando dopo '--'.")
        return 2

    i = 0
    while i < len(opts):
        if opts[i] == "--quiet":
            quiet = True
        elif opts[i] == "--tail":
            i += 1
            tail_n = int(opts[i]) if i < len(opts) else 15
        i += 1

    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")

    if not quiet:
        sys.stdout.write(out)
        if out and not out.endswith("\n"):
            sys.stdout.write("\n")
    elif proc.returncode != 0:
        # in caso di errore mostra comunque la coda, utile per capire
        righe = out.splitlines()
        coda = righe[-tail_n:] if len(righe) > tail_n else righe
        print("--- ultime righe output ---")
        for r in coda:
            print(r)
        print("---------------------------")

    print("=" * 40)
    if proc.returncode == 0:
        print("ESITO: OK (exit 0)")
    else:
        print(f"ESITO: FALLITO (exit {proc.returncode})")
    print("=" * 40)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
