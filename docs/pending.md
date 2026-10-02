# 사주 사이트 — 서준님 확인·지원 필요 목록

작업 중 서준님의 결정이나 도움이 있어야 끝나는 항목만 모아 둔 메모예요. 진행될 때마다 갱신합니다. (기준일 2026-10-02)

## 🔴 지금 막혀 있는 것

- [ ] **Vidu 영상 생성 실행 환경** — 이 채팅에서는 Vidu 화면을 직접 조작할 수 없어요. 첫 테스트는 서준님이 아래 「Vidu 첫 테스트」 설정을 붙여 넣어 실행하거나, Vidu가 로그인된 브라우저에서 Claude in Chrome / Cowork로 진행해야 해요.
- [ ] **인스타 레퍼런스 영상(다크문) 화면 녹화 업로드** — 인스타는 제 쪽에서 열리지 않아요. 화면 녹화(mp4)를 올려 주시면 프레임 단위로 잘라 움직임(속도·눈 깜빡임·고개 각도·말할 때 입 크기)을 분석해 프롬프트에 반영할게요.

## 🟡 확정해 주셔야 하는 것

- [ ] **원본 이미지·레퍼런스 폴더 업로드** — 저장소에 `assets/source/`(흑월 확정 시트 등 원본), `assets/vidu/`, `reference/halmakase/`(캡처 40장)가 안 올라와 있어요. 지금 빌드는 게시본에서 뽑은 `assets/images.json`(data URI)으로 돌아가요. 원본 파일을 올려 주시면 이미지 파일 분리(HANDOFF §7-2)를 진행할게요.
- [ ] **용궁사주(해랑) 문구 확인** — 게시본이 예전 구조라 템플릿용 문구가 남아 있지 않았어요. 게시본의 해랑 대사(“인간”, 여의주·물때·진주)를 바탕으로 `src/characters.py`에 새로 써 넣었어요. 말투 확인 부탁해요.
- [ ] **태령당 수비학 체계 자료** — 지금은 일반 피타고라스식 계산이에요. 태령당이 뽑는 숫자와 해석 규칙(정리본 또는 리포트 캡처)을 주시면 무료 Ch1·기본 Ch5\~6·심화 숫자 파트를 교체해요.
- [ ] **전생 캐릭터 36종 시안 확정** — 나라·시대 제한 없이 다시 짰어요(한국 인물 5명 유지). 이미지 36장 생성 완료, `dist/character-36-types.html`에서 확인
- [ ] **배우자 가상 이미지 10종 확인** (오행 5 × 남녀) — 10장 생성 완료, 심화 9에 연결됨
- [ ] **고대신점 체계** — 주역 매화역수로 구현함. 염두에 둔 다른 체계가 있으면 알려주기
- [ ] **용궁사주 게시** — 게시 승인이 두 번 안 들어옴. 올릴지 여부
- [ ] **립싱크 음성** — TTS로 갈지, 성우 녹음으로 갈지 / 흑월 목소리 톤 결정

## ⚪ 오픈 전 필수 (서준님 쪽 계약·정보)

- [ ] 결제 연동 (카카오페이·네이버페이·토스 등 PG 계약) — 지금은 화면만 있음
- [ ] 사업자 정보 (상호·대표·사업자번호·통신판매업) 푸터 기재
- [ ] 누적 건수·만족도·후기·할인 타이머를 실제 데이터로 교체 — 근거 없는 수치·가짜 후기·끝나지 않는 타이머는 표시광고법·전자상거래법 위험
- [ ] 친구 초대 집계·챕터 잠금 해제 서버 (백엔드)
- [ ] 음력 생일 → 양력 변환표 탑재 (지금은 양력만 정확)
- [ ] 각 시안 링크 공개 공유 설정

## ✅ 완료

- [x] 이미지 원본 해상도 교체 — Canva 내보내기로 47장 원본 확보(`assets/source/canva/`), 사이트용 축소본으로 교체
- [ ] (서준님) Canva에 남은 임시 디자인 「[삭제해도 됨] 사주사이트 이미지 원본 추출용」 휴지통으로 — 도구로는 삭제가 안 돼요
- [x] 이미지 47장 생성 (Canva) — 전생 36 · 배우자 10 · 서월×흑월 듀오 1. `assets/img/`, 리포트 Ch3·심화 9에 연결
- [x] 저장소 위치 확정 — jinssung 저장소에서 계속 진행 (서준님, 2026-10-02)
- [x] 소스 복원 — claude.ai 게시본에서 `src/tpl.html`·`src/paid.js`·`src/characters.py`·`assets/images.json` 복원, 빌드 재현 확인 (2026-10-02)
- [x] 검사 스크립트 재작성 — `tests/test_calc_full.py`(ephem 기준 대조) · `tests/test_render.py`
- [x] 대운 시작 나이를 실제 출생 시각 기준으로 계산 (전에는 묘시 고정)
- [x] 흑월 캐릭터 시트 확정
- [x] 리포트 무료/기본(39,000)/심화(79,000) 구분
- [x] 1900년생\~오늘 출생 전 구간 검증 (계산 648,144건 · 화면 6,614명 오류 0)
- [x] 예시 시안: 1986-02-12 유시 양력 · 남성 · ENTP

## 🎬 Vidu 첫 테스트 (무료 크레딧 1회)

**목표**: 흑월 대기 루프 1컷 (첫 화면·선택 화면·로딩에 재사용) — 한 번으로 화풍 유지·얼굴 일관성·손·잔 형태를 검증

- 모드: 이미지 → 영상 (Image to Video)
- 참조 이미지: `heukwol_vidu_ref_A_portrait.png` (확정 시트의 달빛 잔 컷)
- 길이: 무료로 가능한 가장 짧은 길이 (4초 내외)
- 해상도·품질: 무료 기본값
- 움직임 강도: 가능하면 '작게/자연스럽게'

프롬프트:

```
The man slowly swirls the whiskey glass with a relaxed wrist, the amber liquid moves gently. He lifts only his eyes toward the camera with a lazy, knowing half-smile, holds the gaze for a moment, then lets his eyes drift slightly away. Subtle breathing, natural irregular blinking, a strand of hair shifts softly. Moonlight and faint candle glow in the background. Static camera with a very slow push-in. Keep the exact same face, hairstyle, outfit and art style as the input image. Calm, cinematic, natural micro-movements.
```

검수 기준 (하나라도 안 맞으면 프롬프트 수정 후 재시도):

- [ ] 클립 내내 같은 얼굴인가
- [ ] 손가락 개수·잔 모양이 유지되는가
- [ ] 눈 깜빡임이 자연스럽고 불규칙한가
- [ ] 움직임이 과하지 않은가 (모션 바이블: 흑월은 거의 움직이지 않다가 툭 멈추는 캐릭터)
- [ ] 첫 프레임과 마지막 프레임이 비슷해 루프가 가능한가
