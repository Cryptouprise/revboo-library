#!/usr/bin/env python3
"""Build the Revboo video library: encode web copies, posters, and manifest.json.
Re-run any time: python3 build.py   (skips files already encoded)."""
import os, json, subprocess, datetime
R='/workspace/revboo/'; L=R+'library/'
os.makedirs(L+'media/finals',exist_ok=True); os.makedirs(L+'media/clips',exist_ok=True); os.makedirs(L+'media/posters',exist_ok=True)

def dur(p): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode().strip())
def mdate(p):
    t=os.path.getmtime(p); d=datetime.datetime.fromtimestamp(t)
    return d.strftime('%b %-d, %Y'), d.isoformat(timespec='seconds')
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

# ---------- FINISHED ADS ----------
# group = one ad concept; newest version in a group is featured, older ones collapse under it.
# web: an existing under-6MB chat copy (copied as is) or 'encode' (two-pass 1650k from src)
FINALS=[
 dict(id='clone-war-room',pt=9.0,group='Clone War Room',title='Clone War Room',version='v1 · Seedance 2.5',src='/workspace/refs/ref1.mp4',web='encode',category='Seedance originals (made by Chase)',date_override=('Sep 28, 2026','2026-09-28T07:24:50'),note='15s Seedance 2.5 generation with native voice and SFX.'),
 dict(id='blast-furnace-take1',pt=5.0,group='Blast Furnace / Change the Creative',title='Blast Furnace / Change the Creative',version='take 1 · Seedance',src='/workspace/refs/hf/hf_20260928_043048_b9755242-d220-41de-8935-3936d2143bcb.mp4',web='encode',category='Seedance originals (made by Chase)',date_override=('Sep 27, 2026','2026-09-27T22:30:48'),note='Made about 10:30 PM MT on Sep 27.'),
 dict(id='counselor-v2',pt=20.2,group='Your Move, Counselor',title='Your Move, Counselor',version='v2 (slower)',src='Revboo-Counselor-v2.mp4',web='copy'),
 dict(id='counselor-v1',pt=20.2,group='Your Move, Counselor',title='Your Move, Counselor',version='v1',src='Revboo-Counselor.mp4',web='copy'),
 dict(id='pi-attorneys',pt=10.0,group='PI Attorneys',title='PI Attorneys',version='v1',src='Revboo-PI-Attorneys.mp4',web='copy'),
 dict(id='remake',pt=10.0,group='The Remake',title='The Remake',version='v1',src='Revboo-Remake.mp4',web='copy'),
 dict(id='graveyard-v2',pt=4.6,group='The Ad Graveyard',title='The Ad Graveyard',version='v2 (retimed)',src='Revboo-Graveyard-v2.mp4',web='copy'),
 dict(id='graveyard-v1',pt=2.6,group='The Ad Graveyard',title='The Ad Graveyard',version='v1',src='Revboo-Graveyard-small.mp4',datesrc='Revboo-Graveyard.mp4',web='copy'),
 dict(id='promo-v3',pt=4.3,group='The Revenue Engine',title='The Revenue Engine',version='v3 (real engine SFX)',src='revboo-promo-v3.mp4',datesrc='Revboo-Promo-v3.mp4',web='encode'),
 dict(id='promo-v2',pt=4.3,group='The Revenue Engine',title='The Revenue Engine',version='v2',src='revboo-promo-v2.mp4',datesrc='Revboo-Promo-v2.mp4',web='encode'),
 dict(id='promo-v1',pt=0.5,group='The Revenue Engine',title='The Revenue Engine',version='v1 (stills)',src='revboo-promo-v1.mp4',web='copy',status='rejected',note='Rejected: stills slideshow. Kept for the archive.'),
]
C_CAR='Cars/Engine';C_PH='Phones & Scrolling';C_PPL='People/Reactions';C_LEG='Legal/PI';C_PROD='Products';C_BR='Brand cards & Logo';C_FX='Transitions/FX'
A_P1='Revenue Engine v1';A_P23='Revenue Engine v2/v3';A_G='Ad Graveyard v1/v2';A_RM='The Remake';A_PI='PI Attorneys';A_CO='Counselor'
# ---------- CLIP LIBRARY ---------- (src, name, categories, used in, note, poster time)
CLIPS=[
 ('chase-asset1.mp4','Chase card – print ad shatters to Revboo logo',[C_BR,C_FX],[A_G,A_RM,A_PI,A_CO],'CapCut watermark top-left: crop 689:1225:15:52 before use.',3.2,True),
 ('chase-asset2.mp4','Chase card – NEW ADS EVERY WEEK',[C_BR],[A_G,A_RM,A_PI,A_CO],'CapCut watermark top-left: crop 689:1225:15:52. Don\'t stack extra text on it.',2.5,True),
 ('car.mp4','Revboo supercar hood – sunset (still)',[C_CAR,C_BR],[A_P1],'Still-image move from the v1 stills promo.',1.5,False),
 ('rock.mp4','Revboo rock logo – molten title card',[C_BR],[A_P1],'Still-image move from the v1 stills promo. Small tagline text; check spelling before reuse.',1.5,False),
 ('s1.mp4','Text card – "YOUR ADS ARE TIRED."',[C_BR],[A_P1],'',2.0,False),
 ('s2.mp4','Text card – "SAME CREATIVE. SAME RESULTS. EVERY WEEK."',[C_BR],[A_P1],'',2.0,False),
 ('s5.mp4','Text card – "FRESH PERFORMANCE ADS. EVERY WEEK. DONE FOR YOU."',[C_BR],[A_P1],'',2.4,False),
 ('s6.mp4','End card – Revboo logo + "OLD ADS IN. BANGERS OUT."',[C_BR],[A_P1],'',2.8,False),
 ('v.mp4','Stills promo v1 – silent picture cut',[C_BR],[A_P1],'Archive: picture-only cut of the rejected v1 stills promo (rock, car and text cards).',2.0,False),
 ('v2/c1.mp4','Dusty car stalls – dim garage',[C_CAR],[A_P23,A_G],'',2.0,False),
 ('v2/c2.mp4','Dashboard warning light – night',[C_CAR],[A_P23],'',1.5,False),
 ('v2/c3.mp4','Stressed media buyer at laptop',[C_PPL],[A_P23],'Blur the Apple logo on the laptop.',4.0,False),
 ('v2/c4.mp4','Ignition button press – orange sparks',[C_CAR,C_FX],[A_P23,A_RM,A_CO],'Garbled AI lettering on the panel labels: blur around the button (radial focus at 380,640).',3.5,False),
 ('v2/c5.mp4','Engine pistons – orange fire',[C_CAR],[A_P23],'',3.5,False),
 ('v2/c6.mp4','Revboo supercar hood, then launch – sunset',[C_CAR,C_BR],[A_P23,A_G],'Keep the grade mild: the orange "R" disappears into the hood when saturation is pushed.',1.5,False),
 ('v2/c7.mp4','Supercar through tunnel – sparks to sunset',[C_CAR],[A_P23],'',1.5,False),
 ('grave/g1.mp4','Foggy graveyard – blank tombstones, night',[C_FX],[A_G],'Tombstones are blank; crisp names are added in post.',2.5,False),
 ('grave/g2.mp4','Media buyer on tombstone – big shrug',[C_PPL],[A_G],'',4.5,False),
 ('grave/g3.mp4','Grave bursts open – orange fire & dirt',[C_FX],[A_G],'',3.5,False),
 ('grave/g4.mp4','Phone erupts in hearts – dark desk',[C_PH,C_FX],[A_G],'',3.0,False),
 ('grave/g5.mp4','Creator points at camera – pink neon',[C_PPL],[A_G],'',4.5,False),
 ('grave/g6.mp4','Thumb scrolling a feed – close-up',[C_PH],[A_G,A_PI],'Screen is already blurred (no fake UI text).',2.5,False),
 ('remake/r1.mp4','POV hand – blank white phone screen',[C_PH],[A_RM,A_CO],'Blank screen for compositing your own feed (quads in remake/r1_quads.npy).',2.5,False),
 ('remake/r2.mp4','Boring sneaker – turntable, white wall',[C_PROD],[A_RM],'',2.5,False),
 ('remake/r3.mp4','Bored couch scroller – yawns at ~3s',[C_PPL,C_PH],[A_RM,A_CO],'',3.0,False),
 ('remake/r4.mp4','Sneaker lights off & levitates – orange glow',[C_PROD,C_FX],[A_RM],'',4.3,False),
 ('remake/r5.mp4','Sneaker drops into black water – splash',[C_PROD,C_FX],[A_RM],'',4.3,False),
 ('remake/r6.mp4','Couch guy lights up & taps – big grin',[C_PPL,C_PH],[A_RM,A_CO],'',4.3,False),
 ('pi/k1.mp4','Hand holding phone – green screen',[C_PH],[A_PI,A_CO],'Green screen: key in your own screen content.',2.5,False),
 ('pi/k2.mp4','Rain intersection – night headlights',[C_LEG,C_CAR],[A_PI,A_CO],'Blur the license plate and BMW badge (tracked in pi/blurtrack.json).',2.5,False),
 ('pi/k3.mp4','Worried driver on phone – roadside, night',[C_LEG,C_PPL,C_PH],[A_PI],'Blur the fake license plate at bottom-left.',4.5,False),
 ('pi/k4.mp4','Courthouse attorney – golden hour',[C_LEG,C_PPL],[A_PI,A_CO],'Blur the fake building inscription (tracked). Tight crop at 3.6–4.8s works as a hero close-up.',3.8,False),
 ('pi/k5.mp4','Phone on desk – green screen',[C_PH,C_LEG],[A_PI,A_CO],'Green screen: key in your own screen content; fake the buzz with a frame shake.',2.5,False),
]

def poster(src,t,out,w=720):
    if not os.path.exists(out):
        run(['ffmpeg','-y','-ss',str(t),'-i',src,'-frames:v','1','-vf',f'scale={w}:-2','-q:v','4',out])

man=dict(site='Revboo Video Library',brand=dict(color='#FF4B0A',font='Anton',site='revboo.video'),finals=[],clips=[],brand_assets=[])
for f in FINALS:
    src=f['src'] if f['src'].startswith('/') else R+f['src']
    if not os.path.exists(src): print('skip (missing):',f['src']); continue
    out=L+'media/finals/'+f['id']+'.mp4'
    if not os.path.exists(out):
        if f['web']=='copy' and os.path.getsize(src)<6_000_000: run(['cp',src,out])
        else:
            for p in (1,2):
                run(['ffmpeg','-y','-i',src,'-c:v','libx264','-preset','slow','-b:v','1650k','-maxrate','2500k','-bufsize','3300k','-profile:v','main','-pix_fmt','yuv420p','-pass',str(p),'-passlogfile','/tmp/revlib']+(['-an','-f','mp4','/dev/null'] if p==1 else ['-c:a','aac','-b:a','128k','-movflags','+faststart',out]))
    d=dur(out); pp=L+'media/posters/'+f['id']+'.jpg'; poster(out,min(f.get('pt',d*0.33),d-0.3),pp)
    ds,iso=f['date_override'] if 'date_override' in f else mdate(R+f.get('datesrc',f['src']))
    man['finals'].append(dict(id=f['id'],category=f.get('category','Revboo ads'),group=f['group'],title=f['title'],version=f['version'],date=ds,datetime=iso,duration=round(d,1),
        video='media/finals/'+f['id']+'.mp4',poster='media/posters/'+f['id']+'.jpg',status=f.get('status','final'),note=f.get('note',''),
        size_mb=round(os.path.getsize(out)/1e6,1)))
for (s,name,cats,used,note,pt,brand) in CLIPS:
    src=R+s; cid=s.replace('/','-').replace('.mp4','')
    if not os.path.exists(src): print('skip (missing):',s); continue
    out=L+'media/clips/'+cid+'.mp4'
    if not os.path.exists(out):
        crf=26
        while True:
            a=['-c:a','aac','-b:a','96k'] if brand else ['-an']
            run(['ffmpeg','-y','-i',src,'-vf','scale=720:1280:flags=lanczos,fps=30' if not brand else 'scale=720:1280','-c:v','libx264','-preset','slow','-crf',str(crf),'-maxrate','2200k','-bufsize','3000k','-profile:v','main','-pix_fmt','yuv420p']+a+['-movflags','+faststart',out])
            if os.path.getsize(out)<1_500_000 or crf>=34: break
            crf+=2
    d=dur(out); pp=L+'media/posters/'+cid+'.jpg'; poster(out,min(pt,d-0.2),pp,w=360)
    ds,iso=mdate(src)
    e=dict(id=cid,name=name,categories=cats,used_in=used,note=note,date=ds,datetime=iso,duration=round(d,1),
        video='media/clips/'+cid+'.mp4',poster='media/posters/'+cid+'.jpg',source=s,size_mb=round(os.path.getsize(out)/1e6,2))
    man['clips'].append(e)
    if brand: man['brand_assets'].append(cid)
man['finals'].sort(key=lambda x:x['datetime'],reverse=True)
man['clips'].sort(key=lambda x:x['datetime'],reverse=True)
json.dump(man,open(L+'manifest.json','w'),indent=2,ensure_ascii=False)
print('finals',len(man['finals']),'clips',len(man['clips']))
