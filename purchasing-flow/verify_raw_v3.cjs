const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/원료배합설정_v3.html','utf8');
const app={innerHTML:''},storage={};
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
function make(){const c=vm.createContext({document:{querySelectorAll:()=>[],getElementById:id=>id==='app'?app:null},location:{hash:''},localStorage:{getItem:k=>storage[k]||null,setItem:(k,v)=>storage[k]=v},window:{addEventListener:()=>{},scrollTo:()=>{}}});vm.runInContext(script,c);return c}
let c=make(),run=x=>vm.runInContext(x,c);
assert.ok(app.innerHTML.includes('원재료를 만드는 원료 배합 설정'));
assert.equal(run('recipeCheck().valid'),false);
run('currentRecipe().rows[0].ratio=70;currentRecipe().rows[1].ratio=30;currentRecipe().amount=100');
assert.equal(run('recipeCheck().valid'),true);
run('render()');assert.ok(app.innerHTML.includes('70.0000 kg'));
run('addRaw()');assert.equal(run('currentRecipe().rows.length'),2);
assert.equal(run('saveRecipe()'),true);
c=make();assert.equal(run('currentRecipe().rows[0].ratio'),70);
run("selectTarget('strong','pp');selectTarget('strong','glassmat')");
assert.equal(run('currentRecipe().rows[0].ratio'),70);
run("currentRecipe().rows[1].key='glass'");assert.equal(run('recipeCheck().valid'),false);
run("selectTarget('strong','polyester');currentRecipe().rows=[{key:'custom',name:'',ratio:0}]");assert.equal(run('recipeCheck().valid'),false);
run("currentRecipe().rows[0].name='<test>';currentRecipe().rows[0].ratio=100;render()");
assert.equal(run('recipeCheck().valid'),true);assert.ok(app.innerHTML.includes('&lt;test&gt;'));
assert.ok(!app.innerHTML.includes('<test>'));
for(const p of run('Object.keys(productCatalog)')){for(const t of run(`productCatalog['${p}'].targets`)){run(`selectTarget('${p}','${t}');render()`);assert.ok(!/NaN|Infinity|undefined/.test(app.innerHTML));assert.ok(run('currentRecipe().rows.length')<=2)}}
console.log('PASS: product/material/raw hierarchy, max 2 raws, ratio validation, batch quantities, per-material persistence, escaping and all target presets.');
