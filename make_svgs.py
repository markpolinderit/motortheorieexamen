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


print("borden:", len(os.listdir(D)))
