#!/usr/bin/env node
/**
 * md-to-statblock-pdf.js — Genera PDF stat block in stile WotC da un file XML FightClub
 * Uso: node tech/fightclub/md-to-statblock-pdf.js <file.xml> [-o output.pdf] [--image foto.png]
 * 
 * Richiede: Playwright (già installato nel progetto per le mappe Watabou)
 * Input: file XML FightClub (generato da md-to-fightclub.py)
 * Output: PDF con stat block nella grafica D&D 5e
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

function parseXML(xmlText) {
    // Parser XML minimale — estrae i tag di un <monster>
    const get = (tag) => {
        const m = xmlText.match(new RegExp(`<${tag}>(.*?)</${tag}>`, 's'));
        return m ? m[1].trim() : '';
    };
    const getAll = (parentTag, childTags) => {
        const results = [];
        const regex = new RegExp(`<${parentTag}>(.*?)</${parentTag}>`, 'gs');
        let match;
        while ((match = regex.exec(xmlText)) !== null) {
            const block = match[1];
            const item = {};
            for (const tag of childTags) {
                const m2 = block.match(new RegExp(`<${tag}>(.*?)</${tag}>`, 's'));
                item[tag] = m2 ? m2[1].trim() : '';
            }
            results.push(item);
        }
        return results;
    };

    return {
        name: get('name'),
        size: get('size'),
        type: get('type'),
        alignment: get('alignment'),
        ac: get('ac'),
        hp: get('hp'),
        speed: get('speed'),
        str: get('str'), dex: get('dex'), con: get('con'),
        int: get('int'), wis: get('wis'), cha: get('cha'),
        save: get('save'),
        skill: get('skill'),
        vulnerable: get('vulnerable'),
        resist: get('resist'),
        immune: get('immune'),
        conditionImmune: get('conditionImmune'),
        senses: get('senses'),
        languages: get('languages'),
        cr: get('cr'),
        traits: getAll('trait', ['name', 'text']),
        actions: getAll('action', ['name', 'text']),
        reactions: getAll('reaction', ['name', 'text']),
        legendaries: getAll('legendary', ['name', 'text']),
        description: get('description'),
    };
}

const SIZE_MAP = { T: 'Tiny', S: 'Small', M: 'Medium', L: 'Large', H: 'Huge', G: 'Gargantuan' };

function buildHTML(monster, imagePath) {
    const sizeName = SIZE_MAP[monster.size] || monster.size;
    let subtitle;
    if (monster.type) {
        // Monster format
        subtitle = `${sizeName} ${monster.type}, ${monster.alignment}`;
    } else {
        // PC format: parse "Race Class Level" or "Race (Subrace) Class Level" from original name
        // monster.name has been overridden with label, so we need the original
        const origName = monster._origName || '';
        const pcMatch = origName.match(/^(.+?)\s+(\w+)\s+(\d+)$/);
        if (pcMatch) {
            subtitle = `${sizeName} ${pcMatch[1]}, ${pcMatch[2]} level ${pcMatch[3]}`;
        } else if (origName) {
            subtitle = `${sizeName} ${origName}`;
        } else {
            subtitle = sizeName;
        }
    }

    // Immagine opzionale — convertita in base64 per essere self-contained
    let imageTag = '';
    if (imagePath && fs.existsSync(imagePath)) {
        const ext = path.extname(imagePath).slice(1).toLowerCase();
        const mime = ext === 'jpg' ? 'jpeg' : ext;
        const data = fs.readFileSync(imagePath).toString('base64');
        imageTag = `<div style="text-align:center;margin-bottom:8px;"><img src="data:image/${mime};base64,${data}" style="max-width:100%;max-height:200px;border-radius:4px;"/></div>`;
    }

    let properties = '';
    const addProp = (label, value) => {
        if (value) properties += `      <property-line>
        <h4>${label}</h4>
        <p>${value}</p>
      </property-line>\n`;
    };

    addProp('Armor Class', monster.ac);
    addProp('Hit Points', monster.hp);
    addProp('Speed', monster.speed);

    // Optional properties
    if (monster.save) addProp('Saving Throws', monster.save);
    if (monster.skill) addProp('Skills', monster.skill);
    if (monster.vulnerable) addProp('Damage Vulnerabilities', monster.vulnerable);
    if (monster.resist) addProp('Damage Resistances', monster.resist);
    if (monster.immune) addProp('Damage Immunities', monster.immune);
    if (monster.conditionImmune) addProp('Condition Immunities', monster.conditionImmune);
    if (monster.senses) addProp('Senses', monster.senses);
    if (monster.languages) addProp('Languages', monster.languages);
    addProp('Challenge', monster.cr);

    let blocks = '';
    const addBlock = (items, heading) => {
        if (items.length === 0) return;
        if (heading) blocks += `<h3>${heading}</h3>\n`;
        for (const item of items) {
            blocks += `<property-block><h4>${item.name}.&nbsp;</h4><p>${item.text}</p></property-block>\n`;
        }
    };

    addBlock(monster.traits, '');
    addBlock(monster.actions, 'Actions');
    addBlock(monster.reactions, 'Reactions');
    addBlock(monster.legendaries, 'Legendary Actions');

    // Leggi il template e inietta il contenuto
    const templatePath = path.join(__dirname, 'statblock5e-template.html');
    let html = fs.readFileSync(templatePath, 'utf-8');

    // Sostituisci i Google Fonts con fallback locali per funzionare offline
    html = html.replace(/<link href="\/\/fonts\.googleapis\.com[^"]*"[^>]*>/g, '');

    // Rimuovi il contenuto demo e inietta il nostro
    const statblockContent = `
<stat-block>
  <creature-heading>
    <h1>${monster.name}</h1>
    <h2>${subtitle}</h2>
  </creature-heading>

  ${imageTag}

  <top-stats>
    ${properties}
    <abilities-block data-str="${monster.str}"
                     data-dex="${monster.dex}"
                     data-con="${monster.con}"
                     data-int="${monster.int}"
                     data-wis="${monster.wis}"
                     data-cha="${monster.cha}"></abilities-block>
  </top-stats>

  ${blocks}
</stat-block>`;

    // Sostituisci il contenuto tra <body> ... </body> mantenendo i <template> e <script>
    // Trova l'ultimo </script> prima del <stat-block> demo
    const lastScriptEnd = html.lastIndexOf('</script>');
    const bodyEnd = html.indexOf('</body>');
    
    if (lastScriptEnd > 0 && bodyEnd > 0) {
        // Trova il <stat-block> demo
        const demoStart = html.indexOf('<stat-block>', lastScriptEnd);
        if (demoStart > 0) {
            html = html.substring(0, demoStart) + statblockContent + '\n' + html.substring(bodyEnd);
        }
    }

    return html;
}

async function generatePDF(htmlContent, outputPath) {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    // Carica l'HTML
    await page.setContent(htmlContent, { waitUntil: 'networkidle' });
    
    // Aspetta che i Web Components si renderizzino
    await page.waitForTimeout(1000);

    if (outputPath.endsWith('.png')) {
        // Screenshot per PNG
        const statblock = await page.$('stat-block');
        if (statblock) {
            await statblock.screenshot({ path: outputPath });
        } else {
            await page.screenshot({ path: outputPath, fullPage: true });
        }
    } else {
        // PDF
        await page.pdf({
            path: outputPath,
            width: '450px',
            printBackground: true,
            margin: { top: '10px', bottom: '10px', left: '10px', right: '10px' }
        });
    }

    await browser.close();
}

async function main() {
    const args = process.argv.slice(2);
    if (args.length === 0) {
        console.log('Uso: node md-to-statblock-pdf.js <file.xml> [-o output.pdf|output.png]');
        process.exit(1);
    }

    const inputFile = args[0];
    let outputFile = null;
    let imagePath = null;
    const oIdx = args.indexOf('-o');
    if (oIdx >= 0 && oIdx + 1 < args.length) {
        outputFile = args[oIdx + 1];
    }
    const imgIdx = args.indexOf('--image');
    if (imgIdx >= 0 && imgIdx + 1 < args.length) {
        imagePath = args[imgIdx + 1];
    }

    if (!outputFile) {
        outputFile = inputFile.replace(/\.xml$/, '.pdf');
    }

    const xmlText = fs.readFileSync(inputFile, 'utf-8');

    // Supporta sia <monster> che <pc>
    let monster;
    if (xmlText.includes('<monster>')) {
        monster = parseXML(xmlText);
    } else if (xmlText.includes('<pc>')) {
        // Adatta il formato pc al formato monster
        const getPC = (tag) => {
            const m = xmlText.match(new RegExp(`<${tag}>(.*?)</${tag}>`, 's'));
            return m ? m[1].trim() : '';
        };
        const getAllPC = (tag) => {
            const results = [];
            const regex = new RegExp(`<${tag}>(.*?)</${tag}>`, 'gs');
            let match;
            while ((match = regex.exec(xmlText)) !== null) results.push(match[1].trim());
            return results;
        };
        monster = parseXML(xmlText);
        // Override name with label if present, but keep original
        const label = getPC('label');
        monster._origName = monster.name;
        if (label) monster.name = label;
        // Merge multiple save/skill tags
        const saves = getAllPC('save');
        if (saves.length > 1) monster.save = saves.join(', ');
        const skills = getAllPC('skill');
        if (skills.length > 1) monster.skill = skills.join(', ');
    } else {
        console.error('Nessun <monster> o <pc> trovato.');
        process.exit(1);
    }

    const html = buildHTML(monster, imagePath);
    
    // Salva anche l'HTML intermedio per debug
    const htmlPath = outputFile.replace(/\.(pdf|png)$/, '.html');
    fs.writeFileSync(htmlPath, html);

    await generatePDF(html, outputFile);
    console.log(`✓ ${inputFile} → ${outputFile}`);
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
