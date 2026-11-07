"""Falsifier: recompute the toy claim from raw trial JSONL; exits 1 if the 10-point difference fails."""
from pathlib import Path
import json, sys
HERE = Path(__file__).resolve().parents[1]
rows = [json.loads(x) for x in (HERE/'results/trials.jsonl').read_text().splitlines() if x.strip()]
a = {arm: [r['success'] for r in rows if r['arm'] == arm] for arm in ('preserve','strip')}
diff = sum(a['strip'])/len(a['strip']) - sum(a['preserve'])/len(a['preserve'])
line = f"preserve={sum(a['preserve'])}/{len(a['preserve'])} strip={sum(a['strip'])}/{len(a['strip'])} difference={diff:.6f}\n"
(HERE/'falsify/C1').mkdir(parents=True, exist_ok=True)
(HERE/'falsify/C1/check.log').write_text(line)
print(line, end='')
sys.exit(0 if abs(diff) >= 0.10 else 1)
