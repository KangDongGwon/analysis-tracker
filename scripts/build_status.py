# -*- coding: utf-8 -*-
"""research_status.json (+ analysis_board.json 분석 집계) -> research_status.html
포트폴리오 병목 매트릭스. 재생성: python build_status.py"""
import json, os, datetime, sys
DATA_DIR = (sys.argv[1] if len(sys.argv) > 1 else None) or os.environ.get("TRACKER_DIR") \
    or os.path.join(os.getcwd(), "tracker_data")

with open(os.path.join(DATA_DIR, "research_status.json"), encoding="utf-8") as f:
    data = json.load(f)
with open(os.path.join(DATA_DIR, "analysis_board.json"), encoding="utf-8") as f:
    board = json.load(f)

# 프로젝트별 분석 집계 (해석완료/전체)
stats = {}
for t in board["meta"]["topics"]:
    recs = [r for r in board["records"] if r["topic"] == t]
    done = sum(1 for r in recs if r["stage"] == "해석 완료")
    inprog = sum(1 for r in recs if r["stage"] in ("결과 수령", "결과 대기", "의뢰 (분석센터)"))
    stats[t] = {"total": len(recs), "done": done, "inprog": inprog}

generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
data_js = json.dumps(data, ensure_ascii=False)
stats_js = json.dumps(stats, ensure_ascii=False)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>연구 현황 · 병목</title>
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<style>
:root{--navy:#0F0F70;--gold:#C5A86F;--orange:#FA901E;--gray:#888888;--red:#F8312A;--peri:#475DA3;
  --bg:#eef0f5;--line:#dfe3ec;--ink:#111;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'NanumSquare','Malgun Gothic',sans-serif;font-weight:700}
.hband{background:var(--navy);color:#fff;padding:15px 24px 13px;position:relative}
.hband::after{content:"";position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(252,152,40,.88)}
.htop{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
h1{font-size:24px;font-weight:800;margin:0;letter-spacing:-.5px}
.sub{font-size:12px;color:#aeb7e0;font-weight:800}
.spacer{flex:1}
.btn{font-family:inherit;font-weight:800;font-size:13px;border:none;border-radius:20px;padding:8px 16px;cursor:pointer}
.btn-ghost{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.45);padding:6px 14px}
.btn-ghost:hover{background:rgba(255,255,255,.16)}
.legend{display:flex;gap:16px;flex-wrap:wrap;padding:14px 24px 4px;font-size:12px;font-weight:800;color:#46586a}
.legend span{display:inline-flex;align-items:center;gap:5px}
.dot{font-size:15px;line-height:1}
.wrap{padding:14px 24px 40px;overflow-x:auto}
table{border-collapse:separate;border-spacing:0;min-width:880px;width:100%}
th,td{padding:0;text-align:left}
thead th{font-size:13px;font-weight:800;color:#fff;background:var(--navy);padding:9px 12px;position:sticky;top:0}
thead th:first-child{border-top-left-radius:10px}
thead th.bn{background:var(--red);border-top-right-radius:10px}
tbody td{border-bottom:1px solid var(--line);background:#fff;vertical-align:top}
.proj{font-weight:800;font-size:15px;color:var(--navy);padding:12px;white-space:nowrap;border-left:5px solid var(--navy)}
.cell{padding:9px 11px;cursor:pointer;min-width:118px;transition:.1s}
.cell:hover{background:#f6f8fc}
.cell .sym{font-size:17px;font-weight:800}
.cell .lab{font-size:10px;font-weight:800;margin-left:5px;opacity:.7}
.cell .nt{font-size:10.5px;color:#5a6b7b;margin-top:3px;line-height:1.45;font-weight:700}
.cell.ana{background:#fbfaf4}
.bn{padding:10px 12px;border-left:3px solid var(--red);background:#fff7f5;cursor:pointer;min-width:200px}
.bn .bt{font-size:11px;font-weight:800;color:var(--red)}
.bn .bnt{font-size:11.5px;color:#46586a;margin-top:2px;font-weight:700;line-height:1.45}
/* modal */
.ovl{position:fixed;inset:0;background:rgba(15,15,40,.5);display:none;z-index:60;align-items:flex-start;justify-content:center;padding:60px 16px;overflow:auto}
.ovl.on{display:flex}
.modal{background:#fff;border-radius:14px;width:430px;max-width:100%;padding:22px 24px;border-top:6px solid var(--navy);box-shadow:0 16px 50px rgba(0,0,0,.3)}
.modal h2{margin:0 0 14px;font-size:16px;font-weight:800;color:var(--navy)}
.fld{margin-bottom:11px}
.fld label{display:block;font-size:12px;font-weight:800;color:var(--navy);margin-bottom:4px}
.fld select,.fld textarea{width:100%;font-family:inherit;font-weight:700;font-size:13px;border:2px solid var(--line);border-radius:7px;padding:7px 9px}
.fld textarea{resize:vertical;min-height:54px}
.mfoot{display:flex;gap:8px;justify-content:flex-end;margin-top:14px}
.btn-save{background:var(--navy);color:#fff}.btn-cancel{background:#e7ebf2;color:#445}
.btn-open{background:var(--orange);color:#3a2400}
.note{font-size:11px;color:#8a97a6;padding:0 24px 18px;font-weight:700}
.abhead{padding:8px 24px 6px;font-size:13px;font-weight:800;color:var(--navy)}
.abframe{width:100%;height:80vh;border:none;border-top:3px solid var(--orange);background:var(--bg);display:block}
</style></head><body>
<div class="hband"><div class="htop">
  <h1>연구 현황 · 병목</h1><span class="sub" id="genat"></span>
  <div class="spacer"></div>
  <button class="btn btn-ghost" id="abtoggle" onclick="toggleBoard()">📊 분석 트래커 ▾</button>
  <button class="btn btn-ghost" onclick="exportJSON()">JSON 내보내기</button>
  <label class="btn btn-ghost" style="margin:0">JSON 불러오기<input type="file" id="imp" accept="application/json" style="display:none" onchange="importJSON(event)"></label>
</div></div>
<div class="legend">
  <span><span class="dot" style="color:#0F0F70">●</span>완료</span>
  <span><span class="dot" style="color:#FA901E">◐</span>진행</span>
  <span><span class="dot" style="color:#888888">○</span>대기</span>
  <span><span class="dot" style="color:#F8312A">✕</span>막힘</span>
  <span style="color:#8a97a6">· 분석 셀=자동집계(클릭→보드) · 나머지 셀 클릭→수정 · 병목 셀 클릭→수정</span>
</div>
<div class="wrap"><table id="mx"></table></div>
<div class="note" id="note"></div>

<div id="boardWrap" style="display:none">
  <div class="abhead">📊 분석 트래커 (characterization) — 단계 클릭 시 동기화 갱신은 build 시점</div>
  <iframe id="abframe" class="abframe" title="분석 트래커"></iframe>
</div>

<div class="ovl" id="ovl"><div class="modal">
  <h2 id="mtitle">수정</h2>
  <input type="hidden" id="f_proj"><input type="hidden" id="f_track"><input type="hidden" id="f_mode">
  <div class="fld" id="fld_track" style="display:none"><label>병목 단계</label><select id="f_bntrack"></select></div>
  <div class="fld" id="fld_stat"><label>상태</label><select id="f_stat"></select></div>
  <div class="fld"><label>메모</label><textarea id="f_note"></textarea></div>
  <div class="mfoot"><button class="btn btn-cancel" onclick="closeModal()">취소</button><button class="btn btn-save" onclick="saveCell()">저장</button></div>
</div></div>

<script>
const EMBED=__DATA__, STATS=__STATS__, GEN="__GEN__";
const LSKEY="researchStatus.v1";
function load(){try{const r=localStorage.getItem(LSKEY);if(r){const o=JSON.parse(r);if(o.base===GEN&&o.data)return o.data;}}catch(e){}return JSON.parse(JSON.stringify(EMBED));}
let DATA=load();
function persist(){localStorage.setItem(LSKEY,JSON.stringify({base:GEN,data:DATA}));}
const STAT={done:{s:"●",c:"#0F0F70",l:"완료"},prog:{s:"◐",c:"#FA901E",l:"진행"},wait:{s:"○",c:"#888888",l:"대기"},block:{s:"✕",c:"#F8312A",l:"막힘"},na:{s:"–",c:"#bbb",l:"해당없음"}};
const tracks=DATA.meta.tracks;
function esc(s){return (s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]));}

function anaCell(proj){
  const st=STATS[proj]||{total:0,done:0,inprog:0};
  let s="wait"; if(st.total&&st.done===st.total)s="done"; else if(st.done>0||st.inprog>0)s="prog";
  const m=STAT[s];
  return `<td class="cell ana" onclick="openBoardFiltered('${esc(proj)}')">
    <div><span class="sym" style="color:${m.c}">${m.s}</span><span class="lab" style="color:${m.c}">${st.done}/${st.total}</span></div>
    <div class="nt">해석완료 ${st.done} · 진행 ${st.inprog} · 전체 ${st.total}</div></td>`;
}
function cell(proj,tr){
  if(tr==="분석") return anaCell(proj);
  const o=(DATA.projects.find(p=>p.name===proj).tracks||{})[tr]||{s:"na",note:""};
  const m=STAT[o.s]||STAT.na;
  return `<td class="cell" onclick="editCell('${esc(proj)}','${esc(tr)}')">
    <div><span class="sym" style="color:${m.c}">${m.s}</span><span class="lab" style="color:${m.c}">${m.l}</span></div>
    ${o.note?`<div class="nt">${esc(o.note)}</div>`:""}</td>`;
}
function render(){
  document.getElementById("genat").textContent="갱신 "+GEN;
  let h="<thead><tr><th>프로젝트</th>";
  tracks.forEach(t=>h+=`<th>${esc(t)}</th>`);
  h+=`<th class="bn">현재 병목</th></tr></thead><tbody>`;
  DATA.projects.forEach(p=>{
    h+=`<tr><td class="proj">${esc(p.name)}</td>`;
    tracks.forEach(t=>h+=cell(p.name,t));
    const b=p.bottleneck||{track:"",note:""};
    h+=`<td class="bn" onclick="editBn('${esc(p.name)}')"><div class="bt">▸ ${esc(b.track||"-")}</div><div class="bnt">${esc(b.note||"")}</div></td></tr>`;
  });
  h+="</tbody>";
  document.getElementById("mx").innerHTML=h;
  document.getElementById("note").textContent=DATA.meta.note||"";
  persist();
}
function toggleBoard(){
  const w=document.getElementById("boardWrap"),f=document.getElementById("abframe"),t=document.getElementById("abtoggle");
  if(w.style.display==="none"){ if(!f.getAttribute("src")) f.setAttribute("src","analysis_board.html"); w.style.display="block"; t.textContent="📊 분석 트래커 ▴"; w.scrollIntoView({behavior:"smooth"}); }
  else { w.style.display="none"; t.textContent="📊 분석 트래커 ▾"; }
}
function openBoardFiltered(proj){
  const w=document.getElementById("boardWrap"),f=document.getElementById("abframe"),t=document.getElementById("abtoggle");
  const hash="topic="+encodeURIComponent(proj);
  if(w.style.display==="none"){ w.style.display="block"; t.textContent="📊 분석 트래커 ▴"; }
  if(!f.getAttribute("src")) f.setAttribute("src","analysis_board.html#"+hash);
  else { try{ f.contentWindow.location.hash=hash; }catch(e){ f.setAttribute("src","analysis_board.html#"+hash); } }
  w.scrollIntoView({behavior:"smooth"});
}

function fillStat(sel){document.getElementById("f_stat").innerHTML=Object.keys(STAT).map(k=>`<option value="${k}">${STAT[k].s} ${STAT[k].l}</option>`).join("");document.getElementById("f_stat").value=sel||"wait";}
function editCell(proj,tr){
  document.getElementById("f_mode").value="cell";
  document.getElementById("mtitle").textContent=`${proj} · ${tr}`;
  document.getElementById("f_proj").value=proj;document.getElementById("f_track").value=tr;
  document.getElementById("fld_track").style.display="none";document.getElementById("fld_stat").style.display="block";
  const o=(DATA.projects.find(p=>p.name===proj).tracks||{})[tr]||{s:"wait",note:""};
  fillStat(o.s);document.getElementById("f_note").value=o.note||"";
  document.getElementById("ovl").classList.add("on");
}
function editBn(proj){
  document.getElementById("f_mode").value="bn";
  document.getElementById("mtitle").textContent=`${proj} · 병목`;
  document.getElementById("f_proj").value=proj;
  document.getElementById("fld_track").style.display="block";document.getElementById("fld_stat").style.display="none";
  document.getElementById("f_bntrack").innerHTML=tracks.map(t=>`<option value="${esc(t)}">${esc(t)}</option>`).join("");
  const b=DATA.projects.find(p=>p.name===proj).bottleneck||{track:tracks[0],note:""};
  document.getElementById("f_bntrack").value=b.track||tracks[0];document.getElementById("f_note").value=b.note||"";
  document.getElementById("ovl").classList.add("on");
}
function saveCell(){
  const proj=document.getElementById("f_proj").value,mode=document.getElementById("f_mode").value;
  const p=DATA.projects.find(x=>x.name===proj);const note=document.getElementById("f_note").value.trim();
  if(mode==="cell"){const tr=document.getElementById("f_track").value;p.tracks=p.tracks||{};p.tracks[tr]={s:document.getElementById("f_stat").value,note:note};}
  else{p.bottleneck={track:document.getElementById("f_bntrack").value,note:note};}
  closeModal();render();
}
function closeModal(){document.getElementById("ovl").classList.remove("on");}
function exportJSON(){const blob=new Blob([JSON.stringify(DATA,null,2)],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="research_status.json";a.click();}
function importJSON(ev){const f=ev.target.files[0];if(!f)return;const rd=new FileReader();rd.onload=()=>{try{DATA=JSON.parse(rd.result);render();alert("불러오기 완료");}catch(e){alert("실패: "+e);}};rd.readAsText(f);}
document.getElementById("ovl").addEventListener("click",e=>{if(e.target.id==="ovl")closeModal();});
render();
</script></body></html>
"""
html = (TEMPLATE.replace("__DATA__", data_js).replace("__STATS__", stats_js).replace("__GEN__", generated_at))
with open(os.path.join(DATA_DIR, "research_status.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("built: research_status.html")
print("projects:", [p["name"] for p in data["projects"]])
print("분석 집계:", stats)
