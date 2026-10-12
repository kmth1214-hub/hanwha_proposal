const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/한화_통합구매분석_v4.html','utf8');
assert.ok(!/<script[^>]+src=|<link[^>]+href=|<iframe|fetch\(/i.test(html),'Standalone asset contract');
const app={innerHTML:''},storage={};let click;
const navItems=[...html.matchAll(/<a href="#([a-z0-9]+)"><span>/g)].map(m=>({hash:'#'+m[1],active:false,current:false,classList:{toggle(_n,v){this.owner.active=v}},setAttribute(){this.current=true},removeAttribute(){this.current=false}}));navItems.forEach(a=>a.classList.owner=a);
const c=vm.createContext({document:{getElementById:id=>id==='app'?app:null,querySelectorAll:s=>s==='nav a'?navItems:[],addEventListener:(name,fn)=>{if(name==='click')click=fn}},location:{hash:''},localStorage:{getItem:k=>storage[k]||null,setItem:(k,v)=>storage[k]=v},window:{addEventListener:()=>{},scrollTo:()=>{}}});
vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],c);
const run=x=>vm.runInContext(x,c);
assert.ok(app.innerHTML.includes('전체 구매 의사결정 플로우'));
assert.equal(navItems.length,10);
function go(route){click({target:{closest:()=>({getAttribute:()=> '#'+route})},preventDefault:()=>{}});assert.ok(app.innerHTML.length>300);assert.equal(navItems.find(n=>n.hash==='#'+route).current,true);assert.ok(!/NaN|Infinity|undefined/.test(app.innerHTML),route)}
for(const route of run('V4_ROUTES'))go(route);
for(const target of ['pp','glassmat','polyester']){run(`selectTarget('strong','${target}');state.material='${target}'`);for(const route of run('V4_ROUTES'))go(route)}
run("selectTarget('strong','pp');state.material='pp';currentRecipe().rows=[{key:'ep',name:'',ratio:100}];draftCost().prices[rawName(currentRecipe().rows[0])]=1;draftCost().fx=1000;draftCost().overhead=100000;draftCost().actual=1200000");
assert.equal(run('costCalc().target'),1100000);
assert.ok(Math.abs(run('costCalc().gap')-9.090909090909092)<1e-9);
assert.equal(run('recordTarget()'),true);
assert.ok(storage['purchase-v4-costs']);
run('scenarioDraft().delta=-10;scenarioDraft().fx=1000;scenarioDraft().qty=100;scenarioDraft().split=50');
assert.equal(run('scenarioResult(latestTarget(),scenarioDraft()).future'),1000000);
assert.equal(run('scenarioResult(latestTarget(),scenarioDraft()).total'),105000000);
assert.equal(run('scenarioResult(latestTarget(),scenarioDraft()).diff'),-5000000);
assert.equal(run('scenarioResult(latestTarget(),scenarioDraft()).sensitivity'),450000);
run('scenarioDraft().split=100');assert.equal(run('scenarioResult(latestTarget(),scenarioDraft()).diff'),0);assert.equal(run('scenarioResult(latestTarget(),scenarioDraft()).sensitivity'),0);
go('c');assert.ok(app.innerHTML.includes('연결된 계산'));
run('draftCost().prices[rawName(currentRecipe().rows[0])]=0;draftCost().overhead=0');go('target');assert.equal(run('costCalc().gap'),null);assert.equal(run('recordTarget()'),false);
for(const mode of ['index','absolute'])for(const lag of [0,2,4,6]){run(`market.mode='${mode}';market.healthLag=${lag}`);go('health')}
for(const lag of [0,30,42,60]){run(`market.lag=${lag}`);go('spread')}
run("market.issue='';market.query='';state.start='2026-09-01';state.end='2026-09-30'");assert.equal(run('importedNews().length'),1);
run("state.material='glassmat'");assert.equal(run('importedNews().length'),0);
console.log('PASS: 10 menu routes × 3 materials, active navigation, standalone assets, blend-to-target-to-scenario calculation, history persistence, lag modes and unmapped-data empty states.');
