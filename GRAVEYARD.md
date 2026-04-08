# Code Graveyard — dropInStructure

Code removed during cleanup on 2026-04-08. Each section includes context about why it was removed and where it lived in `index.html`.

---

## 1. Bloop Audio System (removed: unused after sorting sounds were disabled)

Originally at lines ~3519-3529. The `_BLOOP_C` data URI was a ~36KB base64 WAV file used for a "bloop" sound when cards landed in sort buckets during the sorting game. The sound was disabled by commenting out `playBloop()` calls, making the entire audio pipeline dead code.

```javascript
// ── Bloops from audio file ──
// ── Bloop C (from recording) ──
const _BLOOP_C = "data:audio/wav;base64,..."; // ~36KB base64 WAV omitted for size

function playBell() {
  try {
    const a = new Audio(_BLOOP_C);
    a.volume = 0.85;
    a.play().catch(() => {});
  } catch(e) {}
}
const playBloop = playBell;
```

---

## 2. First `exitSortBoard()` definition (removed: overwritten by later definition)

Originally at lines ~3715-3740. This was the first definition, but a second definition at ~line 4218 overwrote it. The second definition includes `_sortBucketFilter = null` for scoped sorting support and has the same notice-refresh logic. The first definition's `_clearHeld()` call was unique but not needed after the gameboard refactor.

```javascript
function exitSortBoard() {
  const phase = document.getElementById('sort-card-phase');
  if (phase) phase.style.display = 'none';
  _clearHeld();
  document.getElementById('sort-input-phase').style.display = '';
  document.getElementById('sort-done-phase').style.display = 'none';
  const cui = document.getElementById('sort-completion-ui');
  if (cui) cui.style.display = 'none';
  (function updateSortNoticeRefresh() {
    const el = document.getElementById('sort-existing-notice');
    if (!el) return;
    const items = loadSortItems();
    const pending = SORT_ROUNDS.filter(r => r.queue(items).length > 0);
    if (items.length > 0) {
      const pendingCount = pending.reduce((s,r) => s + r.queue(items).length, 0);
      if (pendingCount > 0) {
        el.innerHTML = `<span style="border-bottom:1px dashed rgba(48,28,29,0.4);">${items.length} items · ${pendingCount} need sorting → continue</span>`;
      } else {
        el.textContent = `${items.length} item${items.length===1?'':'s'} · all sorted`;
      }
    }
  })();
}
window.exitSortBoard = exitSortBoard;
```

---

## 3. Round 7 Completion System (removed: permanently disabled, queue returns [])

The completion round was designed to prompt users for duration and date after sorting. It was disabled by setting `queue: items => []` so the round was never reached. All supporting UI and JS were dead code.

### 3a. HTML — Completion overlay UI (originally at lines ~2418-2438)

```html
<div id="sort-completion-ui" style="display:none;position:absolute;inset:0;z-index:30;align-items:center;justify-content:center;background:rgba(48,28,29,0.95);">
  <div style="background:#F7B338;border:2px solid #301C1D;padding:28px;max-width:460px;width:90vw;box-sizing:border-box;">
    <div id="sort-comp-title" style="font-family:'Archivo Black',sans-serif;font-size:20px;color:#301C1D;margin-bottom:18px;text-align:center;"></div>
    <div style="margin-bottom:14px;text-align:center;">
      <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(48,28,29,0.55);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;">How long did it take?</div>
      <div style="display:flex;gap:8px;align-items:center;justify-content:center;">
        <input id="sort-dur-input" type="number" min="1" max="999" placeholder="mins"
          style="background:#FFFEE7;border:2px solid #301C1D;color:#301C1D;font-family:'Space Mono',monospace;font-size:16px;padding:8px 12px;width:90px;outline:none;text-align:center;"
          onkeydown="if(event.key==='Enter')submitCompletionCard()"/>
        <span style="font-family:'Space Mono',monospace;font-size:11px;color:rgba(48,28,29,0.4);">minutes</span>
      </div>
    </div>
    <div style="margin-bottom:18px;text-align:center;">
      <div style="font-family:'Space Mono',monospace;font-size:10px;color:rgba(48,28,29,0.55);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:6px;">When?</div>
      <div id="sort-date-btns" style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center;"></div>
    </div>
    <div style="text-align:center;">
      <button onclick="submitCompletionCard()" style="background:#301C1D;border:2px solid #301C1D;color:#FFFEE7;font-family:'Space Mono',monospace;font-size:13px;letter-spacing:0.08em;text-transform:uppercase;padding:11px 24px;cursor:pointer;">Save &amp; Next &rarr;</button>
    </div>
  </div>
</div>
```

### 3b. JS — Completion round logic in showSortCard (originally at lines ~4128-4164)

```javascript
// Special completion round: show dedicated overlay
if (round.special === 'completion') {
  const tile = document.getElementById('sort-card-tile');
  if (tile) tile.style.display = 'none';

  const today = new Date(); const yd = new Date(today); yd.setDate(yd.getDate()-1);
  const fmt = d => `${d.getMonth()+1}/${d.getDate()}/${String(d.getFullYear()).slice(-2)}`;

  const compTitle = document.getElementById('sort-comp-title');
  if (compTitle) compTitle.textContent = item.text;

  const dateBtns = document.getElementById('sort-date-btns');
  if (dateBtns) {
    dateBtns.innerHTML = `
      <button onclick="setCompletionDate('${fmt(today)}')" id="sort-date-today"
        style="background:#7FA497;border:2px solid #7FA497;color:#FFFEE7;font-family:'Archivo Black',sans-serif;font-size:13px;text-transform:uppercase;padding:8px 16px;cursor:pointer;">Today<br><span style="font-family:'Space Mono',monospace;font-size:9px;font-weight:normal;">${fmt(today)}</span></button>
      <button onclick="setCompletionDate('${fmt(yd)}')" id="sort-date-yesterday"
        style="background:none;border:2px solid #7FA497;color:#7FA497;font-family:'Archivo Black',sans-serif;font-size:13px;text-transform:uppercase;padding:8px 16px;cursor:pointer;">Yesterday<br><span style="font-family:'Space Mono',monospace;font-size:9px;font-weight:normal;">${fmt(yd)}</span></button>
      <input id="sort-date-other" type="text" placeholder="MM/DD/YY"
        style="background:none;border:2px solid rgba(48,28,29,0.3);color:#301C1D;font-family:'Space Mono',monospace;font-size:13px;padding:8px 10px;width:100px;outline:none;text-align:center;"
        oninput="setCompletionDate(this.value)" />`;
  }

  const durInput = document.getElementById('sort-dur-input');
  if (durInput) durInput.value = '';
  window._sortCompletionDate = fmt(today);

  const cui = document.getElementById('sort-completion-ui');
  if (cui) { cui.style.display = 'flex'; }
  return;
} else {
  const cui = document.getElementById('sort-completion-ui');
  if (cui) cui.style.display = 'none';
}
```

### 3c. JS — Completion date/submit functions (originally at lines ~4167-4195)

```javascript
let _sortCompletionDate = null;

function setCompletionDate(val) {
  window._sortCompletionDate = val;
  const td = document.getElementById('sort-date-today');
  const yd = document.getElementById('sort-date-yesterday');
  const od = document.getElementById('sort-date-other');
  const today = new Date(); const yesterday = new Date(today); yesterday.setDate(yesterday.getDate()-1);
  const fmt = d => `${d.getMonth()+1}/${d.getDate()}/${String(d.getFullYear()).slice(-2)}`;
  if (td) td.style.background = val === fmt(today) ? '#7FA497' : 'none';
  if (yd) { yd.style.background = val === fmt(yesterday) ? '#7FA497' : 'none'; yd.style.color = val === fmt(yesterday) ? '#FFFEE7' : '#7FA497'; }
}

function submitCompletionCard() {
  const minsInput = document.getElementById('sort-dur-input');
  const mins = minsInput ? parseInt(minsInput.value) : null;
  const date = window._sortCompletionDate;
  const item = sortQueue[sortQueueIdx];
  sortHistory.push({ id: item.id, field: 'completedOn', prev: item.completedOn, extraField: 'completedMins', prevExtra: item.completedMins });
  item.completedOn = date || null;
  item.completedMins = mins || null;
  saveSortItems(sortAllItems);
  sortQueueIdx++;
  window._sortCompletionDate = null;
  showSortCard();
}
window.setCompletionDate = setCompletionDate;
window.submitCompletionCard = submitCompletionCard;
```
