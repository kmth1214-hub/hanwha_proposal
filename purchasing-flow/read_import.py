from html.parser import HTMLParser
from pathlib import Path
out=Path(__file__).parent/'imported-v02'
out.mkdir(exist_ok=True)
class Reader(HTMLParser):
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='iframe' and 'data-document' in a:
            (out/(a['id']+'.html')).write_text(a['data-document'],encoding='utf-8')
Reader().feed(Path(r'C:\Users\김태화\Downloads\hanwha_ai_purchase_integrated_v0.2 (2).html').read_text(encoding='utf-8'))
print('Extracted:', ', '.join(f.name for f in out.iterdir()))
