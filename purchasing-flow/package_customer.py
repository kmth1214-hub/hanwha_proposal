from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).parent
out = root / '고객공유_v3'
out.mkdir(exist_ok=True)
html = (root / '원료배합설정_v3.html').read_text(encoding='utf-8')
html = html.replace('<main id="app"></main>', '<main id="app"><section class="card"><h1>원료 배합 설정</h1><p>화면을 불러오는 중입니다. 이 안내가 계속 보이면 JavaScript가 실행되지 않은 상태입니다.</p><p>파일을 PC에 내려받고 ZIP 압축을 푼 뒤, index.html을 Chrome 또는 Edge에서 열어주세요.</p><p>회사 보안 정책으로 HTML 실행이 차단된 경우 담당자에게 확인해주세요.</p></section></main>')
html = html.replace('<div class="workspace">', '<div id="runtimeError" role="alert" style="display:none;padding:16px;background:#fff0ee;color:#963d39"></div><div class="workspace">')
html = html.replace("'use strict';", """'use strict';
function hasOwnKey(obj,key){return Object.prototype.hasOwnProperty.call(obj,key)}
window.addEventListener('error',function(event){var box=document.getElementById('runtimeError');if(box){box.style.display='block';box.textContent='화면 실행 중 오류가 발생했습니다. 이 메시지를 담당자에게 전달해주세요: '+event.message;}});
""")
html = html.replace('Object.hasOwn(', 'hasOwnKey(')
html = html.replace('rows.at(-1)', 'rows[rows.length-1]')
html = html.replace("window.addEventListener('hashchange'", """document.addEventListener('click',function(event){var link=event.target.closest('nav a, .flow-node, .actions a');if(!link)return;var hash=link.getAttribute('href');if(!/^#(flow|setting|a1|a2|b|c)$/.test(hash))return;event.preventDefault();location.hash=hash;render();window.scrollTo(0,0);});
window.addEventListener('hashchange'""")
(out / 'index.html').write_text(html, encoding='utf-8')
readme = '''원료 배합 설정 v3 - 고객 실행 안내

1. ZIP 파일을 PC에 다운로드합니다.
2. ZIP 파일을 우클릭하여 "압축 풀기"를 실행합니다.
3. 압축을 푼 폴더의 index.html을 Chrome 또는 Edge로 엽니다.
   필요하면 파일 우클릭 → 연결 프로그램 → Microsoft Edge / Google Chrome.
4. 좌측 메뉴와 전체 플로우의 박스로 화면을 이동합니다.

인터넷 연결이나 별도 프로그램 설치 없이 실행하는 HTML 시안입니다.
메일/메신저/클라우드의 첨부 미리보기 대신 다운로드한 파일을 열어주세요.

원료 배합 설정
- 원재료: PP, 유리섬유 매트, 불포화 polyester 수지
- 원재료 하나당 최대 2개 구성 원료
- 원료 비중 합계 100% 및 기준 생산량 설정
- 배합 저장은 이 PC의 현재 브라우저에만 저장됩니다.
  다른 고객이나 다른 브라우저로 입력값이 자동 공유되지 않습니다.

메뉴가 움직이지 않으면
- 파일을 압축 폴더 밖으로 꺼냈는지 확인합니다.
- 받은 파일명이 index.html인지 확인합니다.
- 화면 상단에 오류 안내가 있으면 해당 문구를 담당자에게 전달합니다.
- 회사 보안 정책이 다운로드한 HTML/JavaScript를 차단할 수 있습니다.
  보안 설정을 임의로 해제하지 말고 회사 담당자에게 확인합니다.
- 담당자에게 브라우저 이름/버전, 화면 스크린샷, 오류 문구를 전달합니다.

데이터 안내
배합 비중은 사용자가 입력하는 값입니다.
시장가/SAP/환율/뉴스 차트는 가상 예시이며 실제 서비스에 연결하지 않았습니다.
화면 검토용이며 자동 구매 또는 발주 기능이 없습니다.
'''
(out / '실행안내.txt').write_text(readme, encoding='utf-8-sig')
with ZipFile(root / '고객공유_v3.zip', 'w', ZIP_DEFLATED) as z:
    for name in ['index.html', '실행안내.txt']:
        z.write(out / name, arcname=name)
print('Packaged: 고객공유_v3.zip (index.html + 실행안내.txt)')
