# 분석센터 정의 가이드 (예시)

`analysis_board.json`의 `centers[]`에 분석을 어디서 측정하는지 정의한다. `note`에 "가능 분석명"을 적어두면 🏛 기기원 패널에서 한눈에 보이고, `url`이 있으면 카드의 센터명이 링크가 된다.

## 분류 예시

### 자체 보유 (in-house — 외부 의뢰 불필요)
```json
{"name": "lab in-house", "url": "", "note": "DRIFTS · BET · chemisorption(TPD/TPR) · 활성평가 (직접 측정)"}
```

### 외부 공동기기원 (의뢰)
```json
{"name": "공동기기원 (example)", "url": "https://example.org",
 "note": "가능: XRD · XPS · TEM · ICP · Raman · UV-vis · FT-IR · NMR"}
```

### 방사광 가속기 (XAS)
```json
{"name": "Synchrotron BL (example)", "url": "https://example.org", "note": "XANES/EXAFS"}
```

## 매핑 팁
- 각 record의 `center` 필드를 `centers[].name`과 정확히 일치시키면 카드↔센터 링크/패널이 연동된다.
- characterization이 아닌 단계(합성·계산·활성평가 등)는 분석센터로 넣지 말고, 포트폴리오 매트릭스(`research_status.json`)의 해당 track으로 관리한다.
