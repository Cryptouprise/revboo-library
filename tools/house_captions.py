#!/usr/bin/env python3
"""Revboo HOUSE CAPTION STANDARD (Style C) helper.

Extracted from the Chase-approved Furnace captioned cut (RB-005), build dir
/workspace/revboo/edits/fire-money-captioned/work/ (capslib.py, render.py, plan.py, plan45.py, qa_sheet.py,
thumbs.py, master_audio.sh). Caption rendering, motion, safe zones, keep-out rules, QA sheet, cover and
audio mastering are the same code and numbers as that build. Additions: person detection (YOLOv8n) so
people without a visible face are also kept clear, an OCR read-back check, and the best-of thumbnail
extras (subline, orange rule, Revboo .video wordmark) as cover() options. Read BRAND.md first.

THE STANDARD
  Font   Inter Tight ExtraBold (variable font, wght 800), sentence/mixed case. Never Anton or all-caps meme text.
  Color  white #FFFFFF, exactly ONE orange #FF4B0A accent word per caption line (mark it *like this*).
  Type   60-64 px on a 1080-wide frame, tracking -0.02 em, line height 1.12, soft shadow
         (mask blur 9 px @ 62% + blur 22 px @ 35%, 3 px down). No boxes, no strokes.
  Motion fade in 0.30 s (ease-out cubic) while rising 26 px; fade out over the last 0.20 s. Nothing else.
  Timing about 2.2-3 s per caption, cut on the VO.
  Zones  9:16: nothing in the top 12% (y < 230) or bottom 20% (y > 1536). 4:5: 5% margins.
         Clean zones only: never over a face, a person/torso, on-screen text, or the key action.
         If the action fills the frame, no caption.

USAGE
    import sys; sys.path.insert(0, '/workspace/revboo/library/tools'); import house_captions as hc
    det  = hc.detect('src_916.mp4', 'detect.json')        # faces + persons + burned-in text every 0.25 s
    caps = [dict(id='C1', t0=0.00, t1=2.25, text='Before you throw more *money* at your ads,',
                 size=62, maxw=900, align='center', x=None, y=250),
            dict(id='C2', t0=7.25, t1=9.45, text="Don’t *fire* your|media buyer.",     # '|' + lines=True = manual breaks
                 size=60, maxw=420, align='left', x=44, y=300, lines=True)]
    bad  = hc.check_all(caps, det, src='src_916.mp4')     # {} means every caption printed OK; fix anything else
    hc.run('src_916.mp4', 'cap916_silent.mp4', 1080, 1920, caps)
    hc.master_audio('mix_raw.wav', 'mix_master.wav', dur)  # -14 LUFS integrated, about -1 dBTP
    #   mux: ffmpeg -i cap916_silent.mp4 -i mix_master.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest out.mp4
    hc.qa_sheet('out.mp4', 'contact.png', 'qa.png', 1080, 1920, caps, det)   # 4 fps sheets with boxes; returns overlaps
    hc.ocr_verify('out.mp4', caps, 1080)                    # captions read back correctly
    hc.cover('frame.png', 'Stop feeding|the *furnace*.', 'cover-9x16.png', 0, 1920, 1298, size=106)
    4:5 feed cut: pass crop_fn=lambda t: y0 (per-shot crop offset into the 1080x1920 source) to run()/check_all()
    and give each caption a 4:5 y.

CLI
    python3 house_captions.py detect SRC.mp4 OUT.json
    python3 house_captions.py preview "Give them|better *ads*." OUT.png [size]   # caption on grey, for a look
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = '/usr/share/fonts/truetype/sand-box/google/Inter Tight/InterTight-VariableFont_wght.ttf'
ORANGE = (255, 75, 10)          # #FF4B0A Revboo orange
WHITE = (255, 255, 255)         # #FFFFFF caption white
SUB_WHITE = (235, 232, 228)     # #EBE8E4 cover subline (best-of thumbs)
FPS = 24
MODELS = '/workspace/revboo/tools/models'
RISE, FADE_IN, FADE_OUT = 26, 0.30, 0.20
TOP_SAFE, BOTTOM_SAFE = 0.12, 0.20   # 9:16 caption keep-out bands (fraction of height)

# ------------------------------------------------------------------ text rendering (Furnace capslib.py)
_fc = {}
def font(size, wght=800):
    k = (size, wght)
    if k not in _fc:
        f = ImageFont.truetype(FONT, size); f.set_variation_by_axes([wght]); _fc[k] = f
    return _fc[k]

def parse(text):
    """'Look at what you're *feeding*.' -> [(word, accent)]"""
    return [(w.replace('*', ''), w.count('*') >= 2) for w in text.split(' ')]

def word_w(f, w, track):
    # kerned advances with tracking (em; negative = tighter); apostrophes tightened a bit more
    return f.getlength(w) + track*f.size*(len(w)-1) - 0.035*f.size*sum(
        1 for j, c in enumerate(w) if c == '’' or (j+1 < len(w) and w[j+1] == '’'))

def layout(text, size, maxw, track=-0.02, wght=800):
    f = font(size, wght); words = parse(text); sp = f.getlength(' ') + track*f.size
    lines = [[]]; cur = 0
    for w, a in words:
        ww = word_w(f, w, track)
        if lines[-1] and cur+sp+ww > maxw: lines.append([]); cur = 0
        cur += (sp if lines[-1] else 0) + ww; lines[-1].append((w, a, ww))
    widths = [sum(x[2] for x in L) + sp*(len(L)-1) for L in lines]
    return f, lines, widths, sp

def render(text, size, maxw, align='center', track=-0.02, lh=1.12, lines_override=None, wght=800, fill=WHITE):
    """RGBA caption block incl. shadow padding -> (img, pad, (w, h), nlines).
    Use '|' in text with lines_override=True for explicit line breaks."""
    if lines_override:
        parts = text.split('|'); f = font(size, wght); sp = f.getlength(' ') + track*f.size
        lines = [[(w, a, word_w(f, w, track)) for w, a in parse(p.strip())] for p in parts]
        widths = [sum(x[2] for x in L) + sp*(len(L)-1) for L in lines]
    else:
        f, lines, widths, sp = layout(text, size, maxw, track, wght)
    asc, desc = f.getmetrics(); lhpx = int(size*lh)
    W = int(max(widths)) + 2; H = lhpx*(len(lines)-1) + asc + desc
    pad = 40
    txt = Image.new('RGBA', (W+2*pad, H+2*pad), (0, 0, 0, 0)); d = ImageDraw.Draw(txt)
    msk = Image.new('L', txt.size, 0); dm = ImageDraw.Draw(msk)
    for i, L in enumerate(lines):
        x = pad + (0 if align == 'left' else (W-widths[i])/2 if align == 'center' else W-widths[i]); y = pad + i*lhpx
        for w, a, ww in L:
            cx = x
            for j, ch in enumerate(w):
                d.text((cx, y), ch, font=f, fill=ORANGE if a else fill); dm.text((cx, y), ch, font=f, fill=255)
                nxt = w[j+1] if j+1 < len(w) else ''
                adv = (f.getlength(ch+nxt) - f.getlength(nxt)) if nxt else f.getlength(ch)
                cx += adv + track*size - (0.035*size if (ch == '’' or nxt == '’') else 0)
            x += ww + sp
    # soft shadow: blurred mask, 3 px down, 62% black + wider 35% halo
    sh = Image.new('RGBA', txt.size, (0, 0, 0, 0))
    a1 = msk.filter(ImageFilter.GaussianBlur(9)).point(lambda v: int(v*0.62))
    a2 = msk.filter(ImageFilter.GaussianBlur(22)).point(lambda v: int(v*0.35))
    sh.putalpha(Image.fromarray(np.maximum(np.array(a1), np.array(a2)).astype(np.uint8)))
    sh = sh.transform(sh.size, Image.AFFINE, (1, 0, 0, 0, 1, -3))
    return Image.alpha_composite(sh, txt), pad, (W, H), len(lines)

def accent_counts(text):
    """Accent words per displayed line ('|' splits lines). The standard needs one orange word per caption;
    the Furnace two-line captions carry one orange word per caption block."""
    return [sum(1 for w in part.split(' ') if w.count('*') >= 2) for part in text.split('|')]

def accent_ok(text):
    return sum(accent_counts(text)) == 1

def cap_box(c, W):
    img, pad, (w, h), n = render(c['text'], c['size'], c['maxw'], c['align'], lines_override=c.get('lines'))
    x = c['x'] if c['x'] is not None else (W-w)//2
    return img, pad, (x, c['y'], x+w, c['y']+h)

# ------------------------------------------------------------------ renderer (Furnace render.py)
def ease(u): u = min(max(u, 0), 1); return 1-(1-u)**3

def run(base, out_silent, W, H, caps, crop_fn=None, finish_fn=None, src_size=(1080, 1920), fps=FPS, crf=15):
    """Burn captions into `base` -> silent H.264 (CRF 15, slow, yuv420p, faststart).
    caps: dicts with id,t0,t1,text,size,maxw,align,x,y[,lines]. crop_fn(t)->y0 crops WxH out of the source
    (4:5 feed cut). finish_fn(rgb, t)->rgb is an optional per-frame look (the Furnace cut used none)."""
    for c in caps:
        assert accent_ok(c['text']), f"{c.get('id')}: exactly one *accent* word per caption required"
    pre = []
    for c in caps:
        img, pad, (w, h), n = render(c['text'], c['size'], c['maxw'], c['align'], lines_override=c.get('lines'))
        x = c['x'] if c['x'] is not None else (W-w)//2
        pre.append((c, img, pad, x, c['y']))
    SW, SH = src_size
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', base, '-vf', f'scale={SW}:{SH}', '-f', 'rawvideo',
                            '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow',
                            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out_silent], stdin=subprocess.PIPE)
    fsz = SW*SH*3; i = 0
    while True:
        b = dec.stdout.read(fsz)
        if len(b) < fsz: break
        t = i/fps
        fr = np.frombuffer(b, np.uint8).reshape(SH, SW, 3)
        if finish_fn is not None: fr = finish_fn(fr, t)
        if crop_fn is not None:
            y0 = int(crop_fn(t)); fr = fr[y0:y0+H]
        im = Image.fromarray(np.ascontiguousarray(fr)).convert('RGBA')
        for c, img, pad, x, y in pre:
            if c['t0']-1e-6 <= t <= c['t1']:
                a = ease((t-c['t0'])/FADE_IN); rise = int(round(RISE*(1-a)))
                fo = min(1, max(0, (c['t1']-t)/FADE_OUT))
                alpha = min(a, fo)
                if alpha <= 0: continue
                ci = img if alpha >= 0.999 else img.copy()
                if alpha < 0.999:
                    al = np.array(ci.getchannel('A'), dtype=np.float32)*alpha
                    ci.putalpha(Image.fromarray(al.astype(np.uint8)))
                im.alpha_composite(ci, (int(x-pad), int(y-pad+rise)))
        enc.stdin.write(np.array(im.convert('RGB')).tobytes()); i += 1
    enc.stdin.close(); enc.wait(); dec.wait(); print('frames', i)

# ------------------------------------------------------------------ detection (Furnace detect.py + persons)
_yolo = None
def persons(img, conf=0.35, iou=0.5):
    """YOLOv8n (COCO class 0) -> [[x0,y0,x1,y1,score]] in image pixels. Catches people whose face YuNet misses
    (backs of heads, blurred foreground figures, the BIG SALE cardboard cutout)."""
    global _yolo
    import cv2, onnxruntime as ort
    if _yolo is None:
        _yolo = ort.InferenceSession(f'{MODELS}/yolov8n.onnx', providers=['CPUExecutionProvider'])
    H, W = img.shape[:2]; r = 640/max(H, W); nw, nh = int(W*r), int(H*r)
    pad = np.full((640, 640, 3), 114, np.uint8); pad[:nh, :nw] = cv2.resize(img, (nw, nh))
    x = cv2.cvtColor(pad, cv2.COLOR_BGR2RGB).transpose(2, 0, 1)[None].astype(np.float32)/255
    if 'float16' in _yolo.get_inputs()[0].type: x = x.astype(np.float16)
    o = _yolo.run(None, {'images': x})[0][0].T.astype(np.float32)
    sc = o[:, 4]; k = sc > conf; b = o[k, :4]; sc = sc[k]
    if not len(sc): return []
    xy = np.stack([b[:, 0]-b[:, 2]/2, b[:, 1]-b[:, 3]/2, b[:, 2], b[:, 3]], 1)
    idx = cv2.dnn.NMSBoxes(xy.tolist(), sc.tolist(), conf, iou)
    return [[float(v) for v in (xy[i][0]/r, xy[i][1]/r, (xy[i][0]+xy[i][2])/r, (xy[i][1]+xy[i][3])/r)] + [float(sc[i])]
            for i in np.array(idx).flatten()]

def detect(src, out_json=None, step=0.25, use_persons=True):
    """Faces (YuNet), burned-in text (RapidOCR, conf > 0.5), persons (YOLOv8n) every `step` s, in source pixels."""
    import cv2
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    fd = cv2.FaceDetectorYN.create(f'{MODELS}/face_detection_yunet_2023mar.onnx', '', (540, 960), 0.6, 0.3, 5000)
    cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    out = []; t = 0.0
    while t < n/fps-0.02:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t*fps))); ok, f = cap.read()
        if not ok: break
        Hh, Ww = f.shape[:2]; sh = int(540*Hh/Ww)
        fd.setInputSize((540, sh)); _, faces = fd.detect(cv2.resize(f, (540, sh)))
        fl = [] if faces is None else [[float(v*Ww/540) for v in r[:4]] + [float(r[-1])] for r in faces]
        res, _ = ocr(f)
        tl = [] if not res else [dict(box=[float(min(p[0] for p in b)), float(min(p[1] for p in b)),
                                           float(max(p[0] for p in b)), float(max(p[1] for p in b))], txt=s, c=float(c))
                                 for b, s, c in res if float(c) > 0.5]
        pl = [dict(box=p[:4], s=p[4]) for p in persons(f)] if use_persons else []
        out.append(dict(t=round(t, 2), faces=fl, text=tl, persons=pl))
        t += step
    if out_json: json.dump(out, open(out_json, 'w'), indent=0)
    return out

def fire_mask(bgr):
    """Furnace plan.py: bright fire/explosion pixels (key action). Captions may cover at most 2% of it."""
    import cv2
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    return (hsv[..., 2] > 200) & (hsv[..., 1] > 110) & (hsv[..., 0] < 32)

def keepouts(det, t, H=1920, manual=None):
    """Furnace keep-out rules: face box (+20% each side, +35% above, +10% below) and a torso box under each face
    wider than 45 px (centre +-1.7 face widths, down to the frame bottom); every OCR text box +14 px; person boxes
    with no detected face inside are kept whole. manual(t) -> extra [(label,x0,y0,x1,y1)] for props / key action
    (Furnace: the money piles)."""
    d = min(det, key=lambda q: abs(q['t']-t)); boxes = []; fcs = d['faces']
    for x, y, w, h, s in fcs:
        boxes.append(('face', x-0.2*w, y-0.35*h, x+1.2*w, y+1.1*h))
        if w > 45: cx = x+w/2; boxes.append(('torso', cx-1.7*w, y+1.0*h, cx+1.7*w, H))
    for p in d.get('persons', []):
        x0, y0, x1, y1 = p['box']
        if not any(x0-10 <= fx+fw/2 <= x1+10 and y0-10 <= fy+fh/2 <= y1+10 for fx, fy, fw, fh, _ in fcs):
            boxes.append(('person', x0, y0, x1, y1))
    for tb in d['text']:
        x0, y0, x1, y1 = tb['box']; boxes.append(('text:'+tb['txt'][:12], x0-14, y0-14, x1+14, y1+14))
    if manual: boxes += manual(t)
    return boxes

def check(c, det, W=1080, H=1920, crop_fn=None, manual=None, src=None, verbose=True):
    """Overlap check over the caption's whole life in 0.25 s steps, including the 26 px rise.
    crop_fn(t)->y0 for 4:5 cuts (det is in 1080x1920 source pixels). src= also runs the fire/key-action mask."""
    _, _, (x0, y0, x1, y1) = cap_box(c, W); issues = []
    if crop_fn is None:
        if y0 < TOP_SAFE*H: issues.append('top12')
        if y1+RISE > (1-BOTTOM_SAFE)*H: issues.append('bottom20')
    elif y0 < 0.05*H or y1+RISE > 0.95*H: issues.append('margin')
    if not accent_ok(c['text']): issues.append(f'accents={accent_counts(c["text"])}')
    cap = None
    if src:
        import cv2; cap = cv2.VideoCapture(src); sfps = cap.get(cv2.CAP_PROP_FPS)
    t = c['t0']
    while t <= c['t1']+1e-6:
        oy = crop_fn(t) if crop_fn else 0
        bx = (x0, y0+oy, x1, y1+oy+(RISE if t-c['t0'] < 0.35 else 0))
        for k, a0, b0, a1, b1 in keepouts(det, t, 1920, manual):
            ix = max(0, min(bx[2], a1)-max(bx[0], a0)); iy = max(0, min(bx[3], b1)-max(bx[1], b0))
            if ix*iy > 0: issues.append(f'{t:.2f}:{k}:{int(ix*iy)}px')
        if cap is not None:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t*sfps))); ok, f = cap.read()
            if ok:
                fm = fire_mask(f)[max(0, int(bx[1])):int(bx[3]), max(0, int(bx[0])):int(bx[2])]
                if fm.size and fm.mean() > 0.02: issues.append(f'{t:.2f}:fire{fm.mean():.2f}')
        t += 0.25
    if verbose: print(c.get('id'), (x0, y0, x1, y1), 'OK' if not issues else issues[:12], len(issues))
    return issues

def check_all(caps, det, W=1080, H=1920, crop_fn=None, manual=None, src=None):
    bad = {c.get('id'): check(c, det, W, H, crop_fn, manual, src) for c in caps}
    return {k: v for k, v in bad.items() if v}

# ------------------------------------------------------------------ QA (Furnace qa_sheet.py + OCR read-back)
def qa_sheet(video, out_clean, out_qa, W, H, caps, det, y0fn=lambda t: 0, manual=None, cols=10, tw=216):
    """4 fps contact sheets: clean, and QA with caption (green), face/torso/person (red), text (blue),
    manual (yellow) boxes. Returns [(t, caption id, keep-out)] overlaps; must be empty."""
    import cv2
    th = int(tw*H/W); cap = cv2.VideoCapture(video); n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps = cap.get(cv2.CAP_PROP_FPS)
    ts = [i/4 for i in range(int(n/fps*4))]; rows = (len(ts)+cols-1)//cols
    A = Image.new('RGB', (cols*tw, rows*(th+18)), (16, 16, 16)); B = A.copy()
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
    boxes = {c['id']: cap_box(c, W)[2] for c in caps}; bad = []
    for i, t in enumerate(ts):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t*fps))); ok, f = cap.read()
        if not ok: break
        im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)); q = im.copy(); d = ImageDraw.Draw(q)
        y0 = y0fn(t); live = [c for c in caps if c['t0'] <= t <= c['t1']]
        for c in live:
            r = RISE if t-c['t0'] < 0.35 else 0; x0, a, x1, b = boxes[c['id']]
            d.rectangle([x0, a, x1, b+r], outline=(0, 255, 0), width=5)
        for k, a0, b0, a1, b1 in keepouts(det, t, 1920, manual):
            col = (255, 0, 0) if k in ('face', 'torso', 'person') else (0, 140, 255) if k.startswith('text') else (255, 200, 0)
            d.rectangle([a0, b0-y0, a1, b1-y0], outline=col, width=4)
            for c in live:
                r = RISE if t-c['t0'] < 0.35 else 0; x0, a, x1, b = boxes[c['id']]
                if min(x1, a1) > max(x0, a0) and min(b+r, b1-y0) > max(a, b0-y0): bad.append((t, c['id'], k))
        cx, cy = (i % cols)*tw, (i//cols)*(th+18)
        for S, src in ((A, im), (B, q)):
            S.paste(src.resize((tw, th)), (cx, cy)); ImageDraw.Draw(S).text((cx+4, cy+th+2), f'{t:.2f}s', fill=(220, 220, 220), font=fnt)
    A.save(out_clean); B.save(out_qa); return bad

def ocr_verify(video, caps, W):
    """OCR each caption once it is fully in and confirm its words read back inside its box."""
    import cv2
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR(); cap = cv2.VideoCapture(video); fps = cap.get(cv2.CAP_PROP_FPS); probs = []
    norm = lambda s: ''.join(ch for ch in s.lower().replace('’', "'") if ch.isalnum())
    for c in caps:
        t = min(c['t0']+0.6, (c['t0']+c['t1'])/2)
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t*fps))); ok, f = cap.read()
        x0, y0, x1, y1 = cap_box(c, W)[2]
        res, _ = ocr(f[max(0, int(y0)-20):int(y1)+20, max(0, int(x0)-20):int(x1)+20])
        got = ' '.join(r[1] for r in (res or [])); want = c['text'].replace('*', '').replace('|', ' ')
        ok = norm(want) in norm(got) or sum(1 for w in want.split() if norm(w) in norm(got)) >= len(want.split())-1
        if not ok: probs.append((c['id'], want, got))
        print(c['id'], 'OCR:', got, 'OK' if ok else '<-- MISMATCH')
    return probs

# ------------------------------------------------------------------ cover / thumbnail (Furnace thumbs.py + best-of extras)
def _grade_bottom(im, y_from, y_to, k=0.55):
    a = np.array(im).astype(np.float32); ys = np.arange(a.shape[0]); g = np.ones(a.shape[0], np.float32)
    m = ys > y_from; g[m] = 1-k*np.clip((ys[m]-y_from)/(y_to-y_from), 0, 1)
    return Image.fromarray((a*g[:, None, None]).clip(0, 255).astype(np.uint8))

def _grade_top(im, y_from, y_to, k=0.55):
    a = np.array(im).astype(np.float32); ys = np.arange(a.shape[0]); g = np.ones(a.shape[0], np.float32)
    m = ys < y_to; g[m] = 1-k*np.clip((y_to-ys[m])/(y_to-y_from), 0, 1)
    return Image.fromarray((a*g[:, None, None]).clip(0, 255).astype(np.uint8))

def cover(src, text, out, crop_y0, H, text_y, size=106, W=1080, align='right', margin=48, grad='bottom',
          sub=None, rule=False, wordmark=False):
    """Furnace cover: a real frame from the ad, soft legibility gradient (bottom: darken from 62% to 86% of H by
    up to 55%; grad='top' mirrors it over 6-36%), 2 short lines Inter Tight ExtraBold, tracking -0.025, line height
    1.04, white with ONE orange word, right-aligned 48 px from the edge. Furnace sizes: 106 px (9:16), 112 px (4:5).
    Best-of extras: sub='small subline' (0.36x size, wght 600, #EBE8E4), rule=True (130x12 orange bar above the
    headline), wordmark=True ('Revboo' 38 px wght 700 white + '.video' wght 600 orange, bottom-left).
    With the extras off the output is identical to the approved Furnace covers."""
    assert accent_ok(text), 'cover headline needs exactly one *orange* word'
    base = Image.open(src).convert('RGB') if isinstance(src, str) else src
    im = base.crop((0, crop_y0, W, crop_y0+H))
    im = (_grade_bottom(im, int(H*0.62), int(H*0.86)) if grad == 'bottom' else _grade_top(im, int(H*0.06), int(H*0.36))).convert('RGBA')
    cap, pad, (w, h), n = render(text, size, 1000, align, track=-0.025, lh=1.04, lines_override=True)
    x = W-margin-w if align == 'right' else margin if align == 'left' else (W-w)//2
    if rule:
        rx = x if align != 'right' else W-margin-130
        ImageDraw.Draw(im).rectangle([rx+4, text_y-40, rx+4+130, text_y-28], fill=ORANGE+(255,))
    im.alpha_composite(cap, (x-pad, text_y-pad))
    if sub:
        sc, sp, (sw, shh), _ = render(sub, int(size*0.36), 1000, align, track=-0.02, lh=1.12, lines_override=True,
                                      wght=600, fill=SUB_WHITE)
        sx = W-margin-sw if align == 'right' else margin+4 if align == 'left' else (W-sw)//2
        im.alpha_composite(sc, (sx-sp, text_y+h+int(size*0.18)-sp))
    if wordmark:
        d = ImageDraw.Draw(im); fb = font(38, 700); wy = H-(150 if H >= 1900 else 74)
        d.text((76, wy), 'Revboo', font=fb, fill=(250, 248, 245, 235))
        d.text((76+fb.getlength('Revboo')+8, wy), '.video', font=font(38, 600), fill=ORANGE+(255,))
    im.convert('RGB').save(out); print(out, (x, text_y, x+w, text_y+h)); return (x, text_y, x+w, text_y+h)

# ------------------------------------------------------------------ audio (Furnace master_audio.sh)
def lufs(path):
    o = subprocess.run(['ffmpeg', '-hide_banner', '-i', path, '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    j = json.loads(o[o.rindex('{'):o.rindex('}')+1]); return float(j['input_i']), float(j['input_tp'])

def master_audio(inp, out, dur, target=-14.0):
    """-14 LUFS integrated, about -1 dBTP: static gain, then alimiter (limit 0.85, attack 1, release 60),
    trimmed to `dur`, 48 kHz 24-bit; re-measured, up to 3 passes until within 0.3 LU."""
    I, _ = lufs(inp); g = target-I
    for k in range(3):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', inp, '-af',
                        f'volume={g:.3f}dB,alimiter=limit=0.85:attack=1:release=60:level=disabled,atrim=0:{dur}',
                        '-ar', '48000', '-c:a', 'pcm_s24le', out], check=True)
        M, tp = lufs(out); print(f'pass {k+1} gain {g:.2f} -> {M} LUFS, TP {tp}')
        if abs(M-target) < 0.3: break
        g += target-M
    return M, tp

if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == 'detect':
        detect(a[1], a[2]); print('wrote', a[2])
    elif len(a) >= 3 and a[0] == 'preview':
        img, pad, (w, h), n = render(a[1], int(a[3]) if len(a) > 3 else 62, 900, 'center', lines_override='|' in a[1])
        bg = Image.new('RGBA', img.size, (90, 90, 90, 255)); bg.alpha_composite(img); bg.convert('RGB').save(a[2]); print('wrote', a[2])
    else:
        print(__doc__)
