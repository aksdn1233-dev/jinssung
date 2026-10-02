# CLAUDE.md — innerarc 캐릭터 사주 사이트

먼저 `HANDOFF.md`를 끝까지 읽고 시작할 것. 원칙(§2)과 계산 규칙(§6)이 이 프로젝트의 기준이다.

## 작업 규칙
- 소스는 `src/` 와 `assets/` 만 수정한다. `dist/`는 `python3 build.py` 산출물이다 (단, `dist/character-36-types.html`, `dist/ssangwol-duo.html`은 정적 시안).
- 계산 로직(절기·간지·십성·대운·수비학·주역)을 건드리면 반드시:
  1) `python3 build.py`
  2) `python3 tests/test_calc_full.py` → errors 0
  3) `for k in 0 1 2 3 4 5; do python3 tests/test_render.py $k 6; done` → failures 비어 있음
- 결과 리포트는 **객관적**이어야 한다: 같은 입력이면 같은 결과, 난수 금지, 해석마다 `📐 근거` 줄 유지.
- 화면·리포트의 **모든 문장은 캐릭터 말투**(흑월: 나른하고 무심한 반말). 중립 문구를 새로 넣지 말 것.
- 한국어 조사는 `jo(word,을를)`, 숫자는 `nj(n,은는)` 헬퍼를 쓴다.
- 심화 리포트에 생성형 AI 대화·채우기 콘텐츠를 넣지 않는다 (서준님 지시).
- 서준님 결정·자료가 필요한 일은 `docs/pending.md`에 체크박스로 추가하고 진행을 멈추지 말 것.
- 근거 없는 수치·가짜 후기·끝나지 않는 할인 타이머를 실제 오픈본에 넣지 않는다.
