# -*- coding: utf-8 -*-
"""Genereert verkeerssituaties in bestuurdersperspectief als SVG."""
import os

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(D, exist_ok=True)

W, H = 480, 300
HOR = 118          # horizon
CX = 240           # verdwijnpunt x


def yof(u):
    """u=1 vlak voor je, u->0 bij de horizon."""
    return HOR + (H - HOR) * u


def halfw(u):
    return 10 + 218 * u


def px(xf, u):
    return CX + xf * halfw(u)


# ---------------------------------------------------------------- omgeving
def sky(top="#8fc4e8", bot="#dcecf7"):
    return (f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/>'
            f'</linearGradient></defs>'
            f'<rect width="{W}" height="{HOR}" fill="url(#sky)"/>')


def ground(c="#7fa86b"):
    return f'<rect y="{HOR}" width="{W}" height="{H-HOR}" fill="{c}"/>'


def road(width=1.0, c="#5f6266"):
    a, b = 10 * width, 218 * width
    return (f'<polygon points="{CX-a},{HOR} {CX+a},{HOR} {CX+b+10},{H} {CX-b-10},{H}" fill="{c}"/>')


def midline(dash=True, c="#f2f2f2", xf=0.0):
    out = []
    if dash:
        u = 0.10
        while u < 1.05:
            u2 = min(u * 1.42, 1.15)
            y1, y2 = yof(min(u, 1)), yof(min(u2, 1))
            w1, w2 = max(1.2, 5 * u), max(1.6, 5 * u2)
            x1, x2 = px(xf, min(u, 1)), px(xf, min(u2, 1))
            out.append(f'<polygon points="{x1-w1},{y1} {x1+w1},{y1} {x2+w2},{y2} {x2-w2},{y2}" fill="{c}"/>')
            u *= 2.0
    else:
        out.append(f'<polygon points="{px(xf,0.02)-1.5},{yof(0.02)} {px(xf,0.02)+1.5},{yof(0.02)} '
                   f'{px(xf,1)+5},{H} {px(xf,1)-5},{H}" fill="{c}"/>')
    return "".join(out)


def edgelines(c="#f2f2f2"):
    return (midline(dash=False, c=c, xf=-0.97) + midline(dash=False, c=c, xf=0.97))


def verge_grass():
    return ""


def trees(side=-1, n=4, c="#3f6b3a"):
    out = []
    for i in range(n):
        u = 0.10 + i * 0.22
        if u > 1:
            break
        x = px(side * (1.35 + 0.1 * i), u)
        y = yof(u)
        s = 34 * u + 6
        out.append(f'<g transform="translate({x:.0f},{y:.0f})">'
                   f'<rect x="{-s*0.08:.1f}" y="{-s*0.5:.1f}" width="{s*0.16:.1f}" height="{s*0.5:.1f}" fill="#6b5236"/>'
                   f'<ellipse cx="0" cy="{-s*0.75:.1f}" rx="{s*0.42:.1f}" ry="{s*0.5:.1f}" fill="{c}"/></g>')
    return "".join(out)


def houses(side=-1, n=3):
    out = []
    cols = ["#b98a6a", "#a97a5c", "#c49a78"]
    for i in range(n):
        u = 0.14 + i * 0.26
        if u > 1.1:
            break
        x = px(side * (1.45 + 0.14 * i), min(u, 1))
        y = yof(min(u, 1))
        s = 70 * u + 10
        c = cols[i % 3]
        out.append(f'<g transform="translate({x:.0f},{y:.0f})">'
                   f'<rect x="{-s*0.5:.1f}" y="{-s*0.9:.1f}" width="{s:.1f}" height="{s*0.9:.1f}" fill="{c}"/>'
                   f'<polygon points="{-s*0.58:.1f},{-s*0.9:.1f} {s*0.58:.1f},{-s*0.9:.1f} 0,{-s*1.28:.1f}" fill="#7a4a3a"/>'
                   f'<rect x="{-s*0.28:.1f}" y="{-s*0.66:.1f}" width="{s*0.22:.1f}" height="{s*0.22:.1f}" fill="#dfeaf2"/>'
                   f'<rect x="{s*0.06:.1f}" y="{-s*0.66:.1f}" width="{s*0.22:.1f}" height="{s*0.22:.1f}" fill="#dfeaf2"/>'
                   f'</g>')
    return "".join(out)


def sidewalk(side=-1, c="#c9c4bb"):
    a = px(side * 1.0, 0.02)
    b = px(side * 1.0, 1.0)
    a2 = px(side * 1.45, 0.02)
    b2 = px(side * 1.6, 1.0)
    return f'<polygon points="{a},{yof(0.02)} {a2},{yof(0.02)} {b2},{H} {b},{H}" fill="{c}"/>'


# ---------------------------------------------------------------- objecten
def car_rear(xf, u, c="#c0392b", brake=False):
    w = 0.80 * halfw(u)
    w = min(w, 210)
    h = w * 0.78
    x, y = px(xf, u), yof(u)
    lights = "#ff2b2b" if brake else "#8c1d18"
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<ellipse cx="0" cy="0" rx="{w*0.52:.1f}" ry="{h*0.08:.1f}" fill="#000" opacity=".22"/>'
            f'<rect x="{-w/2:.1f}" y="{-h*0.62:.1f}" width="{w:.1f}" height="{h*0.62:.1f}" rx="{w*0.07:.1f}" fill="{c}"/>'
            f'<rect x="{-w*0.36:.1f}" y="{-h:.1f}" width="{w*0.72:.1f}" height="{h*0.42:.1f}" rx="{w*0.06:.1f}" fill="{c}"/>'
            f'<rect x="{-w*0.30:.1f}" y="{-h*0.95:.1f}" width="{w*0.60:.1f}" height="{h*0.30:.1f}" rx="{w*0.03:.1f}" fill="#3b4c5a"/>'
            f'<rect x="{-w*0.46:.1f}" y="{-h*0.42:.1f}" width="{w*0.16:.1f}" height="{h*0.16:.1f}" rx="2" fill="{lights}"/>'
            f'<rect x="{w*0.30:.1f}" y="{-h*0.42:.1f}" width="{w*0.16:.1f}" height="{h*0.16:.1f}" rx="2" fill="{lights}"/>'
            f'<rect x="{-w*0.13:.1f}" y="{-h*0.26:.1f}" width="{w*0.26:.1f}" height="{h*0.13:.1f}" rx="2" fill="#e8e8e8"/>'
            f'</g>')


def car_front(xf, u, c="#2c5f9e", lights=False, blink=None):
    w = min(0.80 * halfw(u), 210)
    h = w * 0.78
    x, y = px(xf, u), yof(u)
    lamp = "#fff6c8" if lights else "#dfe6ea"
    bl = ''
    if blink == "left":
        bl = f'<rect x="{-w*0.50:.1f}" y="{-h*0.30:.1f}" width="{w*0.12:.1f}" height="{h*0.12:.1f}" rx="2" fill="#ffa41b"/>'
    if blink == "right":
        bl = f'<rect x="{w*0.38:.1f}" y="{-h*0.30:.1f}" width="{w*0.12:.1f}" height="{h*0.12:.1f}" rx="2" fill="#ffa41b"/>'
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<ellipse cx="0" cy="0" rx="{w*0.52:.1f}" ry="{h*0.08:.1f}" fill="#000" opacity=".22"/>'
            f'<rect x="{-w/2:.1f}" y="{-h*0.62:.1f}" width="{w:.1f}" height="{h*0.62:.1f}" rx="{w*0.07:.1f}" fill="{c}"/>'
            f'<rect x="{-w*0.36:.1f}" y="{-h:.1f}" width="{w*0.72:.1f}" height="{h*0.42:.1f}" rx="{w*0.06:.1f}" fill="{c}"/>'
            f'<rect x="{-w*0.30:.1f}" y="{-h*0.95:.1f}" width="{w*0.60:.1f}" height="{h*0.30:.1f}" rx="{w*0.03:.1f}" fill="#5a6f80"/>'
            f'<rect x="{-w*0.46:.1f}" y="{-h*0.45:.1f}" width="{w*0.18:.1f}" height="{h*0.14:.1f}" rx="3" fill="{lamp}"/>'
            f'<rect x="{w*0.28:.1f}" y="{-h*0.45:.1f}" width="{w*0.18:.1f}" height="{h*0.14:.1f}" rx="3" fill="{lamp}"/>'
            f'<rect x="{-w*0.20:.1f}" y="{-h*0.22:.1f}" width="{w*0.40:.1f}" height="{h*0.10:.1f}" rx="2" fill="#111" opacity=".5"/>'
            + bl + '</g>')


def car_side(xf, u, c="#8e44ad", face=1, blink=None):
    """Auto van opzij (kruisend verkeer). face=1 rijdt naar rechts."""
    w = min(1.05 * halfw(u), 240)
    h = w * 0.42
    x, y = px(xf, u), yof(u)
    bl = (f'<rect x="{(w*0.40 if face>0 else -w*0.48):.1f}" y="{-h*0.55:.1f}" '
          f'width="{w*0.08:.1f}" height="{h*0.22:.1f}" fill="#ffa41b"/>') if blink else ''
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale({face},1)">'
            f'<ellipse cx="0" cy="0" rx="{w*0.52:.1f}" ry="{h*0.14:.1f}" fill="#000" opacity=".22"/>'
            f'<rect x="{-w/2:.1f}" y="{-h*0.75:.1f}" width="{w:.1f}" height="{h*0.62:.1f}" rx="{h*0.22:.1f}" fill="{c}"/>'
            f'<path d="M{-w*0.26:.1f} {-h*0.75:.1f} L{-w*0.16:.1f} {-h*1.18:.1f} L{w*0.20:.1f} {-h*1.18:.1f} '
            f'L{w*0.30:.1f} {-h*0.75:.1f} Z" fill="{c}"/>'
            f'<path d="M{-w*0.22:.1f} {-h*0.78:.1f} L{-w*0.14:.1f} {-h*1.10:.1f} L{w*0.16:.1f} {-h*1.10:.1f} '
            f'L{w*0.24:.1f} {-h*0.78:.1f} Z" fill="#6d8496"/>'
            f'<circle cx="{-w*0.28:.1f}" cy="{-h*0.10:.1f}" r="{h*0.24:.1f}" fill="#1c1c1c"/>'
            f'<circle cx="{w*0.30:.1f}" cy="{-h*0.10:.1f}" r="{h*0.24:.1f}" fill="#1c1c1c"/>'
            + bl + '</g>')


def truck_rear(xf, u, c="#e8e8e8", blink=None):
    w = min(1.05 * halfw(u), 250)
    h = w * 1.05
    x, y = px(xf, u), yof(u)
    bl = (f'<rect x="{(w*0.34 if blink=="right" else -w*0.46):.1f}" y="{-h*0.14:.1f}" '
          f'width="{w*0.12:.1f}" height="{h*0.08:.1f}" fill="#ffa41b"/>') if blink else ''
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<ellipse cx="0" cy="0" rx="{w*0.52:.1f}" ry="{h*0.05:.1f}" fill="#000" opacity=".25"/>'
            f'<rect x="{-w/2:.1f}" y="{-h:.1f}" width="{w:.1f}" height="{h*0.92:.1f}" rx="{w*0.03:.1f}" fill="{c}" stroke="#9aa3a9" stroke-width="1.5"/>'
            f'<rect x="{-w*0.44:.1f}" y="{-h*0.90:.1f}" width="{w*0.88:.1f}" height="{h*0.55:.1f}" fill="#cfd6da"/>'
            f'<rect x="{-w*0.46:.1f}" y="{-h*0.13:.1f}" width="{w*0.12:.1f}" height="{h*0.08:.1f}" fill="#8c1d18"/>'
            f'<rect x="{w*0.34:.1f}" y="{-h*0.13:.1f}" width="{w*0.12:.1f}" height="{h*0.08:.1f}" fill="#8c1d18"/>'
            + bl + '</g>')


def bus_side(xf, u, c="#1f6fb2", blink=False):
    w = min(1.5 * halfw(u), 300)
    h = w * 0.42
    x, y = px(xf, u), yof(u)
    win = "".join(f'<rect x="{-w*0.42 + i*w*0.16:.1f}" y="{-h*1.05:.1f}" width="{w*0.12:.1f}" '
                  f'height="{h*0.38:.1f}" fill="#cfe3f2"/>' for i in range(5))
    bl = (f'<rect x="{w*0.42:.1f}" y="{-h*0.55:.1f}" width="{w*0.06:.1f}" height="{h*0.20:.1f}" fill="#ffa41b"/>') if blink else ''
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<rect x="{-w/2:.1f}" y="{-h*1.25:.1f}" width="{w:.1f}" height="{h*1.15:.1f}" rx="{h*0.14:.1f}" fill="{c}"/>'
            + win +
            f'<circle cx="{-w*0.30:.1f}" cy="{-h*0.08:.1f}" r="{h*0.22:.1f}" fill="#1c1c1c"/>'
            f'<circle cx="{w*0.30:.1f}" cy="{-h*0.08:.1f}" r="{h*0.22:.1f}" fill="#1c1c1c"/>'
            + bl + '</g>')


def person(xf, u, c="#c0392b", scale=1.0, walk=0):
    s = (0.42 * halfw(u)) * scale
    x, y = px(xf, u), yof(u)
    leg = 0.30 if walk else 0.14
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<ellipse cx="0" cy="0" rx="{s*0.18:.1f}" ry="{s*0.05:.1f}" fill="#000" opacity=".22"/>'
            f'<circle cx="0" cy="{-s*0.86:.1f}" r="{s*0.13:.1f}" fill="#e8b98f"/>'
            f'<rect x="{-s*0.13:.1f}" y="{-s*0.74:.1f}" width="{s*0.26:.1f}" height="{s*0.40:.1f}" rx="{s*0.08:.1f}" fill="{c}"/>'
            f'<path d="M{-s*0.05:.1f} {-s*0.34:.1f} L{-s*leg:.1f} 0" stroke="#2f3640" stroke-width="{s*0.09:.1f}" stroke-linecap="round"/>'
            f'<path d="M{s*0.05:.1f} {-s*0.34:.1f} L{s*leg:.1f} 0" stroke="#2f3640" stroke-width="{s*0.09:.1f}" stroke-linecap="round"/>'
            f'</g>')


def child(xf, u, c="#f1c40f"):
    return person(xf, u, c=c, scale=0.62, walk=1)


def cyclist(xf, u, c="#f39c12", face=1):
    s = 0.55 * halfw(u)
    x, y = px(xf, u), yof(u)
    return (f'<g transform="translate({x:.0f},{y:.0f}) scale({face},1)">'
            f'<ellipse cx="0" cy="0" rx="{s*0.30:.1f}" ry="{s*0.06:.1f}" fill="#000" opacity=".22"/>'
            f'<circle cx="{-s*0.22:.1f}" cy="{-s*0.18:.1f}" r="{s*0.18:.1f}" fill="none" stroke="#2f3640" stroke-width="{s*0.045:.1f}"/>'
            f'<circle cx="{s*0.22:.1f}" cy="{-s*0.18:.1f}" r="{s*0.18:.1f}" fill="none" stroke="#2f3640" stroke-width="{s*0.045:.1f}"/>'
            f'<path d="M{-s*0.22:.1f} {-s*0.18:.1f} L{0:.1f} {-s*0.42:.1f} L{s*0.22:.1f} {-s*0.18:.1f}" fill="none" stroke="#555" stroke-width="{s*0.05:.1f}"/>'
            f'<path d="M{0:.1f} {-s*0.42:.1f} L{s*0.10:.1f} {-s*0.72:.1f}" stroke="{c}" stroke-width="{s*0.09:.1f}" stroke-linecap="round"/>'
            f'<rect x="{-s*0.10:.1f}" y="{-s*0.86:.1f}" width="{s*0.22:.1f}" height="{s*0.34:.1f}" rx="{s*0.08:.1f}" fill="{c}"/>'
            f'<circle cx="{s*0.02:.1f}" cy="{-s*0.98:.1f}" r="{s*0.12:.1f}" fill="#e8b98f"/>'
            f'</g>')


def moped(xf, u, c="#2d3436"):
    return cyclist(xf, u, c=c)


def tractor(xf, u):
    w = min(0.9 * halfw(u), 200)
    h = w * 0.85
    x, y = px(xf, u), yof(u)
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<rect x="{-w*0.38:.1f}" y="{-h*0.75:.1f}" width="{w*0.76:.1f}" height="{h*0.50:.1f}" fill="#2e7d32"/>'
            f'<rect x="{-w*0.30:.1f}" y="{-h*1.05:.1f}" width="{w*0.60:.1f}" height="{h*0.34:.1f}" fill="#1b5e20"/>'
            f'<rect x="{-w*0.24:.1f}" y="{-h*1.00:.1f}" width="{w*0.48:.1f}" height="{h*0.24:.1f}" fill="#9fc4d6"/>'
            f'<circle cx="{-w*0.34:.1f}" cy="{-h*0.16:.1f}" r="{h*0.26:.1f}" fill="#1c1c1c"/>'
            f'<circle cx="{w*0.34:.1f}" cy="{-h*0.16:.1f}" r="{h*0.26:.1f}" fill="#1c1c1c"/>'
            f'<rect x="{-w*0.44:.1f}" y="{-h*1.28:.1f}" width="{w*0.10:.1f}" height="{h*0.18:.1f}" fill="#f1c40f"/>'
            f'</g>')


def tram(xf, u):
    w = min(1.3 * halfw(u), 280)
    h = w * 0.55
    x, y = px(xf, u), yof(u)
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<rect x="{-w/2:.1f}" y="{-h*1.15:.1f}" width="{w:.1f}" height="{h*1.05:.1f}" rx="{h*0.16:.1f}" fill="#d6d6d6" stroke="#9aa3a9"/>'
            f'<rect x="{-w*0.44:.1f}" y="{-h*1.02:.1f}" width="{w*0.88:.1f}" height="{h*0.38:.1f}" fill="#7fb2d9"/>'
            f'<rect x="{-w/2:.1f}" y="{-h*0.42:.1f}" width="{w:.1f}" height="{h*0.10:.1f}" fill="#1f6fb2"/>'
            f'</g>')


def sign_post(xf, u, kind="b6", scale=1.0):
    s = 0.30 * halfw(u) * scale
    x, y = px(xf, u), yof(u)
    head = ""
    if kind == "b6":
        head = f'<polygon points="{-s:.1f},{-s*2.6:.1f} {s:.1f},{-s*2.6:.1f} 0,{-s*0.9:.1f}" fill="#fff" stroke="#d0021b" stroke-width="{s*0.34:.1f}"/>'
    elif kind == "b1":
        head = f'<rect x="{-s*0.72:.1f}" y="{-s*2.5:.1f}" width="{s*1.44:.1f}" height="{s*1.44:.1f}" transform="rotate(45 0 {-s*1.78:.1f})" fill="#f5c400" stroke="#fff" stroke-width="{s*0.18:.1f}"/>'
    elif kind == "a1":
        head = (f'<circle cx="0" cy="{-s*1.9:.1f}" r="{s:.1f}" fill="#fff" stroke="#d0021b" stroke-width="{s*0.26:.1f}"/>'
                f'<text x="0" y="{-s*1.55:.1f}" font-family="Arial" font-size="{s*1.05:.1f}" font-weight="bold" fill="#111" text-anchor="middle">50</text>')
    elif kind == "waarschuwing":
        head = f'<polygon points="0,{-s*2.9:.1f} {s*1.05:.1f},{-s*0.95:.1f} {-s*1.05:.1f},{-s*0.95:.1f}" fill="#fff" stroke="#d0021b" stroke-width="{s*0.28:.1f}"/>'
    elif kind == "voetgangers":
        head = (f'<polygon points="0,{-s*2.9:.1f} {s*1.05:.1f},{-s*0.95:.1f} {-s*1.05:.1f},{-s*0.95:.1f}" fill="#fff" stroke="#d0021b" stroke-width="{s*0.28:.1f}"/>'
                f'<circle cx="{s*0.05:.1f}" cy="{-s*2.05:.1f}" r="{s*0.16:.1f}" fill="#111"/>'
                f'<rect x="{-s*0.06:.1f}" y="{-s*1.9:.1f}" width="{s*0.2:.1f}" height="{s*0.5:.1f}" fill="#111"/>')
    return (f'<g transform="translate({x:.0f},{y:.0f})">'
            f'<rect x="{-s*0.09:.1f}" y="{-s*1.0:.1f}" width="{s*0.18:.1f}" height="{s*1.0:.1f}" fill="#9aa3a9"/>'
            + head + '</g>')


def shark_teeth(u=0.72, n=9):
    """Haaientanden dwars over de weg."""
    y = yof(u)
    hw = halfw(u)
    t = []
    for i in range(n):
        x = CX - hw + (2 * hw) * (i + .5) / n
        w = 2 * hw / n * 0.7
        t.append(f'<polygon points="{x-w/2:.1f},{y:.1f} {x+w/2:.1f},{y:.1f} {x:.1f},{y-w*0.9:.1f}" fill="#f2f2f2"/>')
    return "".join(t)


def zebra(u=0.62, n=6):
    y = yof(u)
    hw = halfw(u)
    out = []
    for i in range(n):
        x = CX - hw + (2 * hw) * (i + .5) / n
        w = 2 * hw / n * 0.55
        out.append(f'<polygon points="{x-w/2:.1f},{y+16:.1f} {x+w/2:.1f},{y+16:.1f} '
                   f'{x+w*0.42:.1f},{y-10:.1f} {x-w*0.42:.1f},{y-10:.1f}" fill="#f2f2f2"/>')
    return "".join(out)


def cockpit():
    """Stuur en spiegels van je eigen motor, onderin beeld."""
    return ('<g opacity=".95">'
            '<path d="M120 300 L150 268 L330 268 L360 300 Z" fill="#2b3138"/>'
            '<rect x="150" y="262" width="180" height="12" rx="6" fill="#3b444d"/>'
            '<circle cx="240" cy="286" r="16" fill="#1b2026"/>'
            '<g fill="#2b3138">'
            '<rect x="128" y="236" width="10" height="30" rx="4"/>'
            '<rect x="342" y="236" width="10" height="30" rx="4"/>'
            '<ellipse cx="120" cy="230" rx="24" ry="15" fill="#1b2026"/>'
            '<ellipse cx="360" cy="230" rx="24" ry="15" fill="#1b2026"/>'
            '</g>'
            '<ellipse cx="120" cy="230" rx="20" ry="11.5" fill="#8fa6bb"/>'
            '<ellipse cx="360" cy="230" rx="20" ry="11.5" fill="#8fa6bb"/>'
            '</g>')


def write(name, title, body, cock=True):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">'
           f'<title>{title}</title>{body}'
           f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" fill="none" stroke="#00000022"/></svg>')
    open(os.path.join(D, name + ".svg"), "w", encoding="utf-8").write(svg)


BASE_BUITEN = sky() + ground() + road() + midline() + edgelines()
BASE_KOM = (sky() + ground("#9aa79a") + sidewalk(-1) + sidewalk(1) + road() + midline() + edgelines())


# ---------------------------------------------------------------- scènes
write("pov-kind-bal", "Bal rolt tussen geparkeerde auto's de weg op",
      BASE_KOM + houses(-1) + houses(1)
      + car_rear(-0.72, 0.42, "#4b5b6b") + car_rear(-0.78, 0.60, "#7d6b57")
      + f'<circle cx="{px(-0.30,0.72):.0f}" cy="{yof(0.72)-10:.0f}" r="9" fill="#e74c3c"/>'
      + child(-0.60, 0.66))

write("pov-file-snelweg", "Stilstaande file op de autosnelweg",
      sky() + ground("#8d9c86") + road(1.15, "#57595c") + midline() + edgelines()
      + car_rear(-0.45, 0.55, "#2c3e50", brake=True) + car_rear(0.45, 0.52, "#b03a2e", brake=True)
      + car_rear(-0.45, 0.34, "#7f8c8d", brake=True) + car_rear(0.45, 0.33, "#34495e", brake=True)
      + car_rear(-0.45, 0.22, "#95a5a6", brake=True) + car_rear(0.45, 0.21, "#c0392b", brake=True))

write("pov-fietser-rechts", "Fietser rechts naast je terwijl je rechtsaf wilt",
      BASE_KOM + houses(-1) + houses(1)
      + f'<polygon points="{px(0.98,0.55):.0f},{yof(0.55):.0f} {W},{yof(0.55)+6:.0f} {W},{H} {px(0.99,1):.0f},{H}" fill="#5f6266"/>'
      + cyclist(0.80, 0.80, "#e67e22"))

write("pov-zebra-voetganger", "Voetganger stapt het zebrapad op",
      BASE_KOM + houses(-1) + houses(1) + zebra(0.60)
      + sign_post(-1.15, 0.55, "voetgangers")
      + person(-0.55, 0.60, "#8e44ad", walk=1))

write("pov-tegenligger-inhalen", "Tegenligger tijdens het inhalen buiten de bebouwde kom",
      BASE_BUITEN + trees(-1) + trees(1)
      + car_rear(0.42, 0.62, "#2c5f9e") + car_front(-0.45, 0.34, "#37474f", lights=True))

write("pov-vrachtwagen-rechtsaf", "Vrachtwagen voor je met richtingaanwijzer naar rechts",
      BASE_KOM + houses(-1) + houses(1)
      + truck_rear(0.05, 0.62, blink="right"))

write("pov-bus-halte", "Lijnbus vertrekt van een halte binnen de bebouwde kom",
      BASE_KOM + houses(-1) + houses(1)
      + bus_side(0.55, 0.55, blink=True))

write("pov-kruispunt-rechts", "Auto nadert van rechts op een gelijkwaardig kruispunt",
      BASE_KOM + houses(-1)
      + f'<polygon points="{px(1.0,0.52):.0f},{yof(0.52)-4:.0f} {W},{yof(0.52)-14:.0f} {W},{yof(0.72):.0f} {px(1.0,0.72):.0f},{yof(0.72):.0f}" fill="#5f6266"/>'
      + f'<polygon points="{px(-1.0,0.52):.0f},{yof(0.52)-4:.0f} 0,{yof(0.52)-14:.0f} 0,{yof(0.72):.0f} {px(-1.0,0.72):.0f},{yof(0.72):.0f}" fill="#5f6266"/>'
      + car_side(1.35, 0.60, "#c0392b", face=-1))

write("pov-rotonde", "Je nadert een rotonde met haaientanden",
      BASE_BUITEN + trees(-1) + trees(1)
      + f'<ellipse cx="{CX}" cy="{yof(0.36):.0f}" rx="150" ry="46" fill="#5f6266"/>'
      + f'<ellipse cx="{CX}" cy="{yof(0.36):.0f}" rx="72" ry="21" fill="#7fa86b" stroke="#f2f2f2" stroke-width="3"/>'
      + shark_teeth(0.60) + sign_post(-1.12, 0.55, "b6")
      + car_side(0.30, 0.44, "#2c5f9e", face=1))

write("pov-natte-bocht", "Natte bocht met slecht zicht",
      sky("#7d93a6", "#c3ced6") + ground("#6d8a63")
      + f'<path d="M{CX-10},{HOR} L{CX+10},{HOR} L{W},{H} L{CX-190},{H} Z" fill="#4e5155"/>'
      + f'<ellipse cx="300" cy="270" rx="120" ry="22" fill="#7f97ab" opacity=".55"/>'
      + f'<ellipse cx="170" cy="292" rx="90" ry="16" fill="#7f97ab" opacity=".45"/>'
      + trees(-1, 5) + sign_post(-1.05, 0.5, "waarschuwing"))

write("pov-schoolzone", "Kinderen bij een school langs de weg",
      BASE_KOM + houses(1)
      + f'<rect x="0" y="{HOR-6}" width="150" height="86" fill="#c8b08a"/>'
      + f'<rect x="14" y="{HOR+16}" width="26" height="26" fill="#dfeaf2"/>'
      + f'<rect x="56" y="{HOR+16}" width="26" height="26" fill="#dfeaf2"/>'
      + sign_post(1.15, 0.5, "a1")
      + child(-0.92, 0.62, "#e74c3c") + child(-1.02, 0.70, "#3498db") + child(-0.86, 0.74, "#f1c40f"))

write("pov-uitrit-auto", "Auto rijdt een uitrit uit",
      BASE_KOM + houses(-1) + houses(1)
      + f'<polygon points="{px(1.0,0.60):.0f},{yof(0.60):.0f} {px(1.45,0.60):.0f},{yof(0.60)-6:.0f} '
        f'{px(1.6,0.78):.0f},{yof(0.78):.0f} {px(1.0,0.78):.0f},{yof(0.78):.0f}" fill="#8d8d8d"/>'
      + car_side(1.05, 0.68, "#16a085", face=-1, blink=True))

write("pov-tram", "Tram kruist de weg",
      BASE_KOM + houses(-1)
      + f'<g stroke="#b8b8b8" stroke-width="3"><line x1="0" y1="{yof(0.58)-6:.0f}" x2="{W}" y2="{yof(0.58)-14:.0f}"/>'
        f'<line x1="0" y1="{yof(0.62)+2:.0f}" x2="{W}" y2="{yof(0.62)-6:.0f}"/></g>'
      + tram(0.9, 0.58))

write("pov-mist", "Dichte mist buiten de bebouwde kom",
      sky("#c3ccd2", "#dde3e7") + ground("#93a58c") + road(1.0, "#66686b") + midline() + edgelines()
      + car_rear(0.35, 0.50, "#5a5f63", brake=True)
      + f'<rect y="{HOR-10}" width="{W}" height="{H}" fill="#e3e9ec" opacity=".55"/>'
      + f'<rect y="{HOR-10}" width="{W}" height="120" fill="#e3e9ec" opacity=".55"/>')

write("pov-nacht-tegenligger", "Verblindende tegenligger in het donker",
      sky("#101a2b", "#20304a") + ground("#1b2a1c") + road(1.0, "#26282b") + midline("#c9c9c9") + edgelines("#c9c9c9")
      + f'<defs><radialGradient id="glow"><stop offset="0" stop-color="#fffbe0" stop-opacity=".95"/>'
        f'<stop offset="1" stop-color="#fffbe0" stop-opacity="0"/></radialGradient></defs>'
      + f'<circle cx="{px(-0.40,0.42):.0f}" cy="{yof(0.42)-26:.0f}" r="70" fill="url(#glow)"/>'
      + car_front(-0.40, 0.42, "#1c2733", lights=True))

write("pov-wegwerkzaamheden", "Wegwerkzaamheden met rijstrookversmalling",
      BASE_BUITEN + trees(1)
      + "".join(f'<g transform="translate({px(-0.15-0.10*i, 0.72-0.09*i):.0f},{yof(0.72-0.09*i):.0f})">'
                f'<polygon points="-9,0 9,0 5,-22 -5,-22" fill="#e8622a"/>'
                f'<rect x="-6" y="-16" width="12" height="5" fill="#fff"/></g>' for i in range(5))
      + sign_post(-1.1, 0.62, "waarschuwing"))

write("pov-spoorwegovergang", "Onbewaakte spoorwegovergang",
      BASE_BUITEN + trees(-1)
      + f'<g stroke="#8a8f94" stroke-width="4"><line x1="0" y1="{yof(0.56)-4:.0f}" x2="{W}" y2="{yof(0.56)-16:.0f}"/>'
        f'<line x1="0" y1="{yof(0.60)+4:.0f}" x2="{W}" y2="{yof(0.60)-8:.0f}"/></g>'
      + f'<g transform="translate({px(-1.05,0.55):.0f},{yof(0.55):.0f})">'
        f'<rect x="-3" y="-46" width="6" height="46" fill="#9aa3a9"/>'
        f'<polygon points="0,-72 22,-46 -22,-46" fill="#fff" stroke="#d0021b" stroke-width="6"/></g>')

write("pov-tractor", "Langzaam landbouwvoertuig op een 80-weg",
      BASE_BUITEN + trees(-1) + trees(1) + tractor(0.30, 0.55))

write("pov-portier", "Portier van een geparkeerde auto gaat open",
      BASE_KOM + houses(-1) + houses(1)
      + car_rear(-0.80, 0.55, "#34495e")
      + f'<g transform="translate({px(-0.62,0.58):.0f},{yof(0.58):.0f})">'
        f'<polygon points="0,0 34,-14 34,-52 0,-46" fill="#4a6b8a"/></g>'
      + car_rear(-0.84, 0.80, "#7f8c8d"))

write("pov-invoegen-snelweg", "Invoegend verkeer op de autosnelweg",
      sky() + ground("#8d9c86") + road(1.15, "#57595c") + midline() + edgelines()
      + f'<polygon points="{px(1.05,0.42):.0f},{yof(0.42):.0f} {W},{yof(0.42)-8:.0f} {W},{H} {px(1.15,1):.0f},{H}" fill="#57595c"/>'
      + car_side(1.25, 0.52, "#c0392b", face=-1, blink=True)
      + car_rear(-0.45, 0.30, "#2c3e50"))

write("pov-overstekend-dier", "Overstekend wild op een landweg",
      BASE_BUITEN + trees(-1, 5) + trees(1, 5)
      + f'<g transform="translate({px(-0.35,0.62):.0f},{yof(0.62):.0f})">'
        f'<ellipse cx="0" cy="-26" rx="26" ry="14" fill="#8b5a2b"/>'
        f'<rect x="-18" y="-16" width="6" height="18" fill="#8b5a2b"/>'
        f'<rect x="10" y="-16" width="6" height="18" fill="#8b5a2b"/>'
        f'<path d="M22 -34 L34 -48" stroke="#8b5a2b" stroke-width="7" stroke-linecap="round"/>'
        f'<circle cx="36" cy="-52" r="9" fill="#8b5a2b"/>'
        f'<path d="M32 -60 L28 -72 M40 -60 L46 -72" stroke="#6b4423" stroke-width="4"/></g>'
      + sign_post(1.12, 0.5, "waarschuwing"))

write("pov-smalle-weg-tegenligger", "Smalle weg met een tegenligger en een fietser",
      sky() + ground("#7fa86b") + road(0.72, "#5f6266") + edgelines()
      + trees(-1, 5) + trees(1, 5)
      + car_front(-0.30, 0.42, "#616a6b", lights=True)
      + cyclist(0.75, 0.72, "#27ae60"))

write("pov-glad-tramrails", "Natte tramrails in een bocht",
      sky("#8d9fae", "#ccd6dd") + ground("#8a9c82")
      + f'<path d="M{CX-10},{HOR} L{CX+10},{HOR} L{W-40},{H} L{CX-200},{H} Z" fill="#4e5155"/>'
      + f'<g stroke="#b3bcc2" stroke-width="4" fill="none">'
        f'<path d="M{CX-4},{HOR+6} C{CX+40},200 {CX+120},260 {W-90},{H}"/>'
        f'<path d="M{CX+6},{HOR+6} C{CX+55},200 {CX+140},262 {W-30},{H}"/></g>'
      + f'<ellipse cx="250" cy="278" rx="110" ry="18" fill="#7f97ab" opacity=".5"/>')

write("pov-file-kop-staart", "Remlichten van de auto vlak voor je",
      BASE_BUITEN + trees(-1) + trees(1)
      + car_rear(0.02, 0.86, "#2c3e50", brake=True))

write("pov-brommer-rechts", "Bromfietser rechts van je op de rijbaan",
      BASE_KOM + houses(-1) + houses(1) + moped(0.72, 0.70, "#2d3436"))

write("pov-verkeerslicht-groen", "Kruispunt met groen licht en vrij zicht",
      BASE_KOM + houses(-1) + houses(1)
      + f'<g transform="translate({px(1.10,0.48):.0f},{yof(0.48):.0f})">'
        f'<rect x="-3" y="-64" width="6" height="64" fill="#6b7075"/>'
        f'<rect x="-11" y="-96" width="22" height="46" rx="4" fill="#22282d"/>'
        f'<circle cx="0" cy="-86" r="6" fill="#4b2020"/><circle cx="0" cy="-73" r="6" fill="#4b4320"/>'
        f'<circle cx="0" cy="-60" r="6" fill="#2ecc71"/></g>')

write("pov-vrachtwagen-dodehoek", "Vlak achter een vrachtwagen in de dode hoek",
      BASE_BUITEN + trees(-1) + trees(1) + truck_rear(0.0, 0.92))

write("pov-zijwind-brug", "Harde zijwind op een open brug",
      sky("#96bcd8", "#dfeaf2") + f'<rect y="{HOR}" width="{W}" height="{H-HOR}" fill="#9fb6c4"/>'
      + road(1.0, "#5f6266") + midline() + edgelines()
      + f'<g stroke="#8c99a4" stroke-width="6" opacity=".8">'
        f'<line x1="30" y1="{HOR}" x2="10" y2="{H}"/><line x1="450" y1="{HOR}" x2="470" y2="{H}"/></g>'
      + f'<g stroke="#c7d3db" stroke-width="3" opacity=".9">'
        f'<path d="M40 130 C120 120 160 140 240 128" fill="none"/>'
        f'<path d="M60 152 C150 142 200 162 280 150" fill="none"/></g>'
      + truck_rear(0.55, 0.40))

print("scènes:", len([f for f in os.listdir(D) if f.startswith("pov-")]))
