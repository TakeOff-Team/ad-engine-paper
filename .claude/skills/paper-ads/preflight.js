#!/usr/bin/env node
/**
 * preflight.js — measure every ad artboard in the brand's Paper file and fail the ones that
 * are not ready. Reads positions, sizes, text and computed styles straight from Paper, so
 * nothing here depends on eyeballing a screenshot.
 *
 * Usage (from project root, Paper Desktop open with the brand file open):
 *   node .claude/skills/paper-ads/preflight.js --file <paperFileId> [--only a1-v1,a3-v2] [--campaign brands/<brand>/generation/paper-ads/<campaign>] [--config brands/<brand>/intelligence/preflight.json] [--out report.json]
 *
 * --campaign points at the concept folders; with it the script reads each variant's product_bbox from
 * spec.json (written by product-bbox.py or extend-plate.py) and fails text that overlaps the product or a
 * product that enters the 9:16 rail, which Paper alone cannot see because the product is baked into the plate.
 *
 * Checks, per artboard named "a1-v1 · 4x5" or "a1-v1 · 9x16":
 *   FAIL  canvas is not 1080×1350 (4:5) or 1080×1920 (9:16)
 *   FAIL  a text layer overlaps a photo it does not belong to, or another text layer (a transparent cutout: WARN, check at 100%)
 *   FAIL  a text layer runs outside the artboard
 *   FAIL  a text layer sits outside the critical-content zone (wordmark and legal: WARN)
 *   FAIL  in 9:16, a CTA, proof, product or badge sits in the platform-controls rail
 *   FAIL  a text layer is under its mobile type floor (role from the layer name), or under a brand minimum from preflight.json
 *   FAIL  a photo frame carries objectPosition (Paper keeps it but ignores it; the crop never applied)
 *   WARN  a photo frame's backgroundPosition was never set (still the 50% 50% default)
 *   WARN  the bottom band below the last element is taller than the allowed empty band (4:5 120px, 9:16 360px)
 *   HELD  an artboard named "a3-v1 · 9x16 (HELD: reason)" is listed with its reason and never counted as a pass
 *   WARN  a 4:5 and 9:16 pair are not side by side, or a Meta ad text card is not last in its row
 *
 * preflight.json (optional, in the brand's intelligence/ folder) lets a brand tighten the floors:
 *   { "min_px": { "subhead": 42, "cta": 38 }, "max_empty_bottom": { "4x5": 120, "9x16": 220 } }
 * Exit code 1 when any artboard FAILs. Free, local, no image model.
 */
const fs = require('fs');
const path = require('path');
const { PaperClient } = require('./paper-client');

const ZONES = {
  '4x5':  { w: 1080, h: 1350, live: { x0: 54, y0: 54, x1: 1026, y1: 1296 }, rail: null,                              emptyBottom: 120 },
  '9x16': { w: 1080, h: 1920, live: { x0: 90, y0: 250, x1: 990, y1: 1570 }, rail: { x0: 840, y0: 560, x1: 1080, y1: 1500 }, emptyBottom: 360 },
};
const FLOORS = [ // first match on the lower-cased layer name wins; same roles as compose-text.py
  [/legal|footnote|disclaimer/, 20], [/caption|subline|subhead|proof/, 30], [/statistic|^stat(-\d+)?$|big-?number/, 96], [/headline/, 88],
  [/^(price|cta|cta-text|button)$/, 34], [/kicker|eyebrow|label|badge|tag|before|after|order|save|code/, 28], [/old-price/, 24],
];
const RAIL_ROLES = /cta|button|price|proof|rating|stars|review|badge|product|wordmark|logo|offer|guarantee/;
const SOFT_ZONE = /wordmark|logo|legal|footnote|disclaimer/;

function arg(flag, dflt) { const i = process.argv.indexOf(flag); return i > -1 ? process.argv[i + 1] : dflt; }
function px(v) { const m = /^(-?[\d.]+)px$/.exec(String(v || '')); return m ? parseFloat(m[1]) : null; }
function rect(n) { return { x0: n.worldX, y0: n.worldY, x1: n.worldX + n.width, y1: n.worldY + n.height }; }
// artboard-local rect: the zones are defined on the 1080-wide canvas, not in world space
function local(n, ab) { return { x0: n.worldX - ab.worldX, y0: n.worldY - ab.worldY, x1: n.worldX - ab.worldX + n.width, y1: n.worldY - ab.worldY + n.height }; }
function inter(a, b) { return Math.max(0, Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0)) * Math.max(0, Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0)); }
function inside(a, z) { return a.x0 >= z.x0 - 1 && a.y0 >= z.y0 - 1 && a.x1 <= z.x1 + 1 && a.y1 <= z.y1 + 1; }
function floorFor(name, cfg) {
  const n = name.toLowerCase();
  for (const role of Object.keys(cfg.min_px || {})) if (n.includes(role)) return { px: cfg.min_px[role], from: 'preflight.json' };
  for (const [re, v] of FLOORS) if (re.test(n)) return { px: v, from: 'mobile floor' };
  return null;
}

async function pool(items, limit, fn) {
  const out = new Array(items.length); let i = 0;
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, async () => { while (i < items.length) { const k = i++; out[k] = await fn(items[k], k); } }));
  return out;
}

async function loadArtboard(c, fileId, ab) {
  // every node, with bounds, text and ancestry
  const nodes = []; const byId = {};
  async function walk(id, ancestors) {
    const info = PaperClient.json(await c.call('get_node_info', { fileId, nodeId: id }));
    if (!info || info.width == null || info.worldX == null) return;
    const n = { id, name: info.name || '', component: info.component, width: info.width, height: info.height, worldX: info.worldX, worldY: info.worldY,
      text: info.textContent, visible: info.isVisible !== false, ancestors, childIds: info.childIds || [] };
    nodes.push(n); byId[id] = n;
    for (const ch of n.childIds) await walk(ch, [...ancestors, id]);
  }
  await walk(ab.id, []);
  const styles = {};
  const ids = nodes.map(n => n.id);
  for (let k = 0; k < ids.length; k += 40) {
    const r = PaperClient.json(await c.call('get_computed_styles', { fileId, nodeIds: ids.slice(k, k + 40) }));
    Object.assign(styles, (r && r.styles) || {});
  }
  for (const n of nodes) n.style = styles[n.id] || {};
  return { nodes, byId };
}

function specFor(campaign, cid, ratio) {
  if (!campaign) return null;
  const f = path.join(campaign, cid, 'spec.json'); if (!fs.existsSync(f)) return null;
  try { const sp = JSON.parse(fs.readFileSync(f, 'utf8')); return ((sp.variants || {})[ratio === '4x5' ? 'feed_4x5' : 'fullscreen_9x16']) || null; } catch (e) { return null; }
}

function check(ab, ratio, nodes, byId, cfg, vspec) {
  const Z = ZONES[ratio]; const fails = [], warns = [];
  const held = ab.m && ab.m[4];
  if (held) warns.push(`held: ${held}`);
  const pb = vspec && Array.isArray(vspec.product_bbox) && vspec.product_bbox.length === 4 ? { x0: vspec.product_bbox[0], y0: vspec.product_bbox[1], x1: vspec.product_bbox[2], y1: vspec.product_bbox[3] } : null;
  if (pb && Z.rail && inter(pb, Z.rail) > 0) fails.push(`product (from spec.json) enters the 9:16 platform-controls rail by ${Math.round(pb.x1 - Z.rail.x0)}px`);
  if (pb && ratio === '9x16' && !inside(pb, { x0: 120, y0: 430, x1: 810, y1: 1350 })) warns.push(`product (from spec.json) sits outside the 9:16 product stage x120–810, y430–1350`);
  const A = { x0: 0, y0: 0, x1: ab.width, y1: ab.height };
  if (ab.width !== Z.w || ab.height !== Z.h) fails.push(`canvas is ${ab.width}×${ab.height}, expected ${Z.w}×${Z.h}`);
  const vis = nodes.filter(n => n.visible && n.id !== ab.id);
  const texts = vis.filter(n => n.component === 'Text' && (n.text || '').trim());
  const photos = vis.filter(n => /url\(/.test(n.style.backgroundImage || '') || n.component === 'Image');
  const isCutout = p => /cutout|figure|person|founder|portrait/.test(p.name.toLowerCase()) || /contain/.test(p.style.backgroundSize || '');
  const fullBleed = n => n.width >= ab.width - 2 && n.height >= ab.height - 2;
  const isGround = p => (p.width * p.height) >= 0.5 * ab.width * ab.height; // a plate-first design: the photo is the canvas
  if (!pb && photos.some(isGround)) warns.push('the photo is the whole canvas and spec.json has no product_bbox for this variant: run product-bbox.py (or pass --bbox) so text can be checked against the product');

  for (const p of photos) {
    if (p.style.objectPosition) fails.push(`"${p.name}": objectPosition "${p.style.objectPosition}" is ignored by Paper; the crop never applied (set backgroundPosition)`);
    const bp = (p.style.backgroundPosition || '').replace(/\s+/g, ' ').trim();
    if (!fullBleed(p) && (!bp || bp === '50% 50%' || bp === 'center' || bp === 'center center')) warns.push(`"${p.name}": photo crop never set (backgroundPosition is the default). Check the subject at 100%`);
  }
  for (const t of texts) {
    const R = rect(t), L = local(t, ab); const nm = t.name.toLowerCase();
    if (!inside(L, A)) fails.push(`"${t.name}" runs outside the artboard`);
    else if (!inside(L, Z.live)) (SOFT_ZONE.test(nm) ? warns : fails).push(`"${t.name}" is outside the ${ratio} critical-content zone (y ${Math.round(L.y0)}–${Math.round(L.y1)}, x ${Math.round(L.x0)}–${Math.round(L.x1)})`);
    const railShare = Z.rail ? inter(L, Z.rail) / Math.max(1, (L.x1 - L.x0) * (L.y1 - L.y0)) : 0;
    if (Z.rail && RAIL_ROLES.test(nm) && (L.x0 >= Z.rail.x0 || railShare >= 0.5) && inter(L, Z.rail) > 0) fails.push(`"${t.name}" sits in the 9:16 platform-controls rail (x840–1080, y560–1500)`);
    if (pb) { const ov = inter(L, pb); if (ov > 4 * 4) fails.push(`"${t.name}" overlaps the product (box from spec.json) by ${Math.round(ov)}px²`); }
    const fl = floorFor(t.name, cfg); const fs_ = px(t.style.fontSize);
    if (fl && fs_ != null && fs_ < fl.px) fails.push(`"${t.name}" is ${fs_}px, under the ${fl.px}px ${fl.from}`);
    for (const p of photos) {
      if (t.ancestors.includes(p.id) || isGround(p)) continue; // text on the photo on purpose; a ground plate is checked through the product box instead
      const ov = inter(R, rect(p)); if (ov > 4 * 4) (isCutout(p) ? warns : fails).push(`"${t.name}" overlaps ${isCutout(p) ? 'cutout' : 'photo'} "${p.name}" by ${Math.round(ov)}px²${isCutout(p) ? ' (transparent PNG: confirm at 100% that the figure itself stays clear of the text)' : ''}`);
    }
    for (const u of texts) {
      if (u === t || u.ancestors.includes(t.id) || t.ancestors.includes(u.id)) continue;
      if (t.id > u.id) continue; // report each pair once
      const ov = inter(R, rect(u)); if (ov > 6 * 6) fails.push(`"${t.name}" overlaps text "${u.name}" by ${Math.round(ov)}px²`);
    }
  }
  if (Z.rail) for (const p of photos) if (!fullBleed(p) && /product|pack/.test(p.name.toLowerCase()) && inter(local(p, ab), Z.rail) > 0) fails.push(`"${p.name}" (product) enters the 9:16 platform-controls rail`);
  // empty band at the bottom: distance from the lowest non-bleed element to the artboard edge
  const content = vis.filter(n => !fullBleed(n) && !(n.component === 'Frame' && n.childIds.length && !(n.style.backgroundImage || n.style.backgroundColor)));
  const lowest = content.reduce((m, n) => Math.max(m, local(n, ab).y1), A.y0);
  const band = A.y1 - lowest; const maxBand = (cfg.max_empty_bottom || {})[ratio] ?? Z.emptyBottom;
  if (band > maxBand) warns.push(`${Math.round(band)}px of nothing below the last element (allowed ${maxBand}px). Let the photo, figure or ground reach the edge, or move the CTA down`);
  return { fails, warns };
}

(async () => {
  const fileId = arg('--file'); if (!fileId) { console.error('usage: node preflight.js --file <paperFileId> [--only ids] [--config preflight.json] [--out report.json]'); process.exit(2); }
  const only = arg('--only') ? arg('--only').split(',').map(s => s.trim()) : null;
  const cfgPath = arg('--config'); const cfg = cfgPath && fs.existsSync(cfgPath) ? JSON.parse(fs.readFileSync(cfgPath, 'utf8')) : {};
  const c = new PaperClient(); await c.connect();
  const info = PaperClient.json(await c.call('get_basic_info', { fileId }));
  if (!info || !info.artboards) { console.error('could not read the file. Is Paper Desktop open with this file?'); process.exit(2); }
  const ads = info.artboards.map(a => ({ ...a, m: /^(a\d+-v\d+[a-z]?)\s*·\s*(4x5|9x16)(\s*\((.*)\))?$/.exec(a.name || '') })).filter(a => a.m && (!only || only.includes(a.m[1])));
  const campaign = arg('--campaign'); // concept folders with spec.json: product boxes measured on the plates
  const cards = info.artboards.filter(a => /·\s*Meta ad text$/.test(a.name || ''));
  console.log(`preflight · ${info.fileName} · ${ads.length} ad artboard(s)\n`);
  const report = { file: fileId, ran_at: new Date().toISOString(), artboards: {} }; let anyFail = false;
  const results = await pool(ads, 3, async ab => {
    const { nodes, byId } = await loadArtboard(c, fileId, ab);
    return { ab, r: check(ab, ab.m[2], nodes, byId, cfg, specFor(campaign, ab.m[1], ab.m[2])) };
  });
  // row layout: 4x5 then 9x16 side by side, Meta card last in its row
  const byConcept = {}; for (const { ab } of results) (byConcept[ab.m[1]] = byConcept[ab.m[1]] || {})[ab.m[2]] = ab;
  for (const [cid, pair] of Object.entries(byConcept)) {
    if (pair['4x5'] && pair['9x16']) {
      const gap = pair['9x16'].worldX - (pair['4x5'].worldX + pair['4x5'].width);
      const sameRow = Math.abs(pair['9x16'].worldY - pair['4x5'].worldY) < 2;
      if (!sameRow || gap < 40 || gap > 200) results.find(x => x.ab === pair['4x5']).r.warns.push(`pair layout: 9:16 is ${sameRow ? Math.round(gap) + 'px to the right' : 'on a different row'} (spec: side by side, 80px gap)`);
    }
    const angle = cid.split('-')[0]; const card = cards.find(k => (k.name || '').startsWith(angle + ' ·'));
    const rowY = (pair['4x5'] || pair['9x16']).worldY;
    const rowAds = results.filter(x => Math.abs(x.ab.worldY - rowY) < 2).map(x => x.ab);
    const rightmost = Math.max(...rowAds.map(a => a.worldX + a.width));
    if (card && Math.abs(card.worldY - rowY) < 2 && card.worldX < rightmost && pair['4x5']) results.find(x => x.ab === pair['4x5']).r.warns.push(`"${card.name}" is not the last artboard in the row`);
  }
  for (const { ab, r } of results.sort((a, b) => a.ab.name.localeCompare(b.ab.name, undefined, { numeric: true }))) {
    const status = ab.m[4] ? 'HELD' : r.fails.length ? 'FAIL' : r.warns.length ? 'WARN' : 'PASS'; if (r.fails.length && !ab.m[4]) anyFail = true;
    report.artboards[ab.name] = { status, fails: r.fails, warns: r.warns };
    console.log(`${status.padEnd(4)}  ${ab.name}`);
    for (const f of r.fails) console.log(`        ✗ ${f}`);
    for (const w of r.warns) console.log(`        ! ${w}`);
  }
  const nh = results.filter(x => x.ab.m[4]).length, live = results.filter(x => !x.ab.m[4]);
  const n = live.length, nf = live.filter(x => x.r.fails.length).length, nw = live.filter(x => !x.r.fails.length && x.r.warns.length).length;
  console.log(`\n${n - nf - nw} pass · ${nw} warn · ${nf} fail${nh ? ` · ${nh} held` : ''}`);
  if (arg('--out')) { fs.writeFileSync(arg('--out'), JSON.stringify(report, null, 2)); console.log(`report → ${arg('--out')}`); }
  console.log('\nThe script cannot see a face. For every photo listed above, look at the artboard at 100% and confirm the head, hands and product are inside the frame with room to spare.');
  process.exit(anyFail ? 1 : 0);
})().catch(e => { console.error('preflight:', e.message); process.exit(2); });
