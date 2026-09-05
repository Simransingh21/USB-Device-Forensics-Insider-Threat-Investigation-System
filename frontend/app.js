const API="http://127.0.0.1:8000";
const $=s=>document.querySelector(s);
const content=$("#content"), message=$("#message"), scanBtn=$("#scanBtn");
let latestScanId=localStorage.getItem("latestScanId");

async function api(path,options={}){
 const r=await fetch(API+path,{...options,headers:{"Content-Type":"application/json",...(options.headers||{})}});
 if(!r.ok){let e="Request failed";try{const d=await r.json();e=d.detail||e}catch{}throw Error(e)}
 return r.json();
}
function msg(text,error=false){message.textContent=text;message.className="message"+(error?" error":"")}
function clearMsg(){message.className="message hidden"}

function dashboardTemplate(d){
 const x=d?.data||{};
 return `<div class="cards">
 <div class="card"><div class="label">Total Scans</div><div class="value">${x.total_scans??0}</div></div>
 <div class="card"><div class="label">USB Devices</div><div class="value">${x.total_usb_devices??0}</div></div>
 <div class="card"><div class="label">Event Logs</div><div class="value">${x.total_event_logs??0}</div></div>
 <div class="card"><div class="label">Findings</div><div class="value">${x.total_findings??0}</div></div></div>
 <div class="grid">
 <div class="card"><h3>System Status</h3><p class="green">● ${x.system_health||"Healthy"}</p><p class="label">Latest scan: ${x.last_scan||"No scan yet"}</p></div>
 <div class="card"><h3>Latest Investigation</h3><p>${latestScanId?`Scan ID <b>#${latestScanId}</b>`:"No investigation started"}</p><p class="label">Click “Start Investigation” to collect current Windows evidence.</p></div></div>
 <div class="card" style="margin-top:15px"><h3>System Overview</h3><p class="label">Collects USB registry artifacts and Windows event logs, builds a forensic timeline, analyzes suspicious activity, and generates a PDF investigation report.</p></div>`;
}
async function loadDashboard(){
 $("#pageTitle").textContent="Investigation Dashboard";$("#subtitle").textContent="USB device forensic monitoring";clearMsg();
 try{content.innerHTML="<div class='card'>Loading dashboard...</div>";content.innerHTML=dashboardTemplate(await api("/dashboard/"))}
 catch(e){msg(e.message,true);content.innerHTML="<div class='card empty'>Unable to load dashboard.</div>"}
}
async function startScan(){
 scanBtn.disabled=true;scanBtn.textContent="⏳ Scanning...";
 try{const r=await api("/scan/start",{method:"POST"});latestScanId=r?.data?.scan_id;if(latestScanId)localStorage.setItem("latestScanId",latestScanId);await loadDashboard();msg(`Investigation completed successfully. Scan ID: ${latestScanId}`)}
 catch(e){msg(e.message,true)}
 finally{scanBtn.disabled=false;scanBtn.textContent="▶ Start Investigation"}
}
async function timeline(){
 $("#pageTitle").textContent="Investigation Timeline";$("#subtitle").textContent=`Scan #${latestScanId||"—"}`;clearMsg();
 if(!latestScanId){content.innerHTML="<div class='card empty'>Start an investigation first.</div>";return}
 try{const r=await api(`/timeline/${latestScanId}`);const ev=r?.data?.events||[];content.innerHTML=`<div class="card"><h3>Evidence Timeline</h3>${ev.length?ev.map(e=>`<div class="timeline-item"><b>${e.source||"Event"}</b><span>${e.time||""} · Event ID ${e.event_id??"—"}</span></div>`).join(""):"<div class='empty'>No events found.</div>"}</div>`}catch(e){msg(e.message,true)}
}
async function findings(){
 $("#pageTitle").textContent="Suspicious Findings";$("#subtitle").textContent=`Scan #${latestScanId||"—"}`;clearMsg();
 if(!latestScanId){content.innerHTML="<div class='card empty'>Start an investigation first.</div>";return}
 try{const r=await api(`/suspicious/${latestScanId}`);const f=r?.data?.findings||[];content.innerHTML=`<div class="card"><h3>Risk Analysis</h3>${f.length?f.map(x=>`<div class="finding"><span class="sev pill ${String(x.severity).toLowerCase().includes("high")?"red":String(x.severity).toLowerCase().includes("medium")?"yellow":"blue"}">${x.severity||"INFO"}</span><b>${x.reason||"Suspicious activity"}</b><div class="label" style="margin-top:7px">${x.time||""}</div></div>`).join(""):"<div class='empty'>No suspicious findings.</div>"}</div>`}catch(e){msg(e.message,true)}
}
function report(){
 $("#pageTitle").textContent="Investigation Report";$("#subtitle").textContent=`Scan #${latestScanId||"—"}`;clearMsg();
 content.innerHTML=`<div class="card report-box"><div><h3>Forensic Investigation Report</h3><div class="label">Generate and download the PDF evidence report for the latest scan.</div></div><button class="primary" ${latestScanId?"":"disabled"} onclick="window.open('${API}/report/${latestScanId||""}','_blank')">Download PDF</button></div>`;
}
function view(v){if(v==="dashboard")loadDashboard();else if(v==="timeline")timeline();else if(v==="findings")findings();else report()}
document.querySelectorAll(".nav").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll(".nav").forEach(x=>x.classList.remove("active"));b.classList.add("active");view(b.dataset.view)}));
scanBtn.addEventListener("click",startScan);loadDashboard();
