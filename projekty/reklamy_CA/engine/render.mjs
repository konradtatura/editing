// usage: node render.mjs SPEC.json OUTDIR [--from S] [--to S] [--frames 1,2,3 (seconds)] [--par 3]
// Renders the overlay layer (captions, plansze, overlays) as transparent 1080x1920 PNGs, one per frame.
import { createRequire } from 'module';
const req = createRequire(process.env.PW_ROOT || '/opt/node22/lib/node_modules/'); const { chromium } = req('playwright');
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const a = process.argv.slice(2);
const opt = (k, d) => { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; };
const spec = JSON.parse(fs.readFileSync(a[0], 'utf8')); const out = a[1]; fs.mkdirSync(out, { recursive: true });
const fps = spec.fps || 30, N = Math.round(spec.dur * fps);
let frames;
if (opt('--frames')) frames = opt('--frames').split(',').map(s => Math.round(parseFloat(s) * fps));
else { const f0 = Math.round(parseFloat(opt('--from', 0)) * fps), f1 = Math.min(N, Math.round(parseFloat(opt('--to', spec.dur)) * fps)); frames = []; for (let i = f0; i < f1; i++) frames.push(i); }
const icons = {}; const idir = path.join(here, 'assets/icons');
for (const f of fs.readdirSync(idir)) icons[f.replace('.svg', '')] = fs.readFileSync(path.join(idir, f), 'utf8').replace(/<!--.*?-->/s, '').replace(/class="[^"]*"/, '').replace(/width="24"\s*height="24"/, '');
const par = parseInt(opt('--par', 3));
const browser = await chromium.launch({ executablePath: fs.existsSync('/opt/pw-browsers/chromium') ? undefined : undefined });
const t0 = Date.now(); let done = 0;
async function worker(k) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('PAGEERR', e.message));
  await page.addInitScript(ic => { window.ICONS = ic; }, icons);
  await page.goto('file://' + path.join(here, 'overlay.html'));
  await page.evaluate(async () => { await document.fonts.ready; });
  await page.evaluate(s => window.init(s), spec);
  await page.evaluate(async () => { await document.fonts.ready; });
  for (let j = k; j < frames.length; j += par) {
    const f = frames[j];
    await page.evaluate(t => window.seek(t), f / fps);
    await page.screenshot({ path: path.join(out, `f_${String(f).padStart(5, '0')}.png`), omitBackground: true });
    if (++done % 150 === 0) console.log(`${done}/${frames.length} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  await page.close();
}
await Promise.all([...Array(par).keys()].map(worker));
await browser.close();
console.log(`rendered ${frames.length} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
