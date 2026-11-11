import re, os
DASH=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SRC=os.path.join(DASH,'data','logos-raw')
# file: (folder, crop as fractions of the original viewBox: x0, x1, y0, y1, Commons file name)
C = {'AMX':('Amx',(0.80,0.99,0,0.80),'Logo de América Móvil.svg'), 'WALMEX':('Walmex',(0.775,1,0,0.70),'Walmart México y Centroamérica logo (2025).svg'),
     'GMEXICO':('Gmexico',(0,0.175,0,1),'Logo de Grupo México.svg'), 'ASUR':('Asur',(0,1,0,0.63),'Grupo Aeroportuario del Sureste logo.svg'),
     'BANORTE':('Banorte',(0,1,0,1),'Logo de Banorte (neutral).svg'), 'GENTERA':('Gentera',(0.785,1,0,1),'Logo de Gentera.svg'),
     'BIMBO':('Bimbo',(0,1,0,1),'Logo Grupo BIMBO.svg'), 'FEMSA':('Femsa',(0,1,0,1),'FEMSA Logo.svg'), 'OMA':('Omab',(0,1,0,1),'Grupo Aeroportuario Centro Norte logo.svg')}
num = lambda s: float(re.match(r'[\d.]+', s).group(0))
for k,(folder,(x0,x1,y0,y1),name) in C.items():
    s = open(os.path.join(SRC,k+'.svg'), encoding='utf-8').read()
    s = re.sub(r'<\?xml[^>]*\?>\s*', '', s); s = re.sub(r'<!DOCTYPE[^>]*>\s*', '', s)
    m = re.search(r'<svg\b[^>]*>', s); tag = m.group(0)
    vb = re.search(r'viewBox="([^"]+)"', tag)
    if vb: vx,vy,vw,vh = [float(v) for v in vb.group(1).replace(',',' ').split()]
    else: vx,vy = 0,0; vw = num(re.search(r'\bwidth="([^"]+)"', tag).group(1)); vh = num(re.search(r'\bheight="([^"]+)"', tag).group(1))
    nx, ny, nw, nh = vx+vw*x0, vy+vh*y0, vw*(x1-x0), vh*(y1-y0)
    t = re.sub(r'\s(width|height|viewBox)="[^"]*"', '', tag)
    W = 128; H = round(W*nh/nw, 1)
    t = t[:-1].rstrip('/') + f' viewBox="{nx:.3f} {ny:.3f} {nw:.3f} {nh:.3f}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid meet">'
    s = s.replace(tag, f'<!-- {name} (Wikimedia Commons, public domain){" — cropped to the symbol" if (x0,x1,y0,y1)!=(0,1,0,1) else ""} -->\n' + t, 1)
    os.makedirs(os.path.join(DASH,folder), exist_ok=True)
    open(os.path.join(DASH,folder,'logo-mark.svg'),'w',encoding='utf-8',newline='\n').write(s)
    print(k, folder, len(s), (round(nw),round(nh)))
