AHMED ALZAHRANI — RECRUITER PORTFOLIO PACKAGE
==============================================
حزمة بورتفوليو التوظيف — أحمد الزهراني

1) FINAL PORTFOLIO URL / الرابط النهائي
   PENDING — not published yet. No QR exists in this package because no
   real HTTPS URL exists yet. After publishing, run:
       python3 tools/finalize_after_publish.py https://<your-final-url>/
   (requires: pip install weasyprint segno pyzbar pillow vobject
    plus the libzbar0 system package for QR decode verification)

2) FILES / الملفات
   index.html ................................ hosted version (relative PDF/VCF links)
   Ahmed_Alzahrani_CV_EN.pdf ................. English CV (2 pages, ATS-friendly)
   Ahmed_Alzahrani_CV_AR.pdf ................. Arabic CV (2 pages, RTL)
   Ahmed_Alzahrani.vcf ....................... contact card (vCard 3.0, no URL yet)
   assets/preview/portfolio-social-preview.png 1200x630 link-preview image
   assets/qr/ ................................ EMPTY until finalize step (by design)
   assets/cards/ ............................. EMPTY until finalize step (cards need the QR)
   standalone/Ahmed_Alzahrani_Portfolio_Standalone.html
        offline backup — PDFs + VCF embedded once as base64, works without hosting
   tools/ .................................... finalize script + card templates + all sources

3) UPDATING THE CV / تحديث السيرة
   Edit tools/src/cv_en.html + cv_ar.html (shared style: cv_style.css), then:
       cd tools/src && python3 -m weasyprint cv_en.html ../../Ahmed_Alzahrani_CV_EN.pdf
                       python3 -m weasyprint cv_ar.html ../../Ahmed_Alzahrani_CV_AR.pdf
   Then rebuild the standalone copy (tools/src has all portfolio parts; see
   build_package.py in the original work folder) or re-run the finalize script.

4) UPDATING THE VCF / تحديث جهة الاتصال
   Edit Ahmed_Alzahrani.vcf directly (keep CRLF line endings, UTF-8).
   The finalize script re-adds the URL line automatically.

5) REGENERATING THE QR IF THE URL CHANGES
   Re-run tools/finalize_after_publish.py with the new URL. It regenerates
   the QR (navy #0E2A44, EC level H, 4-module quiet zone, 1200x1200 PNG +
   printable SVG), decodes it back to verify, and rebuilds both cards.

6) WARNING / تحذير
   Do NOT change the QR destination after printing physical cards unless the
   printed URL is a redirect you control. A printed QR is permanent.

7) INDEXING STATUS / حالة الفهرسة
   The page ships with: noindex, nofollow, noarchive, nosnippet
   (meta robots + meta googlebot). If the host supports response headers, add:
       X-Robots-Tag: noindex, nofollow, noarchive, nosnippet
   Keep the URL unlisted; do not link it from any public page or sitemap.

8) LAST TEST DATE / آخر اختبار
   2026-08-14 — automated DOM tests (jsdom), HTML5 parse, CSS parse,
   PDF render + metadata check, VCF parse check. See delivery report.

9) QR TEST RESULTS / نتائج اختبار QR
   NOT APPLICABLE YET — QR intentionally not generated (no real URL).
   The finalize script refuses to produce a QR without decode verification.

10) PURPOSE / الغرض
    This package is meant for direct sharing with recruiters (QR on a phone
    card, direct link in chats). It is intentionally excluded from search
    engines.
