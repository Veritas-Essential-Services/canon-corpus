// mnemonicon_pack_browser_test.js -- the exported hymn packs, imported into the
// real Mnemonicon page in headless Chromium (launch plan C5, first link).
//
// Uses the Mnemonicon's own harness: its site/ and its fake cloud
// (tests/fake-backend.js + fake-client.js) are COPIED to a temp folder first,
// so nothing in that repo is touched or run in place. Every request is
// answered from the copy or refused; the real card and Supabase are never hit.
//
// Needs Node, Playwright and the Mnemonicon repo:
//   MNEMONICON_DIR        default ../The Mnemonicon Website
//   MNEMONICON_PLAYWRIGHT a node_modules/playwright; else require('playwright'),
//                         else ../ESSI Website's copy
// Without Playwright or the repo it says so and exits 0.
// Run:  node tests/mnemonicon_pack_browser_test.js
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');

const REPO = path.join(__dirname, '..');
const PACKS = path.join(REPO, 'exports', 'mnemonicon');
const FILES = ['adoro-te.json', 'pange-lingua.json'].map((f) => path.join(PACKS, f));
const MNEMONICON = process.env.MNEMONICON_DIR || path.join(REPO, '..', 'The Mnemonicon Website');

function findPlaywright() {
  const tries = [process.env.MNEMONICON_PLAYWRIGHT, 'playwright', path.join(REPO, '..', 'ESSI Website', 'node_modules', 'playwright')].filter(Boolean);
  for (const t of tries) { try { return require(t); } catch (e) { /* next */ } }
  return null;
}
const pw = findPlaywright();
if (!pw) { console.log('SKIP  browser: Playwright not found (set MNEMONICON_PLAYWRIGHT)'); process.exit(0); }
if (!fs.existsSync(path.join(MNEMONICON, 'site', 'app.js'))) { console.log('SKIP  browser: the Mnemonicon repo is not at ' + MNEMONICON); process.exit(0); }

// The temp copy: site/ and the two harness files.
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'mnemo-pack-'));
fs.cpSync(path.join(MNEMONICON, 'site'), path.join(TMP, 'site'), { recursive: true });
for (const f of ['fake-backend.js', 'fake-client.js']) fs.copyFileSync(path.join(MNEMONICON, 'tests', f), path.join(TMP, f));
const SITE = path.join(TMP, 'site');
const { Backend } = require(path.join(TMP, 'fake-backend.js'));
const FAKE_CLIENT = fs.readFileSync(path.join(TMP, 'fake-client.js'), 'utf8');

const ORIGIN = 'https://mnemonicon.thewordhoard.com';
const TYPES = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.json': 'application/json',
  '.webmanifest': 'application/manifest+json', '.png': 'image/png', '.woff2': 'font/woff2', '.wasm': 'application/wasm' };
const CARD_JS = 'window.WordHoard = { available: true, sb: window.__fakeSb, cards: { setActive: function () {} } };';
const SUPABASE_SHIM = 'window.supabase = { createClient: function () { return window.__fakeSb; } };';
const ADAM = { id: 'u-adam', email: 'adam@example.com' };

let fails = 0, passes = 0;
const ok = (cond, msg, detail) => {
  console.log((cond ? 'ok    ' : 'FAIL  ') + msg + (!cond && detail !== undefined ? '\n        ' + detail : ''));
  cond ? passes++ : fails++;
};

// A device, as in the Mnemonicon's browser.test.js: one context, the shared fake cloud.
async function device(browser, be, user) {
  const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, serviceWorkers: 'block' });
  await ctx.exposeBinding('__be', (_src, req) => be.handle(req));
  await ctx.addInitScript((u) => {
    if (u && !localStorage.getItem('__fake_seeded')) {
      localStorage.setItem('__fake_session', JSON.stringify(u));
      localStorage.setItem('__fake_seeded', '1');
    }
  }, user || null);
  await ctx.addInitScript(FAKE_CLIENT);
  await ctx.route('**/*', (route) => {
    const u = new URL(route.request().url());
    if (u.hostname === 'thewordhoard.com' && u.pathname === '/auth/wordhoard-auth.js')
      return route.fulfill({ status: 200, contentType: TYPES['.js'], body: CARD_JS });
    if (u.hostname === 'mnemonicon.thewordhoard.com') {
      let p = decodeURIComponent(u.pathname); if (p.endsWith('/')) p += 'index.html';
      if (p === '/vendor/supabase.js') return route.fulfill({ status: 200, contentType: TYPES['.js'], body: SUPABASE_SHIM });
      const f = path.join(SITE, p);
      if (!f.startsWith(SITE) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) return route.fulfill({ status: 404, body: 'not found' });
      return route.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'application/octet-stream', body: fs.readFileSync(f) });
    }
    const type = route.request().resourceType();
    if (type === 'stylesheet') return route.fulfill({ status: 200, contentType: 'text/css', body: '' });
    if (type === 'script') return route.fulfill({ status: 200, contentType: TYPES['.js'], body: '' });
    return route.fulfill({ status: 204, body: '' });
  });
  const page = await ctx.newPage();
  const errors = [], dialogs = [];
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errors.push('console: ' + m.text()); });
  page.on('dialog', (d) => { dialogs.push(d.type() + ': ' + d.message()); d.accept(); });
  await page.goto(ORIGIN + '/', { waitUntil: 'load' });
  await page.waitForTimeout(100);
  return { ctx, page, errors, dialogs };
}

const pieces = (page) => page.evaluate(() => JSON.parse(JSON.stringify(pieces)));
const syncNow = (page) => page.evaluate(async () => { await window.__mnemosync.syncNow(true); });
async function settle(page) { await page.waitForTimeout(50); await syncNow(page); await page.waitForTimeout(50); await syncNow(page); }
async function importPacks(d, files) {
  d.dialogs.length = 0;
  await d.page.setInputFiles('#import-file', files);
  await d.page.waitForTimeout(250);
  return d.dialogs.join(' | ');
}

async function main() {
  const packed = FILES.flatMap((f) => JSON.parse(fs.readFileSync(f, 'utf8')));
  const byId = new Map(packed.map((p) => [p.id, p]));
  const browser = await pw.chromium.launch();
  try {
    console.log('\n## signed out: the packs import once');
    const be = new Backend();
    let d = await device(browser, be);
    let msg = await importPacks(d, FILES);
    let got = await pieces(d.page);
    ok(got.length === packed.length, `both packs land: ${packed.length} pieces`, got.length);
    ok(/13 pieces added\./.test(msg), '…and the message counts them', msg);
    ok(got.every((p) => byId.has(p.id)) && new Set(got.map((p) => p.id)).size === got.length, 'each piece appears once, under its own id');
    ok(got.every((p) => { const q = byId.get(p.id); return q && p.text === q.text && p.title === q.title && p.notes === q.notes && p.translation === q.translation; }),
      'text, title, notes and translation arrive unchanged');
    ok(await d.page.locator('#piece-list .p-title').count() === packed.length, 'the Bank lists all of them');
    msg = await importPacks(d, FILES);
    ok((await pieces(d.page)).length === packed.length, 'a second import adds nothing');
    ok(/0 pieces added · 13 already in the bank/.test(msg), '…and says so', msg);
    await d.page.reload(); await d.page.waitForTimeout(150);
    ok((await pieces(d.page)).length === packed.length, 'after a reload the bank still holds exactly 13');

    // A piece in use: the detail page, and line-by-line recitation, one line per clause.
    const first = packed[0];
    await d.page.evaluate((id) => openDetail(id), first.id);
    ok((await d.page.locator('#d-text').innerText()).trim() === first.text.trim(), 'the detail page shows the Latin');
    const meta = await d.page.locator('#d-meta').innerText();
    ok(meta.includes(first.translation) && meta.includes('#hymn'), 'its meta line names the English witness and the tags', meta);
    await d.page.evaluate((id) => { startReview(pieces.find((p) => p.id === id)); setMode('lines'); }, first.id);
    const spans = await d.page.locator('#r-text span').count();
    ok(spans === first.text.split('\n').length, `line-by-line recites it in ${spans} lines (one per clause)`, spans);
    const rmeta = await d.page.locator('#r-meta').innerText();
    const eng = first.notes.split('\n')[0].replace(/^English[^:]*: /, '').slice(0, 24);
    ok(eng.length > 10 && !rmeta.includes(eng) && !(await d.page.locator('#r-text').innerText()).includes(eng), 'the English never shows while reciting', rmeta);
    ok(!d.errors.length, 'no page errors', d.errors.join(' | '));
    await d.ctx.close();

    console.log('\n## signed in: the pieces sync under their own ids');
    const be2 = new Backend();
    d = await device(browser, be2, ADAM);
    await importPacks(d, FILES);
    await settle(d.page);
    const rows = be2.db.pieces.filter((r) => !r.deleted_at);
    ok(rows.length === packed.length && rows.every((r) => byId.has(r.id)), 'all 13 are in the cloud under the pack’s ids', rows.length);
    ok(rows.every((r) => r.category === 'Song' && r.tags.includes('latin')), '…with category and tags intact');
    msg = await importPacks(d, FILES);
    await settle(d.page);
    ok(be2.db.pieces.filter((r) => !r.deleted_at).length === packed.length && /0 pieces added/.test(msg), 'importing again after sync adds nothing, here or in the cloud', msg);
    ok(!d.errors.length, 'no page errors', d.errors.join(' | '));
    await d.ctx.close();
  } finally {
    await browser.close();
    fs.rmSync(TMP, { recursive: true, force: true });
  }
  console.log(`\nbrowser: ${passes} passed, ${fails} failed`);
  process.exit(fails ? 1 : 0);
}
main().catch((e) => { console.error(e); fs.rmSync(TMP, { recursive: true, force: true }); process.exit(1); });
