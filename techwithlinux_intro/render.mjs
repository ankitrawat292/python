import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const root = path.dirname(new URL(import.meta.url).pathname);
const FPS = 30;
const only = process.argv[2]; // optional: comma list of seconds for preview stills
const types = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json' };
const server = http.createServer((req, res) => {
  const p = path.join(root, decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(p, (e, d) => { if (e) { res.writeHead(404); return res.end(); } res.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' }); res.end(d); });
}).listen(8765);

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
page.on('console', m => console.log('page:', m.text()));
page.on('pageerror', e => console.log('pageerror:', e.message));
await page.goto('http://localhost:8765/index.html');
await page.waitForFunction('window.READY === true', null, { timeout: 60000 });

const grab = async t => {
  const b64 = await page.evaluate(t => { window.renderFrame(t); return document.querySelector('canvas').toDataURL('image/png').split(',')[1]; }, t);
  return Buffer.from(b64, 'base64');
};

if (only) {
  for (const s of only.split(',')) fs.writeFileSync(path.join(root, `still_${s}.png`), await grab(+s));
} else {
  const dur = await page.evaluate('window.DURATION');
  const total = Math.round(dur * FPS);
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', path.join(root, 'video_noaudio.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < total; i++) {
    const buf = await grab(i / FPS);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 30 === 0) console.log(`frame ${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
}
await browser.close();
server.close();
