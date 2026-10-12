const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const h=fs.readFileSync(__dirname+'/고객공유_v3/index.html','utf8');
assert.ok(!/<script[^>]+src=|<link[^>]+href=|fetch\(/.test(h));
let click;
const app={innerHTML:''};
const errorBox={style:{},textContent:''};
const c=vm.createContext({document:{getElementById:id=>id==='app'?app:id==='runtimeError'?errorBox:null,querySelectorAll:()=>[],addEventListener:(type,fn)=>{if(type==='click')click=fn}},location:{hash:''},localStorage:{getItem:()=>{throw Error('blocked')},setItem:()=>{throw Error('blocked')}},window:{addEventListener:()=>{},scrollTo:()=>{}}});
vm.runInContext(h.match(/<script>([\s\S]*?)<\/script>/)[1],c);
assert.ok(app.innerHTML.includes('원材料')===false);
assert.ok(app.innerHTML.includes('원재료를 만드는 원료 배합 설정'));
for(const [hash,text] of [['#flow','전체 구매 분석 플로우'],['#a1','시장가와 실제 구매 이력 비교'],['#a2','환율 변화와 구매 행동 확인'],['#b','뉴스와 가격 신호'],['#c','구매 시나리오 검토'],['#setting','원재료를 만드는 원료 배합 설정']]){
 click({target:{closest:()=>({getAttribute:()=>hash})},preventDefault:()=>{}});
 assert.ok(app.innerHTML.includes(text),hash);
 assert.equal(c.location.hash,hash);
}
console.log('PASS: offline assets, menu click routing across all 6 pages, startup with browser storage blocked.');
