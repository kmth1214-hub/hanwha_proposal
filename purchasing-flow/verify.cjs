const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const html = fs.readFileSync(__dirname + '/index.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const app = { innerHTML: '' };
let onHashChange;
const navItems = [...html.matchAll(/<a href="#([a-z0-9]+)"><span>/g)].map(m => ({
  hash: '#' + m[1], active: false, current: false,
  classList: { toggle(_name, value) { this.owner.active = value; } },
  setAttribute() { this.current = true; }, removeAttribute() { this.current = false; },
}));
navItems.forEach(item => item.classList.owner = item);
const context = vm.createContext({
  document: { querySelectorAll: selector => selector === 'nav a' ? navItems : [], getElementById: () => app },
  location: { hash: '#b' },
  localStorage: { getItem: () => null, setItem: () => {} },
  window: { addEventListener: (name, fn) => { if (name === 'hashchange') onHashChange = fn; }, scrollTo: () => {} },
});
vm.runInContext(script, context);
function run(expression) { return vm.runInContext(expression, context); }
assert.equal(run('getNews().length'), 6);
assert.equal(run('getPurchases().reduce((s,p)=>s+p[4],0)'), 7400);
assert.equal(run("macd('pp').every(d=>Number.isFinite(d.macd)&&Math.abs(d.hist-(d.macd-d.signal))<1e-10)"), true);
assert.equal(run('ema([8,8,8,8],12).every(x=>x===8)'), true);
const baseline = run("macd('pp').find(d=>d.date==='2026-09-15').macd");
run("state.start='2026-09-01'");
assert.equal(run("macd('pp').find(d=>d.date==='2026-09-15').macd"), baseline);
assert.equal(run('getNews().length'), 3);
run("state.material='eva'");
assert.equal(run('getNews().length'), 3);
for (const page of ['flow', 'setting', 'a1', 'a2', 'b', 'c']) {
  context.location.hash = '#' + page;
  run('render()');
  assert.ok(app.innerHTML.length > 500);
  assert.ok(!/NaN|Infinity|undefined/.test(app.innerHTML), page);
}
assert.equal(navItems[0].hash, '#flow');
context.location.hash = ''; onHashChange();
assert.ok(app.innerHTML.includes('전체 구매 분석 플로우'));
assert.equal(navItems[0].current, true);
const flowA1 = app.innerHTML.match(/href="#a1" aria-label="a-1 [^"]+"/);
assert.ok(flowA1, 'Flow a-1 must link to its own menu route');
const previousMaterial = run('state.material');
context.location.hash = '#a1'; onHashChange();
assert.ok(app.innerHTML.includes('시장가와 실제 구매 이력 비교'));
assert.equal(navItems.find(item => item.hash === '#a1').current, true);
assert.equal(navItems[0].current, false);
assert.equal(run('state.material'), previousMaterial);
run("state.start='2026-06-01';state.end='2026-06-30'");
assert.equal(run('getNews().length'), 0);
context.location.hash = '#b'; run('render()');
assert.ok(app.innerHTML.includes('해당 기간의 뉴스가 없습니다'));
run("state.start='2026-09-30';state.end='2026-09-30'");
run('render()');
assert.ok(app.innerHTML.includes('2일 이상의 기간'));
assert.ok(!/NaN|Infinity|undefined/.test(app.innerHTML));
console.log('PASS: 6 screens, flow entry and a-1 navigation, active sidebar, retained filters, empty states, quantity sums and MACD consistency.');
