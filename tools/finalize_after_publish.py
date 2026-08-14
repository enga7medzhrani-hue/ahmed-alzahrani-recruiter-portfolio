#!/usr/bin/env python3
"""
Finalize the recruiter package AFTER the site is live on a real HTTPS URL.

Usage:
    python3 finalize_after_publish.py https://your-domain.example/unlisted-path/

What it does (in order):
 1. Validates the URL (must be https, no file:///, no trailing spaces).
 2. Regenerates Ahmed_Alzahrani.vcf with URL:<final-url>.
 3. Adds the clickable portfolio URL line to both CV HTML sources and
    rebuilds the two PDFs (requires: pip install weasyprint).
 4. Generates assets/qr/Ahmed_Alzahrani_QR.svg + .png
    (navy #0E2A44 on white, error correction H, quiet zone 4 modules,
     PNG 1200x1200). QR target = <final-url>?source=qr-card
 5. DECODES the generated PNG back (requires: pip install pyzbar + libzbar0)
    and aborts if the decoded text does not exactly match the QR target.
 6. Renders the two 1080x1920 digital cards from tools/card_en.html /
    card_ar.html with the real QR embedded, then decodes the QR from the
    final card PNGs as well.
 7. Updates og:url / og:image / twitter:image in index.html and the
    standalone copy to absolute URLs.
 8. Prints a checklist of the remaining manual steps (host headers,
    X-Robots-Tag, re-upload).

Nothing here runs before you supply the URL — by design, no QR exists
until a real destination exists.
"""
import sys, os, re, io, subprocess, base64

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
NAVY = '#0E2A44'

def die(msg):
    print('ABORT:', msg); sys.exit(1)

def main():
    if len(sys.argv) != 2:
        die('usage: finalize_after_publish.py <https-final-url>')
    url = sys.argv[1].strip()
    if not re.match(r'^https://[^\s/]+\.[^\s/]+', url):
        die('URL must be a real https:// address')
    if 'file:' in url:
        die('file:/// links are not allowed')
    base = url if url.endswith('/') else url  # keep as given
    qr_target = base + ('&' if '?' in base else '?') + 'source=qr-card'

    # ---- 2. VCF with URL ----
    vcf_path = os.path.join(PKG, 'Ahmed_Alzahrani.vcf')
    lines = open(vcf_path, encoding='utf-8').read().replace('\r\n','\n').strip().split('\n')
    lines = [l for l in lines if not l.startswith('URL')]
    lines.insert(-1, 'URL:' + base)
    open(vcf_path,'wb').write(('\r\n'.join(lines)+'\r\n').encode('utf-8'))
    print('VCF updated with URL')

    # ---- 3. CVs with clickable URL ----
    for f, label in [('cv_en.html','Portfolio'), ('cv_ar.html','البورتفوليو')]:
        p = os.path.join(HERE,'src',f)
        s = open(p, encoding='utf-8').read()
        s = re.sub(r'<div class="cv-portfolio-link">.*?</div>\n?', '', s, flags=re.S)
        link = f'<div class="cv-portfolio-link" style="margin-top:2mm;font-size:9.5pt"><b>{label}:</b> <a href="{base}" style="color:#2A4A66">{base}</a></div>\n'
        s = s.replace('</body>', link + '</body>')
        open(p,'w',encoding='utf-8').write(s)
        out = os.path.join(PKG, 'Ahmed_Alzahrani_CV_EN.pdf' if 'en' in f else 'Ahmed_Alzahrani_CV_AR.pdf')
        subprocess.run(['python3','-m','weasyprint',p,out], check=True, cwd=os.path.join(HERE,'src'))
        print('rebuilt', out)

    # ---- 4. QR ----
    import segno
    qr = segno.make(qr_target, error='h')
    qdir = os.path.join(PKG,'assets','qr'); os.makedirs(qdir, exist_ok=True)
    svg_p = os.path.join(qdir,'Ahmed_Alzahrani_QR.svg')
    png_p = os.path.join(qdir,'Ahmed_Alzahrani_QR.png')
    qr.save(svg_p, dark=NAVY, light='#FFFFFF', border=4)
    scale = max(1, 1200 // (qr.symbol_size(border=4)[0]))
    qr.save(png_p, dark=NAVY, light='#FFFFFF', border=4, scale=scale)
    from PIL import Image
    im = Image.open(png_p)
    if im.size[0] != 1200:
        im = im.resize((1200,1200), Image.NEAREST); im.save(png_p)
    print('QR written', im.size)

    # ---- 5. decode-verify ----
    from pyzbar import pyzbar
    decoded = pyzbar.decode(Image.open(png_p))
    if not decoded or decoded[0].data.decode() != qr_target:
        die('QR decode mismatch: ' + repr(decoded))
    print('QR decode verified ==', qr_target)

    # ---- 6. cards ----
    for card, out in [('card_en.html','Ahmed_Alzahrani_Digital_Card_EN.png'),
                      ('card_ar.html','Ahmed_Alzahrani_Digital_Card_AR.png')]:
        tpl = open(os.path.join(HERE, card), encoding='utf-8').read()
        qr_b64 = base64.b64encode(open(png_p,'rb').read()).decode()
        tpl = tpl.replace('__QR_B64__', qr_b64).replace('__URL__', base)
        tmp = os.path.join(HERE, '_'+card)
        open(tmp,'w',encoding='utf-8').write(tpl)
        pdf = tmp.replace('.html','.pdf')
        subprocess.run(['python3','-m','weasyprint',tmp,pdf], check=True)
        png_out = os.path.join(PKG,'assets','cards',out)
        subprocess.run(['pdftoppm','-png','-r','96','-singlefile',pdf,png_out[:-4]], check=True)
        cim = Image.open(png_out)
        if cim.size != (1080,1920):
            cim = cim.resize((1080,1920)); cim.save(png_out)
        d = pyzbar.decode(Image.open(png_out))
        if not d or d[0].data.decode() != qr_target:
            die('card QR failed decode: ' + out)
        print('card ok + QR verified:', out)

    # ---- 7. absolute OG/twitter URLs ----
    img_abs = base.rstrip('/') + '/assets/preview/portfolio-social-preview.png'
    for f in [os.path.join(PKG,'index.html'),
              os.path.join(PKG,'standalone','Ahmed_Alzahrani_Portfolio_Standalone.html')]:
        s = open(f, encoding='utf-8').read()
        s = re.sub(r'<meta property="og:image" content="[^"]*">',
                   f'<meta property="og:image" content="{img_abs}">', s)
        s = re.sub(r'<meta name="twitter:image" content="[^"]*">',
                   f'<meta name="twitter:image" content="{img_abs}">', s)
        if 'og:url' not in s:
            s = s.replace('<meta property="og:image"',
                          f'<meta property="og:url" content="{base}">\n<meta property="og:image"')
        open(f,'w',encoding='utf-8').write(s)
    print('OG/twitter updated')

    print('\nREMAINING MANUAL STEPS:')
    print(' - Upload the refreshed package (index.html, PDFs, VCF, assets/) to the host')
    print(' - If the host supports headers, add: X-Robots-Tag: noindex, nofollow, noarchive, nosnippet')
    print(' - Re-test the QR from a phone screen and from a 3x3cm print before ordering cards')

if __name__ == '__main__':
    main()
