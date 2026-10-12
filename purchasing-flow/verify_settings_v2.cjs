const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/원료구성비설정_v2.html','utf8');
const app={innerHTML:''};
const context=vm.createContext({document:{querySelectorAll:()=>[],getElementById:id=>id==='app'?app:null},location:{hash:''},localStorage:{getItem:()=>null,setItem:()=>{}},window:{addEventListener:()=>{},scrollTo:()=>{}}});
vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
const run=x=>vm.runInContext(x,context);
assert.ok(app.innerHTML.includes('원료와 구성비 설정'));
assert.equal(run('blendCheck().valid'),true);
assert.ok(Math.abs(run('blendCheck().total')-1.708)<1e-10);
run("blend=defaultBlend('buff')");
assert.ok(Math.abs(run('blendCheck().total')-1.6855)<1e-10);
run("blend=defaultBlend('pvc');addBlendRow();addBlendRow()");
assert.equal(run('blend.rows.length'),2);
assert.equal(run('blendCheck().valid'),false);
run("blend=defaultBlend('strong');blend.rows[0].price=1580;blend.rows[0].unit='mt'");
assert.ok(Math.abs(run('blendCheck().total')-1.708)<1e-10);
run("blend.rows[1].key='pp'");
assert.equal(run('blendCheck().valid'),false);
run("blend=defaultBlend('smc')");
assert.equal(run('blendCheck().ratio'),70);
assert.equal(run('blendCheck().valid'),false);
run("blend=defaultBlend('super')");
assert.equal(run('blendCheck().valid'),false);
for(const k of run('Object.keys(productCatalog)')){run(`blend=defaultBlend('${k}');render()`);assert.ok(!/NaN|Infinity|undefined/.test(app.innerHTML),k);assert.ok(run('blend.rows.length')<=2,k)}
for(const hash of ['#flow','#a1','#a2','#b','#c']){context.location.hash=hash;run('render()');assert.ok(app.innerHTML.length>500)}
console.log('PASS: product presets, max 2 ingredients, ratio/duplicate/missing-price validation, unit conversion, weighted cost and all routes.');
