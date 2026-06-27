#!/usr/bin/env node
/**
 * carbon-statblock-pdf.js — Genera PDF stat block per Carbon 2185 da un file .md PG/NPC
 * Uso: node tech/fightclub/carbon-statblock-pdf.js <file.md> [-o output.pdf]
 * 
 * Richiede: Playwright
 * Input: file .md nel formato Carbon 2185 (vedi tech/rules/npc-format.md § Variante Carbon 2185)
 * Output: PDF con stat block in stile cyberpunk
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

function parseMd(mdText) {
  const lines = mdText.split('\n');
  const data = { name: '', meta: '', abilities: {}, saves: '', skills: [], augmentations: [], weapons: [], features: [], notes: [], hp: '', ac: '', speed: '', bt: '', influence: '', wonlongs: '' };

  // Nome dal titolo
  const titleMatch = mdText.match(/^# (.+)/m);
  if (titleMatch) {
    data.name = titleMatch[1].replace(/^(PG|NPC|MON)_/, '').split(',')[0].trim();
    data.meta = titleMatch[1].split(',').slice(1).join(',').trim();
  }

  // Campi inline
  const field = (pattern) => { const m = mdText.match(pattern); return m ? m[1].trim() : ''; };
  data.classe = field(/\*\*Classe\*\*:\s*(.+)/);
  data.livello = field(/\*\*Livello\*\*:\s*(.+)/);
  data.origine = field(/\*\*Origine\*\*:\s*(.+)/);
  data.hp = field(/\*\*PF:\*\*\s*(.+)/);
  data.ac = field(/\*\*CA:\*\*\s*(.+)/);
  data.speed = field(/\*\*Velocita:\*\*\s*(.+)/);
  data.saves = field(/\*\*Tiri salvezza:\*\*\s*(.+)/);
  data.bt = field(/\*\*Blood Toxicity:\*\*\s*(.+)/);
  data.influence = field(/\*\*Influence:\*\*\s*(.+)/);
  data.wonlongs = field(/\*\*Wonlongs:\*\*\s*(.+)/);

  // Ability scores dalla tabella
  const abilityRow = mdText.match(/\|\s*(\d+\s*\([^)]+\))\s*\|\s*(\d+\s*\([^)]+\))\s*\|\s*(\d+\s*\([^)]+\))\s*\|\s*(\d+\s*\([^)]+\))\s*\|\s*(\d+\s*\([^)]+\))\s*\|\s*(\d+\s*\([^)]+\))\s*\|/);
  if (abilityRow) {
    data.abilities = { STR: abilityRow[1], DEX: abilityRow[2], CON: abilityRow[3], INT: abilityRow[4], TEC: abilityRow[5], PEO: abilityRow[6] };
  }

  // Competenze (dalla tabella)
  const skillSection = mdText.match(/## Competenze\n([\s\S]*?)(?=\n## )/);
  if (skillSection) {
    const rows = skillSection[1].split('\n').filter(r => r.match(/^\|/) && !r.match(/^\|\s*-/) && !r.match(/^\|\s*Skill/));
    data.skills = rows.map(r => { const cells = r.split('|').map(c => c.trim()).filter(Boolean); return cells.length >= 2 ? `${cells[0]} ${cells[1]}` : ''; }).filter(Boolean);
  }

  // Augmentations
  const augSection = mdText.match(/## Augmentations\n([\s\S]*?)(?=\n## )/);
  if (augSection) {
    const rows = augSection[1].match(/\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|/g) || [];
    data.augmentations = rows.slice(2).map(r => { const m = r.match(/\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|/); return m ? { name: m[1].trim(), slot: m[2].trim(), effect: m[3].trim() } : null; }).filter(Boolean);
  }

  // Armi
  const weapSection = mdText.match(/## Armi\n([\s\S]*?)(?=\n## )/);
  if (weapSection) {
    const rows = weapSection[1].match(/\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|/g) || [];
    data.weapons = rows.slice(2).map(r => { const m = r.match(/\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|/); return m ? { name: m[1].trim(), bonus: m[2].trim(), damage: m[3].trim(), type: m[4].trim(), note: m[5].trim() } : null; }).filter(Boolean);
  }

  // Capacita di classe
  const featSection = mdText.match(/## Capacita di classe\n([\s\S]*?)(?=\n## )/);
  if (featSection) {
    const feats = featSection[1].split(/\n### /).filter(Boolean);
    data.features = feats.map(f => { const lines = f.trim().split('\n'); return { name: lines[0].trim(), desc: lines.slice(1).join(' ').trim() }; });
  }

  // Note
  const noteSection = mdText.match(/## Note\n([\s\S]*?)$/);
  if (noteSection) data.notes = [noteSection[1].trim()];

  return data;
}

function buildHTML(data, imgPath) {
  const imgTag = imgPath && fs.existsSync(imgPath) ?
    `<img class="portrait" src="data:image/png;base64,${fs.readFileSync(imgPath).toString('base64')}">` : '';

  // Background image
  const bgPath = path.join(__dirname, 'carbon-bg.jpg');
  const bgTag = fs.existsSync(bgPath) ? `data:image/jpeg;base64,${fs.readFileSync(bgPath).toString('base64')}` : '';

  return `<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', sans-serif; background: #1f2030; color: #e0e0e8; padding: 20px; width: 210mm; }
.card { border: 1px solid #4a6a7a; border-radius: 8px; padding: 20px; max-width: 700px; position: relative; ${bgTag ? `background: linear-gradient(rgba(25,27,45,0.55), rgba(25,27,45,0.55)), url(${bgTag}) center/cover no-repeat;` : 'background: rgba(30,32,50,0.9);'} }
.card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; border-radius: 8px; background: repeating-linear-gradient(0deg, transparent, transparent 40px, rgba(0,180,200,0.04) 40px, rgba(0,180,200,0.04) 41px); pointer-events: none; }
h1 { color: #00d4e6; font-size: 1.6em; border-bottom: 2px solid #00d4e6; padding-bottom: 5px; margin-bottom: 3px; }
.meta { color: #9ab; font-size: 0.9em; margin-bottom: 10px; }
.portrait { float: left; width: 150px; border-radius: 5px; border: 1px solid #4a6a7a; margin: 0 15px 10px 0; }
.stats-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 5px; margin: 10px 0; text-align: center; clear: both; }
.stat-box { background: rgba(20, 22, 40, 0.8); border: 1px solid #4a6a7a; border-radius: 4px; padding: 5px; }
.stat-box .label { color: #00d4e6; font-size: 0.7em; font-weight: bold; }
.stat-box .value { font-size: 1.1em; font-weight: bold; color: #e0e0e8; }
.section-title { color: #e06080; font-size: 0.85em; font-weight: bold; text-transform: uppercase; border-bottom: 1px solid #3a4a5a; margin-bottom: 5px; }
.row { font-size: 0.85em; margin-bottom: 2px; }
.row b { color: #bcc; }
.weapon { background: rgba(20, 22, 40, 0.6); border-left: 3px solid #e06080; padding: 3px 8px; margin-bottom: 4px; font-size: 0.85em; }
.feat { margin-bottom: 6px; font-size: 0.82em; }
.feat-name { color: #00d4e6; font-weight: bold; }
.aug { font-size: 0.82em; margin-bottom: 2px; }
.note { font-size: 0.78em; color: #9ab; margin-top: 8px; white-space: pre-wrap; }
.note-title { color: #e06080; font-weight: bold; font-size: 0.82em; margin-top: 6px; }
.skill-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3px; margin-top: 5px; break-inside: avoid; page-break-inside: avoid; }
.skill-item { font-size: 0.82em; }
.skill-item .skill-name { color: #9ab; }
.skill-item .skill-val { color: #00d4e6; font-weight: bold; }
.section { margin-top: 10px; break-inside: avoid; page-break-inside: avoid; }
.save-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin-top: 5px; }
.save-item { background: rgba(20, 22, 40, 0.8); border: 1px solid #4a6a7a; border-radius: 4px; padding: 4px 8px; text-align: center; }
.save-item .save-name { font-size: 0.7em; color: #9ab; text-transform: uppercase; }
.save-item .save-val { font-size: 1em; font-weight: bold; color: #00d4e6; }
</style></head><body><div class="card">
${imgTag}
<h1>${data.name}</h1>
<div class="meta">${data.classe} ${data.livello} | ${data.origine}</div>
<div class="stats-grid">
${Object.entries(data.abilities).map(([k,v]) => `<div class="stat-box"><div class="label">${k}</div><div class="value">${v}</div></div>`).join('')}
</div>
<div class="section"><div class="section-title">Combat</div>
<div class="row"><b>CA:</b> ${data.ac}</div>
<div class="row"><b>PF:</b> ${data.hp}</div>
<div class="row"><b>Velocita:</b> ${data.speed}</div>
<div class="row"><b>Blood Toxicity:</b> ${data.bt}</div>
</div>
<div class="section"><div class="section-title">Tiri Salvezza</div>
<div class="save-grid">
${data.saves.split(',').map(s => { const parts = s.trim().split(/\s+/); return `<div class="save-item"><div class="save-name">${parts[0]}</div><div class="save-val">${parts[1]}</div></div>`; }).join('')}
</div></div>
<div class="section"><div class="section-title">Armi</div>
${data.weapons.map(w => `<div class="weapon"><b>${w.name}</b> ${w.bonus} | ${w.damage} ${w.type} ${w.note ? '(' + w.note + ')' : ''}</div>`).join('')}
</div>
<div class="section"><div class="section-title">Augmentations</div>
${data.augmentations.map(a => `<div class="aug"><b>${a.name}</b> [${a.slot}] ${a.effect}</div>`).join('')}
</div>
<div class="section"><div class="section-title">Capacita</div>
${data.features.map(f => `<div class="feat"><span class="feat-name">${f.name}</span> ${f.desc}</div>`).join('')}
</div>
${data.skills.length ? `<div class="section"><div class="section-title">Skills</div><div class="skill-grid">${data.skills.map(s => { const parts = s.match(/(.+?)\s+([+-]?\d+)/); return parts ? `<div class="skill-item"><span class="skill-name">${parts[1]}</span> <span class="skill-val">${parts[2]}</span></div>` : ''; }).join('')}</div></div>` : ''}
${data.notes.length ? `<div class="section"><div class="section-title">Note</div>${data.notes[0].replace(/### (.+)/g, '<div class="note-title">$1</div>').replace(/\n/g, '<br>')}</div>` : ''}
</div></body></html>`;
}

async function main() {
  const args = process.argv.slice(2);
  if (!args.length) { console.error('Uso: node carbon-statblock-pdf.js <file.md> [-o output.pdf] [--image img.png]'); process.exit(1); }

  const mdFile = args[0];
  let outFile = mdFile.replace(/\.md$/, '.pdf');
  let imgFile = null;

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '-o' && args[i+1]) { outFile = args[++i]; }
    if (args[i] === '--image' && args[i+1]) { imgFile = args[++i]; }
  }

  const mdText = fs.readFileSync(mdFile, 'utf-8');
  const data = parseMd(mdText);

  // Auto-detect image
  if (!imgFile) {
    const dir = path.dirname(mdFile);
    const baseName = data.name.replace(/[^a-zA-Z0-9]/g, '');
    const candidates = [`${dir}/../img/${baseName}.png`, `${dir}/../../characters/img/${baseName}.png`];
    for (const c of candidates) { if (fs.existsSync(c)) { imgFile = c; break; } }
  }

  const html = buildHTML(data, imgFile);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.pdf({ path: outFile, width: '210mm', printBackground: true, preferCSSPageSize: false });
  await browser.close();

  const size = fs.statSync(outFile).size;
  console.log(`PDF generato: ${outFile} (${(size/1024).toFixed(0)} KB)`);
}

main().catch(e => { console.error(e); process.exit(1); });
