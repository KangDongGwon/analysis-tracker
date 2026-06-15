---
name: analysis-tracker
description: 연구 분석/실험 진행 트래커(HTML 칸반 + 포트폴리오 병목 매트릭스)를 생성·운영. characterization 분석을 단계별로 관리하고, 프로젝트별로 어디서 막혔는지(병목)를 한눈에 본다. 신규 트래커 생성 + 기존 트래커 갱신. Triggers - /analysis-tracker, 분석 트래커, 분석 보드, 연구 현황, 병목 트래커, 트래커에 추가, 트래커 갱신, analysis tracker, research bottleneck.
---

# analysis-tracker — 분석/연구 진행 트래커 엔진

JSON(진실원천) → 생성기(python) → 단일파일 HTML 대시보드. **두 개의 연동 툴**:
1. **분석 트래커**(`analysis_board.html`) — characterization 5단계 칸반 (필요 샘플 → 의뢰(분석센터) → 결과 대기 → 결과 수령 → 해석 완료). 주제 필터칩·★필수 토글·🏛 기기원 패널·카드 드래그&드롭 단계이동·샘플명 강조.
2. **연구 현황·병목 매트릭스**(`research_status.html` = 통합 진입점) — 행=프로젝트, 열=단계(합성/분석/실험/계산/작성/투고)+현재병목. **분석 셀은 analysis_board에서 자동 집계**(해석완료/전체). "📊 분석 트래커" 버튼/분석 셀 클릭 시 하단에 분석보드를 iframe으로 전개(`#topic=프로젝트` 필터).

스타일 = navy `#0F0F70`/gold `#C5A86F`/orange `#FA901E`, NanumSquare. 상태색 ●완료/◐진행/○대기/✕막힘.

## 데이터 위치 (DATA_DIR)
생성기는 **DATA_DIR**을 `CLI 인자 > env TRACKER_DIR > 기본값(./tracker_data)`으로 결정.
- 기본 실행: `python scripts/build_board.py`  → cwd의 `tracker_data/`
- 명시 실행: `python scripts/build_board.py /path/to/tracker`  또는  `set TRACKER_DIR=...`

## 운영 (기존 트래커 갱신)
**핵심 규칙: 데이터는 JSON에서 고치고, HTML은 항상 생성기로 재생성한다. HTML 직접 편집 금지(브라우저 Add/드래그는 localStorage 임시저장 — 영구화는 JSON 내보내기→저장→재빌드).**

1. **분석 record 추가/수정** → `<DATA_DIR>/analysis_board.json`의 `records[]` 편집 → `python scripts/build_board.py <DATA_DIR>`
2. **프로젝트 단계/병목 수정** → `research_status.json`의 `projects[]` 편집 → `python scripts/build_status.py <DATA_DIR>`
3. 분석보드 갱신 후 매트릭스 분석 셀 수치 동기화하려면 build_status.py도 재실행(집계는 build 시점).

## 신규 트래커 생성
1. `python scripts/init_tracker.py <DATA_DIR>` → 빈 트래커 템플릿 2개 + HTML 생성(기존 보존, `--force`로 덮어쓰기).
2. `analysis_board.json`에 topics/centers/records, `research_status.json`에 projects 추가 → build 재실행.
3. 스키마는 `references/schema.md`, 센터 정의는 `references/centers_example.md` 참조.

## 검증 (완료 전)
- playwright headless로 콘솔에러 0 + 카드/행 수 확인. 드래그&드롭은 합성마우스로 안 되니 DragEvent dispatch로 로직 검증.
- 인라인 JS 핸들러에 `JSON.stringify` 값 넣을 땐 속성을 **작은따옴표**로 (큰따옴표면 깨짐).

## 파일
- `scripts/build_board.py` — analysis_board.json → analysis_board.html (칸반)
- `scripts/build_status.py` — research_status.json(+board 집계) → research_status.html (매트릭스+iframe 통합)
- `scripts/init_tracker.py` — 신규 트래커 템플릿 생성
- `references/schema.md` — 데이터 스키마 (record/center/status 필드)
- `references/centers_example.md` — 센터 정의 가이드(예시)
- `examples/*.json` — 데모 데이터 (구조 참고용)
