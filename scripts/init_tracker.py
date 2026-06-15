# -*- coding: utf-8 -*-
"""신규 분석 트래커 초기화. TRACKER_DIR(env) 또는 CLI 인자로 대상 폴더 지정.
사용: python init_tracker.py <DATA_DIR> [--force]
  - analysis_board.json / research_status.json 템플릿 생성(기존 있으면 보존, --force로 덮어쓰기)
  - 이어서 build_board.py / build_status.py 실행해 HTML 생성
"""
import json, os, sys, subprocess

args = [a for a in sys.argv[1:] if not a.startswith("--")]
force = "--force" in sys.argv
DATA_DIR = (args[0] if args else None) or os.environ.get("TRACKER_DIR")
if not DATA_DIR:
    print("ERROR: DATA_DIR 필요 (CLI 인자 또는 env TRACKER_DIR)"); sys.exit(1)
os.makedirs(DATA_DIR, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))

BOARD = {
    "meta": {"title": "분석 트래커", "updated": "",
             "stages": ["필요 샘플", "의뢰 (분석센터)", "결과 대기", "결과 수령", "해석 완료"],
             "topics": []},
    "centers": [
        {"name": "lab 자체 (연구실 보유)", "url": "", "note": "연구실 자체 보유 장비 (외부 의뢰 불필요)"},
    ],
    "records": []
}
STATUS = {
    "meta": {"title": "연구 현황 (포트폴리오 병목)", "updated": "",
             "tracks": ["합성", "분석", "실험", "계산", "작성", "투고"],
             "note": "분석 셀은 analysis_board.json에서 자동 집계. 나머지는 셀 클릭으로 수정."},
    "projects": []
}

def maybe_write(name, obj):
    path = os.path.join(DATA_DIR, name)
    if os.path.exists(path) and not force:
        print(f"보존(이미 존재): {name}  (--force 로 덮어쓰기)")
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"생성: {name}")

maybe_write("analysis_board.json", BOARD)
maybe_write("research_status.json", STATUS)

# HTML 빌드
for s in ("build_board.py", "build_status.py"):
    subprocess.run([sys.executable, os.path.join(HERE, s), DATA_DIR], check=False)
print("\n초기화 완료:", DATA_DIR)
print("→ research_status.html 을 브라우저로 열면 됨. record는 HTML의 '+분석 추가' 또는 JSON 직접 편집 후 build 재실행.")
