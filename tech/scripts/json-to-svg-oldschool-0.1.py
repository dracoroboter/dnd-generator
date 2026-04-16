#!/usr/bin/env python3
"""
json-to-svg-oldschool.py v0.2 — Renderer SVG stile old-school D&D (B&W, hatching random).

COMPATIBILITÀ: generate-dungeon.py cell-grid-0.3+
USO: python3 tech/scripts/json-to-svg-oldschool.py <input.json> [--tile-size N] [--seed N] [--output FILE]
"""

import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
from dungeon_svg_core import (
    load_data, rebuild_grid, get_grid_size, get_doors,
    bounding_box, is_exterior_wall, write_svg,
    EXTERIOR, WALL, FLOOR, CORR
)

TILE = 20



def hatch_lines(cx, cy, tile, rng, density=18, ext=False):
    lines = []
    pad = 1
    for _ in range(density):
        x1 = cx + pad + rng.random() * (tile - pad*2)
        y1 = cy + pad + rng.random() * (tile - pad*2)
        angle = math.radians(40 + rng.random() * 20)
        length = tile * 0.25 + rng.random() * tile * 0.35
        x2 = max(cx+pad, min(cx+tile-pad, x1 + math.cos(angle)*length))
        y2 = max(cy+pad, min(cy+tile-pad, y1 + math.sin(angle)*length))
        sw = 0.6 if ext else 0.5
        op = 0.5 if ext else 0.85
        lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="black" stroke-width="{sw}" opacity="{op}"/>')
    return lines


def render(data, tile, output_path, seed):
    rooms = data['rooms']
    title = data.get('title', 'Dungeon')
    year  = (data.get('generated') or '')[:4] or '2026'
    gw, gh = get_grid_size(data)
    rng   = random.Random(seed)
    grid  = rebuild_grid(rooms, gw, gh)
    doors = get_doors(data)
    bb    = bounding_box(grid, gw, gh)
    if not bb:
        return
    x0, y0, x1, y1 = bb
    W, H, header_h = (x1-x0)*tile, (y1-y0)*tile, 48
    sw = max(1.5, tile * 0.12)  # spessore bordi

    L = []
    L.append('<?xml version="1.0" encoding="UTF-8"?>')
    L.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H+header_h}" viewBox="0 0 {W} {H+header_h}">')
    L.append(f'<rect width="{W}" height="{H+header_h}" fill="white"/>')
    L.append(f'<text x="{W//2}" y="28" text-anchor="middle" font-family="Georgia,serif" font-size="20" font-weight="bold" fill="black">{title}</text>')
    L.append(f'<text x="{W//2}" y="42" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#555">© {year} Dracosoft — CC BY</text>')
    L.append(f'<g transform="translate(0,{header_h})">')

    # Pavimento (griglia sottile)
    for y in range(y0, y1):
        for x in range(x0, x1):
            if grid[y][x] in (FLOOR, CORR):
                px, py = (x-x0)*tile, (y-y0)*tile
                L.append(f'<rect x="{px}" y="{py}" width="{tile}" height="{tile}" fill="white" stroke="#ccc" stroke-width="0.4"/>')

    # Hatching muri
    for y in range(y0, y1):
        for x in range(x0, x1):
            if grid[y][x] == WALL and (x, y) not in doors:
                px, py = (x-x0)*tile, (y-y0)*tile
                ext = is_exterior_wall(grid, x, y, gh, gw)
                L.extend(hatch_lines(px, py, tile, rng, density=14 if ext else 20, ext=ext))

    # Bordi neri tra pavimento e muro
    for y in range(y0, y1):
        for x in range(x0, x1):
            if grid[y][x] not in (FLOOR, CORR):
                continue
            px, py = (x-x0)*tile, (y-y0)*tile
            if y > 0    and grid[y-1][x] == WALL and (x, y-1) not in doors:
                L.append(f'<line x1="{px}" y1="{py}" x2="{px+tile}" y2="{py}" stroke="black" stroke-width="{sw}"/>')
            if y < gh-1 and grid[y+1][x] == WALL and (x, y+1) not in doors:
                L.append(f'<line x1="{px}" y1="{py+tile}" x2="{px+tile}" y2="{py+tile}" stroke="black" stroke-width="{sw}"/>')
            if x > 0    and grid[y][x-1] == WALL and (x-1, y) not in doors:
                L.append(f'<line x1="{px}" y1="{py}" x2="{px}" y2="{py+tile}" stroke="black" stroke-width="{sw}"/>')
            if x < gw-1 and grid[y][x+1] == WALL and (x+1, y) not in doors:
                L.append(f'<line x1="{px+tile}" y1="{py}" x2="{px+tile}" y2="{py+tile}" stroke="black" stroke-width="{sw}"/>')

    # Porte: varco nel muro con stipiti a rientranza
    # Le celle porta vengono raggruppate per connessione (celle consecutive stesso orient)
    # Per ogni gruppo: pavimento bianco + due stipiti perpendicolari agli estremi
    stipite_depth = max(2, tile // 3)  # quanto rientra lo stipite verso l'interno

    # Raggruppa celle porta consecutive (stesso orient, adiacenti)
    door_cells = sorted(doors.items())
    used = set()
    door_groups = []
    for (dx, dy), orient in door_cells:
        if (dx, dy) in used:
            continue
        group = [(dx, dy)]
        used.add((dx, dy))
        # Cerca celle adiacenti stesso orient
        if orient == 'h':
            nx, ny = dx, dy+1
        else:
            nx, ny = dx+1, dy
        while (nx, ny) in doors and doors[(nx, ny)] == orient and (nx, ny) not in used:
            group.append((nx, ny))
            used.add((nx, ny))
            if orient == 'h':
                ny += 1
            else:
                nx += 1
        door_groups.append((group, orient))

    for group, orient in door_groups:
        # Disegna pavimento su tutte le celle del gruppo
        for (dx, dy) in group:
            if not (x0 <= dx < x1 and y0 <= dy < y1): continue
            px, py = (dx-x0)*tile, (dy-y0)*tile
            L.append(f'<rect x="{px}" y="{py}" width="{tile}" height="{tile}" fill="white"/>')
            L.append(f'<rect x="{px}" y="{py}" width="{tile}" height="{tile}" fill="white" stroke="#ccc" stroke-width="0.4"/>')

        # Coordinate bounding box del gruppo
        gxs = [dx for dx, dy in group]
        gys = [dy for dx, dy in group]
        gx0, gy0 = min(gxs), min(gys)
        gx1, gy1 = max(gxs), max(gys)
        px0 = (gx0-x0)*tile
        py0 = (gy0-y0)*tile
        px1 = (gx1-x0)*tile + tile
        py1 = (gy1-y0)*tile + tile

        if orient == 'h':
            # Solo i 4 denti agli angoli (orizzontali, rientrano verso l'interno)
            L.append(f'<line x1="{px0}" y1="{py0}" x2="{px0+stipite_depth}" y2="{py0}" stroke="black" stroke-width="{sw}"/>')
            L.append(f'<line x1="{px0}" y1="{py1}" x2="{px0+stipite_depth}" y2="{py1}" stroke="black" stroke-width="{sw}"/>')
            L.append(f'<line x1="{px1}" y1="{py0}" x2="{px1-stipite_depth}" y2="{py0}" stroke="black" stroke-width="{sw}"/>')
            L.append(f'<line x1="{px1}" y1="{py1}" x2="{px1-stipite_depth}" y2="{py1}" stroke="black" stroke-width="{sw}"/>')
        else:
            # Solo i 4 denti agli angoli (verticali, rientrano verso l'interno)
            L.append(f'<line x1="{px0}" y1="{py0}" x2="{px0}" y2="{py0+stipite_depth}" stroke="black" stroke-width="{sw}"/>')
            L.append(f'<line x1="{px1}" y1="{py0}" x2="{px1}" y2="{py0+stipite_depth}" stroke="black" stroke-width="{sw}"/>')
            L.append(f'<line x1="{px0}" y1="{py1}" x2="{px0}" y2="{py1-stipite_depth}" stroke="black" stroke-width="{sw}"/>')
            L.append(f'<line x1="{px1}" y1="{py1}" x2="{px1}" y2="{py1-stipite_depth}" stroke="black" stroke-width="{sw}"/>')

    # Etichette
    fs = max(7, tile-5)
    for room in rooms:
        rx2, ry2, rw, rh = room['x'], room['y'], room['w'], room['h']
        cx = (rx2+rw/2-x0)*tile
        cy = (ry2+rh/2-y0)*tile
        L.append(f'<text x="{cx:.1f}" y="{cy+fs*0.35:.1f}" text-anchor="middle" font-family="sans-serif" font-size="{fs}" fill="#333">{room["id"]}</text>')

    L.append('</g>')
    L.append('</svg>')
    write_svg(output_path, L)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('input')
    p.add_argument('--tile-size', type=int, default=TILE, dest='tile_size')
    p.add_argument('--seed',      type=int, default=0)
    p.add_argument('--output',    default=None)
    args = p.parse_args()
    data = load_data(args.input)
    output = args.output or os.path.splitext(args.input)[0] + '_oldschool.svg'
    render(data, args.tile_size, output, args.seed or data.get('seed', 42))
    print(f'✓ {output}')


if __name__ == '__main__':
    main()
