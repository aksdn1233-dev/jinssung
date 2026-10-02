"""결과 리포트 렌더링 검사 (playwright · chromium).

    python3 tests/test_render.py K N    # N개로 나눈 묶음 중 K번째 (0부터)
    for k in 0 1 2 3 4 5; do python3 tests/test_render.py $k 6; done

dist/heukwol-reports.html 을 열고 입력 패널 값을 바꿔 renderAll() 을 돌린다.
대상: 1900-01-01 부터 오늘까지 7일 간격 전원 + 경계일(입춘 전후 2/3~5, 1/1, 12/31, 2/29, 오늘).
시간·성별·성격유형은 날짜 순번으로 돌려가며 고른다 (난수 없음).

실패 조건
- 페이지 JS 오류
- 리포트 본문에 undefined / NaN / null / [object 노출
- 탭 3개(무료·기본·심화) 또는 챕터가 비어 있음
- 📐 근거 줄이 기준 입력보다 적음
- 전생·배우자 이미지(dist/img/...)가 없거나 파일이 빠짐
- 같은 입력을 두 번 계산했을 때 결과가 다름 (20건마다 1번)
선행: python3 build.py · pip install playwright (버전이 안 맞으면 CHROMIUM_PATH 로 chromium 지정)
"""
import datetime as dt
import json
import os
import sys

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'dist', 'heukwol-reports.html')
MBTI = ['모름', 'ENTP', 'ISFJ', 'INTJ', 'ESFP', 'INFP', 'ESTJ', 'ISTP', 'ENFJ']
BAD = ['undefined', 'NaN', 'null', '[object']


def cases():
    today = dt.date.today()
    d, out = dt.date(1900, 1, 1), []
    while d <= today:
        out.append(d)
        d += dt.timedelta(days=7)
    edge = set()
    for y in range(1900, today.year + 1):
        for md in [(1, 1), (2, 3), (2, 4), (2, 5), (12, 31), (2, 29)]:
            try:
                e = dt.date(y, *md)
            except ValueError:
                continue
            if e <= today:
                edge.add(e)
    edge.add(today)
    return out, sorted(edge - set(out))


SNAP = '''() => {
  const t = document.getElementById('pages');
  return {text: t.textContent, html: t.innerHTML.length,
          tabs: document.querySelectorAll('.tab').length,
          free: document.querySelectorAll('#freeBox .page').length,
          ch: document.querySelectorAll('section.ch2').length,
          why: (t.textContent.match(/📐 근거/g) || []).length,
          imgs: [...document.querySelectorAll('img[src^="img/"]')].map(i => i.getAttribute('src'))};
}'''


def run(page, i, day):
    page.evaluate('''([bd, tm, sx, mb]) => {
      document.getElementById('pBd').value = bd; document.getElementById('pTm').value = tm;
      document.getElementById('pSx').value = sx; document.getElementById('pMb').value = mb;
      document.getElementById('pNm').value = '검사'; renderAll();
    }''', [day.isoformat(), str(i % 14), '남' if i % 2 == 0 else '여', MBTI[i % len(MBTI)]])
    return page.evaluate(SNAP)


def main():
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    weekly, edge = cases()
    todo = [(i, d) for i, d in enumerate(weekly + edge) if i % n == k]
    failures, errs = [], []
    with sync_playwright() as p:
        exe = os.environ.get('CHROMIUM_PATH') or ('/opt/pw-browsers/chromium' if os.path.exists('/opt/pw-browsers/chromium') else None)
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = b.new_page()
        page.route('**/fonts.googleapis.com/**', lambda r: r.abort())
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto('file://' + PAGE)
        base = run(page, 10, dt.date(1986, 2, 12))   # 기준 입력: 유시·남
        min_why = base['why']
        for i, day in todo:
            errs.clear()
            s = run(page, i, day)
            bad = [w for w in BAD if w in s['text']]
            why_bad = s['why'] < min_why
            shape_bad = s['tabs'] != 3 or s['free'] != 5 or s['ch'] < 20
            missing = [x for x in s['imgs'] if not os.path.exists(os.path.join(ROOT, 'dist', x))]
            if len(s['imgs']) < 2 or missing:
                bad.append('이미지 누락 ' + ','.join(missing or ['전생/배우자']))
            if i % 20 == 0:
                again = run(page, i, day)
                if again['text'] != s['text']:
                    bad.append('결과가 매번 다름')
            if errs or bad or why_bad or shape_bad:
                failures.append({'date': str(day), 'i': i, 'js': errs[:2], 'text': bad,
                                 'why': s['why'], 'tabs': s['tabs'], 'free': s['free'], 'ch': s['ch']})
        b.close()
    print(json.dumps({'shard': f'{k}/{n}', 'people': len(todo),
                      'weekly': sum(1 for i, _ in todo if i < len(weekly)),
                      'edge': sum(1 for i, _ in todo if i >= len(weekly)),
                      'min_why': min_why, 'failures': failures[:20], 'n_fail': len(failures)},
                     ensure_ascii=False))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
