#!/usr/bin/env python3
"""Revboo video library builder.  Makes web copies, posters and manifest.json.

  python3 build.py                                   # rebuild everything (skips files already encoded)
  python3 build.py add FILE.mp4 --title "My Ad"      # add a finished ad; brand guessed from path/filename
  python3 build.py add FILE.mp4 --type clip --title "Rain street – night" --brand "Legal/PI" --categories "Legal/PI,Cars/Engine"
  python3 build.py guess FILE.mp4                    # just print the brand it would be filed under
  python3 build.py sync                              # upload any web copies not yet on the GitHub Release, rewrite manifest
  (add --no-upload to any command to skip the release upload)

Video storage: the mp4 web copies are NOT committed to git. They are uploaded as assets on a GitHub Release
of this repo (tags media-v1, media-v2, ...; a new tag is started when one reaches MAX_ASSETS assets), and
manifest.json points `video` at https://github.com/Cryptouprise/revboo-library/releases/download/<tag>/<id>.mp4.
media_release.json (committed) records which tag holds each file plus its size and sha256.
Local copies stay in media/finals and media/clips (gitignored). Posters stay in git (media/posters).
Needs the `gh` CLI logged in with repo scope.

Brands (the only allowed values): Revboo, Legal/PI, The Assist, Infinite AI, Solar Freedom, Generic/Other.
Dates = the source file's modification time unless an entry sets date_override.
Entries added with `add` are saved in extra_sources.json so later rebuilds keep them.
"""
import os, re, sys, json, subprocess, datetime, argparse
R='/workspace/revboo/'; L=os.path.dirname(os.path.abspath(__file__))+'/'
EXTRA=L+'extra_sources.json'
REPO='Cryptouprise/revboo-library'
RELEASE_INDEX=L+'media_release.json'   # {"<id>.mp4": {"tag": "media-v1", "size": ..., "sha256": ...}}
RELEASE_PREFIX='media-v'; MAX_ASSETS=900   # GitHub allows 1000 assets per release; roll over before that
BRANDS=['Revboo','Legal/PI','The Assist','Infinite AI','Solar Freedom','Generic/Other']

# ---------- brand guessing: first matching rule wins (order matters) ----------
RULES=[
 ('Legal/PI',     r'attorney|lawyer|counsel|legal|injury|law-?firm|(^|[/_.\-])pi2?([/_.\-]|$)'),
 ('The Assist',   r'assist|andy|leadroller|lead-roller|newsletter|trovy'),
 ('Infinite AI',  r'infinite|myinfinite|ai-department|control-tower|imagine-sales|speed-to-lead|lead-response'),
 ('Solar Freedom',r'solar|breakyoursolar|scrc'),
 ('Revboo',       r'revboo|chase-asset|/refs/'),
]
def guess_brand(*texts):
    t=' '.join(texts).lower()
    for b,rx in RULES:
        if re.search(rx,t): return b
    return 'Generic/Other'
DEFAULT_CATEGORY={'Revboo':'Revboo ads','Legal/PI':'Ads for attorneys','The Assist':'The Assist ads',
                  'Infinite AI':'Infinite AI videos','Solar Freedom':'Solar Freedom ads','Generic/Other':'Other videos'}

# ---------- FINISHED ADS ----------
# group = one ad concept (newest version is featured, older ones collapse under it)
# brand is optional: guessed from src path/title when missing.  pt = poster time (s)
A=L  # noqa
AB='/workspace/outreach/andy-board/'; IM='/workspace/infinite-media/'
FINALS=[
 # Revboo promos
 dict(id='clone-war-room',pt=9.0,group='Clone War Room',title='Clone War Room',version='v1 · Seedance 2.5',src='/workspace/refs/ref1.mp4',brand='Revboo',category='Seedance originals (made by Chase)',date_override=('Sep 28, 2026','2026-09-28T07:24:50'),note='15s Seedance 2.5 generation with native voice and SFX.'),
 dict(id='blast-furnace-take1',pt=5.0,group='Blast Furnace / Change the Creative',title='Blast Furnace / Change the Creative',version='take 1 · Seedance',src='/workspace/refs/hf/hf_20260928_043048_b9755242-d220-41de-8935-3936d2143bcb.mp4',brand='Revboo',date_override=('Sep 27, 2026','2026-09-27T22:30:48'),status='rejected',category='Rejected takes (do not use)',note='REJECTED, do not use: the last line says "your ABS can\'t afford to miss" instead of "ads" (Whisper small.en, medium.en and large-v3 all hear "abs", p 0.92-1.00, even when prompted toward "ads"). End card also misspelled "Donefor-your". Kept for the archive. Use the captioned Furnace ad listed in FINALS.md. Made about 10:30 PM MT on Sep 27.'),
 dict(id='remake',pt=10.0,group='The Remake',title='The Remake',version='v1',src=R+'Revboo-Remake.mp4'),
 dict(id='graveyard-v2',pt=4.6,group='The Ad Graveyard',title='The Ad Graveyard',version='v2 (retimed)',src=R+'Revboo-Graveyard-v2.mp4'),
 dict(id='graveyard-v1',pt=2.6,group='The Ad Graveyard',title='The Ad Graveyard',version='v1',src=R+'Revboo-Graveyard-small.mp4',datesrc=R+'Revboo-Graveyard.mp4'),
 dict(id='promo-v3',pt=4.3,group='The Revenue Engine',title='The Revenue Engine',version='v3 (real engine SFX)',src=R+'revboo-promo-v3.mp4',datesrc=R+'Revboo-Promo-v3.mp4'),
 dict(id='promo-v2',pt=4.3,group='The Revenue Engine',title='The Revenue Engine',version='v2',src=R+'revboo-promo-v2.mp4',datesrc=R+'Revboo-Promo-v2.mp4'),
 dict(id='promo-v1',pt=0.5,group='The Revenue Engine',title='The Revenue Engine',version='v1 (stills)',src=R+'revboo-promo-v1.mp4',status='rejected',note='Rejected: stills slideshow. Kept for the archive.'),
 # Revboo ads aimed at attorneys -> Legal/PI
 dict(id='counselor-v2',pt=30.5,group='Your Move, Counselor',title='Your Move, Counselor',version='v2 (slower)',src=R+'Revboo-Counselor-v2.mp4'),
 dict(id='counselor-v1',pt=20.2,group='Your Move, Counselor',title='Your Move, Counselor',version='v1',src=R+'Revboo-Counselor.mp4'),
 dict(id='pi-attorneys',pt=10.0,group='PI Attorneys',title='PI Attorneys',version='v1',src=R+'Revboo-PI-Attorneys.mp4'),
 # The Assist (Andy)
 dict(id='assist-01-dave',pt=3.0,group='Assist remake 01 · Dave stole my idea',title='Dave Stole My Idea',version='remake (text motion)',src=AB+'site/assist/remakes/01-dave.mp4',category='Assist remakes (text motion)'),
 dict(id='assist-02-sayno',pt=3.0,group='Assist remake 02 · Say-no script',title='The Say-No Script',version='remake (text motion)',src=AB+'site/assist/remakes/02-sayno.mp4',category='Assist remakes (text motion)'),
 dict(id='assist-03-oneone',pt=3.0,group='Assist remake 03 · 1:1 opener',title='The 1:1 Opener',version='remake (text motion)',src=AB+'site/assist/remakes/03-oneone.mp4',category='Assist remakes (text motion)'),
 dict(id='assist-04-ai',pt=3.0,group='Assist remake 04 · AI busy',title='Not Behind on AI, Busy',version='remake (text motion)',src=AB+'site/assist/remakes/04-ai.mp4',category='Assist remakes (text motion)'),
 dict(id='assist-05-matched',pt=3.0,group='Assist remake 05 · Get matched',title='Get Matched',version='remake (text motion)',src=AB+'site/assist/remakes/05-matched.mp4',category='Assist remakes (text motion)'),
 dict(id='assist-dave-official-gmsd',pt=1.2,group='Dave hepeating · UGC',title='Dave Hepeating (UGC talking head)',version='captions: GET MORE SH*T DONE header',src=AB+'awesome/v2/videos/01-dave-official-gmsd.mp4',category='Assist UGC (Grok talking head)',max_mb=2.0,note='7 caption variants of the same take; no winner picked yet.'),
 dict(id='assist-dave-official-unfair',pt=1.2,group='Dave hepeating · UGC',title='Dave Hepeating (UGC talking head)',version='captions: "Dave stole the credit" → unfair advantage',src=AB+'awesome/v2/videos/01-dave-official-unfair.mp4',category='Assist UGC (Grok talking head)',max_mb=2.0),
 dict(id='assist-dave-official-days',pt=1.2,group='Dave hepeating · UGC',title='Dave Hepeating (UGC talking head)',version='captions: "better professional in 5 min" + weekly lineup',src=AB+'awesome/v2/videos/01-dave-official-days.mp4',category='Assist UGC (Grok talking head)',max_mb=2.0),
 dict(id='assist-dave-official-301697',pt=1.2,group='Dave hepeating · UGC',title='Dave Hepeating (UGC talking head)',version='captions: "The 5-min newsletter" · 301,697 women',src=AB+'awesome/v2/videos/01-dave-official-301697.mp4',category='Assist UGC (Grok talking head)',max_mb=2.0),
 dict(id='assist-dave-overlay-301k',pt=1.2,group='Dave hepeating · UGC',title='Dave Hepeating (UGC talking head)',version='overlay: "Tip: claim your idea before Dave"',src=AB+'awesome/v2/videos/01-dave-overlay-301k.mp4',category='Assist UGC (Grok talking head)',max_mb=2.0),
 dict(id='assist-dave-overlay-hepeat',pt=1.2,group='Dave hepeating · UGC',title='Dave Hepeating (UGC talking head)',version='overlay: "Dave just repeated my idea…"',src=AB+'awesome/v2/videos/01-dave-overlay-hepeat.mp4',category='Assist UGC (Grok talking head)',max_mb=2.0),
 dict(id='assist-dave-overlay-their-line',pt=1.2,group='Dave hepeating · UGC',title='Dave Hepeating (UGC talking head)',version='overlay: their line "better leader, keep your sanity"',src=AB+'awesome/v2/videos/01-dave-overlay-their-line.mp4',category='Assist UGC (Grok talking head)',max_mb=2.0),
 dict(id='trovy-cardcut',pt=1.0,group='Trovy · card-cut UGC',title='Trovy Card-Cut UGC',version='card cut (control winner)',src='/workspace/ads/trovy/chase-ugc/video-a-cardcut.mp4',brand='The Assist',category='Trovy UGC (for Andy)',note='Trovy HELOC ad made for Andy\'s board. Filed under The Assist because it is Andy work.'),
 dict(id='trovy-yellow-card',pt=4.0,group='Trovy · yellow card UGC',title='Trovy Yellow Card UGC',version='draft',src='/workspace/ads/trovy/chase-ugc/video-b.mp4',brand='The Assist',category='Trovy UGC (for Andy)',note='Trovy HELOC ad made for Andy\'s board (draft, 16:9-ish source).'),
 # Infinite AI
 dict(id='infinite-control-tower',pt=7.0,group='AI Department Control Tower',title='AI Department Control Tower',version='vertical',src='/workspace/uploads/ai-department-control-tower.mp4',category='Infinite AI videos',note='imagine-sales.mp4 in uploads is the exact same file.'),
 dict(id='infinite-control-tower-16x9',pt=7.0,group='AI Department Control Tower',title='AI Department Control Tower',version='16:9 cut',src='/workspace/uploads/ai-department-control-tower-16x9.mp4',category='Infinite AI videos',datetime_nudge=-1),
 dict(id='infinite-hero-vsl-repaired',pt=6.0,group='Hero VSL · same presenter',title='Infinite AI Hero VSL',version='final (repaired)',src=IM+'infinite-ai-final-same-presenter-hero-vsl-repaired_006e0a68.mp4',category='Infinite AI videos'),
 dict(id='infinite-hero-vsl',pt=6.0,group='Hero VSL · same presenter',title='Infinite AI Hero VSL',version='final (before repair)',src=IM+'infinite-ai-final-same-presenter-hero-vsl_307b4875.mp4',category='Infinite AI videos',datetime_nudge=-1),
 dict(id='infinite-hero-vsl-source',pt=6.0,group='Hero VSL · same presenter',title='Infinite AI Hero VSL',version='source-locked (1080p)',src=IM+'infinite-ai-source-locked-hero-vsl_37a8cafc.mp4',category='Infinite AI videos',datetime_nudge=-2),
 dict(id='infinite-lead-response-teaser',pt=5.0,group='UGC · lead response teaser',title='Lead Response Teaser (UGC)',version='v1',src=IM+'infinite-ai-ugc-lead-response-teaser_e3ca2454.mp4',category='Infinite AI videos'),
 dict(id='infinite-speed-to-lead',pt=5.0,group='UGC · speed-to-lead demo',title='Speed-to-Lead Demo (UGC)',version='v1',src=IM+'infinite-ai-ugc-speed-to-lead-demo_a4bf59c6.mp4',category='Infinite AI videos'),
]
C_CAR='Cars/Engine';C_PH='Phones & Scrolling';C_PPL='People/Reactions';C_LEG='Legal/PI';C_PROD='Products';C_BR='Brand cards & Logo';C_FX='Transitions/FX'
A_P1='Revenue Engine v1';A_P23='Revenue Engine v2/v3';A_G='Ad Graveyard v1/v2';A_RM='The Remake';A_PI='PI Attorneys';A_CO='Counselor';A_DV='Dave Hepeating UGC'
# ---------- CLIP LIBRARY ---------- (src, name, categories, used in, note, poster time, brand-asset, [brand], [keep audio])
CLIPS=[
 (R+'chase-asset1.mp4','Chase card – print ad shatters to Revboo logo',[C_BR,C_FX],[A_G,A_RM,A_PI,A_CO],'CapCut watermark top-left: crop 689:1225:15:52 before use.',3.2,True),
 (R+'chase-asset2.mp4','Chase card – NEW ADS EVERY WEEK',[C_BR],[A_G,A_RM,A_PI,A_CO],'CapCut watermark top-left: crop 689:1225:15:52. Don\'t stack extra text on it.',2.5,True),
 (R+'car.mp4','Revboo supercar hood – sunset (still)',[C_CAR,C_BR],[A_P1],'Still-image move from the v1 stills promo.',1.5,False),
 (R+'rock.mp4','Revboo rock logo – molten title card',[C_BR],[A_P1],'Still-image move from the v1 stills promo. Small tagline text; check spelling before reuse.',1.5,False),
 (R+'s1.mp4','Text card – "YOUR ADS ARE TIRED."',[C_BR],[A_P1],'',2.0,False),
 (R+'s2.mp4','Text card – "SAME CREATIVE. SAME RESULTS. EVERY WEEK."',[C_BR],[A_P1],'',2.0,False),
 (R+'s5.mp4','Text card – "FRESH PERFORMANCE ADS. EVERY WEEK. DONE FOR YOU."',[C_BR],[A_P1],'',2.4,False),
 (R+'s6.mp4','End card – Revboo logo + "OLD ADS IN. BANGERS OUT."',[C_BR],[A_P1],'',2.8,False),
 (R+'v.mp4','Stills promo v1 – silent picture cut',[C_BR],[A_P1],'Archive: picture-only cut of the rejected v1 stills promo (rock, car and text cards).',2.0,False),
 (R+'v2/c1.mp4','Dusty car stalls – dim garage',[C_CAR],[A_P23,A_G],'',2.0,False),
 (R+'v2/c2.mp4','Dashboard warning light – night',[C_CAR],[A_P23],'',1.5,False),
 (R+'v2/c3.mp4','Stressed media buyer at laptop',[C_PPL],[A_P23],'Blur the Apple logo on the laptop.',4.0,False),
 (R+'v2/c4.mp4','Ignition button press – orange sparks',[C_CAR,C_FX],[A_P23,A_RM,A_CO],'Garbled AI lettering on the panel labels: blur around the button (radial focus at 380,640).',3.5,False),
 (R+'v2/c5.mp4','Engine pistons – orange fire',[C_CAR],[A_P23],'',3.5,False),
 (R+'v2/c6.mp4','Revboo supercar hood, then launch – sunset',[C_CAR,C_BR],[A_P23,A_G],'Keep the grade mild: the orange "R" disappears into the hood when saturation is pushed.',1.5,False),
 (R+'v2/c7.mp4','Supercar through tunnel – sparks to sunset',[C_CAR],[A_P23],'',1.5,False),
 (R+'grave/g1.mp4','Foggy graveyard – blank tombstones, night',[C_FX],[A_G],'Tombstones are blank; crisp names are added in post.',2.5,False),
 (R+'grave/g2.mp4','Media buyer on tombstone – big shrug',[C_PPL],[A_G],'',4.5,False),
 (R+'grave/g3.mp4','Grave bursts open – orange fire & dirt',[C_FX],[A_G],'',3.5,False),
 (R+'grave/g4.mp4','Phone erupts in hearts – dark desk',[C_PH,C_FX],[A_G],'',3.0,False),
 (R+'grave/g5.mp4','Creator points at camera – pink neon',[C_PPL],[A_G],'',4.5,False),
 (R+'grave/g6.mp4','Thumb scrolling a feed – close-up',[C_PH],[A_G,A_PI],'Screen is already blurred (no fake UI text).',2.5,False),
 (R+'remake/r1.mp4','POV hand – blank white phone screen',[C_PH],[A_RM,A_CO],'Blank screen for compositing your own feed (quads in remake/r1_quads.npy).',2.5,False),
 (R+'remake/r2.mp4','Boring sneaker – turntable, white wall',[C_PROD],[A_RM],'',2.5,False),
 (R+'remake/r3.mp4','Bored couch scroller – yawns at ~3s',[C_PPL,C_PH],[A_RM,A_CO],'',3.0,False),
 (R+'remake/r4.mp4','Sneaker lights off & levitates – orange glow',[C_PROD,C_FX],[A_RM],'',4.3,False),
 (R+'remake/r5.mp4','Sneaker drops into black water – splash',[C_PROD,C_FX],[A_RM],'',4.3,False),
 (R+'remake/r6.mp4','Couch guy lights up & taps – big grin',[C_PPL,C_PH],[A_RM,A_CO],'',4.3,False),
 (R+'pi/k1.mp4','Hand holding phone – green screen',[C_PH],[A_PI,A_CO],'Green screen: key in your own screen content.',2.5,False),
 (R+'pi/k2.mp4','Rain intersection – night headlights',[C_LEG,C_CAR],[A_PI,A_CO],'Blur the license plate and BMW badge (tracked in pi/blurtrack.json).',2.5,False),
 (R+'pi/k3.mp4','Worried driver on phone – roadside, night',[C_LEG,C_PPL,C_PH],[A_PI],'Blur the fake license plate at bottom-left.',4.5,False),
 (R+'pi/k4.mp4','Courthouse attorney – golden hour',[C_LEG,C_PPL],[A_PI,A_CO],'Blur the fake building inscription (tracked). Tight crop at 3.6–4.8s works as a hero close-up.',3.8,False),
 (R+'pi/k5.mp4','Phone on desk – green screen',[C_PH,C_LEG],[A_PI,A_CO],'Green screen: key in your own screen content; fake the buzz with a frame shake.',2.5,False),
 # The Assist raw talking-head generations (with voice)
 (AB+'awesome/v2/videos/01-dave-vertical.mp4','Assist host – "Dave stole my idea" talking head (clean vertical)',[C_PPL],[A_DV],'Clean vertical, no captions. Base for the caption variants.',1.2,False,'The Assist',True),
 (AB+'awesome/v2/videos/01-dave-grok.mp4','Assist host – kitchen talking head, Dave take (Grok raw, wide)',[C_PPL],[A_DV],'Raw Grok output, landscape.',3.0,False,'The Assist',True),
 (AB+'awesome/v2/videos/02-mug-their-line-grok.mp4','Assist host – coffee mug talking head (Grok raw, wide)',[C_PPL],[],'Raw Grok output, landscape. Not in a finished ad yet.',3.0,False,'The Assist',True),
 (AB+'awesome/v2/videos/03-office-mom-grok.mp4','Assist host – "office mom" talking head (Grok raw, wide)',[C_PPL],[],'Raw Grok output, landscape. Not in a finished ad yet.',3.0,False,'The Assist',True),
]
CLIP_IDS={R+'pi/k1.mp4':'pi-k1'}  # ids are derived from path; see clip_id()

# ---------------- helpers ----------------
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def probe(p,entries='format=duration'):
    return subprocess.check_output(['ffprobe','-v','error','-show_entries',entries,'-of','csv=p=0',p]).decode().split()
def dur(p): return float(probe(p)[0])
def vinfo(p):
    o=subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=codec_name,width,height','-of','csv=p=0',p]).decode().strip().split(',')
    return o[0],int(o[1]),int(o[2])
def has_audio(p): return bool(subprocess.check_output(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=index','-of','csv=p=0',p]).strip())
def mdate(p):
    d=datetime.datetime.fromtimestamp(os.path.getmtime(p))
    return d.strftime('%b %-d, %Y'), d.isoformat(timespec='seconds')
def clip_id(src):
    rel=src.replace(R,'').replace('/workspace/','')
    rel=re.sub(r'^outreach/andy-board/awesome/v2/videos/','assist-',rel)
    return re.sub(r'[^a-z0-9]+','-',rel.lower().replace('.mp4','')).strip('-')
def poster(src,t,out,w=720):
    if not os.path.exists(out):
        run(['ffmpeg','-y','-ss',str(t),'-i',src,'-map','0:v:0','-frames:v','1','-vf',f'scale={w}:-2','-q:v','4',out])

def web_final(src,out,max_mb=5.6):
    """Under-6MB H.264 web copy. Copies the source if it is already small H.264, else two-pass encode sized to fit."""
    if os.path.exists(out): return
    codec,w,h=vinfo(src)
    if codec=='h264' and os.path.getsize(src)<6_000_000: run(['cp',src,out]); return
    d=dur(src); aud=has_audio(src)
    ab=128 if aud else 0
    vb=int(min(1650, max_mb*8e3/d - ab - 40))
    big=1280 if vb<1000 else 1920   # low bitrate -> 720p so it stays sharp
    scale=f"scale='if(gt(iw,ih),min(1280,iw),-2)':'if(gt(iw,ih),-2,min({big},ih))'"
    for p in (1,2):
        tail=['-an','-f','mp4','/dev/null'] if p==1 else ((['-map','0:a:0','-c:a','aac','-b:a','128k'] if aud else [])+['-movflags','+faststart',out])
        run(['ffmpeg','-y','-i',src,'-map','0:v:0','-vf',scale,'-c:v','libx264','-preset','slow','-b:v',f'{vb}k','-maxrate',f'{int(vb*1.5)}k','-bufsize',f'{vb*2}k',
             '-profile:v','main','-pix_fmt','yuv420p','-pass',str(p),'-passlogfile','/tmp/revlib']+tail)

def web_clip(src,out,keep_audio=False):
    """Clip copy: max 720px on the short side-ish, H.264, faststart, aims under 1.5MB."""
    if os.path.exists(out): return
    d=dur(src); _,w,h=vinfo(src)
    scale='scale=720:-2' if h>=w else 'scale=-2:min(720\\,ih)'
    a=['-map','0:a:0?','-c:a','aac','-b:a','64k'] if keep_audio else ['-an']
    budget=int(min(2200, 1.35e6*8/1000/d - (64 if keep_audio else 0)))
    crf=26
    while True:
        run(['ffmpeg','-y','-i',src,'-map','0:v:0','-vf',scale,'-c:v','libx264','-preset','slow','-crf',str(crf),'-maxrate',f'{budget}k','-bufsize',f'{budget*2}k',
             '-profile:v','main','-pix_fmt','yuv420p']+a+['-movflags','+faststart',out])
        if os.path.getsize(out)<1_500_000 or crf>=36: break
        crf+=2

def load_extra():
    return json.load(open(EXTRA)) if os.path.exists(EXTRA) else {'finals':[],'clips':[]}

# ---------------- video storage (GitHub Release assets) ----------------
def rel_url(tag,name): return f'https://github.com/{REPO}/releases/download/{tag}/{name}'
def load_rel(): return json.load(open(RELEASE_INDEX)) if os.path.exists(RELEASE_INDEX) else {}
def save_rel(idx): json.dump(dict(sorted(idx.items())),open(RELEASE_INDEX,'w'),indent=1)
def sha256(p):
    import hashlib; h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def gh(*a,capture=True):
    return subprocess.run(['gh',*a],check=True,capture_output=capture,text=True).stdout
def release_assets(tag):
    """{name: (size, 'sha256:...')} for a release tag."""
    out=gh('api','--paginate',f'repos/{REPO}/releases/tags/{tag}','--jq','.assets[]|[.name,.size,.digest]|@tsv')
    return {l.split('\t')[0]:(int(l.split('\t')[1]),l.split('\t')[2]) for l in out.splitlines() if l.strip()}
def current_tag():
    """Newest media-vN release with room left; creates the next one when full (or when none exists)."""
    tags=json.loads(gh('release','list','-R',REPO,'--limit','200','--json','tagName'))
    ns=sorted(int(t['tagName'][len(RELEASE_PREFIX):]) for t in tags
              if t['tagName'].startswith(RELEASE_PREFIX) and t['tagName'][len(RELEASE_PREFIX):].isdigit())
    if ns and len(release_assets(RELEASE_PREFIX+str(ns[-1])))<MAX_ASSETS: return RELEASE_PREFIX+str(ns[-1])
    tag=RELEASE_PREFIX+str((ns[-1] if ns else 0)+1)
    gh('release','create',tag,'-R',REPO,'--title',f'Media {tag[len(RELEASE_PREFIX)-1:]} (video storage)','--latest=false',
       '--notes','Video files for the Revboo library page (https://cryptouprise.github.io/revboo-library/). '
                 'Do not delete or rename these assets: the live page streams from their URLs.')
    print('created release',tag); return tag
def sync_release(paths):
    """Upload local web copies that are not on a release yet. Never overwrites an existing asset."""
    idx=load_rel(); todo=[]
    for p in paths:
        n=os.path.basename(p); h=sha256(p); e=idx.get(n)
        if e and e['sha256']==h: continue
        if e: print(f'WARNING: {n} changed locally but {e["tag"]} already has a different {n}; not overwriting. '
                    f'Give the new version a new --id (or --version) instead.'); continue
        todo.append((p,n,h))
    if not todo: return idx
    tag=current_tag(); have=release_assets(tag)
    for p,n,h in todo:
        if n in have and have[n][1]!='sha256:'+h:
            print(f'WARNING: {tag} already has a different {n}; not overwriting. Use a new id.'); continue
        if n not in have:
            print(f'uploading {n} -> release {tag} ({os.path.getsize(p)/1e6:.1f} MB)')
            gh('release','upload',tag,p,'-R',REPO)
        have=release_assets(tag)
        if have.get(n)!=(os.path.getsize(p),'sha256:'+h): raise SystemExit(f'upload check failed for {n}: {have.get(n)}')
        idx[n]=dict(tag=tag,size=os.path.getsize(p),sha256=h); save_rel(idx)
    return idx

def build(upload=True):
    for d in ('media/finals','media/clips','media/posters'): os.makedirs(L+d,exist_ok=True)
    ex=load_extra()
    man=dict(site='Revboo Video Library',brands=BRANDS,brand=dict(color='#FF4B0A',font='Anton',site='revboo.video'),finals=[],clips=[],brand_assets=[])
    for f in FINALS+ex['finals']:
        src=f['src']
        if not os.path.exists(src): print('skip (missing):',src); continue
        brand=f.get('brand') or guess_brand(src,f.get('title',''),f.get('group',''))
        assert brand in BRANDS,brand
        out=L+'media/finals/'+f['id']+'.mp4'; web_final(src,out,f.get('max_mb',5.6))
        d=dur(out); pp=L+'media/posters/'+f['id']+'.jpg'; poster(out,min(f.get('pt',d*0.33),d-0.3),pp)
        ds,iso=f['date_override'] if 'date_override' in f else mdate(f.get('datesrc',src))
        if f.get('datetime_nudge'):  # tie-break for files with identical mtimes (older versions)
            iso=(datetime.datetime.fromisoformat(iso)+datetime.timedelta(seconds=f['datetime_nudge'])).isoformat(timespec='seconds')
        man['finals'].append(dict(id=f['id'],brand=brand,category=f.get('category') or DEFAULT_CATEGORY[brand],group=f['group'],title=f['title'],version=f.get('version','v1'),
            width=vinfo(out)[1],height=vinfo(out)[2],date=ds,datetime=iso,duration=round(d,1),video='media/finals/'+f['id']+'.mp4',poster='media/posters/'+f['id']+'.jpg',
            status=f.get('status','final'),note=f.get('note',''),source=src,size_mb=round(os.path.getsize(out)/1e6,1)))
    clips=[dict(src=c[0],name=c[1],categories=c[2],used_in=c[3],note=c[4],pt=c[5],brand_asset=c[6],
                brand=(c[7] if len(c)>7 else None),audio=(c[8] if len(c)>8 else c[6])) for c in CLIPS]+ex['clips']
    for c in clips:
        src=c['src']
        if not os.path.exists(src): print('skip (missing):',src); continue
        cid=c.get('id') or clip_id(src)
        brand=c.get('brand') or guess_brand(src,c.get('name',''))
        assert brand in BRANDS,brand
        out=L+'media/clips/'+cid+'.mp4'; web_clip(src,out,c.get('audio',False))
        d=dur(out); pp=L+'media/posters/'+cid+'.jpg'; poster(out,min(c.get('pt',d/2),d-0.2),pp,w=360)
        ds,iso=c['date_override'] if 'date_override' in c else mdate(src)
        man['clips'].append(dict(id=cid,brand=brand,name=c['name'],categories=c.get('categories',[]),used_in=c.get('used_in',[]),note=c.get('note',''),date=ds,datetime=iso,
            duration=round(d,1),video='media/clips/'+cid+'.mp4',poster='media/posters/'+cid+'.jpg',source=src,size_mb=round(os.path.getsize(out)/1e6,2)))
        if c.get('brand_asset'): man['brand_assets'].append(cid)
    ids=[e['id'] for e in man['finals']+man['clips']]
    dupes={i for i in ids if ids.count(i)>1}
    assert not dupes, f'ids must be unique across finals and clips (release asset names): {dupes}'
    # point videos at the GitHub Release copies
    entries=man['finals']+man['clips']
    idx=load_rel()
    if upload:
        try: idx=sync_release([L+e['video'] for e in entries])
        except (subprocess.CalledProcessError,FileNotFoundError) as err:
            print('WARNING: release upload failed (is `gh` installed and logged in?):',err)
    missing=[]
    for e in entries:
        n=os.path.basename(e['video']); e['file']=e['video']
        if n in idx: e['video']=rel_url(idx[n]['tag'],n)
        else: missing.append(n)
    if missing: print(f'WARNING: {len(missing)} video(s) are not on a release yet and will NOT play on the live page '
                      f'(media/ is not committed). Run `python3 build.py sync`: {missing[:5]}')
    man['finals'].sort(key=lambda x:x['datetime'],reverse=True)
    man['clips'].sort(key=lambda x:x['datetime'],reverse=True)
    json.dump(man,open(L+'manifest.json','w'),indent=2,ensure_ascii=False)
    from collections import Counter
    print('finals',len(man['finals']),dict(Counter(f['brand'] for f in man['finals'])))
    print('clips',len(man['clips']),dict(Counter(c['brand'] for c in man['clips'])))

def main():
    ap=argparse.ArgumentParser(description='Revboo video library builder')
    ap.add_argument('cmd',nargs='?',default='build',choices=['build','add','guess','sync'])
    ap.add_argument('file',nargs='?')
    ap.add_argument('--brand',choices=BRANDS,help='file under this brand (default: guessed from path/filename)')
    ap.add_argument('--type',choices=['final','clip'],default='final')
    ap.add_argument('--title'); ap.add_argument('--group'); ap.add_argument('--version',default='v1')
    ap.add_argument('--category'); ap.add_argument('--categories',default='',help='clip categories, comma separated')
    ap.add_argument('--used-in',default=''); ap.add_argument('--note',default=''); ap.add_argument('--poster-time',type=float)
    ap.add_argument('--date',help='override date, e.g. "Sep 27, 2026" (default: file mtime)')
    ap.add_argument('--id')
    ap.add_argument('--no-upload',action='store_true',help='do not upload new videos to the GitHub Release')
    a=ap.parse_args()
    if a.cmd=='guess':
        print(guess_brand(os.path.abspath(a.file))); return
    if a.cmd=='add':
        src=os.path.abspath(a.file); assert os.path.exists(src),src
        title=a.title or re.sub(r'[-_]+',' ',os.path.splitext(os.path.basename(src))[0]).strip().title()
        brand=a.brand or guess_brand(src,title)
        eid=a.id or re.sub(r'[^a-z0-9]+','-',(title+'-'+a.version if a.type=='final' else title).lower()).strip('-')
        assert re.fullmatch(r'[a-z0-9][a-z0-9-]*',eid), f'--id must be lowercase letters, digits and dashes: {eid}'
        e=dict(id=eid,src=src,brand=brand,note=a.note)
        if a.poster_time is not None: e['pt']=a.poster_time
        if a.date:
            d=datetime.datetime.strptime(a.date,'%b %d, %Y'); e['date_override']=(d.strftime('%b %-d, %Y'),d.isoformat(timespec='seconds'))
        ex=load_extra()
        if a.type=='final':
            e.update(group=a.group or title,title=title,version=a.version)
            if a.category: e['category']=a.category
            ex['finals']=[x for x in ex['finals'] if x['id']!=eid]+[e]
        else:
            e.update(name=title,categories=[x.strip() for x in a.categories.split(',') if x.strip()],used_in=[x.strip() for x in a.used_in.split(',') if x.strip()])
            ex['clips']=[x for x in ex['clips'] if x['id']!=eid]+[e]
        json.dump(ex,open(EXTRA,'w'),indent=2,ensure_ascii=False)
        print(f'added {a.type} "{title}" -> brand {brand}')
    build(upload=not a.no_upload)

if __name__=='__main__': main()
