"""Write a tiny dependency-free SVG map for the agent-attack research workflow."""
from pathlib import Path

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="560" viewBox="0 0 1200 560">
<rect width="1200" height="560" fill="#fafafa"/><style>text{font:16px sans-serif;fill:#17202a}.box{fill:#eaf2f8;stroke:#2874a6;stroke-width:2}.surf{fill:#fef2e6;stroke:#b9770e;stroke-width:2}.arr{stroke:#566573;stroke-width:2;marker-end:url(#a)}</style>
<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#566573"/></marker></defs>
<text x="40" y="38" font-size="25" font-weight="bold">Agent-attack research workflow</text>
<g class="box"><rect x="40" y="80" width="160" height="58" rx="10"/><rect x="240" y="80" width="190" height="58" rx="10"/><rect x="470" y="80" width="160" height="58" rx="10"/><rect x="670" y="80" width="180" height="58" rx="10"/><rect x="890" y="80" width="220" height="58" rx="10"/></g>
<g text-anchor="middle"><text x="120" y="115">P0 scope + ethics</text><text x="335" y="115">P1 literature + KB</text><text x="550" y="115">P2 ideas</text><text x="760" y="115">P3 threat model</text><text x="1000" y="115">P4 baselines</text></g>
<path class="arr" d="M200 109h38M430 109h38M630 109h38M850 109h38" fill="none"/>
<g class="surf"><rect x="110" y="220" width="290" height="78" rx="12"/><rect x="455" y="220" width="290" height="78" rx="12"/><rect x="800" y="220" width="290" height="78" rx="12"/></g>
<g text-anchor="middle"><text x="255" y="252" font-weight="bold">01 external interaction</text><text x="255" y="277">web · GUI · tool/MCP · evidence</text><text x="600" y="252" font-weight="bold">02 internal cognition</text><text x="600" y="277">backdoor · memory · reasoning · privacy</text><text x="945" y="252" font-weight="bold">03 collaboration</text><text x="945" y="277">infection · tampering · collusion · belief</text></g>
<path class="arr" d="M1000 138v60M600 138v60M600 298v58" fill="none"/>
<g class="box"><rect x="430" y="360" width="340" height="58" rx="10"/><rect x="180" y="460" width="180" height="58" rx="10"/><rect x="440" y="460" width="180" height="58" rx="10"/><rect x="700" y="460" width="180" height="58" rx="10"/></g>
<g text-anchor="middle"><text x="600" y="395">P5 experiments → P6 falsify</text><text x="270" y="495">P7 paper + figures</text><text x="530" y="495">P8 review + disclosure</text><text x="790" y="495">redacted artifact</text></g>
<path class="arr" d="M500 418L330 455M600 418v38M700 418l170 37" fill="none"/>
</svg>'''
Path(__file__).with_name('bigmap.svg').write_text(SVG)
print('wrote bigmap.svg')
