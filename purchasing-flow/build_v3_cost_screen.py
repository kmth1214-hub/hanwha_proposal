from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).parent
html=(root/'원료배합설정_v3.html').read_text(encoding='utf-8')
html=html.replace("window.addEventListener('hashchange',()=>{render();window.scrollTo({top:0,behavior:'smooth'})});render();", "window.addEventListener('hashchange',()=>{render();window.scrollTo({top:0,behavior:'smooth'})});")
html=html.replace("let rawState={product:'strong',target:'glassmat',recipes:{}}", "let rawState={product:'strong',target:'pp',recipes:{}}")
html=html.replace('purchasing-raw-composition-v3','purchase-cost-composition-v3')
html=html.replace('purchasing-flow-raw-v3-analysis','purchase-cost-structure-v3-analysis')
html=html.replace('원료 배합 설정 v3 | 한화첨단소재','원가구조·원료 구성비 v3 | 한화첨단소재')
html=html.replace('<span>01</span>원료 배합 설정','<span>01</span>원가구조·원료 구성비')
css='''
.cost-composition-layout{display:grid;grid-template-columns:minmax(220px,.95fr) minmax(270px,1.15fr) minmax(210px,.9fr);gap:18px;margin-top:20px;align-items:start}.cost-composition-layout .card{padding:20px}.cost-model-table td{padding:15px 7px}.cost-model-table th{padding:12px 7px}.cost-model-table input{width:80px;min-width:0;text-align:right;padding:6px}.cost-model-table tfoot th{background:#f3f6f8}.composition-editor label input,.composition-editor label select{width:100%;min-width:0}.raw-composition-row{margin:18px 0;padding:15px 0;border-top:1px solid var(--line)}.raw-composition-row label{margin-top:10px}.raw-composition-row .button{padding:4px 9px;font-size:11px}.analysis-choice{display:flex;flex-direction:row;align-items:center;gap:12px;padding:15px 0;border-bottom:1px solid var(--line);font-size:14px;color:var(--ink);cursor:pointer}.analysis-choice input{min-width:0;width:18px;height:18px;accent-color:var(--orange)}.analysis-selector>label:last-of-type{margin-top:20px}.market-analysis-header{margin:35px 0 16px}.market-charts{display:grid;grid-template-columns:1fr 1fr;gap:22px}.market-chart{min-width:0}.market-chart h3{font-size:13px}.market-chart .cardhead{align-items:start}.cost-composition-layout h2{font-size:15px}.cost-composition-layout .cardhead{flex-wrap:wrap}@media(max-width:1250px){.cost-composition-layout{grid-template-columns:1fr 1fr}.analysis-selector{grid-column:1/-1}.analysis-choice{display:inline-flex;width:32%;vertical-align:top;padding-right:12px}.market-charts{grid-template-columns:1fr}}@media(max-width:850px){.cost-composition-layout{grid-template-columns:1fr}.analysis-selector{grid-column:auto}.analysis-choice{display:flex;width:100%}.cost-model-table input{width:75px}.cardhead{flex-wrap:wrap}}
'''
html=html.replace('</style>',css+'</style>',1)
html=html.replace('</script></body>',(root/'v3_cost_screen.js').read_text(encoding='utf-8')+'\n</script></body>')
html=html.replace("rows[i].date.slice(5)", "(/^\\d{4}-\\d{2}-\\d{2}$/.test(rows[i].date)?rows[i].date.slice(5):rows[i].date)")
html=html.replace('예시 데이터 · 화면 검토용','원가구조·구성비 시안 · 시장가 예시 지수')
path=root/'원가구조_원료구성비_v3.html'
path.write_text(html,encoding='utf-8')
share=root/'고객공유_v3_원가구조'
share.mkdir(exist_ok=True)
(share/'index.html').write_text(html,encoding='utf-8')
(share/'실행안내.txt').write_text('''원가구조·원료 구성비 v3
ZIP 압축을 풀고 index.html을 Chrome 또는 Edge에서 여세요.

1. 기존 사업 부문·제품을 선택합니다.
2. 제조원가 구조의 비용 비중을 설정합니다. 첨부 표의 50/13/14/10/8/5%가 초기값입니다.
3. PP 등 원재료의 구성 원료(최대 2개)와 배합 비중을 설정합니다.
4. 분석 대상 원재료를 최대 2개 선택하면 구성 원료별 시장가 추이 차트가 표시됩니다.
5. 원가구조와 현재 편집하는 원재료 구성비 합계가 각각 100%이면 저장할 수 있습니다.

원가구조의 비용 비중과 구성 원료의 배합 비중은 별개입니다.
PP 100% 등 초기 배합 값은 검증한 제조 배합이 아닙니다.
시장가 차트는 가상 예시 지수(첫 날짜 100)이며 실제 가격/예측 결과가 아닙니다.
실제 시장가·출처·통화·단위를 연결하면 이 영역을 교체할 수 있습니다.
저장값은 이 PC의 브라우저에만 보관되며 고객 간 자동 공유되지 않습니다.
''',encoding='utf-8-sig')
with ZipFile(root/'고객공유_v3_원가구조.zip','w',ZIP_DEFLATED)as z:
    for name in ['index.html','실행안내.txt']:z.write(share/name,arcname=name)
print('Created revised v3 screen and sharing ZIP; original v3 and v4 preserved.')
