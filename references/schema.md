# 데이터 스키마

## analysis_board.json (분석 트래커)
```jsonc
{
  "meta": {
    "title": "분석 트래커",
    "updated": "YYYY-MM-DD",            // build/export 시 자동 갱신
    "stages": ["필요 샘플","의뢰 (분석센터)","결과 대기","결과 수령","해석 완료"],  // 칸반 5열 (순서=흐름)
    "topics": ["ProjectA","ProjectB"]   // 필터칩. 색=PALETTE 순환
  },
  "centers": [
    {"name": "...", "url": "https://...", "note": "가능 분석명 / in-house 여부"}
    // url 있으면 카드 센터명이 링크. 🏛 기기원 패널에 note 표시.
  ],
  "records": [
    {
      "id": "projecta-001",     // <topic소문자><번호>
      "topic": "ProjectA",      // meta.topics 중 하나 (없으면 추가됨)
      "sample": "Catalyst-X",   // 카드 부제 (강조)
      "analysis": "XRD",        // 카드 제목
      "center": "lab in-house", // centers[].name 과 매칭 시 링크/패널 연동
      "stage": "필요 샘플",       // meta.stages 중 하나 = 칸반 열 (드래그로 변경)
      "essential": true,        // ★ 표시 + "필수만" 토글 대상
      "request_date": "", "result_date": "", "result_link": "",
      "interpretation": "",     // 해석 결과 (있으면 카드에 '解 ...')
      "note": ""                // 목적/비고
    }
  ]
}
```
- 카드 = (analysis, sample) 단위. 같은 분석 여러 샘플이면 sample 필드에 묶어 표기.
- 색: topic index → PALETTE `["#0F0F70","#C5A86F","#475DA3","#FA901E","#888888","#9B7C3F","#626DAE"]` 순환.

## research_status.json (포트폴리오 병목 매트릭스)
```jsonc
{
  "meta": {
    "title": "연구 현황 (포트폴리오 병목)",
    "updated": "YYYY-MM-DD",
    "tracks": ["합성","분석","실험","계산","작성","투고"],  // 매트릭스 열
    "note": "..."
  },
  "projects": [
    {
      "name": "ProjectA",       // 매트릭스 행 (analysis_board.topics 와 별개)
      "tracks": {
        "합성": {"s": "done", "note": "..."},
        "분석": {"s": "auto", "note": ""},   // "auto" = analysis_board에서 해석완료/전체 집계
        "실험": {"s": "prog", "note": "..."},
        "계산": {"s": "wait", "note": ""},
        "작성": {"s": "wait", "note": ""},
        "투고": {"s": "wait", "note": ""}
      },
      "bottleneck": {"track": "실험", "note": "현재 막힌 것 한 줄"}  // 빨강 컬럼
    }
  ]
}
```
- 상태코드 `s`: `done`(●완료 navy) / `prog`(◐진행 orange) / `wait`(○대기 gray) / `block`(✕막힘 red) / `na`(–) / `auto`(분석 전용 자동집계).

## 동기화·편집 원칙
- JSON = 진실원천. HTML은 생성기 출력물(직접 편집 금지).
- 브라우저 Add/Edit/드래그 → localStorage 임시저장. 영구 반영 = HTML "JSON 내보내기" → 해당 JSON 덮어 저장 → build 재실행.
- 인라인 JS 핸들러에서 `${JSON.stringify(id)}` 넣을 땐 속성 따옴표를 **작은따옴표**로(큰따옴표 충돌 주의).
