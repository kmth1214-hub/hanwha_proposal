const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/원가구조_원료구성비_v3.html','utf8');
const app={innerHTML:''};
const c=vm.createContext({document:{getElementById:id=>id==='app'?app:null,querySelectorAll:()=>[]},location:{hash:''},localStorage:{getItem:()=>null,setItem:()=>{}},window:{addEventListener:()=>{},scrollTo:()=>{}}});
vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],c);
const run=x=>vm.runInContext(x,c);
assert.equal(run('rawState.target'),'pp');
assert.equal(run('costTotal()'),100);
assert.ok(app.innerHTML.includes('01 원가구조'));
assert.ok(app.innerHTML.includes('02 원재료的構成')===false);
assert.ok(app.innerHTML.includes('PP · 구성 원료 시장가 추이'));
run("selectAnalysis('glassmat',true);selectAnalysis('polyester',true)");assert.equal(run('screenState.analysis.length'),2);
run('render()');assert.ok(app.innerHTML.includes('유리섬유 매트 · 구성 원료 시장가 추이'));
run("selectAnalysis('pp',false);selectAnalysis('polyester',true);render()");assert.ok(app.innerHTML.includes('불포화 polyester 수지 · 구성 원료 시장가 추이'));
run("selectAnalysis('glassmat',false);selectAnalysis('polyester',false);render()");assert.ok(app.innerHTML.includes('오른쪽에서 분석할 원재료'));
assert.equal(run("demoIndex('test')[0].value"),100);
assert.ok(run("demoIndex('test').every(x=>Number.isFinite(x.value))"));
run('costRows()[0].ratio=40');assert.equal(run('costTotal()'),90);
run("selectTarget('smc','pp')");assert.equal(run('costTotal()'),100);
run("selectTarget('strong','pp')");assert.equal(run('costTotal()'),90);
for(const p of run('Object.keys(productCatalog)')){run(`selectTarget('${p}','pp');render()`);assert.ok(!/NaN|Infinity|undefined/.test(app.innerHTML),p)}
for(const page of ['flow','a1','a2','b','c']){c.location.hash='#'+page;run('render()');assert.ok(app.innerHTML.length>300)}
console.log('PASS: startup, retained business/products, independent cost/composition shares, product-scoped cost drafts, max 2 analysis targets, chart switching and all routes.');
