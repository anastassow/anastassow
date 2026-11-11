// Screenshot #c in each HTML file given, at device scale SCALE (default 1).
const { chromium } = require('playwright-core');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME_BIN });
  const p = await b.newPage({ viewport: { width: 1700, height: 900 }, deviceScaleFactor: +(process.env.SCALE || 1) });
  for (const f of process.argv.slice(2)) {
    await p.goto('file://' + f, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    await p.waitForFunction(() => document.body.dataset.ready === '1' || !document.querySelector('script'));
    await p.waitForTimeout(150);
    const el = await p.$('#c');
    await el.screenshot({ path: f.replace(/\.html$/, '.png'), omitBackground: true });
  }
  await b.close();
})();
