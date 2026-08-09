import os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(D, exist_ok=True)

def w(name, body, vb="0 0 200 200", extra=""):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" {extra}>{body}</svg>'
    open(os.path.join(D, name + ".svg"), "w", encoding="utf-8").write(svg)

# ---------- Verkeersborden ----------
w("bord-b1", '''
<title>Bord B1 voorrangsweg</title>
<rect width="200" height="200" fill="#eef2f7"/>
<g transform="translate(100,100)">
  <rect x="-62" y="-62" width="124" height="124" transform="rotate(45)" fill="#fff" stroke="#111" stroke-width="3"/>
  <rect x="-44" y="-44" width="88" height="88" transform="rotate(45)" fill="#f5c400"/>
</g>''')

w("bord-b6", '''
<title>Bord B6 verleen voorrang</title>
<rect width="200" height="200" fill="#eef2f7"/>
<polygon points="20,45 180,45 100,178" fill="#fff" stroke="#111" stroke-width="2"/>
<polygon points="20,45 180,45 100,178" fill="none" stroke="#d0021b" stroke-width="18"/>''')

w("bord-b7", '''
<title>Bord B7 stop</title>
<rect width="200" height="200" fill="#eef2f7"/>
<polygon points="60,22 140,22 178,60 178,140 140,178 60,178 22,140 22,60"
  fill="#d0021b" stroke="#fff" stroke-width="6"/>
<text x="100" y="118" font-family="Arial,Helvetica,sans-serif" font-size="46" font-weight="bold"
  fill="#fff" text-anchor="middle">STOP</text>''')

w("bord-a1-50", '''
<title>Bord A1 maximumsnelheid 50</title>
<rect width="200" height="200" fill="#eef2f7"/>
<circle cx="100" cy="100" r="82" fill="#fff" stroke="#111" stroke-width="2"/>
<circle cx="100" cy="100" r="72" fill="none" stroke="#d0021b" stroke-width="20"/>
<text x="100" y="126" font-family="Arial,Helvetica,sans-serif" font-size="70" font-weight="bold"
  fill="#111" text-anchor="middle">50</text>''')

w("bord-a1-30", '''
<title>Bord A1 maximumsnelheid 30</title>
<rect width="200" height="200" fill="#eef2f7"/>
<circle cx="100" cy="100" r="82" fill="#fff" stroke="#111" stroke-width="2"/>
<circle cx="100" cy="100" r="72" fill="none" stroke="#d0021b" stroke-width="20"/>
<text x="100" y="126" font-family="Arial,Helvetica,sans-serif" font-size="70" font-weight="bold"
  fill="#111" text-anchor="middle">30</text>''')

w("bord-f1", '''
<title>Bord F1 verbod voor bestuurders elkaar in te halen</title>
<rect width="200" height="200" fill="#eef2f7"/>
<circle cx="100" cy="100" r="82" fill="#fff" stroke="#111" stroke-width="2"/>
<circle cx="100" cy="100" r="72" fill="none" stroke="#d0021b" stroke-width="18"/>
<g>
  <rect x="60" y="72" width="26" height="56" rx="6" fill="#d0021b"/>
  <rect x="64" y="82" width="18" height="14" rx="3" fill="#fff" opacity=".65"/>
  <rect x="114" y="72" width="26" height="56" rx="6" fill="#111"/>
  <rect x="118" y="82" width="18" height="14" rx="3" fill="#fff" opacity=".55"/>
</g>''')

w("bord-d1", '''
<title>Bord D1 rotonde, verplichte rijrichting</title>
<rect width="200" height="200" fill="#eef2f7"/>
<circle cx="100" cy="100" r="82" fill="#0b57a4" stroke="#fff" stroke-width="6"/>
<g fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round">
  <path d="M100 46 A54 54 0 0 1 147 73"/>
  <path d="M147 127 A54 54 0 0 1 100 154"/>
  <path d="M53 73 A54 54 0 0 1 53 127" />
</g>
<g fill="#fff">
  <polygon points="150,60 162,80 138,80"/>
  <polygon points="92,158 112,146 112,170"/>
  <polygon points="50,142 38,122 62,122"/>
</g>''')

w("bord-c11", '''
<title>Bord C11 gesloten voor motorfietsen</title>
<rect width="200" height="200" fill="#eef2f7"/>
<circle cx="100" cy="100" r="82" fill="#fff" stroke="#111" stroke-width="2"/>
<circle cx="100" cy="100" r="72" fill="none" stroke="#d0021b" stroke-width="18"/>
<g fill="#111">
  <circle cx="68" cy="126" r="17" fill="none" stroke="#111" stroke-width="7"/>
  <circle cx="134" cy="126" r="17" fill="none" stroke="#111" stroke-width="7"/>
  <path d="M60 118 L92 96 L120 96 L138 120" fill="none" stroke="#111" stroke-width="8" stroke-linejoin="round"/>
  <path d="M92 96 L104 76 L124 76" fill="none" stroke="#111" stroke-width="8" stroke-linecap="round"/>
  <circle cx="104" cy="72" r="11"/>
</g>''')

w("bord-j1", '''
<title>Bord J1 gevaarlijke bocht naar rechts</title>
<rect width="200" height="200" fill="#eef2f7"/>
<polygon points="100,22 182,166 18,166" fill="#fff" stroke="#111" stroke-width="2"/>
<polygon points="100,22 182,166 18,166" fill="none" stroke="#d0021b" stroke-width="16"/>
<path d="M88 148 L88 110 Q88 88 112 88" fill="none" stroke="#111" stroke-width="11" stroke-linecap="square"/>
<polygon points="106,74 130,88 106,102" fill="#111"/>''')

w("bord-l2", '''
<title>Bord L2 doodlopende weg</title>
<rect width="200" height="200" fill="#eef2f7"/>
<rect x="24" y="24" width="152" height="152" fill="#0b57a4" stroke="#fff" stroke-width="6"/>
<rect x="92" y="66" width="16" height="90" fill="#fff"/>
<rect x="60" y="52" width="80" height="16" fill="#d0021b"/>''')

w("bord-g5", '''
<title>Bord G5 erf (woonerf)</title>
<rect width="200" height="200" fill="#eef2f7"/>
<rect x="24" y="24" width="152" height="152" fill="#0b57a4" stroke="#fff" stroke-width="6"/>
<g fill="#fff">
  <path d="M52 120 L78 96 L104 120 Z"/>
  <rect x="62" y="118" width="32" height="30"/>
  <circle cx="128" cy="104" r="9"/>
  <rect x="122" y="116" width="13" height="30" rx="5"/>
  <circle cx="150" cy="112" r="7"/>
  <rect x="145" y="122" width="10" height="24" rx="4"/>
</g>''')

w("bord-c1", '''
<title>Bord C1 gesloten in beide richtingen</title>
<rect width="200" height="200" fill="#eef2f7"/>
<circle cx="100" cy="100" r="82" fill="#d0021b" stroke="#fff" stroke-width="5"/>
<rect x="34" y="86" width="132" height="28" fill="#fff"/>''')

# ---------- Verkeerssituaties ----------
ROAD = '<rect width="360" height="240" fill="#e8efe6"/>'

def bike(x, y, s=1, c="#1c7ed6"):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<circle cx="-14" cy="10" r="9" fill="none" stroke="#333" stroke-width="3"/>'
            f'<circle cx="14" cy="10" r="9" fill="none" stroke="#333" stroke-width="3"/>'
            f'<path d="M-14 10 L0 -4 L14 10" fill="none" stroke="{c}" stroke-width="4"/>'
            f'<path d="M0 -4 L4 -16" stroke="{c}" stroke-width="4"/>'
            f'<circle cx="4" cy="-22" r="6" fill="#444"/></g>')

def car(x, y, w_=46, h_=26, c="#d0021b", rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="{-w_/2}" y="{-h_/2}" width="{w_}" height="{h_}" rx="6" fill="{c}"/>'
            f'<rect x="{-w_/2+8}" y="{-h_/2+4}" width="{w_-24}" height="{h_-8}" rx="3" fill="#fff" opacity=".55"/>'
            f'</g>')

def moto(x, y, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot})">'
            f'<rect x="-13" y="-9" width="26" height="18" rx="7" fill="#222"/>'
            f'<circle cx="0" cy="-14" r="7" fill="#f5c400"/>'
            f'<circle cx="-13" cy="12" r="4" fill="#333"/><circle cx="13" cy="12" r="4" fill="#333"/>'
            f'</g>')

w("scene-kruispunt-rechts", ROAD + f'''
<title>Gelijkwaardig kruispunt met een auto van rechts</title>
<rect x="130" y="0" width="100" height="240" fill="#8d8d8d"/>
<rect x="0" y="90" width="360" height="90" fill="#8d8d8d"/>
<g stroke="#fff" stroke-width="4" stroke-dasharray="14 14">
  <line x1="180" y1="0" x2="180" y2="80"/><line x1="180" y1="190" x2="180" y2="240"/>
  <line x1="0" y1="135" x2="120" y2="135"/><line x1="240" y1="135" x2="360" y2="135"/>
</g>
{moto(180,210)}
{car(300,120,rot=180)}
<text x="300" y="100" font-family="Arial" font-size="13" fill="#111" text-anchor="middle">auto van rechts</text>
<text x="180" y="234" font-family="Arial" font-size="13" fill="#111" text-anchor="middle">jij</text>
''', vb="0 0 360 240")

w("scene-rotonde", ROAD + f'''
<title>Rotonde met naderend verkeer</title>
<circle cx="180" cy="120" r="92" fill="#8d8d8d"/>
<circle cx="180" cy="120" r="42" fill="#cfe3c6" stroke="#fff" stroke-width="4"/>
<rect x="150" y="200" width="60" height="40" fill="#8d8d8d"/>
<rect x="0" y="100" width="90" height="50" fill="#8d8d8d"/>
<rect x="270" y="100" width="90" height="50" fill="#8d8d8d"/>
{moto(180,222)}
{car(120,60,rot=35)}
<text x="180" y="236" font-family="Arial" font-size="13" fill="#111" text-anchor="middle">jij</text>
''', vb="0 0 360 240")

w("scene-fietser-rechts", ROAD + f'''
<title>Fietser rechts naast je terwijl je rechtsaf wilt</title>
<rect x="0" y="70" width="360" height="110" fill="#8d8d8d"/>
<rect x="0" y="150" width="360" height="30" fill="#c0392b" opacity=".6"/>
<rect x="230" y="150" width="90" height="90" fill="#8d8d8d"/>
<line x1="0" y1="112" x2="360" y2="112" stroke="#fff" stroke-width="4" stroke-dasharray="16 14"/>
{moto(150,130,rot=90)}
{bike(150,166,1)}
<text x="150" y="60" font-family="Arial" font-size="13" fill="#111" text-anchor="middle">jij wilt rechtsaf</text>
''', vb="0 0 360 240")

w("scene-inhalen", ROAD + f'''
<title>Inhalen op een weg buiten de bebouwde kom</title>
<rect x="0" y="80" width="360" height="100" fill="#8d8d8d"/>
<line x1="0" y1="130" x2="360" y2="130" stroke="#fff" stroke-width="4" stroke-dasharray="26 18"/>
{moto(90,155,rot=90)}
{car(190,155,c="#2b6cb0")}
{car(300,105,c="#444",rot=180)}
<text x="300" y="88" font-family="Arial" font-size="13" fill="#111" text-anchor="middle">tegenligger</text>
<text x="90" y="190" font-family="Arial" font-size="13" fill="#111" text-anchor="middle">jij</text>
''', vb="0 0 360 240")

w("scene-voetganger-tussen-autos", ROAD + f'''
<title>Voetganger stapt tussen geparkeerde auto's vandaan</title>
<rect x="0" y="90" width="360" height="100" fill="#8d8d8d"/>
<rect x="0" y="60" width="360" height="30" fill="#d9d2c5"/>
{car(70,78,c="#555")}{car(150,78,c="#777")}{car(250,78,c="#8a6d3b")}
<g transform="translate(200,112)">
  <circle cx="0" cy="-16" r="8" fill="#111"/>
  <rect x="-6" y="-8" width="12" height="26" rx="5" fill="#111"/>
</g>
{moto(160,165,rot=90)}
<text x="160" y="200" font-family="Arial" font-size="13" fill="#111" text-anchor="middle">jij, 50 km/u</text>
''', vb="0 0 360 240")

w("scene-file-snelweg", ROAD + f'''
<title>Stilstaande file op de snelweg</title>
<rect x="0" y="60" width="360" height="130" fill="#8d8d8d"/>
<line x1="0" y1="125" x2="360" y2="125" stroke="#fff" stroke-width="3" stroke-dasharray="24 18"/>
{car(250,95,c="#444")}{car(300,95,c="#c0392b")}
{car(255,155,c="#2b6cb0")}{car(310,155,c="#777")}
{moto(120,125,rot=90)}
<text x="120" y="200" font-family="Arial" font-size="13" fill="#111" text-anchor="middle">jij nadert de file</text>
''', vb="0 0 360 240")

w("scene-tram-bocht", ROAD + f'''
<title>Nat wegdek met tramrails in een bocht</title>
<rect x="0" y="70" width="360" height="120" fill="#6f6f6f"/>
<g stroke="#b8b8b8" stroke-width="5">
  <path d="M0 100 Q180 100 360 150" fill="none"/>
  <path d="M0 118 Q180 118 360 168" fill="none"/>
</g>
<ellipse cx="120" cy="165" rx="55" ry="14" fill="#4a6a8a" opacity=".5"/>
{moto(90,150,rot=100)}
<text x="250" y="205" font-family="Arial" font-size="13" fill="#111" text-anchor="middle">natte rails in de bocht</text>
''', vb="0 0 360 240")

print("done", len(os.listdir(D)))
