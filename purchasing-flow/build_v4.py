from pathlib import Path
import re
from zipfile import ZipFile, ZIP_DEFLATED

root=Path(__file__).parent
html=(root/'고객공유_v3/index.html').read_text(encoding='utf-8')
def literal(file,name,outname):
    text=(root/'imported-v02'/file).read_text(encoding='utf-8')
    found=re.search(r'const\s+'+re.escape(name)+r'\s*=\s*(.*?);\s*\n',text,re.S)
    if not found: raise ValueError(name)
    return 'const '+outname+' = '+found.group(1)+';\n'
data=''.join([
    literal('frame-cost.html','SPREAD_DATASETS','IMPORTED_SPREAD'),
    literal('frame-cost.html','SPREAD_MONTHS','IMPORTED_MONTHS'),
    literal('frame-cost.html','LAG_SPREAD_ADJUSTMENT','IMPORTED_LAG_ADJUST'),
    literal('frame-news.html','NEWS_DATA','IMPORTED_NEWS'),
    literal('frame-health.html','OIL_CARD_DATA','IMPORTED_OIL'),
    literal('frame-health.html','indexedMacroLead','IMPORTED_MACRO'),
    literal('frame-health.html','indexedCostByLag','IMPORTED_LAG_COST'),
    literal('frame-health.html','absMacroOil','IMPORTED_ABS_OIL'),
    literal('frame-health.html','absPPCost','IMPORTED_ABS_COST')
])
js=(root/'v4.js').read_text(encoding='utf-8')
js=js.replace('v3에서 설정한 원료 비중', '설정한 원료 비중')
js=js.replace('IMPORTED_LAG_COST[market.lag]', 'IMPORTED_LAG_COST[market.healthLag]')
js=js.replace('<select id="v4Lag">${[0,30,42,60].map(k=>`<option value="${k}" ${market.lag===k?\'selected\':\'\'}>${k}일</option>`).join(\'\')}</select></label><span class="notice">시차값', '<select id="v4HealthLag">${[0,2,4,6].map(k=>`<option value="${k}" ${market.healthLag===k?\'selected\':\'\'}>${k}주</option>`).join(\'\')}</select></label><span class="notice">시차값')
js=js.replace("v4Oil:['oil',String]", "v4HealthLag:['healthLag',Number],v4Oil:['oil',String]")
js=js.replace('거시 복합지수 (첫 관측치 100)', '거시 복합지수 (기준 100)').replace('PP 구매원가 지수 (첫 관측치 100)', 'PP 구매원가 지수 (기준 100)')
js=js.replace('gap:valid&&Number.isFinite(d.actual)', 'gap:valid&&target>0&&Number.isFinite(d.actual)')
nav=[('flow','◎','전체 플로우'),('setting','01','원료 배합 설정'),('a1','a-1','시장가·실적 비교'),('a2','a-2','환율·경제지표'),('health','시장','마켓헬스'),('news','뉴스','관련 뉴스 상세'),('b','b','뉴스·MACD 분석'),('spread','원가','조달 스프레드'),('target','목표','목표원가 계산'),('c','c','구매 시뮬레이션')]
navhtml='<aside class="nav"><div class="nav-title">PURCHASING / V4</div><nav aria-label="통합 구매 분석 메뉴">'+''.join(f'<a href="#{key}"><span>{code}</span>{name}</a>' for key,code,name in nav)+'</nav></aside>'
html=re.sub(r'<aside class="nav">.*?</aside>',lambda _:navhtml,html,count=1,flags=re.S)
html=html.replace('원료 배합 설정 v3 | 한화첨단소재', '한화첨단소재 통합 구매 분석 v4')
html=html.replace('예시 데이터 · 화면 검토용','V4 통합 시안 · 예시 데이터')
html=html.replace('purchasing-flow-raw-v3-analysis','purchase-v4-analysis').replace('purchasing-raw-composition-v3','purchase-v4-composition')
html=html.replace('01 / V3','01 / V4').replace('v2: 원재료가 제품에서 차지하는 비중 · v3: 구성 원료가 원재료에서 차지하는 비중','현재 설정: 구성 원료가 원재료에서 차지하는 비중 · 배합 저장 후 목표원가 화면에 단가를 입력하세요.')
html=html.replace('v2의 제품 내 원재료 비중이나 원재료 단가를 원료 비중·단가로 재사용하지 않습니다.', '제품 내 원재료 비중과 원재료 내부 원료 비중은 구분합니다.')
html=html.replace('a/b 화면은 기존 PP·유리섬유 매트·불포화 polyester 수지 예시 분석이며 이번 배합과는 아직 연결되지 않았습니다.', '배합은 목표원가와 구매 시뮬레이션으로 연결됩니다. a/b 차트는 별도로 생성한 화면 검토용 시계열입니다.')
html=html.replace('flow|setting|a1|a2|b|c', 'flow|setting|a1|a2|health|news|b|spread|target|c')
html=html.replace("rows[i].date.slice(5)", "(/^\\d{4}-\\d{2}-\\d{2}$/.test(rows[i].date)?rows[i].date.slice(5):rows[i].date)")
css='''
.nav{overflow-y:auto}nav a{padding:10px 12px}.cost-row{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:center;border-top:1px solid var(--line);padding:18px 0}.cost-row input{width:100%;min-width:0}.preset-buttons{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}dialog{border:1px solid var(--line);border-radius:12px;padding:28px;width:min(760px,90vw);max-height:85vh;color:var(--ink);font:inherit}dialog::backdrop{background:#15273880}.small a,.explain a{color:var(--orange);text-decoration:underline}.metrics b{font-size:22px}@media(max-width:650px){.cost-row{grid-template-columns:1fr}.metrics b{font-size:19px}}
'''
html=html.replace('</style>',css+'</style>',1)
html=html.replace('<script>','<dialog id="newsDialog" aria-label="첨부 뉴스 상세"></dialog><script>',1)
html=html.replace('</script></body>',data+'\n'+js+'\n</script></body>')
html=html.replace('원料', '원료')
path=root/'한화_통합구매분석_v4.html'
path.write_text(html,encoding='utf-8')
share=root/'고객공유_v4'
share.mkdir(exist_ok=True)
(share/'index.html').write_text(html,encoding='utf-8')
(share/'실행안내.txt').write_text('''한화첨단소재 통합 구매 분석 v4

ZIP을 PC에 내려받아 압축을 푼 뒤 index.html을 Chrome 또는 Edge로 엽니다.
인터넷 연결 없이 동작하며 별도 설치가 필요하지 않습니다.
첨부 미리보기 대신 다운로드한 실제 파일을 여세요.

사용 순서
1. 전체 플로우에서 분석 화면으로 이동합니다.
2. 원료 배합 설정에서 원재료를 고르고 최대 2개 구성 원료의 비중을 합계 100%로 설정합니다.
3. 목표원가 계산에서 구성 원료 단가 USD/kg, 환율, 가공비 KRW/ton을 입력하고 계산 결과를 저장합니다.
4. 구매 시뮬레이션에서 같은 원재료의 저장 목표원가로 가격 변화·후속 환율·수량·즉시 구매 비중을 비교합니다.
5. 배합이나 단가를 바꾼 경우 목표원가를 다시 저장해야 시나리오에 새 값이 연결됩니다.

데이터 안내
원료명은 제공된 참고 표를 바탕으로 하며 구성 원료 비중은 사용자 입력입니다.
a-1/a-2/b 화면의 가격·환율·구매 이력·감정 분류는 생성된 가상 예시입니다.
마켓헬스·스프레드·관련 뉴스는 첨부 v0.2의 데모 스냅샷입니다.
PP 스냅샷은 PP로만 연결하며 EVA/M10을 다른 원재료로 바꿔 사용하지 않습니다.
마켓헬스 상단과 표는 첨부 PP 및 전체시장 고정 예시이며 선택 원재료별 실제 지표가 아닙니다.
조달 스프레드의 시차 보정은 첨부 고정 보정값이며 실제 날짜 정렬로 계산한 결과가 아닙니다.
뉴스의 출처명·번역문·해설은 검증한 원문이 없는 데모입니다.
계산은 산식과 가정을 비교하며 실제 예측·발주·주문 기능이 아닙니다.

저장은 이 브라우저/파일 위치에 보관됩니다. 다른 사람에게 입력값이 자동 공유되지 않습니다.
회사 보안 정책으로 HTML 실행이 차단된 경우 IT 담당자에게 확인하세요.
실행 오류가 나면 화면 위 오류 메시지와 브라우저 버전을 담당자에게 전달하세요.
''',encoding='utf-8-sig')
with ZipFile(root/'고객공유_v4.zip','w',ZIP_DEFLATED)as z:
    for name in ['index.html','실행안내.txt']:z.write(share/name,arcname=name)
print('Created v4 HTML and customer ZIP')
