"""빌드: src/ + assets/ → dist/

    python3 build.py

결과
  dist/wolsik-saju.html      월식사주(서월) 사이트
  dist/heukwol-saju.html     흑월관(흑월) 사이트  ← 확정 캐릭터
  dist/heukwol-reports.html  흑월관 결과 리포트 (무료 / 기본 39,000 / 심화 79,000) + 입력 패널
  dist/img/                  전생 36종(past/01~36.jpg) · 배우자 10종(spouse/{오행}{f|m}.jpg)
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))


def P(*a):
    return os.path.join(ROOT, *a)


ns = {}
exec(open(P('src', 'characters.py'), encoding='utf-8').read(), ns)
CH = ns['CH']
IM = json.load(open(P('assets', 'images.json')))
KEY = {'wolsik-saju.html': 'wolsik', 'heukwol-saju.html': 'heukwol'}

tpl = open(P('src', 'tpl.html'), encoding='utf-8').read()
paid = open(P('src', 'paid.js'), encoding='utf-8').read()
os.makedirs(P('dist'), exist_ok=True)
# 전생 36종 · 배우자 10종 이미지 (리포트에서 img/... 상대경로로 참조)
shutil.copytree(P('assets', 'img'), P('dist', 'img'), dirs_exist_ok=True)

for c in CH:
    c = dict(c)
    out = c.pop('out')
    c.pop('src', None)
    k = KEY[out]
    if k == 'heukwol':
        c['imgs'] = IM['heukwol']
        c['img'] = IM['heukwol']['land']
    else:
        c['img'] = IM[k]
    cfg = json.dumps(c, ensure_ascii=False)
    html = tpl.replace('__CFG__', cfg).replace('__TITLE__', c['title']).replace('__OGDESC__', c['og'])
    open(P('dist', out), 'w', encoding='utf-8').write(html)
    print('built', out, len(html))
    if k == 'heukwol':
        rep = (tpl.replace('__CFG__', cfg)
               .replace('__TITLE__', '흑월관 결과 리포트 (무료 / 기본 / 심화)')
               .replace('__OGDESC__', '흑월관 결과 리포트')
               .replace('</body>', paid + '</body>'))
        open(P('dist', 'heukwol-reports.html'), 'w', encoding='utf-8').write(rep)
        print('built heukwol-reports.html', len(rep))
