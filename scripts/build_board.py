# -*- coding: utf-8 -*-
"""analysis_board.json -> analysis_board.html (CCEL 스타일 칸반 대시보드).
재생성: python build_board.py"""
import json, os, datetime, sys

# DATA_DIR: CLI 인자 > env TRACKER_DIR > 기본값(./tracker_data). 범용 엔진 — 어느 폴더든 동작.
DATA_DIR = (sys.argv[1] if len(sys.argv) > 1 else None) or os.environ.get("TRACKER_DIR") \
    or os.path.join(os.getcwd(), "tracker_data")
JSON_PATH = os.path.join(DATA_DIR, "analysis_board.json")
HTML_PATH = os.path.join(DATA_DIR, "analysis_board.html")

with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

generated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
data_js = json.dumps(data, ensure_ascii=False)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>분석 트래커 · CCEL</title>
<link href="https://cdn.jsdelivr.net/gh/moonspam/NanumSquare@2.0/nanumsquare.css" rel="stylesheet">
<style>
:root{
  --navy:#0F0F70; --gold:#C5A86F; --gold-d:#9B7C3F; --gold-l:#D5C097;
  --orange:#FA901E; --orange2:#FC9828; --gray:#888888; --peri:#475DA3; --peri-l:#626DAE;
  --ink:#111; --bg:#eef0f5; --panel:#ffffff; --line:#dfe3ec;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:'NanumSquare','나눔스퀘어','Malgun Gothic',sans-serif;font-weight:700;}
/* ---- header band (navy + orange strip) ---- */
header{position:sticky;top:0;z-index:30}
.hband{background:var(--navy);color:#fff;padding:15px 24px 13px}
.hband::after{content:"";position:absolute;left:0;right:0;bottom:0;height:6px;
  background:rgba(252,152,40,.88)}
.htop{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
h1{font-size:25px;font-weight:800;margin:0;letter-spacing:-.5px}
.sub{font-size:12px;color:#aeb7e0;font-weight:800}
.spacer{flex:1}
.note-sync{font-size:11px;color:#c3ccef;font-weight:700;margin-top:7px}
.note-sync b{color:var(--orange2);font-weight:800}
/* ---- buttons (chip) ---- */
.btn{font-family:inherit;font-weight:800;font-size:13px;border:none;border-radius:20px;
  padding:8px 16px;cursor:pointer;transition:.15s}
.btn-add{background:var(--orange);color:#3a2400;box-shadow:0 2px 6px rgba(250,144,30,.4)}
.btn-add:hover{background:var(--orange2)}
.btn-ghost{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.45);padding:6px 14px}
.btn-ghost:hover{background:rgba(255,255,255,.16)}
/* ---- topic filter chips ---- */
.chips{display:flex;gap:9px;flex-wrap:wrap;padding:16px 24px 2px}
.chip{font-weight:800;font-size:13px;border:2px solid var(--navy);background:#fff;color:var(--navy);
  border-radius:20px;padding:5px 16px;cursor:pointer;transition:.12s}
.chip.active{background:var(--navy);color:#fff}
.chip-ess{border-color:var(--orange);color:var(--gold-d)}
.chip-ess.active{background:var(--orange);color:#3a2400;border-color:var(--orange)}
.chip .n{opacity:.55;font-size:11px;margin-left:6px}
/* ---- centers directory ---- */
.centers-panel{display:flex;flex-wrap:wrap;gap:11px;padding:14px 24px 0}
.cen{background:#fff;border:1.5px solid var(--gold);border-left:5px solid var(--gold);
  border-radius:10px;padding:10px 14px;min-width:250px;max-width:360px}
.cen .cn{font-weight:800;color:var(--navy);font-size:13px}
.cen .cn a{color:var(--peri);text-decoration:none}
.cen .cn a:hover{text-decoration:underline}
.cen .cnote{font-size:11.5px;color:#46586a;margin-top:4px;font-weight:700;line-height:1.55}
/* ---- board ---- */
.board{display:flex;gap:18px;padding:30px 24px 46px;overflow-x:auto;align-items:flex-start}
.col{position:relative;margin-top:14px;background:var(--panel);border-radius:13px;
  min-width:262px;width:262px;flex:0 0 auto;padding-top:24px;padding-bottom:4px;
  border:2.25px solid var(--gray);
  opacity:0;transform:translateY(8px);transition:opacity .5s,transform .5s}
.col.visible{opacity:1;transform:none}
.colhead{position:absolute;top:-15px;left:50%;transform:translateX(-50%);
  white-space:nowrap;color:#fff;font-weight:800;font-size:13.5px;border-radius:18px;
  padding:6px 17px;display:flex;align-items:center;gap:8px;box-shadow:0 2px 5px rgba(0,0,0,.18)}
.colhead .cnt{background:rgba(255,255,255,.32);border-radius:11px;padding:0 8px;font-size:12px}
.col0{border-color:var(--gray)}        .col0 .colhead{background:var(--gray)}
.col1{border-color:var(--peri)}        .col1 .colhead{background:var(--peri)}
.col2{border-color:var(--gold)}        .col2 .colhead{background:var(--gold)}
.col3{border-color:var(--orange)}      .col3 .colhead{background:var(--orange)}
.col4{border-color:var(--navy)}        .col4 .colhead{background:var(--navy)}
.col.dover{background:#fff3e2;box-shadow:0 0 0 2px var(--orange) inset}
.cards{padding:10px 11px;display:flex;flex-direction:column;gap:10px;min-height:40px}
.card[draggable]{cursor:grab}
.card.dragging{opacity:.45}
.card{background:#fff;border:1px solid var(--line);border-left:5px solid var(--navy);
  border-radius:10px;padding:11px 12px;cursor:pointer;transition:.12s;
  box-shadow:0 1px 3px rgba(15,15,112,.07)}
.card:hover{box-shadow:0 4px 12px rgba(15,15,112,.16);transform:translateY(-1px)}
.card .a{font-weight:800;font-size:14.5px;color:var(--navy)}
.card .s{font-size:12px;color:var(--peri);font-weight:800;margin-top:2px;
  text-decoration:underline;text-decoration-color:#aab6d6;text-underline-offset:2px}
.card .meta{font-size:11px;color:#7a8694;margin-top:7px;line-height:1.55;font-weight:700}
.card .tg{display:inline-block;font-size:10px;font-weight:800;color:#fff;border-radius:9px;
  padding:1px 9px;margin-top:8px}
.card a.lk{color:var(--peri);text-decoration:none;font-weight:800}
.card a.lk:hover{text-decoration:underline}
.empty{color:#b3bcc7;font-size:12px;text-align:center;padding:12px 0;font-weight:800}
/* ---- modal ---- */
.ovl{position:fixed;inset:0;background:rgba(15,15,40,.5);display:none;z-index:60;
  align-items:flex-start;justify-content:center;padding:40px 16px;overflow:auto}
.ovl.on{display:flex}
.modal{background:#fff;border-radius:15px;width:490px;max-width:100%;padding:24px 26px;
  box-shadow:0 16px 54px rgba(0,0,0,.34);border-top:6px solid var(--navy)}
.modal h2{margin:0 0 16px;font-size:18px;font-weight:800;color:var(--navy)}
.fld{margin-bottom:11px}
.fld label{display:block;font-size:12px;font-weight:800;color:var(--navy);margin-bottom:4px}
.fld input,.fld select,.fld textarea{width:100%;font-family:inherit;font-weight:700;font-size:13px;
  border:2px solid var(--line);border-radius:8px;padding:7px 10px;color:var(--ink)}
.fld input:focus,.fld select:focus,.fld textarea:focus{outline:none;border-color:var(--peri)}
.fld textarea{resize:vertical;min-height:48px}
.row2{display:flex;gap:10px}.row2 .fld{flex:1}
.mfoot{display:flex;gap:8px;justify-content:space-between;margin-top:18px}
.btn-save{background:var(--navy);color:#fff}.btn-cancel{background:#e7ebf2;color:#445}
.btn-del{background:#fbe6e1;color:#b23a1e}
footer{padding:0 24px 26px;font-size:11px;color:#9aa7b3;font-weight:800}
</style>
</head>
<body>
<header>
  <div class="hband">
    <div class="htop">
      <h1>분석 트래커</h1>
      <span class="sub" id="genat"></span>
      <div class="spacer"></div>
      <button class="btn btn-add" onclick="openAdd()">+ 분석 추가</button>
      <button class="btn btn-ghost" onclick="toggleCenters()">🏛 기기원</button>
      <button class="btn btn-ghost" onclick="exportJSON()">JSON 내보내기</button>
      <label class="btn btn-ghost" style="margin:0">JSON 불러오기
        <input type="file" id="imp" accept="application/json" style="display:none" onchange="importJSON(event)">
      </label>
    </div>
    <div class="note-sync">입력 후 <b>JSON 내보내기</b> → 파일 저장해야 Claude와 동기화 (브라우저 편집은 자동 임시저장)</div>
  </div>
</header>

<div class="chips" id="chips"></div>
<div class="centers-panel" id="centers" style="display:none"></div>
<div class="board" id="board"></div>
<footer id="foot"></footer>

<div class="ovl" id="ovl"><div class="modal">
  <h2 id="mtitle">분석 추가</h2>
  <input type="hidden" id="f_id">
  <div class="row2">
    <div class="fld"><label>연구주제</label><input id="f_topic" list="dl_topic"></div>
    <div class="fld"><label>샘플</label><input id="f_sample" placeholder="예: Catalyst-X"></div>
  </div>
  <div class="row2">
    <div class="fld"><label>분석항목</label><input id="f_analysis" placeholder="예: XPS"></div>
    <div class="fld"><label>분석센터</label><input id="f_center" list="dl_center"></div>
  </div>
  <div class="row2">
    <div class="fld"><label>단계</label><select id="f_stage"></select></div>
    <div class="fld"><label>필수 분석 (★)</label><select id="f_essential"><option value="false">일반</option><option value="true">★ 필수</option></select></div>
  </div>
  <div class="row2">
    <div class="fld"><label>의뢰일</label><input id="f_request_date" placeholder="YYYY-MM-DD"></div>
    <div class="fld"><label>결과일</label><input id="f_result_date" placeholder="YYYY-MM-DD"></div>
  </div>
  <div class="fld"><label>결과 링크 (파일/URL)</label><input id="f_result_link" placeholder="https:// 또는 파일경로"></div>
  <div class="fld"><label>해석된 결과</label><textarea id="f_interpretation"></textarea></div>
  <div class="fld"><label>비고 / 목적</label><textarea id="f_note"></textarea></div>
  <div class="mfoot">
    <button class="btn btn-del" id="btnDel" onclick="delRec()">삭제</button>
    <div style="display:flex;gap:8px">
      <button class="btn btn-cancel" onclick="closeModal()">취소</button>
      <button class="btn btn-save" onclick="saveRec()">저장</button>
    </div>
  </div>
</div></div>

<datalist id="dl_topic"></datalist>
<datalist id="dl_center"></datalist>

<script>
const EMBED = __DATA__;
const GENERATED_AT = "__GENERATED_AT__";
const LSKEY = "analysisBoard.v1";

function load(){
  try{
    const raw = localStorage.getItem(LSKEY);
    if(raw){ const o = JSON.parse(raw); if(o.base === GENERATED_AT && o.data) return o.data; }
  }catch(e){}
  return JSON.parse(JSON.stringify(EMBED));
}
let DATA = load();
function persist(){ localStorage.setItem(LSKEY, JSON.stringify({base:GENERATED_AT, data:DATA})); }

const stages = DATA.meta.stages;
let filter = "ALL";
let essOnly = false;
const PALETTE = ["#0F0F70","#C5A86F","#475DA3","#FA901E","#888888","#9B7C3F","#626DAE"];

function centerURL(name){ const c=(DATA.centers||[]).find(c=>c.name===name); return c&&c.url?c.url:""; }
function topicColor(t){ const i=DATA.meta.topics.indexOf(t); return i>=0?PALETTE[i%PALETTE.length]:"#0F0F70"; }
function esc(s){return (s||"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]));}

function render(){
  document.getElementById("genat").textContent = "갱신 "+GENERATED_AT;
  const counts={ALL:DATA.records.length};
  DATA.meta.topics.forEach(t=>counts[t]=DATA.records.filter(r=>r.topic===t).length);
  let ch=`<div class="chip ${filter==='ALL'?'active':''}" onclick="setF('ALL')">전체<span class="n">${counts.ALL}</span></div>`;
  DATA.meta.topics.forEach(t=>{
    ch+=`<div class="chip ${filter===t?'active':''}" onclick="setF('${esc(t)}')">${esc(t)}<span class="n">${counts[t]||0}</span></div>`;
  });
  const essN=DATA.records.filter(r=>r.essential&&(filter==="ALL"||r.topic===filter)).length;
  ch+=`<div class="chip chip-ess ${essOnly?'active':''}" onclick="toggleEss()" style="margin-left:6px">★ 필수만<span class="n">${essN}</span></div>`;
  document.getElementById("chips").innerHTML=ch;
  let recs = DATA.records.filter(r=>(filter==="ALL"||r.topic===filter)&&(!essOnly||r.essential));
  let html="";
  stages.forEach((st,si)=>{
    const cards=recs.filter(r=>r.stage===st);
    html+=`<div class="col col${si} fadeblk" data-stage="${esc(st)}" ondragover="allowDrop(event,this)" ondragleave="this.classList.remove('dover')" ondrop="dropCol(event,this)" style="transition-delay:${si*0.08}s"><div class="colhead">${esc(st)}<span class="cnt">${cards.length}</span></div><div class="cards">`;
    if(!cards.length) html+=`<div class="empty">—</div>`;
    cards.forEach(r=>{
      const col=topicColor(r.topic);
      const url=r.result_link?`<a class="lk" href="${esc(r.result_link)}" target="_blank" onclick="event.stopPropagation()">결과↗</a>`:"";
      const curl=centerURL(r.center);
      const cen=r.center?(curl?`<a class="lk" href="${esc(curl)}" target="_blank" onclick="event.stopPropagation()">${esc(r.center)}↗</a>`:esc(r.center)):"";
      let meta=[];
      if(cen) meta.push("센터: "+cen);
      if(r.request_date) meta.push("의뢰 "+esc(r.request_date));
      if(r.result_date) meta.push("결과 "+esc(r.result_date));
      if(r.interpretation) meta.push("解 "+esc(r.interpretation.slice(0,40)));
      else if(r.note) meta.push(esc(r.note.slice(0,40)));
      const star=r.essential?`<span style="color:#FA901E" title="필수">★</span> `:"";
      html+=`<div class="card" draggable="true" ondragstart='dragStart(event,${JSON.stringify(r.id)})' ondragend="dragEnd(event)" style="border-left-color:${col}" onclick='openEdit(${JSON.stringify(r.id)})'>
        <div class="a">${star}${esc(r.analysis||"(분석)")}</div>
        <div class="s">${esc(r.sample||"")}</div>
        <div class="meta">${meta.join("<br>")} ${url}</div>
        <span class="tg" style="background:${col}">${esc(r.topic)}</span>
      </div>`;
    });
    html+=`</div></div>`;
  });
  document.getElementById("board").innerHTML=html;
  document.getElementById("foot").textContent=`총 ${DATA.records.length}건 · 주제 ${DATA.meta.topics.length} · 단계 ${stages.length}`;
  document.getElementById("dl_topic").innerHTML=DATA.meta.topics.map(t=>`<option value="${esc(t)}">`).join("");
  document.getElementById("dl_center").innerHTML=(DATA.centers||[]).map(c=>`<option value="${esc(c.name)}">`).join("");
  document.getElementById("f_stage").innerHTML=stages.map(s=>`<option value="${esc(s)}">${esc(s)}</option>`).join("");
  requestAnimationFrame(()=>document.querySelectorAll(".fadeblk").forEach(e=>e.classList.add("visible")));
  persist();
}
function setF(t){filter=t;render();}
function toggleEss(){essOnly=!essOnly;render();}
// ---- drag & drop (단계 이동) ----
let dragId=null;
function dragStart(ev,id){dragId=id; ev.dataTransfer.effectAllowed="move"; try{ev.dataTransfer.setData("text/plain",id);}catch(e){} const c=ev.target.closest(".card"); if(c)c.classList.add("dragging");}
function dragEnd(ev){const c=ev.target.closest&&ev.target.closest(".card"); if(c)c.classList.remove("dragging"); document.querySelectorAll(".col.dover").forEach(e=>e.classList.remove("dover"));}
function allowDrop(ev,el){ev.preventDefault(); ev.dataTransfer.dropEffect="move"; if(el)el.classList.add("dover");}
function dropCol(ev,el){ev.preventDefault(); el.classList.remove("dover");
  const id=dragId||(ev.dataTransfer&&ev.dataTransfer.getData("text/plain"));
  const st=el.getAttribute("data-stage");
  const r=DATA.records.find(x=>x.id===id);
  if(r&&st&&r.stage!==st){r.stage=st; render();}
  dragId=null;}
function renderCenters(){
  let h="";
  (DATA.centers||[]).forEach(c=>{
    if(!c.note && !c.url) return;
    const nm=c.url?`<a href="${esc(c.url)}" target="_blank">${esc(c.name)} ↗</a>`:esc(c.name);
    h+=`<div class="cen"><div class="cn">${nm}</div>${c.note?`<div class="cnote">${esc(c.note)}</div>`:""}</div>`;
  });
  document.getElementById("centers").innerHTML=h;
}
function toggleCenters(){const e=document.getElementById("centers");e.style.display=(e.style.display==="none"?"flex":"none");}

function openAdd(){
  document.getElementById("mtitle").textContent="분석 추가";
  ["id","sample","analysis","center","request_date","result_date","result_link","interpretation","note"].forEach(k=>document.getElementById("f_"+k).value="");
  document.getElementById("f_topic").value=(filter!=="ALL"?filter:DATA.meta.topics[0]||"");
  document.getElementById("f_stage").value=stages[0];
  document.getElementById("f_essential").value="false";
  document.getElementById("btnDel").style.display="none";
  document.getElementById("ovl").classList.add("on");
}
function openEdit(id){
  const r=DATA.records.find(x=>x.id===id); if(!r)return;
  document.getElementById("mtitle").textContent="분석 편집";
  document.getElementById("f_id").value=r.id;
  ["topic","sample","analysis","center","stage","request_date","result_date","result_link","interpretation","note"].forEach(k=>document.getElementById("f_"+k).value=r[k]||"");
  document.getElementById("f_essential").value=r.essential?"true":"false";
  document.getElementById("btnDel").style.display="block";
  document.getElementById("ovl").classList.add("on");
}
function closeModal(){document.getElementById("ovl").classList.remove("on");}
function saveRec(){
  const id=document.getElementById("f_id").value;
  const get=k=>document.getElementById("f_"+k).value.trim();
  const rec={topic:get("topic"),sample:get("sample"),analysis:get("analysis"),center:get("center"),
    stage:get("stage")||stages[0],request_date:get("request_date"),result_date:get("result_date"),
    result_link:get("result_link"),interpretation:get("interpretation"),note:get("note"),
    essential:document.getElementById("f_essential").value==="true"};
  if(!rec.topic){alert("연구주제를 입력하세요");return;}
  if(rec.topic && !DATA.meta.topics.includes(rec.topic)) DATA.meta.topics.push(rec.topic);
  if(id){ const r=DATA.records.find(x=>x.id===id); Object.assign(r,rec); }
  else { rec.id=(rec.topic.toLowerCase().replace(/[^a-z0-9]/g,"")||"rec")+"-"+Date.now().toString(36); DATA.records.push(rec); }
  closeModal();render();
}
function delRec(){
  const id=document.getElementById("f_id").value;
  if(id && confirm("이 분석 항목을 삭제할까요?")){ DATA.records=DATA.records.filter(x=>x.id!==id); closeModal();render(); }
}
function exportJSON(){
  const out={meta:DATA.meta,centers:DATA.centers,records:DATA.records};
  out.meta.updated=new Date().toISOString().slice(0,10);
  const blob=new Blob([JSON.stringify(out,null,2)],{type:"application/json"});
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="analysis_board.json";a.click();
}
function importJSON(ev){
  const f=ev.target.files[0]; if(!f)return;
  const rd=new FileReader();
  rd.onload=()=>{ try{ DATA=JSON.parse(rd.result); render(); alert("불러오기 완료"); }catch(e){ alert("JSON 파싱 실패: "+e); } };
  rd.readAsText(f);
}
document.getElementById("ovl").addEventListener("click",e=>{if(e.target.id==="ovl")closeModal();});
function applyHash(){
  const m=(location.hash||"").match(/topic=([^&]+)/);
  if(m){ const t=decodeURIComponent(m[1]); filter=(t==="ALL"||DATA.meta.topics.includes(t))?t:"ALL"; }
}
applyHash();
window.addEventListener("hashchange",()=>{applyHash();render();});
render();
renderCenters();
</script>
</body>
</html>
"""

html = TEMPLATE.replace("__DATA__", data_js).replace("__GENERATED_AT__", generated_at)
with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("built:", HTML_PATH)
print("records:", len(data["records"]), "| topics:", data["meta"]["topics"])
