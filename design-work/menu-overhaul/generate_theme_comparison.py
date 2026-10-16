from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import random, math

OUT = Path(__file__).parent / "mockups"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1280, 720
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(size, bold=False):
    try:
        return ImageFont.truetype(BOLD if bold else FONT, size)
    except Exception:
        return ImageFont.load_default()

F10, F12, F14, F16, F20, F24, F30 = [font(s, s in (20,24,30)) for s in (10,12,14,16,20,24,30)]
TEXT=(236,244,247,255); MUTED=(160,174,184,255)

def draw_text(d, xy, text, fill=TEXT, f=F14, anchor=None):
    d.text(xy, text, fill=fill, font=f, anchor=anchor)

def scene(seed, tint=(18,24,38), beam=(72,238,255)):
    random.seed(seed)
    img=Image.new('RGBA',(W,H),(0,0,0,255)); d=ImageDraw.Draw(img)
    for y in range(H):
        t=y/H
        d.line([0,y,W,y], fill=(int(tint[0]+20*t), int(tint[1]+16*t), int(tint[2]+34*t),255))
    gy=H-112
    for x in range(0,W,48):
        h=random.randint(64,180); col=random.choice([(36,44,58,255),(44,52,68,255),(28,36,50,255)])
        d.rectangle([x,gy-h,x+48,gy], fill=col)
        d.rectangle([x,gy-h,x+48,gy-h+6], fill=(70,84,102,255))
    d.polygon([(0,gy),(W,gy-20),(W,H),(0,H)], fill=(30,36,43,255))
    for x in range(-200,W+200,64): d.line([(x,gy),(x+260,H)], fill=(55,65,75,145), width=2)
    for y in range(gy,H,30): d.line([(0,y),(W,y-20)], fill=(49,59,69,135), width=2)
    px,py=W//2-72,H//2+92; target=(W//2+300,H//2-62)
    glow=Image.new('RGBA',(W,H),(0,0,0,0)); gd=ImageDraw.Draw(glow)
    for width,alpha in [(40,30),(25,60),(12,118),(4,235)]: gd.line([px,py,*target], fill=(*beam,alpha), width=width)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(4)))
    d=ImageDraw.Draw(img); d.line([px,py,*target], fill=(230,255,255,255), width=3)
    d.ellipse([target[0]-15,target[1]-15,target[0]+15,target[1]+15], outline=(*beam,230), width=3)
    d.rectangle([px-14,py-40,px+14,py+34], fill=(14,17,22,255), outline=(100,118,130,255))
    return img

def panel(img, box, title, accent, fill=(18,23,31,230), fantasy=False, hard=True):
    d=ImageDraw.Draw(img); x1,y1,x2,y2=box
    d.rectangle(box, fill=fill, outline=(30,36,45,255), width=2)
    d.rectangle([x1+2,y1+2,x2-2,y2-2], outline=accent, width=1)
    if hard:
        b=6
        for sx,sy in [(x1,y1),(x2-b,y1),(x1,y2-b),(x2-b,y2-b)]:
            d.rectangle([sx,sy,sx+b,sy+b], fill=(9,13,18,255), outline=accent)
    else:
        d.rounded_rectangle([x1+3,y1+3,x2-3,y2-3], radius=10, outline=accent, width=1)
    if fantasy:
        for cx,cy in [(x1+20,y1+20),(x2-20,y1+20),(x1+20,y2-20),(x2-20,y2-20)]:
            d.arc([cx-14,cy-14,cx+14,cy+14], 25, 330, fill=accent, width=2)
            d.ellipse([cx-2,cy-2,cx+2,cy+2], fill=accent)
    if title:
        tw=d.textlength(title,font=F14)
        d.rectangle([x1+14,y1-9,x1+26+tw,y1+13], fill=(8,12,17,245), outline=accent)
        draw_text(d,(x1+20,y1-6),title,accent,F14)

def button(d, box, label, selected, accent, fantasy=False):
    x1,y1,x2,y2=box; fill=(34,45,57,240) if selected else (18,23,31,225)
    if fantasy:
        d.rounded_rectangle(box, radius=8, fill=fill, outline=accent if selected else (84,74,54,255), width=2 if selected else 1)
        if selected:
            d.arc([x1+4,y1+4,x1+22,y1+22], 180, 300, fill=accent, width=1)
            d.arc([x2-22,y1+4,x2-4,y1+22], 240, 360, fill=accent, width=1)
    else:
        d.rectangle(box, fill=fill, outline=accent if selected else (78,92,105,255), width=2 if selected else 1)
        d.line([x1+2,y1+2,x2-2,y1+2], fill=(255,255,255,55))
    draw_text(d,((x1+x2)//2,y1+7),label,TEXT if selected else MUTED,F12,anchor='ma')

def slider(d,x,y,w,label,val,accent,fantasy=False):
    draw_text(d,(x,y-15),label,MUTED,F12)
    if fantasy:
        d.rounded_rectangle([x,y,x+w,y+8], radius=4, fill=(16,10,20,255), outline=(90,72,60,255))
        d.rounded_rectangle([x+1,y+1,x+int(w*val),y+7], radius=3, fill=accent)
        k=x+int(w*val); d.polygon([(k,y-5),(k+5,y+4),(k,y+13),(k-5,y+4)], fill=(255,239,196,255), outline=(42,28,14,255))
    else:
        d.rectangle([x,y,x+w,y+8], fill=(12,15,20,255), outline=(71,84,96,255))
        d.rectangle([x+1,y+1,x+int(w*val),y+7], fill=accent)
        k=x+int(w*val); d.rectangle([k-4,y-4,k+4,y+12], fill=(232,244,248,255), outline=(23,30,36,255))

def chip(d,x,y,c,label,selected,accent,fantasy=False):
    if fantasy:
        d.rounded_rectangle([x,y,x+28,y+28], radius=6, fill=c, outline=accent if selected else (90,72,60,255), width=2)
    else:
        d.rectangle([x,y,x+28,y+28], fill=c, outline=accent if selected else (70,82,92,255), width=2)
    draw_text(d,(x+14,y+34),label,MUTED,F10,anchor='ma')

def mock(theme):
    if theme=='sci':
        accent=(78,238,255,255); gold=(255,194,86,255); beam=(72,238,255); tint=(15,22,38); title='PURE SCI-FI HUD'; note='Clean hologlass, hard corners, tactical console language.'; fantasy=False; hard=True
    elif theme=='arcane':
        accent=(202,111,255,255); gold=(245,193,99,255); beam=(190,92,255); tint=(32,18,42); title='PURE ARCANE FANTASY'; note='Runic corners, rounded insets, warmer magical ornament.'; fantasy=True; hard=False
    else:
        accent=(78,238,255,255); gold=(226,174,88,255); beam=(72,238,255); tint=(18,24,38); title='ARCANE STARFORGE HYBRID'; note='Starforge: sci-fi drawer structure with subtle arcane glyph accents.'; fantasy=True; hard=True
    img=scene(hash(theme)%100, tint, beam); d=ImageDraw.Draw(img)
    # subtle overlay
    overlay=Image.new('RGBA',(W,H),(0,0,0,22)); img.alpha_composite(overlay)
    # top tabs
    panel(img,(160,24,1120,74),None,gold,(12,16,22,210),fantasy=fantasy,hard=hard)
    x=190
    for lab in ['Arcane','Rail','Lightning','Altar','Storm','Smite','Archon']:
        ww=118 if lab=='Lightning' else 94
        button(d,(x,38,x+ww,64),lab,lab=='Lightning',gold,fantasy=fantasy); x+=ww+12
    # safe zone
    col=(*accent[:3],135)
    for xx in range(108,1172,24):
        d.line([xx,77,min(xx+12,1172),77],fill=col,width=2); d.line([xx,439,min(xx+12,1172),439],fill=col,width=2)
    for yy in range(77,439,24):
        d.line([108,yy,108,min(yy+12,439)],fill=col,width=2); d.line([1172,yy,1172,min(yy+12,439)],fill=col,width=2)
    draw_text(d,(120,88),'live preview remains open',col,F12)
    # drawer
    panel(img,(74,470,1206,692),title,gold,(22,27,36,240),fantasy=fantasy,hard=hard)
    draw_text(d,(98,501),note,MUTED,F12)
    columns=[(104,'Shape'),(390,'Flash'),(676,'Audio'),(962,'Profiles')]
    for cx,label in columns:
        if fantasy and theme=='arcane':
            d.rounded_rectangle([cx,532,cx+230,654], radius=10, fill=(17,12,22,225), outline=(100,78,64,255))
        else:
            d.rectangle([cx,532,cx+230,654], fill=(10,14,20,215), outline=(67,78,91,255))
        draw_text(d,(cx+14,544),label,gold if label=='Shape' else accent,F16)
    slider(d,122,584,180,'End radius',.72,gold,fantasy=fantasy)
    slider(d,122,628,180,'Ring thickness',.38,gold,fantasy=fantasy)
    colors=[accent,(255,255,255,255),(35,154,255,255),(190,255,150,255)] if theme!='arcane' else [accent,(255,236,190,255),(124,42,220,255),(255,158,88,255)]
    for i,c in enumerate(colors): chip(d,408+i*44,582,c,['Ring','Core','Cone','Spots'][i],i==0,accent,fantasy=fantasy)
    button(d,(694,580,858,610),'Seismic Charge' if theme!='arcane' else 'Ritual Pulse',True,accent,fantasy=fantasy)
    slider(d,694,640,180,'Volume',.36,accent,fantasy=fantasy)
    button(d,(980,580,1168,610),'Profile: Main',True,(92,255,166,255),fantasy=fantasy)
    button(d,(980,624,1062,654),'Add',False,(92,255,166,255),fantasy=fantasy)
    button(d,(1074,624,1168,654),'Done',False,(92,255,166,255),fantasy=fantasy)
    # handle
    d.rectangle([540,458,740,482], fill=(10,14,20,245), outline=gold, width=2)
    draw_text(d,(640,463),'collapse preview drawer',gold,F12,anchor='ma')
    if theme=='hybrid':
        # custom star/rune corner marks, intentionally original
        for cx,cy in [(96,492),(1184,492),(96,670),(1184,670)]:
            d.line([cx-8,cy,cx+8,cy],fill=accent,width=1); d.line([cx,cy-8,cx,cy+8],fill=accent,width=1)
            d.arc([cx-10,cy-10,cx+10,cy+10],25,155,fill=gold,width=1)
    return img

def contact():
    variants=[('sci','1. Sci-Fi HUD'),('arcane','2. Arcane Fantasy'),('hybrid','3. Arcane Starforge')]
    imgs=[mock(k) for k,_ in variants]
    sheet=Image.new('RGBA',(1280,1040),(10,12,16,255)); d=ImageDraw.Draw(sheet)
    draw_text(d,(34,28),'Option B Theme Comparison',TEXT,F30)
    draw_text(d,(36,68),'Same layout, different visual language. The hybrid keeps the practical HUD structure while adding arcane identity.',MUTED,F14)
    y=112
    for im,(key,label) in zip(imgs,variants):
        thumb=im.resize((590,332),Image.Resampling.LANCZOS)
        x=34 if key!='arcane' else 656
        if key=='hybrid': x=345; y=486
        sheet.alpha_composite(thumb,(x,y))
        d.rectangle([x,y,x+590,y+332],outline=(104,128,144,255),width=2)
        draw_text(d,(x,y+348),label,(78,238,255,255) if key!='arcane' else (202,111,255,255),F20)
        notes={
            'sci':'Readable and sharp, but too generic if the mod wants arcane identity.',
            'arcane':'Distinct fantasy mood, but heavier ornament competes with precise sliders.',
            'hybrid':'Recommended: original space-magic vault console, strong preview readability.'
        }
        draw_text(d,(x,y+376),notes[key],MUTED,F12)
    return imgs,sheet

def main():
    imgs,sheet=contact()
    names=['theme_sci_fi_hud.png','theme_arcane_fantasy.png','theme_arcane_starforge_hybrid.png']
    for im,n in zip(imgs,names): im.save(OUT/n)
    sheet.save(OUT/'option_b_theme_comparison.png')
    print('Generated:')
    for n in names+['option_b_theme_comparison.png']:
        print(OUT/n)
if __name__=='__main__': main()
