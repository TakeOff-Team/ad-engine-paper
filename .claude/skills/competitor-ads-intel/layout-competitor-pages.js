#!/usr/bin/env node
/**
 * competitor-ads-intel / layout-competitor-pages.js
 *
 * Lays the ads that fetch-competitor-ads.py saved onto the brand's Paper file:
 * one Paper page per competitor, one artboard per page, every ad numbered with how
 * long it has been running, longest-running first. The person looks at a page and
 * says the numbers they like.
 *
 *   node .claude/skills/competitor-ads-intel/layout-competitor-pages.js --file <paperFileId> --batch <batch-folder> [--cols 6]
 *
 * Paper Desktop must be open. Writes the page and artboard ids back into
 * <batch>/summary.json so picks can be traced to a page.
 */
const fs = require('fs');
const path = require('path');
const { PaperClient } = require(path.join(__dirname, '..', 'paper-ads', 'paper-client.js'));

const arg = k => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const fileId = arg('--file'), batch = arg('--batch'), COLS = parseInt(arg('--cols') || '6', 10);
if (!fileId || !batch) { console.error('usage: layout-competitor-pages.js --file <paperFileId> --batch <folder> [--cols 6]'); process.exit(1); }

const TILE_W = 280, IMG_H = 350, GAP = 32, PAD = 64, HEAD = 190, TILE_H = 34 + 10 + IMG_H + 10 + 22;
const esc = s => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const FONT = "font-family:Inter, system-ui, sans-serif;";
const sleep = ms => new Promise(r => setTimeout(r, ms));
const ran = d => d >= 60 ? `running ${Math.round(d / 30)} months` : `running ${d} days`;

(async () => {
  const sumPath = path.join(batch, 'summary.json');
  const summary = JSON.parse(fs.readFileSync(sumPath, 'utf8'));
  const c = new PaperClient(); await c.connect();

  for (const comp of summary.competitors) {
    const idxPath = path.join(comp.folder, 'index.json');
    const ads = fs.existsSync(idxPath) ? JSON.parse(fs.readFileSync(idxPath, 'utf8')) : [];
    if (!ads.length) { console.log(`${comp.name}: no image ads to lay out, skipped`); continue; }

    const page = PaperClient.json(await c.call('create_page', { fileId, name: `Competitor · ${comp.name}` }));
    const pageId = page.pageId || page.id;
    const rows = Math.ceil(ads.length / COLS);
    const width = PAD * 2 + COLS * TILE_W + (COLS - 1) * GAP;
    const height = PAD * 2 + HEAD + rows * TILE_H + (rows - 1) * GAP;
    const ab = PaperClient.json(await c.call('create_artboard', {
      fileId, pageId, name: `${comp.name} · ${ads.length} image ads`,
      styles: { width: `${width}px`, height: `${height}px`, backgroundColor: '#F4F2EE', display: 'flex', flexDirection: 'column', padding: `${PAD}px`, gap: '0px' },
    }));

    const link = comp.ad_library ? `<div style="${FONT}font-size:18px;line-height:24px;color:#4040FF">${esc(comp.ad_library)}</div>` : '';
    await c.call('write_html', { fileId, targetNodeId: ab.id, mode: 'insert-children', html:
      `<div style="display:flex;flex-direction:column;gap:10px;height:${HEAD}px">
        <div style="${FONT}font-size:56px;font-weight:600;letter-spacing:-0.03em;line-height:60px;color:#1A1816">${esc(comp.name)}</div>
        <div style="${FONT}font-size:24px;line-height:32px;color:#5A554F">${ads.length} image ads running now, longest-running first. The ones running longest are the ones they keep paying for. Say the numbers you like.</div>
        ${link}
      </div>` });

    // one row per write: Paper drops parallel writes, so these go one at a time.
    // The first row creates the grid (an empty div would become a plain shape); later rows go into it.
    const tilesFor = list => list.map(a =>
      `<div style="display:flex;flex-direction:column;gap:10px;width:${TILE_W}px">
        <div style="${FONT}font-size:30px;font-weight:700;line-height:34px;color:#1A1816">${String(a.n).padStart(2, '0')}</div>
        <img src="paper-asset://${a.file}" style="width:${TILE_W}px;height:${IMG_H}px;object-fit:contain;background:#FFFFFF;border-radius:10px"/>
        <div style="${FONT}font-size:16px;line-height:22px;color:#6B655F">${ran(a.days_running)}</div>
      </div>`).join('');
    const first = PaperClient.json(await c.call('write_html', { fileId, targetNodeId: ab.id, mode: 'insert-children', html:
      `<div style="display:flex;flex-wrap:wrap;gap:${GAP}px;width:${width - PAD * 2}px">${tilesFor(ads.slice(0, COLS))}</div>` }));
    const gridId = first && first.createdNodes && first.createdNodes[0] && first.createdNodes[0].id;
    for (let i = COLS; i < ads.length; i += COLS) {
      await c.call('write_html', { fileId, targetNodeId: gridId, mode: 'insert-children', html: tilesFor(ads.slice(i, i + COLS)) });
      await sleep(150);
    }
    await c.call('finish_working_on_nodes', { fileId, nodeIds: [ab.id] });
    comp.paper_page_id = pageId; comp.paper_artboard_id = ab.id;
    console.log(`${comp.name}: ${ads.length} ads on page "Competitor · ${comp.name}"`);
  }
  summary.paper_file_id = fileId;
  fs.writeFileSync(sumPath, JSON.stringify(summary, null, 2));
})().catch(e => { console.error('layout-competitor-pages:', e.message); process.exit(1); });
