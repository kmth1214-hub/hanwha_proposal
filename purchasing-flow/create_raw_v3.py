from pathlib import Path

root = Path(__file__).parent
html = (root / '원료구성비설정_v2.html').read_text(encoding='utf-8')
html = html.replace('purchasing-flow-settings-v2-analysis', 'purchasing-flow-raw-v3-analysis')
html = html.replace('원료·구성비 설정 v2', '원료 배합 설정 v3')
html = html.replace('<span>01</span>원료·구성비 설정', '<span>01</span>원료 배합 설정')
start = html.index('const ingredientCatalog=')
end = html.index('function cPage()', start)
code = r'''
const rawCatalog={
 ep:'Ethylene propylene copolymer (에틸렌 프로필렌 공중합체)',
 glass:'유리',coupling:'커플링제 (Coupling Agent)',filmforming:'피막형성제 (Film-forming Agent)',polymer:'고분자 수지 / 에멀전 (Polymer Resin / Emulsion)',
 polypropylene:'Polypropylene (폴리프로필렌)',peba:'폴리에테르 블록 아미드 (PEBA)',ester:'폴리에틸렌 에스테르 공중합체',peo:'폴리에틸렌 옥사이드 (PEO) 기반 특수 공중합체',
 maleic:'무수말레산',fumaric:'푸마르산',phthalic:'무수프탈산',isophthalic:'이소프탈산',pg:'프로필렌 글리콜 (PG)',eg:'에틸렌 글리콜 (EG)',npg:'네오펜틸 글리콜 (NPG)',sm:'스티렌 모노머 (SM)',
 gcc:'중질 탄산칼슘 (GCC)',stearic:'스테아르산 등 지방산류 (표면 처리제)',
 alkali:'무알칼리 유리',silane:'실란 커플링제',emulsion:'폴리우레탄/폴리에스테르 에멀전 (피막형성제)',lubricant:'윤활제 및 대전방지제',custom:'직접 입력'
};
const targetCatalog={
 pp:{name:'PP',raws:['ep'],note:'참고 표에 기재된 구성 원료: Ethylene propylene copolymer'},
 glassmat:{name:'유리섬유 매트',raws:['glass','coupling','filmforming','polymer']},
 epp:{name:'PP 수지',raws:['polypropylene'],note:'참고 표 2의 BuffLite 연결 항목에는 SuperLite(LWRT)로 적혀 있어, 표 1의 PP 수지와 표 2의 Polypropylene을 함께 참고했습니다.'},
 antistatic:{name:'대전방지제',raws:['peba','ester','peo']},
 polyester:{name:'불포화 polyester 수지',raws:['maleic','fumaric','phthalic','isophthalic','pg','eg','npg','sm']},
 filler:{name:'탄산칼슘 (충진제)',raws:['gcc','stearic']},
 chopped:{name:'유리섬유 (Glass chopped strand)',raws:['alkali','silane','emulsion','lubricant']},
 catalyst:{name:'촉매',raws:[]},release:{name:'이형제',raws:[]},
 slurry:{name:'Resin/Glass Slurry',raws:[]},scrim:{name:'Scrim',raws:[]},film:{name:'Film',raws:[]},
 pvc:{name:'PVC (가소화)',raws:[]},tpo:{name:'TPO',raws:[]},tpu:{name:'TPU',raws:[]},bio:{name:'바이오 및 리사이클 TPO',raws:[]}
};
const productCatalog={
 strong:{name:'StrongLite (GMT)',business:'자동차 경량복합소재',targets:['pp','glassmat']},
 buff:{name:'BuffLite (EPP)',business:'자동차 경량복합소재',targets:['epp','antistatic']},
 super:{name:'SuperLite (LWRT)',business:'자동차 경량복합소재',targets:['slurry','scrim','film']},
 smc:{name:'SMC',business:'자동차 경량복합소재',targets:['polyester','filler','chopped','catalyst','release']},
 pvc:{name:'IntermLite (PVC)',business:'자동차 내장재',targets:['pvc']},
 tpo:{name:'IntermLite (TPO)',business:'자동차 내장재',targets:['tpo']},
 tpu:{name:'IntermLite (TPU)',business:'자동차 내장재',targets:['tpu']},
 bio:{name:'IntermLite (Bio/Re)',business:'자동차 내장재',targets:['bio']}
};
const availableTargets=['pp','glassmat','polyester'];
Object.values(productCatalog).forEach(p=>p.targets=[...availableTargets]);
function defaultRecipe(target){let keys=targetCatalog[target].raws.slice(0,2);if(!keys.length)keys=['custom'];return {amount:1,rows:keys.map(key=>({key,name:'',ratio:keys.length===1&&key!=='custom'?100:0}))}}
let rawState={product:'strong',target:'glassmat',recipes:{}};
function recipeKey(){return rawState.product+':'+rawState.target}
function currentRecipe(){return rawState.recipes[recipeKey()]||(rawState.recipes[recipeKey()]=defaultRecipe(rawState.target))}
function recipeIsSafe(r){return r&&Number.isFinite(r.amount)&&r.amount>0&&Array.isArray(r.rows)&&r.rows.length>=1&&r.rows.length<=2&&r.rows.every(x=>Object.hasOwn(rawCatalog,x.key)&&typeof x.name==='string'&&Number.isFinite(x.ratio)&&x.ratio>=0&&x.ratio<=100)}
try{const saved=JSON.parse(localStorage.getItem('purchasing-raw-composition-v3')||'null');if(saved&&Object.hasOwn(productCatalog,saved.product)&&productCatalog[saved.product].targets.includes(saved.target)&&saved.recipes&&typeof saved.recipes==='object'&&!Array.isArray(saved.recipes)){let recipes={};for(let [k,r]of Object.entries(saved.recipes)){let [p,t]=k.split(':');if(Object.hasOwn(productCatalog,p)&&productCatalog[p].targets.includes(t)&&recipeIsSafe(r))recipes[k]=r}rawState={product:saved.product,target:saved.target,recipes}}}catch(e){}
function escapeText(v){return String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function rawName(row){return row.key==='custom'?row.name.trim():rawCatalog[row.key]}
function recipeCheck(){let r=currentRecipe(),total=r.rows.reduce((s,x)=>s+x.ratio,0);let names=r.rows.map(rawName),duplicate=new Set(names).size!==names.length;let issue=!r.rows.every(x=>rawName(x))?'직접 입력 원료의 이름을 입력하세요.':duplicate?'같은 원료를 중복 설정할 수 없습니다.':!r.rows.every(x=>Number.isFinite(x.ratio)&&x.ratio>0&&x.ratio<=100)?'선택한 각 원료의 비중을 0% 초과로 입력하세요.':Math.abs(total-100)>.000001?'원료 비중의 합계를 100%로 맞춰주세요.':!Number.isFinite(r.amount)||r.amount<=0?'기준 생산량을 0kg 초과로 입력하세요.':'';return {total,valid:!issue&&r.rows.length>=1&&r.rows.length<=2,issue}}
function addRaw(){let r=currentRecipe();if(r.rows.length===2)return;let key=targetCatalog[rawState.target].raws.find(k=>!r.rows.some(x=>x.key===k))||'custom';r.rows.push({key,name:'',ratio:0})}
function selectTarget(product,target){rawState.product=product;rawState.target=target;currentRecipe()}
function saveRecipe(){if(!recipeCheck().valid)return false;localStorage.setItem('purchasing-raw-composition-v3',JSON.stringify(rawState));return true}
function settingPage(){let p=productCatalog[rawState.product],t=targetCatalog[rawState.target],r=currentRecipe(),check=recipeCheck();return heading('01 / V3','원재료를 만드는 원료 배합 설정','제품에 투입하는 원재료를 선택한 뒤, 그 원재료를 구성하는 원료의 비중을 설정합니다.')+`<section class="card"><div class="blend-selection"><label>사업 부문<select id="rawBusiness">${['자동차 경량복합소재','자동차 내장재'].map(b=>`<option ${b===p.business?'selected':''}>${b}</option>`).join('')}</select></label><label>주요 제품<select id="rawProduct">${Object.entries(productCatalog).filter(([k,x])=>x.business===p.business).map(([k,x])=>`<option value="${k}" ${k===rawState.product?'selected':''}>${x.name}</option>`).join('')}</select></label><label>만들 원재료<select id="rawTarget">${p.targets.map(k=>`<option value="${k}" ${k===rawState.target?'selected':''}>${targetCatalog[k].name}</option>`).join('')}</select></label><label>원재료 기준 생산량 (kg)<input id="rawAmount" type="number" min="0.000001" step="any" value="${r.amount}"></label></div><div class="explain"><strong>${p.name} → ${t.name} → 구성 원료 배합</strong><br>v2: 원재료가 제품에서 차지하는 비중 · v3: 구성 원료가 원재료에서 차지하는 비중</div><div class="blend-alert">원료명은 참고 표를 바탕으로 제공합니다. 원료별 배합 비중은 표에 없으므로 직접 입력하세요. 단일 원료의 초기 비중 100%는 편집용 값입니다. ${t.raws.length>2?'참고 표에는 구성 원료가 '+t.raws.length+'개입니다. 이번 화면에서는 그중 최대 2개만 선택하는 단순화된 배합을 설정합니다.':''}${!t.raws.length?'이 원재료의 상세 구성 원료는 참고 표에 없으므로 원료명을 직접 입력하세요.':''}${t.note?'<br>'+t.note:''}</div></section><div class="blend-grid">${r.rows.map((row,i)=>`<section class="card"><div class="cardhead"><h2>구성 원료 ${i+1}</h2>${r.rows.length===2?`<button type="button" class="button" data-remove-raw="${i}">삭제</button>`:'<span class="tag">필수 원료</span>'}</div><div class="blend-fields"><label class="wide">원료 선택<select data-raw-row="${i}" data-raw-field="key">${[...new Set([...t.raws,'custom'])].map(k=>`<option value="${k}" ${k===row.key?'selected':''} ${k!=='custom'&&r.rows.some((x,j)=>j!==i&&x.key===k)?'disabled':''}>${rawCatalog[k]}</option>`).join('')}</select></label>${row.key==='custom'?`<label class="wide">원료명 직접 입력<input data-raw-row="${i}" data-raw-field="name" maxlength="120" value="${escapeText(row.name)}" placeholder="예: 강화용 유리"></label>`:''}<label class="wide">원재료 내 원료 비중 (%)<input type="number" min="0" max="100" step="any" data-raw-row="${i}" data-raw-field="ratio" value="${row.ratio}"></label></div><div class="explain">${check.valid?'기준 생산량에 필요한 원료량 <strong>'+fmt(r.amount*row.ratio/100,4)+' kg</strong>':'비중 합계 100%를 맞추면 필요 원료량을 표시합니다.'}</div><p class="small">${row.key==='custom'?'직접 입력 원료':'참고 표에 기재된 원료'} · 비중은 사용자 설정</p></section>`).join('')}${r.rows.length===1?'<button type="button" id="addRaw" class="add-material"><span>＋</span><strong>두 번째 원료 추가</strong><span>원재료 하나당 최대 2개 원료</span></button>':''}</div><div class="blend-summary"><section class="card"><div class="cardhead"><h2>원료 배합 비중</h2><span class="tag">${r.rows.length} / 2개</span></div><div class="ratio-bar">${r.rows.map((x,i)=>`<i style="width:${Math.min(100,Math.max(0,x.ratio))}%;background:${i?'#397eac':'#eb6d24'}"></i>`).join('')}</div>${r.rows.map(x=>`<p>${escapeText(rawName(x)||'원료명 미입력')} <strong>${fmt(x.ratio,2)}%</strong></p>`).join('')}<div class="status ${check.valid?'':'negative'}">합계 ${fmt(check.total,2)}% · ${check.valid?'저장 가능':check.issue}</div></section><section class="card"><h2>만들 원재료</h2><div class="blend-price">${t.name}</div><p>제품: ${p.name}</p><p>기준 생산량: <strong>${fmt(r.amount,4)} kg</strong></p><div class="explain">필요 원료량 = 기준 생산량 × 원료 비중 ÷ 100.<br>수율 손실·공정 조건은 반영하지 않은 배합량 계산입니다.</div></section></div><section class="card" style="margin-top:20px"><h2>원재료 배합 명세</h2><div class="tablewrap"><table><thead><tr><th>주요 제품</th><th>만들 원재료</th><th>구성 원료</th><th>원료 비중</th><th>필요 원료량</th></tr></thead><tbody>${r.rows.map(x=>`<tr><td>${p.name}</td><td>${t.name}</td><td>${escapeText(rawName(x)||'미입력')}</td><td>${fmt(x.ratio,2)}%</td><td>${check.valid?fmt(r.amount*x.ratio/100,4)+' kg':'비중 설정 필요'}</td></tr>`).join('')}</tbody></table></div></section><div class="blend-toolbar"><span id="rawSaveStatus" class="small" role="status">원재료별 입력값은 화면 이동 중 유지됩니다. ‘배합 저장’으로 다시 열 때도 유지하세요.</span><button type="button" id="saveRaw" class="button primary" ${check.valid?'':'disabled'}>배합 저장</button></div><div class="explain">현재 설정은 선택 원재료 내부의 원료 배합입니다. v2의 제품 내 원재료 비중이나 원재료 단가를 원료 비중·단가로 재사용하지 않습니다. a/b 화면은 기존 PP·EVA 예시 분석이며 이번 배합과는 아직 연결되지 않았습니다.</div>`+actions('flow','a1','전체 플로우','시장가·실적 비교')}
function bindBlend(){document.querySelectorAll('[data-raw-row]').forEach(el=>el.addEventListener('change',()=>{let row=currentRecipe().rows[Number(el.dataset.rawRow)],field=el.dataset.rawField;if(field==='key'){row.key=el.value;row.name=''}else if(field==='name')row.name=el.value;else{if(!el.checkValidity()){el.reportValidity();return}row.ratio=el.value===''?0:Number(el.value)}render()}));document.querySelectorAll('[data-remove-raw]').forEach(el=>el.addEventListener('click',()=>{let r=currentRecipe();if(r.rows.length===2)r.rows.splice(Number(el.dataset.removeRaw),1);render()}));let add=document.getElementById('addRaw');if(add)add.addEventListener('click',()=>{addRaw();render()});let business=document.getElementById('rawBusiness');if(business)business.addEventListener('change',()=>{let key=Object.keys(productCatalog).find(k=>productCatalog[k].business===business.value);selectTarget(key,productCatalog[key].targets[0]);render()});let product=document.getElementById('rawProduct');if(product)product.addEventListener('change',()=>{selectTarget(product.value,productCatalog[product.value].targets[0]);render()});let target=document.getElementById('rawTarget');if(target)target.addEventListener('change',()=>{selectTarget(rawState.product,target.value);render()});let amount=document.getElementById('rawAmount');if(amount)amount.addEventListener('change',()=>{if(!amount.value||!amount.checkValidity()){amount.reportValidity();return}currentRecipe().amount=Number(amount.value);render()});let save=document.getElementById('saveRaw');if(save)save.addEventListener('click',()=>{try{if(saveRecipe())document.getElementById('rawSaveStatus').textContent='원재료별 원료 배합을 저장했습니다.'}catch(e){document.getElementById('rawSaveStatus').textContent='브라우저 저장이 제한되어 저장하지 못했습니다.'}})}
'''
html = html[:start] + code + '\n' + html[end:]
html = html.replace("const materials={pp:{name:'PP',full:'PP (폴리프로필렌)',base:1040},eva:{name:'EVA',full:'EVA Resin',base:1490}};", "const materials={pp:{name:'PP',full:'PP',base:1040},glassmat:{name:'유리섬유 매트',full:'유리섬유 매트',base:1900},polyester:{name:'불포화 polyester 수지',full:'불포화 polyester 수지',base:3530}};")
html = html.replace('eva:1490+Math.sin(t/31+.8)*95+Math.cos(t/12)*20-t*.06', 'glassmat:1900+Math.sin(t/31+.8)*95+Math.cos(t/12)*20-t*.06,polyester:3530+Math.sin(t/25)*125+Math.cos(t/11)*30-t*.1')
html = html.replace('PP·EVA 예시 분석', 'PP·유리섬유 매트·불포화 polyester 수지 예시 분석')
html = html.replace('설정 단가·비중은 첨부 참고 표 기준입니다.', '원료명은 참고 표 기준 · 배합 비중은 사용자 입력입니다.')
html = html.replace("flowNode('01','원료 (S&P)','분석할 원료 선택','setting')", "flowNode('01','원료','원재료를 구성할 원료 선택','setting')")
html = html.replace("flowNode('02','구성비','한화 제공 구성비 설정','setting')", "flowNode('02','원료 비중','원재료 내 원료 배합 설정','setting')")
html = html.replace("flowNode('03','원재료','원료별 분석 기준 확인','setting')", "flowNode('03','원재료','선택 원료의 배합으로 구성','setting')")
(root / '원료배합설정_v3.html').write_text(html, encoding='utf-8')
print('V3 created successfully')
