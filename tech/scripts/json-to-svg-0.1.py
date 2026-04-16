#!/usr/bin/env python3
"""
json-to-svg.py v0.1 — Converte il JSON strutturale del dungeon in SVG grafico.

COMPATIBILITÀ
  Richiede JSON generato da generate-dungeon.py (cell-grid-0.3+).
  Campi JSON utilizzati:
    - rooms[].{id, x, y, w, h, type}   — vani (stanze e corridoi)
    - doors[].{x, y, orient}            — posizioni porte (da cell-grid-0.3+)
    - title, generated                  — metadati
    - grid_size                         — dimensione griglia (es. "60x60")
  Se 'doors' non è presente nel JSON, le porte vengono calcolate dalla griglia
  ricostruita (fallback, meno preciso).

USO
  python3 tech/scripts/json-to-svg.py <input.json> [opzioni]

  Opzioni:
    --tile-size N     Pixel per quadretto (default: 20)
    --tileset DIR     Directory con floor.png, wall.png, floor_stone.png
                      (default: tech/assets/tilesets/dcss)
    --output FILE     File SVG di output (default: <input>.svg)

TILESET
  Il tileset deve contenere:
    floor.png       — pavimento stanze
    wall.png        — muri
    floor_stone.png — pavimento corridoi (opzionale, fallback su floor.png)
  Tileset consigliati:
    - DCSS (incluso): tech/assets/tilesets/dcss/
    - Kenney Dungeon Tileset (CC0): kenney.nl/assets/dungeon-tileset
    - OpenGameArt: opengameart.org (cerca "dungeon tileset")

OUTPUT
  File SVG con:
    - Header scuro con titolo e copyright
    - Muri con texture tileset (esterni più scuri degli interni)
    - Pavimento stanze e corridoi con texture tileset
    - Porte come rettangoli marroni con bordo dorato
    - Etichette vani (S1, C1, ecc.) con badge
  Apribile nel browser o editabile in Inkscape.
"""

import argparse
import json
import os
import base64

EXTERIOR = 3
WALL     = 0
FLOOR    = 1
CORR     = 2

TILE = 20


def rebuild_grid(rooms_data, gw, gh):
    grid = [[EXTERIOR] * gw for _ in range(gh)]
    for room in rooms_data:
        rx, ry, rw, rh = room['x'], room['y'], room['w'], room['h']
        cell_val = CORR if room['type'] == 'corridor' else FLOOR
        for y in range(ry-1, ry+rh+1):
            for x in range(rx-1, rx+rw+1):
                if 0 <= y < gh and 0 <= x < gw and grid[y][x] == EXTERIOR:
                    grid[y][x] = WALL
        for y in range(ry, ry+rh):
            for x in range(rx, rx+rw):
                if 0 <= y < gh and 0 <= x < gw:
                    grid[y][x] = cell_val
    return grid


def find_doors(grid, gh, gw):
    """
    Celle WALL tra due vani percorribili su lati opposti = porta.
    Restituisce set di (x, y) con orientamento ('h' o 'v').
    """
    doors = {}
    for y in range(1, gh-1):
        for x in range(1, gw-1):
            if grid[y][x] != WALL:
                continue
            # Porta orizzontale: FLOOR/CORR a sinistra e destra
            l, r = grid[y][x-1], grid[y][x+1]
            if l in (FLOOR, CORR) and r in (FLOOR, CORR):
                doors[(x, y)] = 'h'
                continue
            # Porta verticale: FLOOR/CORR sopra e sotto
            u, d = grid[y-1][x], grid[y+1][x]
            if u in (FLOOR, CORR) and d in (FLOOR, CORR):
                doors[(x, y)] = 'v'
    return doors


def png_to_b64(path):
    try:
        with open(path, 'rb') as f:
            return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
    except Exception:
        return None


def generate_svg(data, tile, tileset_dir, output_path):
    rooms = data['rooms']
    title = data.get('title', 'Dungeon')
    year  = (data.get('generated') or '')[:4] or '2026'

    gw = gh = 60
    if rooms:
        gw = max(gw, max(r['x'] + r['w'] + 2 for r in rooms))
        gh = max(gh, max(r['y'] + r['h'] + 2 for r in rooms))

    grid = rebuild_grid(rooms, gw, gh)
    # Porte dal JSON (posizioni esatte dalla griglia originale)
    doors = {(d['x'], d['y']): d['orient'] for d in data.get('doors', [])}
    # Fallback: calcola dalla griglia ricostruita se non presenti nel JSON
    if not doors:
        doors = find_doors(grid, gh, gw)

    xs = [x for y in range(gh) for x in range(gw) if grid[y][x] != EXTERIOR]
    ys = [y for y in range(gh) for x in range(gw) if grid[y][x] != EXTERIOR]
    if not xs:
        print("Nessun vano trovato.")
        return

    margin = 3
    x0, y0 = max(0, min(xs)-margin), max(0, min(ys)-margin)
    x1, y1 = min(gw, max(xs)+margin+1), min(gh, max(ys)+margin+1)
    W = (x1-x0)*tile
    H = (y1-y0)*tile
    header_h = 56

    floor_b64 = png_to_b64(os.path.join(tileset_dir, 'floor.png'))
    wall_b64  = png_to_b64(os.path.join(tileset_dir, 'wall.png'))
    corr_b64  = png_to_b64(os.path.join(tileset_dir, 'floor_stone.png')) or floor_b64

    L = []
    L.append('<?xml version="1.0" encoding="UTF-8"?>')
    L.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H+header_h}" viewBox="0 0 {W} {H+header_h}">')
    L.append('<defs>')

    if floor_b64:
        L.append(f'<pattern id="p_floor" patternUnits="userSpaceOnUse" width="{tile}" height="{tile}"><image href="{floor_b64}" width="{tile}" height="{tile}"/></pattern>')
    if wall_b64:
        L.append(f'<pattern id="p_wall_int" patternUnits="userSpaceOnUse" width="{tile}" height="{tile}"><image href="{wall_b64}" width="{tile}" height="{tile}"/></pattern>')
        L.append(f'<pattern id="p_wall_ext" patternUnits="userSpaceOnUse" width="{tile}" height="{tile}"><image href="{wall_b64}" width="{tile}" height="{tile}"/><rect width="{tile}" height="{tile}" fill="rgba(0,0,0,0.45)"/></pattern>')
    if corr_b64:
        L.append(f'<pattern id="p_corr" patternUnits="userSpaceOnUse" width="{tile}" height="{tile}"><image href="{corr_b64}" width="{tile}" height="{tile}"/></pattern>')

    L.append(f'<pattern id="hatch_int" patternUnits="userSpaceOnUse" width="6" height="6"><rect width="6" height="6" fill="#787068"/><line x1="0" y1="6" x2="6" y2="0" stroke="#5a5248" stroke-width="1"/></pattern>')
    L.append(f'<pattern id="hatch_ext" patternUnits="userSpaceOnUse" width="6" height="6"><rect width="6" height="6" fill="#1e1e1e"/><line x1="0" y1="6" x2="6" y2="0" stroke="#0a0a0a" stroke-width="1.5"/></pattern>')
    L.append(f'<pattern id="grid_floor" patternUnits="userSpaceOnUse" width="{tile}" height="{tile}"><rect width="{tile}" height="{tile}" fill="#f0e6b4"/><rect width="{tile}" height="{tile}" fill="none" stroke="#c8b87a" stroke-width="0.5"/></pattern>')
    L.append(f'<pattern id="grid_corr" patternUnits="userSpaceOnUse" width="{tile}" height="{tile}"><rect width="{tile}" height="{tile}" fill="#dcb478"/><rect width="{tile}" height="{tile}" fill="none" stroke="#b8904a" stroke-width="0.5"/></pattern>')
    L.append('</defs>')

    L.append(f'<rect width="{W}" height="{H+header_h}" fill="white"/>')
    L.append(f'<rect width="{W}" height="{header_h}" fill="#1a1008"/>')
    L.append(f'<text x="{W//2}" y="32" text-anchor="middle" font-family="Georgia,serif" font-size="24" font-weight="bold" fill="#f0d890" letter-spacing="2">{title}</text>')
    L.append(f'<text x="{W//2}" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#a09070">© {year} Dracosoft — CC BY</text>')
    L.append(f'<g transform="translate(0,{header_h})">')

    # Ombre muri esterni
    for y in range(y0, y1):
        for x in range(x0, x1):
            if grid[y][x] == WALL and (x,y) not in doors:
                is_ext = any(0 <= y+dy < gh and 0 <= x+dx < gw and grid[y+dy][x+dx] == EXTERIOR for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)])
                if is_ext:
                    px, py = (x-x0)*tile, (y-y0)*tile
                    L.append(f'<rect x="{px+2}" y="{py+2}" width="{tile}" height="{tile}" fill="rgba(0,0,0,0.2)"/>')

    # Celle
    for y in range(y0, y1):
        for x in range(x0, x1):
            px, py = (x-x0)*tile, (y-y0)*tile
            v = grid[y][x]
            if v == EXTERIOR:
                continue
            elif v == WALL:
                if (x, y) in doors:
                    continue  # le porte vengono disegnate dopo
                is_ext = any(0 <= y+dy < gh and 0 <= x+dx < gw and grid[y+dy][x+dx] == EXTERIOR for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)])
                fill = ('url(#p_wall_ext)' if is_ext else 'url(#p_wall_int)') if wall_b64 else ('url(#hatch_ext)' if is_ext else 'url(#hatch_int)')
            elif v == FLOOR:
                fill = 'url(#p_floor)' if floor_b64 else 'url(#grid_floor)'
            else:
                fill = 'url(#p_corr)' if corr_b64 else 'url(#grid_corr)'
            L.append(f'<rect x="{px}" y="{py}" width="{tile}" height="{tile}" fill="{fill}"/>')

    # Porte
    dw = max(2, tile//5)
    dl = max(6, tile*3//4)
    for (dx, dy), orient in doors.items():
        if not (x0 <= dx < x1 and y0 <= dy < y1):
            continue
        px, py = (dx-x0)*tile, (dy-y0)*tile
        # Sfondo pavimento sotto la porta
        adj_fill = 'url(#p_floor)' if floor_b64 else 'url(#grid_floor)'
        L.append(f'<rect x="{px}" y="{py}" width="{tile}" height="{tile}" fill="{adj_fill}"/>')
        # Porta
        cx, cy = px + tile//2, py + tile//2
        if orient == 'h':
            L.append(f'<rect x="{cx-dw}" y="{cy-dl//2}" width="{dw*2}" height="{dl}" fill="#3d1f08" stroke="#c8a060" stroke-width="1" rx="1"/>')
        else:
            L.append(f'<rect x="{cx-dl//2}" y="{cy-dw}" width="{dl}" height="{dw*2}" fill="#3d1f08" stroke="#c8a060" stroke-width="1" rx="1"/>')

    # Etichette
    fs = max(8, tile-4)
    for room in rooms:
        rx2, ry2, rw, rh = room['x'], room['y'], room['w'], room['h']
        if not (x0 <= rx2 < x1 and y0 <= ry2 < y1):
            continue
        cx = (rx2 + rw/2 - x0)*tile
        cy = (ry2 + rh/2 - y0)*tile
        label = room['id']
        is_corr = room['type'] == 'corridor'
        bf = 'rgba(220,180,120,0.85)' if is_corr else 'rgba(240,230,180,0.85)'
        bw = len(label)*fs*0.7
        L.append(f'<rect x="{cx-bw/2:.1f}" y="{cy-fs*0.75:.1f}" width="{bw:.1f}" height="{fs*1.1:.1f}" fill="{bf}" rx="3" stroke="#8a7040" stroke-width="0.5"/>')
        L.append(f'<text x="{cx:.1f}" y="{cy+fs*0.3:.1f}" text-anchor="middle" font-family="sans-serif" font-size="{fs}" font-weight="bold" fill="#1a1008">{label}</text>')

    L.append('</g>')
    L.append('</svg>')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('input')
    p.add_argument('--tile-size', type=int, default=TILE, dest='tile_size')
    p.add_argument('--tileset',   default='tech/assets/tilesets/dcss')
    p.add_argument('--output',    default=None)
    args = p.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    output = args.output or os.path.splitext(args.input)[0] + '.svg'
    generate_svg(data, args.tile_size, args.tileset, output)
    print(f'✓ {output}')


if __name__ == '__main__':
    main()
