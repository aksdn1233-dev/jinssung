"""계산 엔진 전수 검사 — 1900-01-01 ~ 오늘 × 시간 선택지 14개.

    python3 tests/test_calc_full.py            # 전체 (약 65만 건)
    python3 tests/test_calc_full.py 1986 1990  # 연도 구간만

src/tpl.html 의 엔진(jdn·sunLon·saju·red)을 그대로 뽑아 node 로 돌리고,
엔진과 독립된 기준값과 비교한다.
- 년주·월주: ephem(VSOP87) 태양 시황경으로 절기(315°+30°k)를 다시 계산
- 일주: 파이썬 date.toordinal (2000-01-01 = 戊午)
- 시주: 오서둔(甲己日→甲子時…), 야자시는 다음 날 일간 기준
- 수비학 red(): 자릿수 합 축약, 11·22·33 유지

절기 경계에서 기준값과 엔진이 0.02°(약 29분) 이내로 갈리는 건 저정밀식 한계라
'경계' 로만 세고 오류에서 뺀다. 나머지 불일치는 전부 errors.
의존: node, `pip install ephem`
"""
import datetime as dt
import json
import math
import os
import subprocess
import sys

import ephem

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, 'src', 'tpl.html')

# tpl.html TIMES 와 같은 순서: (지지, 엔진에 넘기는 시각)
TIMES = [(-1, None), (0, 0.75)] + [(b, b * 2 + 0.5) for b in range(1, 12)] + [(0, 23.75)]
EDGE = 0.02
# 오서둔: 일간 → 子時 천간 (甲己→甲, 乙庚→丙, 丙辛→戊, 丁壬→庚, 戊癸→壬)
ZI_STEM = {0: 0, 5: 0, 1: 2, 6: 2, 2: 4, 7: 4, 3: 6, 8: 6, 4: 8, 9: 8}


def engine_js():
    s = open(TPL, encoding='utf-8').read()
    a = s.index("const ST='")
    b = s.index('function red(')
    b = s.index('\n', b)
    return s[a:b]


NODE = r'''
%s
const [Y0,Y1,TIMES]=[%d,%d,%s];
const out=[];
for(let t=Date.UTC(Y0,0,1);;t+=86400000){
 const D=new Date(t),y=D.getUTCFullYear(),m=D.getUTCMonth()+1,d=D.getUTCDate();
 if(y>Y1||t>Date.now())break;
 const row=[];
 for(const [hb,hm] of TIMES){const P=saju(y,m,d,hb,hm);row.push(P.map(p=>p[0]*12+p[1]).join(','))}
 out.push(row.join(' '));
}
process.stdout.write(out.join('\n'));
const reds=[];for(let n=1;n<=80;n++)reds.push([red(n,true),red(n,false)]);
process.stderr.write(JSON.stringify(reds));
'''


def sun_lon(y, m, d, hm):
    """KST 시각의 태양 시황경(도)."""
    h = 12 if hm is None else hm
    t = dt.datetime(y, m, d) + dt.timedelta(hours=h - 9)
    s = ephem.Sun(ephem.Date(t))
    ecl = ephem.Ecliptic(ephem.Equatorial(s.g_ra, s.g_dec, epoch=ephem.Date(t)))
    return math.degrees(ecl.lon) % 360


def red_ref(n, keep):
    while n > 9 and not (keep and n in (11, 22, 33)):
        n = sum(map(int, str(n)))
    return n


def main():
    y0 = int(sys.argv[1]) if len(sys.argv) > 1 else 1900
    y1 = int(sys.argv[2]) if len(sys.argv) > 2 else dt.date.today().year
    js = NODE % (engine_js(), y0, y1, json.dumps(TIMES))
    p = subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True)
    rows = p.stdout.split('\n')
    errors, edges, total = [], 0, 0

    for n, (r, nr) in enumerate(json.loads(p.stderr), 1):
        if [r, nr] != [red_ref(n, True), red_ref(n, False)]:
            errors.append(('red', n, r, nr))

    base = dt.date(2000, 1, 1).toordinal() - 54  # 戊午 = 60갑자 54번
    day = dt.date(y0, 1, 1)
    for row in rows:
        y, m, d = day.year, day.month, day.day
        di = (day.toordinal() - base) % 60
        for (hb, hm), got in zip(TIMES, row.split(' ')):
            total += 1
            P = [int(x) for x in got.split(',')]
            P = [(v // 12, v % 12) for v in P]
            want_len = 3 if hb < 0 else 4
            bad = []
            if len(P) != want_len or any(s % 2 != b % 2 for s, b in P):
                bad.append('구조')
            lon = sun_lon(y, m, d, hm)
            sy = y - 1 if (m <= 2 and 270 <= lon < 315) else y
            yi = (sy - 4) % 60
            mi = int(((lon - 315) % 360) // 30)
            ms = ((yi % 10) % 5 * 2 + 2 + mi) % 10
            exp = [(yi % 10, yi % 12), (ms, (mi + 2) % 12), (di % 10, di % 12)]
            if hb >= 0:
                hs = (di + 1) % 10 if hm >= 23.5 else di % 10
                exp.append(((ZI_STEM[hs] + hb) % 10, hb))
            if P[2:] != exp[2:]:
                bad.append('일주/시주')
            if P[:2] != exp[:2]:
                off = abs((lon - 315) % 30)
                if min(off, 30 - off) < EDGE:
                    edges += 1
                else:
                    bad.append('년주/월주')
            if bad:
                errors.append((str(day), hb, hm, bad, got))
        day += dt.timedelta(days=1)

    print(json.dumps({'range': [y0, y1], 'checked': total, 'edge_skipped': edges,
                      'errors': len(errors), 'sample': errors[:10]}, ensure_ascii=False, default=str))
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
