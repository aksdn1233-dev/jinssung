# jinssung — 캐릭터 사주 사이트 (흑월관 · 월식사주)

작업 전에 `HANDOFF.md`(원칙·계산 규칙)와 `CLAUDE.md`(작업 규칙)를 먼저 읽으세요.

```bash
python3 build.py                                                   # src + assets → dist
python3 tests/test_calc_full.py                                    # 계산 엔진 전수 검사
for k in 0 1 2 3 4 5; do python3 tests/test_render.py $k 6; done   # 리포트 렌더 검사
```

결과물은 `dist/` — `heukwol-reports.html`(무료/기본/심화 리포트), `heukwol-saju.html`, `wolsik-saju.html`, 정적 시안 `character-36-types.html`, `ssangwol-duo.html`.
확인·지원이 필요한 항목은 `docs/pending.md`.
