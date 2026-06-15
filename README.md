# analysis-tracker

연구 분석/실험 진행을 관리하는 **단일파일 HTML 트래커** + **포트폴리오 병목 매트릭스**. Claude Code 스킬로도 동작하고, 파이썬 생성기로 단독 사용도 가능하다.

촉매·재료 연구처럼 **여러 프로젝트 × 여러 characterization 분석**을 동시에 굴릴 때, "어떤 분석이 어디까지 됐고, 각 연구가 지금 어디서 막혔는지"를 한 화면에서 본다.

## 두 가지 뷰

| | |
|---|---|
| **분석 트래커** (`analysis_board.html`) | characterization 5단계 칸반: 필요 샘플 → 의뢰(분석센터) → 결과 대기 → 결과 수령 → 해석 완료. 주제 필터·★필수 토글·기기원 패널·**카드 드래그&드롭**으로 단계 이동. |
| **연구 현황·병목 매트릭스** (`research_status.html`) | 행=프로젝트, 열=단계(합성/분석/실험/계산/작성/투고)+현재 병목. **분석 셀은 분석 트래커에서 자동 집계**. 클릭하면 해당 프로젝트로 필터된 분석 보드가 하단에 펼쳐진다. |

데이터는 JSON(진실원천) → 파이썬 생성기 → 자기완결 HTML(외부 의존 없음, 더블클릭으로 열림).

## 빠른 시작
```bash
# 1) 새 트래커 초기화 (빈 템플릿 + HTML 생성)
python scripts/init_tracker.py ./my_tracker

# 2) 데이터 편집: my_tracker/analysis_board.json, my_tracker/research_status.json
#    (또는 브라우저에서 '+ 분석 추가' 후 'JSON 내보내기')

# 3) 재생성
python scripts/build_board.py ./my_tracker
python scripts/build_status.py ./my_tracker

# research_status.html 을 브라우저로 열면 됨 (통합 진입점)
```
`DATA_DIR`은 `CLI 인자 > 환경변수 TRACKER_DIR > 기본값(./tracker_data)` 순으로 결정된다.

## 데이터 모델
- `analysis_board.json` — 분석 record(topic·sample·analysis·center·stage·essential·…), centers, stages/topics.
- `research_status.json` — 프로젝트별 단계 상태(done/prog/wait/block) + 병목.
- 상세: [`references/schema.md`](references/schema.md). 데모: [`examples/`](examples/).

## 편집 원칙
JSON이 진실원천이고 HTML은 생성물이다. 브라우저에서의 추가/드래그는 localStorage에 임시 저장되며, 영구 반영하려면 **JSON 내보내기 → 파일 저장 → 생성기 재실행**.

## 요건
Python 3 + [`python-pptx`는 불필요], 표준 라이브러리만 사용. 웹폰트(NanumSquare)는 CDN.

## 라이선스
MIT
