# -*- coding: utf-8 -*-
"""Static site generator for stiersconstruction.com  ->  ./public  (deploy this folder to Netlify)"""
import hashlib, html, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import *
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blog'))
from blog_data import POSTS, POST_BY_SLUG, CATS
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'areas'))
from towns import TOWNS, TOWN_BY_SLUG, WATERS, GROUPS
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = f'{ROOT}/src', f'{ROOT}/public'
URL = SITE['url']
IM = json.load(open(f'{SRC}/data/images.json'))
esc = lambda s: html.escape(s, quote=True)

# ---------- reset output + hashed assets ----------
os.makedirs(OUT, exist_ok=True)
for _f in os.listdir(OUT):
    _p = f'{OUT}/{_f}'; shutil.rmtree(_p) if os.path.isdir(_p) else os.remove(_p)
os.makedirs(f'{OUT}/assets/css'); os.makedirs(f'{OUT}/assets/js'); os.makedirs(f'{OUT}/assets/fonts')
def hashed(src, dest_dir, ext):
    data = open(src, 'rb').read()
    try:  # minify when the minifiers are installed (pip install rcssmin rjsmin); output is identical in behaviour
        if ext == 'css':
            import rcssmin; data = rcssmin.cssmin(data.decode('utf-8')).encode('utf-8')
        elif ext == 'js':
            import rjsmin; data = rjsmin.jsmin(data.decode('utf-8')).encode('utf-8')
    except ImportError:
        pass
    name = f"site.{hashlib.md5(data).hexdigest()[:8]}.{ext}"
    open(f'{OUT}/assets/{dest_dir}/{name}', 'wb').write(data)
    return f'/assets/{dest_dir}/{name}'
CSS = hashed(f'{SRC}/css/site.css', 'css', 'css')
JS = hashed(f'{SRC}/js/site.js', 'js', 'js')
shutil.copy(f'{SRC}/fonts/archivo-latin.woff2', f'{OUT}/assets/fonts/archivo-latin.woff2')
shutil.copytree(f'{SRC}/assets/img', f'{OUT}/assets/img')
for f in os.listdir(f'{SRC}/assets'):
    p = f'{SRC}/assets/{f}'
    if os.path.isfile(p): shutil.copy(p, f'{OUT}/assets/{f}')
XSEC = open(f'{SRC}/partials/xsec.html').read()

# ---------- helpers ----------
def img(key, sizes='100vw', cls='', lazy=True, prio=False, alt=None):
    m = IM[key]; files = m['files']
    srcset = ', '.join(f'/assets/img/{n} {w}w' for w, n in files)
    default = files[min(1, len(files) - 1)][1]
    a = esc(alt if alt is not None else m['alt'])
    extra = ' fetchpriority="high"' if prio else ''
    load = 'loading="lazy" decoding="async"' if lazy and not prio else 'decoding="async"'
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="/assets/img/{default}" srcset="{srcset}" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" alt="{a}" {load}{extra}>')

def img_url(key, width=None):
    files = IM[key]['files']
    n = files[-1][1] if width is None else min(files, key=lambda f: abs(f[0] - width))[1]
    return f'/assets/img/{n}'

PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
CHEV = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M2 4l4 4 4-4"/></svg>'
IG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor" stroke="none"/></svg>'
FB = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.6h2.6l.4-3h-3V8.5c0-.9.3-1.5 1.5-1.5h1.6V4.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21z"/></svg>'
CHECK_SVG = '<svg class="thanks-check" viewBox="0 0 64 64" fill="none" aria-hidden="true"><circle class="ring" cx="32" cy="32" r="29" stroke="currentColor" stroke-width="3"/><path class="tick" d="M19 33.5 27.5 42 45 23" stroke="currentColor" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'
PHOTO_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="4.5" width="19" height="15" rx="2"/><circle cx="8.5" cy="10" r="1.75"/><path d="m3 16.5 5-5 4 4 3.5-3.5L21 16"/></svg>'
def product_photo(label):
    return f'<div class="product-photo" role="img" aria-label="Photo of the {esc(label)} coming soon">{PHOTO_SVG}<span>Photo coming soon</span></div>'

def tel(cls='', label=None, icon=False):
    return f'<a class="{cls}" href="tel:{SITE["phone_e164"]}">{PHONE_SVG if icon else ""}{label or SITE["phone"]}</a>'

def with_article(name, plural=False):
    if plural or name.lower().startswith('the '): return name
    return ('an ' if name[:1].upper() in 'AEIOUX' else 'a ') + name

def nav_html(active):
    water = [s for s in SERVICES if s['group'] == 'water']; land = [s for s in SERVICES if s['group'] == 'land']
    li = lambda ss: ''.join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in ss)
    cur = lambda p: ' aria-current="page"' if active == p else ''
    return f'''<nav id="site-nav" class="site-nav" aria-label="Primary"><ul class="nav-list">
<li class="has-menu"><button type="button" class="nav-link menu-btn" aria-expanded="false" aria-controls="menu-services">Services{CHEV}</button>
<div class="mega" id="menu-services"><div><p class="mega-h">In and over the water</p><ul>{li(water)}</ul></div><div><p class="mega-h">On the lot</p><ul>{li(land)}</ul></div><div class="mega-foot"><a class="mega-all" href="/services/">See all services</a><a class="mega-all" href="/service-area/">Where we work</a><a class="mega-all" href="/services/boat-hoists/hi-tide/">Hi-Tide boat lifts</a><a class="mega-all" href="/services/docks/candock/">Candock floating docks</a></div></div></li>
<li><a class="nav-link" href="/projects/"{cur('projects')}>Projects</a></li>
<li><a class="nav-link" href="/financing/"{cur('financing')}>Financing</a></li>
<li><a class="nav-link" href="/blog/"{cur('blog')}>Blog</a></li>
<li><a class="nav-link" href="/about/"{cur('about')}>About</a></li>
<li><a class="nav-link" href="/contact/"{cur('contact')}>Contact</a></li></ul>
<div class="nav-cta-m"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></nav>'''

def header(active):
    return f'''<header class="site-header"><div class="wrap header-inner">
<a class="brand" href="/" aria-label="Stier’s Welding &amp; Construction, home"><img src="/assets/mark-dark.png" width="160" height="88" alt=""><span class="brand-text"><span class="brand-name">Stier’s</span> <span class="brand-sub">Welding &amp; Construction</span></span></a>
{nav_html(active)}
{tel('header-phone', '<span>' + SITE['phone'] + '</span>', True).replace('<a class="header-phone"', '<a class="header-phone" aria-label="Call ' + SITE['phone'] + '"')}
<a class="btn btn-primary header-cta" href="/contact/">Get a free quote</a>
<button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span class="bars" aria-hidden="true"><i></i></span><span>Menu</span></button>
</div></header>'''

def footer():
    water = [s for s in SERVICES if s['group'] == 'water']; land = [s for s in SERVICES if s['group'] == 'land']
    ls = lambda ss: ''.join(f'<li><a href="/services/{s["slug"]}/">{s["name"]}</a></li>' for s in ss)
    return f'''<footer class="site-footer on-dark"><div class="wrap"><div class="footer-grid">
<div class="foot-brand"><img src="/assets/logo-dark-200.png" width="200" height="149" alt="Stier’s Welding &amp; Construction" loading="lazy">
<p>Marine and construction contractor serving waterfront communities throughout Metro Detroit.</p>
<div class="social"><a href="{SITE['instagram']}" aria-label="Stier’s Construction on Instagram" rel="noopener" target="_blank">{IG}</a><a href="{SITE['facebook']}" aria-label="Stier’s Construction on Facebook" rel="noopener" target="_blank">{FB}</a></div></div>
<div><h2>In and over the water</h2><ul>{ls(water)}</ul></div>
<div><h2>On the lot</h2><ul>{ls(land)}</ul></div>
<div><h2>Contact</h2><ul>
<li><a href="tel:{SITE['phone_e164']}">{SITE['phone']}</a></li><li><a href="mailto:{SITE['email']}">{SITE['email']}</a></li></ul>
<p class="foot-hours mt-s">Monday to Friday, 8am to 5pm<br>Weekends by appointment</p>
<ul class="mt-s"><li><a href="/contact/">Get a free quote</a></li><li><a href="/financing/">Financing</a></li><li><a href="/blog/">Blog</a></li><li><a href="/projects/">Projects</a></li><li><a href="/about/">About</a></li><li><a href="/service-area/">Service area</a></li><li><a href="/careers/">Careers</a></li></ul></div>
</div><div class="foot-areas"><h2>Communities We Serve</h2><ul class="area-links">{''.join(f'<li><a href="/service-area/{t[chr(115)+chr(108)+chr(117)+chr(103)]}/">{t[chr(110)+chr(97)+chr(109)+chr(101)]}</a></li>' for t in TOWNS)}</ul></div><div class="footer-base"><span>© {SITE['year']} {SITE['name']}. All rights reserved.</span><span>Metro Detroit, Michigan</span></div></div></footer>'''

def mobile_bar(fin=True):
    if not fin:
        return f'<nav class="mobile-bar" aria-label="Quick contact"><a class="btn btn-ghost" href="tel:{SITE["phone_e164"]}">{PHONE_SVG}Call</a><a class="btn btn-primary" href="/contact/">Get a free quote</a></nav>'
    return f'<nav class="mobile-bar has-fin" aria-label="Quick contact"><a class="btn btn-ghost" href="tel:{SITE["phone_e164"]}">{PHONE_SVG}Call</a><a class="btn btn-primary" href="/contact/">Free quote</a><a class="btn btn-ghost" href="/financing/" data-fin-open="mobile_bar">Financing</a></nav>'

CALC_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="2.5" width="14" height="19" rx="2"/><rect x="8" y="5.5" width="8" height="3.5"/><path d="M8 13h.01M12 13h.01M16 13h.01M8 17h.01M12 17h.01M16 17h.01"/></svg>'
FIN_FRAME_SRC = 'https://www.enhancify.com/stiersconstruction?siteaction=realwidget&utm_source=realwidget&color1=%23C8202B&color2=%2312323F&color3=%23FFFFFF'
def fin_launcher():
    return f'''<button type="button" class="fin-fab" data-fin-open="sticky_button" aria-haspopup="dialog" aria-controls="fin-dialog" aria-label="Financing options" title="Financing options">{CALC_SVG}</button>
<dialog id="fin-dialog" class="fin-dialog" aria-labelledby="fin-t" data-src="{esc(FIN_FRAME_SRC)}">
<div class="fin-bar"><h2 id="fin-t">Financing options</h2><a href="{ENH_PAGE_URL}" target="_blank" rel="noopener">Open in new tab</a><button type="button" class="fin-close" autofocus>Close</button></div>
<div class="fin-body"><p class="widget-loading">Loading financing options...</p></div>
<p class="fin-note">Financing is arranged through Enhancify.com, an independent marketplace, not a lender. Stier’s Construction does not make credit decisions. Offers are subject to credit approval, and terms vary by lender. <a href="/financing/">More about financing</a></p></dialog>'''
ENH_PAGE_URL = 'https://www.enhancify.com/stiersconstruction'

def cta_band(h='Tell us about your project', p=None):
    p = p or 'Send the address, what you want done and a few photos. Quotes are free. Prefer to talk? Call us Monday to Friday, 8am to 5pm.'
    return f'''<section class="cta-band" aria-labelledby="cta-h"><div class="wrap cta-inner"><div><h2 id="cta-h">{h}</h2><p>{p}</p><p class="cta-fin"><a href="/financing/">Financing available, subject to approval</a></p></div>
<div class="btn-row"><a class="btn btn-light" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div></section>'''

def faq_html(faqs, h='Common questions'):
    items = ''.join(f'<details><summary>{q}</summary><div class="answer">{a}</div></details>' for q, a in faqs)
    return f'<div class="faq">{items}</div>'

def crumbs(trail):
    lis = ''.join(f'<li><a href="{u}">{n}</a></li>' if u else f'<li><span aria-current="page">{n}</span></li>' for n, u in trail)
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'

# ---------- structured data ----------
def business_node():
    return {
     '@type': 'GeneralContractor', '@id': f'{URL}/#business',
     'name': SITE['seo_name'], 'alternateName': [SITE['name'], SITE['legal_alt']], 'url': f'{URL}/',
     'logo': {'@type': 'ImageObject', 'url': f'{URL}/assets/logo-light-400.png', 'width': 400, 'height': 298},
     'image': [f'{URL}/assets/og-image.jpg'],
     'description': 'Marine and construction contractor in Metro Detroit: seawalls, docks, pilings, boat hoists, dredging, welding and fabrication, excavating, demolition, concrete and decks.',
     'telephone': '+1-586-703-7214', 'email': SITE['email'], 'address': {'@type': 'PostalAddress', 'addressRegion': 'MI', 'addressCountry': 'US'},
     'areaServed': [{'@type': 'AdministrativeArea', 'name': 'Metro Detroit, Michigan'}, {'@type': 'Place', 'name': 'Lake St. Clair'}, {'@type': 'Place', 'name': 'Detroit River'}, {'@type': 'Place', 'name': 'St. Clair River'}] + [{'@type': 'City', 'name': t['name'], 'containedInPlace': {'@type': 'AdministrativeArea', 'name': t['county'] + ' County, Michigan'}} for t in TOWNS],
     'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '08:00', 'closes': '17:00'}],
     'sameAs': [SITE['instagram'], SITE['facebook']],
     'employee': [{'@type': 'Person', 'name': 'Kevin', 'jobTitle': 'Owner'}, {'@type': 'Person', 'name': 'Chris', 'jobTitle': 'Project Manager'}],
     'knowsAbout': [s['name'] for s in SERVICES],
     'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Services', 'itemListElement': [
        {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['name'], 'url': f'{URL}/services/{s["slug"]}/'}} for s in SERVICES]},
    }
WEBSITE = {'@type': 'WebSite', '@id': f'{URL}/#website', 'url': f'{URL}/', 'name': SITE['seo_name'], 'publisher': {'@id': f'{URL}/#business'}, 'inLanguage': 'en-US'}

def strip_tags(s):
    import re
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()

def breadcrumb_ld(trail):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': f'{URL}{u}' if u else None} for i, (n, u) in enumerate(trail)]}

def faq_ld(faqs):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in faqs]}

def ld_script(nodes):
    def clean(o):
        if isinstance(o, dict): return {k: clean(v) for k, v in o.items() if v is not None}
        if isinstance(o, list): return [clean(x) for x in o]
        return o
    data = {'@context': 'https://schema.org', '@graph': clean(nodes)}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '</script>'


# ---------- title case (headlines, titles, buttons, nav) ----------
SMALL = {'a','an','and','as','at','but','by','for','in','nor','of','on','or','per','the','to','up','via','vs','vs.'}
KEEP_LOWER = {'ft','lb','lbs','e.g.','i.e.'}
def _tc_word(w, force_cap):
    m = re.match(r'^([^A-Za-z0-9&]*)(.*?)([^A-Za-z0-9&®™]*)$', w)
    lead, core, trail = m.group(1), m.group(2), m.group(3)
    if not core: return w
    if '@' in core or core.lower().startswith(('http', 'www')) or '/' in core: return w
    low = core.lower()
    if low in KEEP_LOWER: return lead + core + trail
    parts = re.split(r'(-)', core)
    out = []
    for i, part in enumerate(parts):
        if part == '-' or not part: out.append(part); continue
        pl = part.lower().rstrip('.')
        first_part = (i == 0)
        if pl in SMALL and not (force_cap and first_part):
            out.append(part.lower() if part.isalpha() or part.endswith('.') else part)
        elif part[0].isalpha():
            out.append(part[0].upper() + part[1:])
        else:
            out.append(part)
    return lead + ''.join(out) + trail

def tc(text):
    """Title-case a plain string (AP-style small words), never lowercasing existing capitals."""
    tokens = re.split(r'(\s+)', text)
    idx = [i for i, t in enumerate(tokens) if t.strip()]
    if not idx: return text
    for n, i in enumerate(idx):
        prev = tokens[idx[n - 1]] if n else ''
        force = (n == 0) or (n == len(idx) - 1) or prev.endswith((':', '?', '!', '—', '–'))
        tokens[i] = _tc_word(tokens[i], force)
    return ''.join(tokens)

def _tc_html(inner):
    parts = re.split(r'(<[^>]+>)', inner)
    tix = [i for i, p in enumerate(parts) if not p.startswith('<') and p.strip()]
    for n, i in enumerate(tix):
        raw = parts[i]
        lead = raw[:len(raw) - len(raw.lstrip())]; trail = raw[len(raw.rstrip()):]
        core = raw.strip()
        prev = parts[tix[n - 1]] if n else ''
        segs = re.split(r'(\s+)', core)
        # emulate tc() with first/last awareness across nodes
        words = [j for j, s in enumerate(segs) if s.strip()]
        for k, j in enumerate(words):
            pw = segs[words[k - 1]] if k else prev.strip().split(' ')[-1] if prev.strip() else ''
            force = (n == 0 and k == 0) or (n == len(tix) - 1 and k == len(words) - 1) or pw.endswith((':', '?', '!', '—', '–'))
            segs[j] = _tc_word(segs[j], force)
        parts[i] = lead + ''.join(segs) + trail
    return ''.join(parts)

def _sub_tag(html, tag_re, inner_ok=None):
    def rep(m):
        inner = m.group(2)
        if inner_ok and not inner_ok(re.sub(r'<[^>]+>', '', inner)): return m.group(0)
        return m.group(1) + _tc_html(inner) + m.group(3)
    return re.sub(tag_re, rep, html, flags=re.S)

def _short_label(t):
    t = t.strip()
    return bool(t) and len(t.split()) <= 7 and not re.search(r'[.?!,@]', t.replace('St.', ''))

def postprocess(h):
    h = _sub_tag(h, r'(<(?:h[1-4]|summary)\b[^>]*>)(.*?)(</(?:h[1-4]|summary)>)')
    h = _sub_tag(h, r'(<title\b[^>]*>)(.*?)(</title>)')
    h = _sub_tag(h, r'(<(?:a|button)\b[^>]*\bclass="[^"]*\b(?:btn|nav-link|mega-all|textlink|fin-fab)\b[^"]*"[^>]*>)(.*?)(</(?:a|button)>)', _short_label)
    h = _sub_tag(h, r'(<p class="mega-h">)(.*?)(</p>)')
    h = _sub_tag(h, r'(<p class="role"[^>]*>)(.*?)(</p>)')
    h = _sub_tag(h, r'(<b>)(.*?)(</b>)')
    h = _sub_tag(h, r'(<th scope="col">)(.*?)(</th>)')
    h = _sub_tag(h, r'(<button type="button" data-filter="[^"]*"[^>]*>)(.*?)(</button>)')
    def in_block(h, open_re, fn):
        return re.sub(open_re, lambda m: fn(m.group(0)), h, flags=re.S)
    h = in_block(h, r'<ul class="facts">.*?</ul>', lambda blk: _sub_tag(blk, r'(<strong>)(.*?)(</strong>)'))
    h = in_block(h, r'<nav class="crumbs".*?</nav>', lambda blk: _sub_tag(_sub_tag(blk, r'(<a\b[^>]*>)(.*?)(</a>)'), r'(<span aria-current="page">)(.*?)(</span>)'))
    h = in_block(h, r'<footer class="site-footer.*?</footer>', lambda blk: _sub_tag(blk, r'(<a\b[^>]*>)(.*?)(</a>)', lambda t: '@' not in t and not re.search(r'\d', t) and _short_label(t)))
    h = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")(.*?)(">)', lambda m: m.group(1) + tc(html.unescape(m.group(2)).replace('&', '&')).replace('&', '&amp;').replace('"', '&quot;') + m.group(3), h)
    return h


# ---------- SEO titles: "<keyword phrase> | Stier’s Marine & Construction" ----------
BRAND = SITE['seo_name']
TITLE_MAP = {
 '/': 'Stier’s Marine & Construction | Metro Detroit Seawalls & Docks',
 '/services/': 'Marine & Waterfront Services',
 '/services/seawalls/': 'Seawall Installation & Repair',
 '/services/docks/': 'Dock Installation & Repair',
 '/services/pilings/': 'Piling Installation & Removal',
 '/services/boat-hoists/': 'Boat Hoist Installation & Repair',
 '/services/dredging/': 'Canal & Boat Well Dredging',
 '/services/welding-fabrication/': 'Custom Welding & Fabrication',
 '/services/excavating-grading/': 'Excavating, Grading & Hauling',
 '/services/demolition/': 'Demolition & Concrete Removal',
 '/services/concrete/': 'Concrete Installation & Removal',
 '/services/decks/': 'Custom Deck Builders',
 '/projects/': 'Seawall & Dock Project Photos',
 '/financing/': 'Waterfront Project Financing',
 '/about/': 'About Our Owner-Led Crew',
 '/service-area/': 'Metro Detroit Service Area',
 '/contact/': 'Get a Free Quote',
 '/careers/': 'Marine & Welding Jobs',
 '/blog/': 'Marine Construction Blog',
 '/thank-you/': 'Thank You',
 '/404.html': 'Page Not Found',
}
def seo_title(path, title):
    t = TITLE_MAP.get(path, title)
    t = re.sub(r'\s*\|\s*Stier’s(?: Construction)?$', '', t)
    t = tc(t)
    return t if BRAND in t else f'{t} | {BRAND}'

# ---------- page shell ----------
SITEMAP = []
def page(path, title, desc, body, active='', trail=None, ld=None, preload=None, noindex=False, bar=True, ptype='WebPage', sm_images=None, prio=0.7):
    title = seo_title(path, title)
    canon = f'{URL}{path}'
    robots = 'noindex,follow' if noindex else 'index,follow,max-image-preview:large'
    nodes = [business_node(), WEBSITE, {'@type': ptype, '@id': f'{canon}#webpage', 'url': canon, 'name': title, 'description': desc, 'isPartOf': {'@id': f'{URL}/#website'}, 'about': {'@id': f'{URL}/#business'}, 'inLanguage': 'en-US'}]
    if trail and len(trail) > 1: nodes.append(breadcrumb_ld(trail))
    nodes += ld or []
    pre = ''
    if preload:
        m = IM[preload]; ss = ', '.join(f'/assets/img/{n} {w}w' for w, n in m['files'])
        pre = f'<link rel="preload" as="image" imagesrcset="{ss}" imagesizes="{preload_sizes(preload)}" fetchpriority="high">'
    og = f'{URL}/assets/og-image.jpg'
    html_ = f'''<!doctype html>
<html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{canon}"><meta name="robots" content="{robots}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{esc(SITE['seo_name'])}"><meta property="og:locale" content="en_US"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Stier’s excavator setting steel sheet piling for a seawall in Metro Detroit">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{og}">
<meta name="theme-color" content="#0D2530"><meta name="format-detection" content="telephone=yes">
<link rel="icon" href="/assets/favicon.ico" sizes="48x48"><link rel="icon" href="/assets/favicon-64.png" type="image/png" sizes="64x64"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest"><link rel="alternate" type="application/rss+xml" title="Stier’s Marine &amp; Construction Blog" href="/blog/feed.xml">
<link rel="preload" href="/assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>{pre}
<link rel="stylesheet" href="{CSS}"><script src="{JS}" defer></script><noscript><style>@media (max-width:1039px){{.nav-toggle{{display:none}}.site-nav{{display:block;position:static;background:none;padding:0 0 12px;width:100%;order:5;overflow:visible}}.header-inner{{flex-wrap:wrap}}}}</style></noscript>
{ld_script(nodes)}
</head><body{'' if bar else ' class="no-bar"'}>
<a class="skip" href="#main">Skip to content</a>
{header(active)}
<main id="main">{body}</main>
{footer()}
{(mobile_bar(path != '/financing/') + (fin_launcher() if path != '/financing/' else '')) if bar else ''}
</body></html>'''
    html_ = postprocess(html_)
    fp = f'{OUT}{path}index.html' if path != '/404.html' else f'{OUT}/404.html'
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w', encoding='utf-8').write(html_)
    if not noindex: SITEMAP.append((path, prio, sm_images or []))

def preload_sizes(key):
    return '100vw' if key == HERO_KEY else '(min-width:940px) 46vw, 92vw'

HERO_KEY = 'sheet-pile-excavator-canal-home'

# ============================================================ HOME
def home():
    facts = [('Owner on the job', 'Kevin has 15+ years of hands-on welding, marine and construction work.'),
             ('One crew for the whole lot', 'Wall, dock, hoist, steel, concrete and deck from one contractor.'),
             ('Our own trucks', 'Hauling and material delivery run on our own fleet.'),
             ('Homes, businesses, marinas', 'Residential, commercial and marina clients.')]
    facts_html = ''.join(f'<li><strong>{a}</strong><span>{b}</span></li>' for a, b in facts)
    hero = f'''<section class="hero on-dark" aria-labelledby="h1"><div class="hero-media">{img(HERO_KEY, '100vw', prio=True, lazy=False, alt='')}</div>
<div class="wrap hero-body"><h1 id="h1">Seawall, dock and marine construction in Metro Detroit</h1>
<p class="lead">Stier’s Construction builds and repairs seawalls, docks, pilings and boat hoists on Lake St. Clair and the Detroit River, then handles the welding, concrete, excavation and decks on the shore side. Owner-operated and committed to honest work and clear communication.</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div>
<ul class="facts">{facts_html}</ul></div></section>'''

    def leg(s, n):
        return f'<li data-part="{s["slug"]}"><a href="/services/{s["slug"]}/"><span class="num" aria-hidden="true">{n}</span><span><b>{s["name"]}</b><small>{s["summary"]}</small></span></a></li>'
    water = ''.join(leg(s, i + 1) for i, s in enumerate(SERVICES[:5])); land = ''.join(leg(s, i + 6) for i, s in enumerate(SERVICES[5:]))
    xsec = f'''<section class="section section-alt" id="services" aria-labelledby="xs-h"><div class="wrap">
<div class="section-head"><h2 id="xs-h">Everything on a waterfront lot, from the deck to the channel bottom</h2>
<p>Most waterfront jobs touch more than one trade. Pick any numbered part of this cross-section to see what we do there.</p></div>
<div class="xsec-grid"><figure class="xsec-fig"><div class="xsec-scroll" tabindex="0" role="region" aria-label="Cross-section illustration of a waterfront lot">{XSEC}</div><figcaption>Illustration of a typical seawall setup. Your site may differ. <span class="swipe-hint">Swipe sideways to see the whole drawing.</span></figcaption></figure>
<div class="legend-cols"><div class="legend-group"><h3>In and over the water</h3><ul class="legend">{water}</ul></div><div class="legend-group"><h3>On the lot</h3><ul class="legend">{land}</ul></div></div></div></div></section>'''

    def tile(cls, key, href, b, t, sizes):
        return f'<a class="tile {cls}" href="{href}"><figure>{img(key, sizes)}<figcaption><b>{b}</b>{t}</figcaption></figure></a>'
    mosaic = f'''<section class="section" aria-labelledby="w-h"><div class="wrap"><div class="section-head"><h2 id="w-h">From the job site</h2><p>Real photos from our own jobs, on the water and on shore.</p></div>
<div class="mosaic">
{tile('t-a', 'barge-excavator-canal', '/services/pilings/', 'Barge work in a canal', 'Pilings and marine construction from the water.', '(min-width:860px) 40vw, 92vw')}
{tile('t-b', 'new-deck-over-seawall', '/services/decks/', 'A new deck along the seawall', 'Waterfront decks and walls, built together.', '(min-width:860px) 33vw, 92vw')}
{tile('t-c', 'welding-at-night-waterfront', '/services/welding-fabrication/', 'Welding after dark', 'Mobile welding on site.', '(min-width:860px) 25vw, 46vw')}
{tile('t-d', 'boat-lift-covered-slip', '/services/boat-hoists/', 'Boat lift in a covered slip', 'Hoist installs and service.', '(min-width:860px) 25vw, 46vw')}
{tile('t-e', 'new-concrete-patio', '/services/concrete/', 'Fresh concrete patio', 'Finished flatwork.', '(min-width:860px) 33vw, 92vw')}
</div><p class="mt-m"><a class="btn btn-outline" href="/projects/">See all project photos</a></p></div></section>'''

    why_items = [('The owner is on the job', 'Kevin brings more than 15 years of hands-on welding, marine and construction experience and stays directly involved on site.'),
                 ('One contractor for the whole waterfront', 'Seawalls, docks, pilings, hoists, welding, concrete, excavation and decks are all part of what we do, so you do not have to line up a different crew for each step.'),
                 ('Welding in the shop and in the field', 'Custom fabrication and mobile welding mean rails, frames and marine steel are built and repaired by the same crew.'),
                 ('Our own trucks', 'Concrete removal, debris hauling and deliveries of topsoil, sand and stone run on our own fleet.'),
                 ('Clear communication', 'One customer review calls out the owner’s communication and a job finished on time with zero issues.')]
    why = f'''<section class="section section-alt" aria-labelledby="y-h"><div class="wrap why"><div class="why-head"><h2 id="y-h">Why waterfront owners call Stier’s</h2>
<p class="lead mt-s">We take pride in dependable, high-quality marine and construction services. We believe in honest work, clear communication, and a commitment to doing the job right, every time.</p><div class="btn-row mt-m"><a class="btn btn-primary" href="/contact/">Get a free quote</a></div></div>
<ul class="why-list">{''.join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a, b in why_items)}</ul></div></section>'''

    hitide = f'''<section class="section section-alt" aria-labelledby="ht-h"><div class="wrap split flip"><figure>{img('boat-lift-covered-slip', '(min-width:900px) 46vw, 92vw')}</figure><div><p class="eyebrow">Authorized dealer</p><h2 id="ht-h">We sell Hi-Tide boat lifts</h2>
<p class="lead mt-s">Stier’s Construction is an authorized Hi-Tide boat lift dealer. Buy the lift and have it installed and serviced by the same crew, backed by our own cable, motor and welding work.</p>
<p class="btn-row mt-s"><a class="btn btn-dark" href="/services/boat-hoists/hi-tide/">Browse the Hi-Tide lineup</a>{tel('btn btn-outline', SITE['phone'], True)}</p></div></div></section>'''

    candock = f'''<section class="section" aria-labelledby="cd-h"><div class="wrap split"><figure>{img('candock-floating-dock-install', '(min-width:900px) 46vw, 92vw')}</figure><div><p class="eyebrow">Authorized dealer</p><h2 id="cd-h">We sell Candock floating docks</h2>
<p class="lead mt-s">Stier’s Construction is an authorized Candock dealer, including the JetRoll drive-on dock for personal watercraft. One crew for the dock, the install and everything after.</p>
<p class="btn-row mt-s"><a class="btn btn-dark" href="/services/docks/candock/">Browse Candock floating docks</a>{tel('btn btn-outline', SITE['phone'], True)}</p></div></div></section>'''

    rev = f'''<section class="section section-dark on-dark" aria-labelledby="r-h"><div class="wrap"><div class="section-head"><h2 id="r-h">What customers say</h2></div>
<div class="reviews"><figure class="quote"><blockquote style="margin:0"><p>“{QUOTES[0][0]}”</p></blockquote><figcaption><cite>{QUOTES[0][1]}</cite></figcaption></figure>
<figure class="quote"><blockquote style="margin:0"><p>“{QUOTES[1][0]}”</p></blockquote><figcaption><cite>{QUOTES[1][1]}</cite></figcaption></figure></div></div></section>'''

    team = f'''<section class="section" aria-labelledby="t-h"><div class="wrap split"><div><h2 id="t-h">Kevin and Chris lead the crew</h2>
<div class="mt-m"><div class="person" style="border-color:var(--concrete-300)"><h3>Kevin</h3><p class="role" style="color:var(--muted)">Owner</p><p>More than 15 years of hands-on welding, marine and construction experience. An active, on-site contractor.</p></div>
<div class="person" style="border-color:var(--concrete-300)"><h3>Chris</h3><p class="role" style="color:var(--muted)">Project manager</p><p>More than 8 years in construction, specializing in carpentry, concrete and marine work. Also owns a trucking business, Stier’s Enterprise.</p></div></div>
<p class="mt-s"><a class="textlink" href="/about/">Meet the team</a></p></div>
<figure>{img('stiers-excavator-demo-site', '(min-width:900px) 46vw, 92vw')}</figure></div></section>'''

    area = f'''<section class="section section-alt" aria-labelledby="a-h"><div class="wrap split flip"><figure>{img('barge-open-water', '(min-width:900px) 46vw, 92vw')}</figure><div><h2 id="a-h">Serving Metro Detroit’s waterfront</h2>
<p class="lead mt-s">We serve waterfront communities on Lake St. Clair, the St. Clair River and the Detroit River.</p>
<ul class="town-links" aria-label="Communities we serve">{''.join(f'<li><a href="/service-area/{t[chr(115)+chr(108)+chr(117)+chr(103)]}/">{t[chr(110)+chr(97)+chr(109)+chr(101)]}</a></li>' for t in TOWNS)}</ul><p class="btn-row mt-s"><a class="btn btn-dark" href="/service-area/">See where we work</a>{tel('btn btn-outline', SITE['phone'], True)}</p></div></div></section>'''

    latest = [POST_BY_SLUG[s] for s in ('seawall-guide-metro-detroit', 'michigan-permits-seawalls-docks-dredging', 'michigan-winter-dock-seawall-damage')]
    guides = f'<section class="section section-alt" aria-labelledby="gd-h"><div class="wrap"><div class="section-head"><h2 id="gd-h">Waterfront Guides for Metro Detroit Owners</h2><p>Plain-English answers on seawalls, docks, permits and more.</p></div><ul class="post-list">{"".join(post_row(p) for p in latest)}</ul><p class="mt-m"><a class="btn btn-outline" href="/blog/">Read the Blog</a></p></div></section>'
    faq = f'''<section class="section" aria-labelledby="f-h"><div class="wrap"><div class="section-head"><h2 id="f-h">Questions we hear a lot</h2></div>{faq_html(HOME_FAQS)}</div></section>'''
    fin = f'''<section class="fin-band" aria-labelledby="fb-h"><div class="wrap fin-band-in"><div><h2 id="fb-h">Financing available for your project</h2><p>Spread the cost of a seawall, dock, deck or concrete job into monthly payments. Arranged through Enhancify, subject to credit approval.</p></div><a class="btn btn-dark" href="/financing/">See financing options</a></div></section>'''
    body = hero + xsec + mosaic + why + hitide + candock + rev + fin + team + area + guides + faq + cta_band()
    page('/', 'Marine & Seawall Contractor in Metro Detroit | Stier’s',
         'Seawalls, docks, pilings, hoists, dredging, welding, concrete and decks on Lake St. Clair and the Detroit River. Owner-led crew. Free quotes.',
         body, ld=[faq_ld(HOME_FAQS)], preload=HERO_KEY, prio=1.0, sm_images=[img_url(HERO_KEY)])

# ============================================================ SERVICE PAGES
def sizechart():
    axis = '<div class="axis" aria-hidden="true"><span></span><div><span>0 ft</span><span>10</span><span>20</span><span>30</span><span>40 ft</span></div><span></span></div>'
    rows = ''
    for name, lo, hi, rng, desc in HOIST_SIZES:
        rows += f'<li><div><b>{name}</b><span class="rng">{desc}</span></div><div class="track" aria-hidden="true"><i style="left:{lo/40*100:.1f}%;width:{(hi-lo)/40*100:.1f}%"></i></div><strong class="range">{rng}</strong></li>'
    return f'<p class="measure">Length is the starting point. These are the size ranges we work from:</p>{axis}<ul class="sizechart">{rows}</ul><div class="mt-m">{note("<p>Davits are available too. Ranges are general guidance: weight, beam and hull shape also matter, so send us your boat’s make, length and weight and we will match the lift.</p>")}</div>'

def service_page(s):
    path = f'/services/{s["slug"]}/'
    trail = [('Home', '/'), ('Services', '/services/'), (s['name'], None)]
    checks = ''.join(f'<li>{c}</li>' for c in s['checks'])
    hero = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div class="page-hero-grid"><div><h1>{s['h1']}</h1><p class="lead">{s['lead']}</p>
<ul class="hero-checks">{checks}</ul><div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div>
<figure class="page-hero-media">{img(s['hero_img'], '(min-width:940px) 46vw, 92vw', prio=True, lazy=False)}</figure></div></div></section>'''
    secs = ''
    for sec in s['sections']:
        h = sec['html'].replace('__SIZECHART__', sizechart())
        secs += f'<section id="{sec["id"]}"><h2>{sec["h2"]}</h2>{h}</section>'
    rel = [BY_SLUG[r] for r in s['related']]
    aside = f'''<aside class="aside-sticky aside-stack" aria-label="Quote and related services"><div class="panel panel-dark"><h3>Get a free quote</h3><small>Mon to Fri, 8am to 5pm</small>
<a class="phone" href="tel:{SITE['phone_e164']}">{SITE['phone']}</a><a class="btn btn-primary" href="/contact/">Send project details</a><p class="fin-line">Financing available. <a href="/financing/">See options</a></p></div>
<div class="panel"><h3>Related work</h3><ul class="related">{''.join(f'<li><a href="/services/{r["slug"]}/"><b>{r["name"]}</b><span>{r["summary"]}</span></a></li>' for r in rel)}</ul></div></aside>'''
    figs = ''.join(f'<figure>{img(k, "(min-width:800px) 30vw, 46vw")}</figure>' for k in s['gallery'][:6])
    strip = f'<section class="section section-alt" aria-labelledby="g-h"><div class="wrap"><div class="section-head"><h2 id="g-h">{s["name"]} work from our jobs</h2></div><div class="strip">{figs}</div><p class="mt-m"><a class="textlink" href="/projects/">See all project photos</a></p></div></section>'
    gs = guides_for(s['slug'])
    guides = (f'<section class="section" aria-labelledby="sg-h"><div class="wrap"><div class="section-head"><h2 id="sg-h">{s["name"]} Guides From Our Blog</h2></div><ul class="post-list">{"".join(post_row(p) for p in gs)}</ul></div></section>') if gs else ''
    faq = f'<section class="section section-alt" aria-labelledby="q-h"><div class="wrap"><div class="section-head"><h2 id="q-h">{s["name"]}: common questions</h2></div>{faq_html(s["faqs"])}</div></section>'
    main = f'<div class="section"><div class="wrap content-grid"><div class="main">{secs}</div>{aside}</div></div>'
    body = hero + main + strip + guides + faq + cta_band('Ready to talk about your ' + s['name'].lower() + ' project?')
    svc = {'@type': 'Service', '@id': f'{URL}{path}#service', 'name': s['name'], 'serviceType': s['name'], 'description': s['desc'], 'url': f'{URL}{path}',
           'provider': {'@id': f'{URL}/#business'}, 'areaServed': [{'@type': 'AdministrativeArea', 'name': 'Metro Detroit, Michigan'}, {'@type': 'Place', 'name': 'Lake St. Clair'}, {'@type': 'Place', 'name': 'Detroit River'}],
           'image': f'{URL}{img_url(s["hero_img"])}'}
    page(path, s['title'], s['desc'], body, active='services', trail=trail, ld=[svc, faq_ld(s['faqs'])], preload=None, ptype='WebPage', prio=0.9,
         sm_images=[img_url(s['hero_img'])] + [img_url(k) for k in s['gallery']])

def services_hub():
    def rows(ss):
        return ''.join(f'''<li class="svc-row"><a href="/services/{s['slug']}/" tabindex="-1" aria-hidden="true">{img(s['hub_img'], '(min-width:800px) 260px, 92vw')}</a>
<div><h3><a href="/services/{s['slug']}/">{s['name']}</a></h3><p>{s['summary']}</p></div><a class="btn btn-outline" href="/services/{s['slug']}/" aria-label="{s['name']} details">Details</a></li>''' for s in ss)
    trail = [('Home', '/'), ('Services', None)]
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div class="page-simple" style="padding-block:clamp(24px,4vw,56px) clamp(40px,6vw,72px)"><h1 style="max-width:20ch">Marine construction and waterfront services in Metro Detroit</h1>
<p class="lead mt-s" style="max-width:60ch">Seawalls, docks, pilings, boat hoists and dredging on the water; welding, excavating, demolition, concrete and decks on the lot. One crew, led by the owner. Not seeing what you are looking for? Send us a message with your project details.</p><div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div></div></section>
<section class="section"><div class="wrap"><h2 class="svc-group-title" style="margin-top:0">In and over the water</h2><ul class="svc-list">{rows(SERVICES[:5])}</ul>
<h2 class="svc-group-title">On the lot</h2><ul class="svc-list">{rows(SERVICES[5:])}</ul></div></section><section class="section section-alt" aria-labelledby="hc-h"><div class="wrap"><div class="section-head"><h2 id="hc-h">Not Sure Where to Start?</h2><p>Most waterfront jobs involve more than one service. A failing seawall may also mean redoing the patio behind it and hauling away old concrete, and a new dock may call for pilings, a hoist and a permit. Start with what you can see:</p></div>
<ul class="related"><li><a href="/services/seawalls/"><b>The wall leans or soil is sinking</b><span>Seawall repair or replacement, including caps, seams and drainage.</span></a></li>
<li><a href="/services/dredging/"><b>Your boat touches bottom</b><span>Boat well, slip and canal dredging to restore depth.</span></a></li>
<li><a href="/services/docks/"><b>A dock or lift shows wear</b><span>Dock repair and re-decking, plus pilings and boat hoist service.</span></a></li>
<li><a href="/services/concrete/"><b>Old slabs, garages or sheds</b><span>Concrete removal, demolition and new flatwork.</span></a></li>
<li><a href="/services/welding-fabrication/"><b>Railings, gates or custom metal</b><span>Shop and mobile welding and fabrication.</span></a></li></ul>
<p class="mt-m">Read our <a href="/blog/">waterfront guides</a> for plain-English answers, or see <a href="/service-area/">where we work</a>.</p></div></section>
{cta_band('Not sure which service you need?', 'Tell us what is going on at your property and we will point you the right way. Quotes are free.')}'''
    page('/services/', 'Marine Construction & Waterfront Services | Stier’s',
         'Seawalls, docks, pilings, boat hoists, dredging, welding, excavating, demolition, concrete and decks in Metro Detroit. One owner-led crew.',
         body, active='services', trail=trail, ld=[{'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{URL}/services/{s["slug"]}/', 'name': s['name']} for i, s in enumerate(SERVICES)]}], prio=0.9,
         sm_images=[img_url(s['hub_img']) for s in SERVICES])

# ============================================================ HI-TIDE BOAT LIFTS
HT_ROOT = '/services/boat-hoists/hi-tide/'
def ht_photo(p, sizes='260px'):
    return img(p['img'], sizes, cls='product-photo-img', alt=f'Hi-Tide {p["name"]} boat lift') if p.get('img') else product_photo(p['name'])

def hi_tide_card(p):
    c = HI_TIDE_CATS[p['cat']]
    return f'''<li class="product-card"><a class="product-card-link" href="{HT_ROOT}{p['slug']}/"><span class="product-photo-frame">{ht_photo(p, '(min-width:1000px) 22vw, (min-width:640px) 30vw, 46vw')}</span>
<div class="product-card-body"><p class="eyebrow">{c['name']}</p><h3>{p['name']}</h3><span class="textlink">View details</span></div></a></li>'''

def hi_tide_hub():
    trail = [('Home', '/'), ('Services', '/services/'), ('Boat Hoists', '/services/boat-hoists/'), ('Hi-Tide Boat Lifts', None)]
    grid = ''.join(hi_tide_card(p) for p in HI_TIDE_PRODUCTS)
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div style="padding-block:clamp(24px,4vw,56px) clamp(36px,5vw,64px)"><p class="eyebrow">Authorized dealer</p><h1 style="max-width:24ch">Hi-Tide boat lifts</h1>
<p class="lead mt-s" style="max-width:62ch">Stier’s Construction sells, installs and services the full Hi-Tide lineup: 4-post cable lifts, yacht lifts, elevator lifts, personal watercraft lifts and specialty configurations. Pick a model to see what it is built for, or request a quote for pricing sized to your boat and site.</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div></div></section>
<section class="section"><div class="wrap"><ul class="product-grid">{grid}</ul></div></section>
{cta_band('Not sure which Hi-Tide lift fits your boat?', 'Send your boat’s make, length and weight, plus your slip or water depth, and we will match the lift and quote the install.')}'''
    ld = [{'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{URL}{HT_ROOT}{p["slug"]}/', 'name': p['name']} for i, p in enumerate(HI_TIDE_PRODUCTS)]}]
    page(HT_ROOT, 'Hi-Tide Boat Lifts', 'Stier’s Construction is an authorized Hi-Tide boat lift dealer: 4-post cable lifts, yacht lifts, elevator lifts, PWC lifts and specialty configurations, installed and serviced by our own crew.',
         body, active='services', trail=trail, ld=ld, ptype='CollectionPage', prio=0.8, sm_images=[img_url(p['img']) for p in HI_TIDE_PRODUCTS if p.get('img')])

def hi_tide_product(p):
    path = f'{HT_ROOT}{p["slug"]}/'
    c = HI_TIDE_CATS[p['cat']]
    has_specs = bool(p.get('features'))
    lead = p.get('tagline') or c['desc']
    trail = [('Home', '/'), ('Services', '/services/'), ('Boat Hoists', '/services/boat-hoists/'), ('Hi-Tide Boat Lifts', HT_ROOT), (p['name'], None)]
    others = [q for q in HI_TIDE_PRODUCTS if q['cat'] == p['cat'] and q['slug'] != p['slug']][:4]
    hero = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div class="page-hero-grid"><div><p class="eyebrow">{c['name']}</p><h1>Hi-Tide {p['name']}</h1><p class="lead">{lead}</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div>
<figure class="page-hero-media">{ht_photo(p, '(min-width:940px) 46vw, 92vw')}</figure></div></div></section>'''
    accessories = p.get('accessories')
    if accessories:
        acc_grid = ''.join(f'''<li class="acc-card"><span class="product-photo-frame">{ht_photo(dict(img=a["img"], name=a["name"]), "(min-width:800px) 30vw, 46vw")}</span>
<div class="acc-card-body"><h3>{a["name"]}</h3><p>{a["desc"]}</p></div></li>''' for a in accessories)
        specs_html = f'<div class="prose"><p>{p["desc"]}</p></div><h3 class="mt-m">Available Accessories</h3><p class="measure">Send us which accessories you want with your quote request.</p><ul class="acc-grid">{acc_grid}</ul>'
    elif has_specs:
        cap = f'<p class="cap-line"><strong>Capacity:</strong> {p["capacity"]}</p>' if p.get('capacity') else ''
        warranty = (('<ul class="warranty-grid">' + ''.join(f'<li><span class="w-label">{lbl}</span><strong>{val}</strong></li>' for lbl, val in p['warranty']) + '</ul>') if p.get('warranty') else '')
        specs_html = f'<div class="prose">{cap}<p>{p["desc"]}</p></div>{warranty}<h3 class="mt-m">Features</h3>{ul(p["features"])}'
    else:
        specs_html = note('<p><strong>Specs and pricing for this model are being confirmed with Hi-Tide.</strong> Send your boat’s make, length and weight, plus your slip or water depth, and we will match capacity and quote the install and any site work it needs.</p>')
    aside = f'''<aside class="aside-sticky aside-stack" aria-label="Quote and related lifts"><div class="panel panel-dark"><h3>Ask About the {p['name']}</h3><small>Mon to Fri, 8am to 5pm</small>
<a class="phone" href="tel:{SITE['phone_e164']}">{SITE['phone']}</a><a class="btn btn-primary" href="/contact/">Send Project Details</a><p class="fin-line">Financing available. <a href="/financing/">See options</a></p></div>
<div class="panel"><h3>More {c['name']}</h3><ul class="related">{''.join(f'<li><a href="{HT_ROOT}{q["slug"]}/"><b>{q["name"]}</b><span>{HI_TIDE_CATS[q["cat"]]["name"]}</span></a></li>' for q in others) or f'<li><a href="{HT_ROOT}"><b>See the full lineup</b><span>All Hi-Tide models</span></a></li>'}</ul>
<p class="mt-s"><a class="textlink" href="{HT_ROOT}">All Hi-Tide boat lifts</a></p></div></aside>'''
    buy_line = (f'Buying Hi-Tide {p["name"].lower()} through Stier’s Construction means one contractor for the parts, the install and everything after.' if accessories else
                f'Buying a Hi-Tide {p["name"]} through Stier’s Construction means one contractor for the lift, the install and everything after: cable change-out, motor maintenance and welding repairs to the frame, all done in-house.')
    main = f'<div class="main"><section><h2>About the {p["name"]}</h2>{specs_html}</section><section><h2>Installed and Serviced by Stier’s Construction</h2><div class="prose"><p>{buy_line} See our <a href="/services/boat-hoists/">full boat hoist service</a>.</p></div></section></div>'
    body = hero + f'<div class="section"><div class="wrap content-grid">{main}{aside}</div></div>' + cta_band(f'Ready to talk about {with_article(p["name"], p.get("plural"))}?')
    svc = {'@type': 'Product', '@id': f'{URL}{path}#product', 'name': f'Hi-Tide {p["name"]}', 'category': c['name'], 'description': p.get('desc') or c['desc'],
           'brand': {'@type': 'Brand', 'name': 'Hi-Tide'}, 'url': f'{URL}{path}'}
    if p.get('img'): svc['image'] = f'{URL}{img_url(p["img"])}'
    page(path, f'Hi-Tide {p["name"]}', f'Hi-Tide {p["name"]} ({c["name"]}): sold, installed and serviced by Stier’s Construction, an authorized Hi-Tide dealer in Metro Detroit. Free quotes.',
         body, active='services', trail=trail, ld=[svc], prio=0.6, sm_images=[img_url(p['img'])] if p.get('img') else None)

# ============================================================ CANDOCK FLOATING DOCKS
CD_ROOT = '/services/docks/candock/'
def cd_photo(p, sizes='260px'):
    return img(p['img'], sizes, cls='product-photo-img', alt=f'Candock {p["name"]}') if p.get('img') else product_photo(p['name'])

def candock_card(p):
    c = CANDOCK_CATS[p['cat']]
    return f'''<li class="product-card"><a class="product-card-link" href="{CD_ROOT}{p['slug']}/"><span class="product-photo-frame">{cd_photo(p, '(min-width:1000px) 22vw, (min-width:640px) 30vw, 46vw')}</span>
<div class="product-card-body"><p class="eyebrow">{c['name']}</p><h3>{p['name']}</h3><span class="textlink">View details</span></div></a></li>'''

def candock_hub():
    trail = [('Home', '/'), ('Services', '/services/'), ('Docks', '/services/docks/'), ('Candock Floating Docks', None)]
    grid = ''.join(candock_card(p) for p in CANDOCK_PRODUCTS)
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div style="padding-block:clamp(24px,4vw,56px) clamp(36px,5vw,64px)"><p class="eyebrow">Authorized dealer</p><h1 style="max-width:24ch">Candock floating docks</h1>
<p class="lead mt-s" style="max-width:62ch">Stier’s Construction sells, installs and services Candock modular floating docks, including the JetRoll drive-on dock for personal watercraft. Unsinkable, foam-filled systems that connect, extend or reconfigure as your waterfront needs change.</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div></div></section>
<section class="section"><div class="wrap"><ul class="product-grid">{grid}</ul>
<div class="mt-m">{note('<p>More of the Candock lineup (residential, commercial and marina floating dock systems) is being added here. Ask when you request a quote if you don’t see what you need yet.</p>')}</div></div></section>
{cta_band('Not sure which Candock system fits your waterfront?', 'Send your shoreline or slip details, plus what you want to dock, and we will lay out a system and quote the install.')}'''
    ld = [{'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': f'{URL}{CD_ROOT}{p["slug"]}/', 'name': p['name']} for i, p in enumerate(CANDOCK_PRODUCTS)]}]
    page(CD_ROOT, 'Candock Floating Docks', 'Stier’s Construction is an authorized Candock dealer: modular floating docks and the JetRoll drive-on PWC dock, installed and serviced by our own crew.',
         body, active='services', trail=trail, ld=ld, ptype='CollectionPage', prio=0.8, sm_images=[img_url(p['img']) for p in CANDOCK_PRODUCTS if p.get('img')])

def candock_product(p):
    path = f'{CD_ROOT}{p["slug"]}/'
    c = CANDOCK_CATS[p['cat']]
    trail = [('Home', '/'), ('Services', '/services/'), ('Docks', '/services/docks/'), ('Candock Floating Docks', CD_ROOT), (p['name'], None)]
    others = [q for q in CANDOCK_PRODUCTS if q['cat'] == p['cat'] and q['slug'] != p['slug']][:4]
    hero = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div class="page-hero-grid"><div><p class="eyebrow">{c['name']}</p><h1>Candock {p['name']}</h1><p class="lead">{p.get('tagline') or c['desc']}</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div>
<figure class="page-hero-media">{cd_photo(p, '(min-width:940px) 46vw, 92vw')}</figure></div></div></section>'''
    specs_grid = ''
    if p.get('material'):
        specs_rows = [('Material', p['material']), ('Dimensions', p['dimensions']), ('Weight', p['weight']), ('Colors', ', '.join(p['colors']))] + p.get('extra_specs', [])
        specs_grid = '<ul class="warranty-grid">' + ''.join(f'<li><span class="w-label">{lbl}</span><strong>{val}</strong></li>' for lbl, val in specs_rows) + '</ul>'
    warranty_note = note(f'<p>{p["warranty"]}.</p>') if p.get('warranty') else ''
    install_note = note(f'<p>{p["install_note"]}</p>') if p.get('install_note') else ''
    config_html = ''
    if p.get('configurations'):
        rows = ''.join(f'<li><h3>{name}<br><small>{tag}</small></h3><p>{desc}</p></li>' for name, tag, desc in p['configurations'])
        config_html = f'<h3 class="mt-l">{p["name"]} Configurations</h3><ol class="steps" style="grid-template-columns:repeat(3,1fr)">{rows}</ol>'
    acc_html = ''
    if p.get('accessories') and isinstance(p['accessories'][0], dict):
        label = p.get('accessories_label', 'Compatible Accessories')
        cards = ''.join(f'<li class="acc-card"><span class="product-photo-frame">{cd_photo(a, "130px")}</span><div class="acc-card-body"><h3>{a["name"]}</h3><p>{a["desc"]}</p></div></li>' for a in p['accessories'])
        acc_html = f'<h3 class="mt-l">{label}</h3><ul class="acc-grid">{cards}</ul>'
    elif p.get('accessories'):
        acc_img = f'<span class="product-photo-frame acc-photo-wide">{img(p["accessories_img"], "260px", alt=p["name"] + " accessories")}</span>' if p.get('accessories_img') else ''
        acc_html = f'<h3 class="mt-l">Compatible Accessories</h3><div class="split" style="align-items:start">{acc_img}{ul(p["accessories"])}</div>'
    uses_html = f'<h3 class="mt-l">Where It Fits</h3>{ul(p["uses"])}' if p.get('uses') else ''
    notes_html = (f'<div class="mt-m">{warranty_note}</div>' if warranty_note else '') + (f'<div class="mt-m">{install_note}</div>' if install_note else '')
    specs_html = f'<div class="prose"><p>{p["desc"]}</p></div>{specs_grid}{notes_html}<h3 class="mt-l">Key Features</h3>{ul(p["features"])}{config_html}{acc_html}{uses_html}'
    aside = f'''<aside class="aside-sticky aside-stack" aria-label="Quote and related docks"><div class="panel panel-dark"><h3>Ask About the {p['name']}</h3><small>Mon to Fri, 8am to 5pm</small>
<a class="phone" href="tel:{SITE['phone_e164']}">{SITE['phone']}</a><a class="btn btn-primary" href="/contact/">Send Project Details</a><p class="fin-line">Financing available. <a href="/financing/">See options</a></p></div>
<div class="panel"><h3>More {c['name']}</h3><ul class="related">{''.join(f'<li><a href="{CD_ROOT}{q["slug"]}/"><b>{q["name"]}</b><span>{CANDOCK_CATS[q["cat"]]["name"]}</span></a></li>' for q in others) or f'<li><a href="{CD_ROOT}"><b>See the full lineup</b><span>All Candock systems</span></a></li>'}</ul>
<p class="mt-s"><a class="textlink" href="{CD_ROOT}">All Candock floating docks</a></p></div></aside>'''
    main = f'<div class="main"><section><h2>About the {p["name"]}</h2>{specs_html}</section><section><h2>Installed and Serviced by Stier’s Construction</h2><div class="prose"><p>Buying a Candock {p["name"]} through Stier’s Construction means one contractor for the dock, the install and everything after. See our <a href="/services/docks/">full dock service</a>.</p></div></section></div>'
    body = hero + f'<div class="section"><div class="wrap content-grid">{main}{aside}</div></div>' + cta_band(f'Ready to talk about {with_article(p["name"], p.get("plural"))}?')
    svc = {'@type': 'Product', '@id': f'{URL}{path}#product', 'name': f'Candock {p["name"]}', 'category': c['name'], 'description': p['desc'],
           'brand': {'@type': 'Brand', 'name': 'Candock'}, 'url': f'{URL}{path}'}
    if p.get('img'): svc['image'] = f'{URL}{img_url(p["img"])}'
    page(path, f'Candock {p["name"]}', f'Candock {p["name"]} ({c["name"]}): sold, installed and serviced by Stier’s Construction, an authorized Candock dealer in Metro Detroit. Free quotes.',
         body, active='services', trail=trail, ld=[svc], prio=0.6, sm_images=[img_url(p['img'])] if p.get('img') else None)

# ============================================================ PROJECTS
def projects():
    btns = ''.join(f'<button type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}</button>' for k, n in GALLERY_CATS)
    figs = ''
    for key, cat in GALLERY:
        m = IM[key]
        figs += f'<figure data-cat="{cat}"><button type="button" data-full="{img_url(key, 1200)}" data-alt="{esc(m["alt"])}">{img(key, "(min-width:1100px) 25vw, (min-width:760px) 33vw, 50vw")}</button></figure>'
    trail = [('Home', '/'), ('Projects', None)]
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div style="padding-block:clamp(24px,4vw,56px) clamp(40px,6vw,72px)"><h1 style="max-width:20ch">Seawall, dock and marine construction projects</h1>
<p class="lead mt-s" style="max-width:60ch">Photos from our own jobs: sheet piling, barge work, docks and hoists, welding, concrete, decks and site work around Metro Detroit.</p></div></div></section>
<section class="section"><div class="wrap"><div class="prose"><p>Every photo here is from one of our own jobs, and captions describe only what you can see. You will find steel sheet piling and barge work, docks and boat hoists, welding and fabrication, concrete and decks, and excavating and demolition, including jobs done in snow and on ice. Use the filters to browse by type of work, tap a photo to enlarge it, and see the matching <a href="/services/">service pages</a> for details on each.</p></div><div class="filters" role="group" aria-label="Filter photos by type of work" hidden>{btns}</div><p id="gallery-status" class="sr-only" aria-live="polite"></p>
<div class="gallery">{figs}</div></div></section>
<dialog id="lightbox" class="lightbox" aria-label="Photo viewer"><button class="lb-btn" type="button">Close</button><figure><img alt="" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" width="1" height="1"><figcaption></figcaption></figure></dialog>
{cta_band('Want results like these?', 'Tell us about your waterfront or site. Quotes are free.')}'''
    page('/projects/', 'Project Photos: Seawalls, Docks, Welding & More | Stier’s',
         'Photos of Stier’s Construction jobs: seawall sheet piling, docks, boat hoists, welding and fabrication, concrete, decks and excavating in Metro Detroit.',
         body, active='projects', trail=trail, ld=None, ptype='CollectionPage', prio=0.7, sm_images=[img_url(k) for k, _ in GALLERY])

# ============================================================ ABOUT
def about():
    trail = [('Home', '/'), ('About', None)]
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div class="page-hero-grid"><div><h1>The crew behind Stier’s Construction</h1>
<p class="lead">We are a marine and construction contractor working across Metro Detroit: docks, seawalls, decks, pilings, and custom welding and fabrication. We work with marinas, commercial properties and homeowners.</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div>
<figure class="page-hero-media">{img('welding-shop-grinding-sparks', '(min-width:940px) 46vw, 92vw', prio=True, lazy=False)}</figure></div></div></section>
<section class="section"><div class="wrap content-grid"><div class="main"><section><h2>Kevin, owner</h2><div class="prose"><p>Kevin brings more than 15 years of hands-on welding, marine and construction experience to every project. He is an active, on-site contractor who stays directly involved in the work, holding each job to high standards of quality, safety and reliability.</p><p>His deep knowledge of construction lets us take on a wide range of projects with confidence: docks, seawalls, decks, pilings, and custom welding and fabrication.</p></div></section>
<section><h2>Chris, project manager</h2><div class="prose"><p>Chris has more than 8 years of hands-on experience in construction and specializes in carpentry, concrete work and marine construction. He leads our construction operations with a practical, solutions-driven mindset.</p><p>Chris also owns and operates a trucking business, Stier’s Enterprise, which gives him a working understanding of logistics, transportation and job-site efficiency. That dual perspective helps us manage projects smoothly.</p></div></section>
<section><h2>How we work</h2><div class="prose"><p>Our goal is long-lasting results through skilled craftsmanship, clear communication and attention to detail. We aim to be the single contractor you can call for marine and waterfront needs, from the seawall to the dock to the deck on the shore.</p></div>
<div class="mt-m">{note('<p>A customer review says it best: “Owner’s communication was terrific and job was complete on time zero issues!”</p>')}</div></section></div>
<aside class="aside-sticky aside-stack"><div class="panel panel-dark"><h3>Work with us</h3><small>Mon to Fri, 8am to 5pm</small><a class="phone" href="tel:{SITE['phone_e164']}">{SITE['phone']}</a><a class="btn btn-primary" href="/contact/">Get a free quote</a></div>
<div class="panel"><h3>Our clients</h3>{ul(['Homeowners', 'Commercial properties', 'Marinas'])}<p class="mt-s"><a class="textlink" href="/careers/">We are hiring. See careers</a></p></div></aside></div></section>
<section class="section section-alt"><div class="wrap"><div class="section-head"><h2>Equipment and crew at work</h2></div><div class="strip">
<figure>{img('stiers-excavator-demo-site', '(min-width:800px) 30vw, 46vw')}</figure><figure>{img('dump-trucks-yard', '(min-width:800px) 30vw, 46vw')}</figure><figure>{img('welder-helmet-sparks', '(min-width:800px) 30vw, 46vw')}</figure></div></div></section>
{cta_band()}'''
    page('/about/', 'About Stier’s Construction | Owner-Led Marine Contractor', 'Meet Kevin and Chris of Stier’s Construction: a Metro Detroit marine and construction contractor for homeowners, commercial properties and marinas.',
         body, active='about', trail=trail, ptype='AboutPage', prio=0.6, sm_images=[img_url('welding-shop-grinding-sparks')])

# ============================================================ SERVICE AREA
GROUP_TEXT = {
 'Lake St. Clair': 'Lake St. Clair is shallow, and its northern arm, Anchor Bay, is only about 1 to 11 feet deep across most of its area. Canals, marinas and open lakefront mean walls, docks, hoists and dredging all come up, and record high water in 2019 and 2020 tested shoreline structures.',
 'St. Clair River': 'The St. Clair River runs at roughly 1.3 to 2.1 mph between Algonac and Marysville, according to NOAA, and faster near the Blue Water Bridge at Port Huron. Ships pass close to shore and river ice is a winter fact of life, so anchoring, scour resistance and protected steel matter.',
 'Detroit River': 'The Detroit River is a busy commercial shipping channel. Its islands, channels and canals combine river frontage with canal lots, so current, wakes, silt and ice all shape the work.',
}
def town_label(t):
    return {'city': 'city', 'township': 'township', 'charter township': 'charter township'}[t['kind']]

def permits_html(t):
    n, w = t['name'], t['water']
    bd = 'township' if 'township' in t['kind'] else 'city'
    local = f'Above the waterline, the {bd} building department handles building permits, zoning and setbacks for decks, patios, retaining walls and demolition, and earth changes near water may need a soil erosion and sedimentation control permit through your county or local enforcing agency. Confirm requirements before work starts.'
    if t['slug'] == 'grosse-pointe-woods':
        return f'<p>Because Grosse Pointe Woods has no Lake St. Clair shoreline of its own, most projects here are governed by the city building department: permits and inspections for decks, driveways, patios, demolition and grading. If you also own waterfront property elsewhere, state and federal permits may apply to that work. See our <a href="/blog/michigan-permits-seawalls-docks-dredging/">Michigan permit guide</a>.</p>'
    if w in ('lsc', 'anchor'):
        core = 'Work at or below the ordinary high-water mark on Lake St. Clair (574.7 feet on the 1955 datum, or 575.3 feet on the 1985 datum) generally needs a permit from Michigan EGLE and often the U.S. Army Corps of Engineers. Applications go through EGLE’s MiEnviro Portal, which forwards them to the Corps.'
    else:
        r = WATERS[w]['short']
        core = f'{r[0].upper() + r[1:]} is a federally navigated connecting waterway, and work in or over the water generally involves EGLE and the U.S. Army Corps of Engineers. EGLE district staff can tell you which part of Michigan law applies to your site, such as Part 325 (Great Lakes Submerged Lands) or Part 301 (Inland Lakes and Streams), and applications go through the MiEnviro Portal.'
    return f'<p>{core}</p><p>{local}</p><p>Read our <a href="/blog/michigan-permits-seawalls-docks-dredging/">Michigan permit guide for seawalls, docks and dredging</a>.</p>'

def town_page(t):
    n = t['name']; path = f'/service-area/{t["slug"]}/'
    w = WATERS[t['water']]
    trail = [('Home', '/'), ('Service Area', '/service-area/'), (n, None)]
    h1 = t.get('h1') or f'Seawall, Dock and Marine Construction in {n}, Michigan'
    title = t.get('title') or f'{n}: Seawalls & Docks'
    desc = t.get('desc') or f'Seawalls, docks, boat hoists, dredging, concrete and decks in {n}, Michigan. Owner-led crew serving {w["short"]}. Free quotes.'
    checks = [f'{t["county"]} County', w['short'][0].upper() + w['short'][1:], 'Owner-led crew', 'Free quotes']
    hero = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div class="page-hero-grid"><div><h1>{h1}</h1><p class="lead">{t['lead']}</p>
<ul class="hero-checks">{''.join(f'<li>{c}</li>' for c in checks)}</ul><div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div>
<figure class="page-hero-media">{img(t['hero'], '(min-width:940px) 46vw, 92vw', prio=True, lazy=False)}</figure></div></div></section>'''
    svc_rows = ''.join(f'<li><a href="/services/{s}/"><b>{BY_SLUG[s]["name"]}</b><span>{reason}</span></a></li>' for s, reason in t['svc'])
    near = ''.join(f'<li><a href="/service-area/{s}/"><b>{TOWN_BY_SLUG[s]["name"]}</b><span>{TOWN_BY_SLUG[s]["county"]} County</span></a></li>' for s in t['near'])
    aside = f'''<aside class="aside-sticky aside-stack" aria-label="Quote and nearby communities"><div class="panel panel-dark"><h3>Get a Free Quote in {n}</h3><small>Mon to Fri, 8am to 5pm</small><a class="phone" href="tel:{SITE['phone_e164']}">{SITE['phone']}</a><a class="btn btn-primary" href="/contact/">Send Project Details</a><p class="fin-line">Financing available. <a href="/financing/">See options</a></p></div>
<div class="panel"><h3>Nearby Communities</h3><ul class="related">{near}</ul><p class="mt-s"><a class="textlink" href="/service-area/">All Service Areas</a></p></div></aside>'''
    kindtxt = {'city': 'city', 'township': 'township', 'charter township': 'charter township'}[t['kind']]
    main = f'''<div class="main"><section><h2>Waterfront Construction in {n}</h2><div class="prose"><p>{t['p1']}</p><p>{t['p2']}</p></div></section>
<section><h2>{n} at a Glance</h2>{ul(t['notes'])}</section>
<section><h2>Services We Provide in {n}</h2><ul class="related one-col">{svc_rows}</ul><p class="mt-s"><a class="textlink" href="/services/">See All Services</a></p></section>
<section><h2>Permits and Local Rules in {n}</h2><div class="prose">{permits_html(t)}</div></section></div>'''
    faqs = [t['faq'], (f'Does Stier’s Construction serve {n}?', f'<p>Yes. Stier’s Construction serves waterfront communities across Metro Detroit, including the {kindtxt} of {n} in {t["county"]} County. Call <a href="tel:{SITE["phone_e164"]}">{SITE["phone"]}</a> or <a href="/contact/">request a free quote</a> and include your address and a few photos.</p>')]
    top = [BY_SLUG[s] for s, _ in t['svc']]
    seen = []; gs = []
    for sv in top:
        for p in guides_for(sv['slug']):
            if p['slug'] not in seen: seen.append(p['slug']); gs.append(p)
    gs = gs[:3]
    guides = f'<section class="section section-alt" aria-labelledby="tg-h"><div class="wrap"><div class="section-head"><h2 id="tg-h">Guides for {n} Waterfront Owners</h2></div><ul class="post-list">{"".join(post_row(p) for p in gs)}</ul></div></section>'
    faq = f'<section class="section" aria-labelledby="tq-h"><div class="wrap"><div class="section-head"><h2 id="tq-h">{n} Questions</h2></div>{faq_html(faqs)}</div></section>'
    body = hero + f'<div class="section"><div class="wrap content-grid">{main}{aside}</div></div>' + guides + faq + cta_band(f'Ready to Start Your {n} Project?')
    city = {'@type': 'City', 'name': n, 'containedInPlace': {'@type': 'AdministrativeArea', 'name': f'{t["county"]} County, Michigan'}}
    svc = {'@type': 'Service', '@id': f'{URL}{path}#service', 'name': f'Waterfront and marine construction in {n}, Michigan', 'serviceType': 'Marine and waterfront construction', 'url': f'{URL}{path}',
           'provider': {'@id': f'{URL}/#business'}, 'areaServed': city, 'description': desc}
    page(path, title, desc, body, active='area', trail=trail, ld=[svc, faq_ld(faqs)], prio=0.8, sm_images=[img_url(t['hero'])])

def service_area():
    trail = [('Home', '/'), ('Service Area', None)]
    sections = ''
    for g in GROUPS:
        ts = [t for t in TOWNS if WATERS[t['water']]['group'] == g]
        rows = ''.join(f'<li><a href="/service-area/{t["slug"]}/"><b>{t["name"]}</b><span>{t["county"]} County. {t["lead"]}</span></a></li>' for t in ts)
        sections += f'<section id="{slugify(g)}" aria-labelledby="{slugify(g)}-h"><h2 id="{slugify(g)}-h">{g}</h2><div class="prose"><p>{GROUP_TEXT[g]}</p></div><ul class="related one-col">{rows}</ul></section>'
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div class="page-hero-grid"><div><h1>Marine and Construction Services Across Metro Detroit’s Waterfront</h1>
<p class="lead">We serve waterfront communities on Lake St. Clair, the St. Clair River and the Detroit River, along with the excavating, concrete, welding and deck work on the lots beside them.</p>
<div class="btn-row"><a class="btn btn-primary" href="/contact/">Get a free quote</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div>
<figure class="page-hero-media">{img('barge-open-water', '(min-width:940px) 46vw, 92vw', prio=True, lazy=False)}</figure></div></div></section>
<section class="section"><div class="wrap content-grid"><div class="main"><section><h2>Where We Work</h2><div class="prose"><p>Lake St. Clair sits between the St. Clair River to the north and the Detroit River to the south, and the three waterways behave differently. Depth, current, ship traffic and ice change how a wall, dock or piling should be built. Pick your community below for local details, or read <a href="/blog/lake-st-clair-detroit-river-st-clair-river-waterfront-differences/">how your waterway changes your seawall and dock</a>.</p><p>Not sure we cover your address? Call and ask. Our team works for homeowners, commercial property owners and marinas.</p></div></section>{sections}
<section><h2>What Waterfront Owners Should Know About Permits</h2><div class="prose"><p>Work in or over Great Lakes waters generally involves state and federal permits. In Michigan that means EGLE, and often the U.S. Army Corps of Engineers, and your city or township may add its own rules. EGLE’s <a href="{EGLE_LINK}" target="_blank" rel="noopener">shoreline protection permit guidance (PDF)</a> explains the process. Requirements depend on your site, so confirm before work starts.</p></div></section></div>
<aside class="aside-sticky aside-stack"><div class="panel panel-dark"><h3>Not Sure We Cover You?</h3><small>Mon to Fri, 8am to 5pm</small><a class="phone" href="tel:{SITE['phone_e164']}">{SITE['phone']}</a><a class="btn btn-primary" href="/contact/">Send Your Address</a></div>
<div class="panel"><h3>Popular Services</h3><ul class="related">{''.join(f'<li><a href="/services/{s}/"><b>{BY_SLUG[s]["name"]}</b><span>{BY_SLUG[s]["summary"]}</span></a></li>' for s in ['seawalls','docks','boat-hoists','dredging','pilings'])}</ul></div></aside></div></section>
{cta_band()}'''
    page('/service-area/', 'Service Area: Lake St. Clair, Detroit River & More | Stier’s', 'Stier’s Construction serves waterfront towns on Lake St. Clair, the St. Clair River and the Detroit River, from Grosse Ile to Port Huron.',
         body, active='area', trail=trail, prio=0.9, sm_images=[img_url('barge-open-water')])

# ============================================================ FORMS
def field(id_, label, type_='text', req=True, attrs='', hint=''):
    r = ' <span class="req" aria-hidden="true">*</span>' if req else ''
    h = f'<p class="hint" id="{id_}-h">{hint}</p>' if hint else ''
    d = f' aria-describedby="{id_}-h"' if hint else ''
    return f'<div class="field"><label for="{id_}">{label}{r}</label><input id="{id_}" name="{id_}" type="{type_}"{" required" if req else ""} {attrs}{d}>{h}</div>'

def contact():
    trail = [('Home', '/'), ('Contact', None)]
    opts = ''.join(f'<option>{o}</option>' for o in ['Seawall', 'Dock', 'Pilings', 'Boat hoist', 'Dredging', 'Welding or fabrication', 'Excavating or grading', 'Demolition', 'Concrete', 'Deck', 'Not sure or something else'])
    form = f'''<form name="quote" method="POST" action="/thank-you/" data-netlify="true" data-netlify-honeypot="bot-field" enctype="multipart/form-data" aria-labelledby="form-h">
<input type="hidden" name="form-name" value="quote"><p class="hp" aria-hidden="true"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
<div class="form-grid g2">{field('name', 'Name', attrs='autocomplete="name"')}{field('phone', 'Phone', 'tel', attrs='autocomplete="tel" inputmode="tel"')}
<div class="full">{field('email', 'Email', 'email', attrs='autocomplete="email"')}</div>{field('address', 'Address of job', attrs='autocomplete="off"')}
<div class="field"><label for="service">What do you need?</label><select id="service" name="service"><option value="">Choose one (optional)</option>{opts}</select></div>
<div class="field full"><label for="message">Tell us about your project <span class="req" aria-hidden="true">*</span></label><textarea id="message" name="message" required aria-describedby="message-h"></textarea><p class="hint" id="message-h">What you want done, any deadlines, and anything we should know about access to the site.</p></div>
<div class="field full"><label for="files">Photos or video (optional)</label><input id="files" name="files" type="file" multiple accept="image/*,video/*" aria-describedby="files-h"><p class="hint" id="files-h">Photos help us quote faster. Attach up to 4.2 MB in total. Videos and larger files are best emailed to <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p></div></div>
<p class="mt-s"><button class="btn btn-primary" type="submit">Send my quote request</button></p><p class="form-status" role="status" aria-live="polite"></p></form>'''
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div style="padding-block:clamp(24px,4vw,56px) clamp(36px,5vw,64px)"><h1 id="form-top" style="max-width:20ch">Get a free quote</h1><p class="lead mt-s" style="max-width:58ch">Tell us about your project. Reach out by phone, email or through our contact form. We’re happy to help and respond promptly to all inquiries and quote requests.</p></div></div></section>
<section class="section"><div class="wrap content-grid"><div><h2 id="form-h" class="sr-only">Quote request form</h2>{form}</div>
<aside class="aside-sticky aside-stack" aria-label="Contact details"><div class="panel panel-dark on-dark"><h3>Prefer to talk?</h3><dl class="contact-card"><div><dt>Call</dt><dd><a class="big" href="tel:{SITE['phone_e164']}">{SITE['phone']}</a></dd></div><div><dt>Email</dt><dd><a href="mailto:{SITE['email']}">{SITE['email']}</a></dd></div><div><dt>Hours</dt><dd>Monday to Friday, 8am to 5pm<br>Weekends by appointment</dd></div></dl></div>
<div class="panel"><h3>What to include</h3>{ul(['The address of the job', 'What you want done', 'Photos or video of the area', 'Your timing, if you have one'])}<p class="mt-s"><a class="textlink" href="/financing/">Financing options</a></p></div></aside></div></section>'''
    page('/contact/', 'Get a Free Quote | Stier’s Construction, Metro Detroit', 'Request a free quote from Stier’s Construction for seawalls, docks, hoists, dredging, welding, concrete, excavating and decks. Call 586-703-7214.',
         body, active='contact', trail=trail, ptype='ContactPage', bar=False, prio=0.8)

def careers():
    trail = [('Home', '/'), ('Careers', None)]
    form = f'''<form name="careers" method="POST" action="/thank-you/" data-netlify="true" data-netlify-honeypot="bot-field" enctype="multipart/form-data" aria-labelledby="c-h">
<input type="hidden" name="form-name" value="careers"><p class="hp" aria-hidden="true"><label>Leave this empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
<div class="form-grid g2">{field('name', 'Name', attrs='autocomplete="name"')}{field('phone', 'Phone', 'tel', attrs='autocomplete="tel" inputmode="tel"')}<div class="full">{field('email', 'Email', 'email', attrs='autocomplete="email"')}</div>
<div class="field full"><label for="experience">Your experience (optional)</label><textarea id="experience" name="experience"></textarea></div>
<div class="field full"><label for="resume">Resume (optional)</label><input id="resume" name="resume" type="file" accept=".pdf,.doc,.docx" aria-describedby="resume-h"><p class="hint" id="resume-h">PDF or Word, up to 4.2 MB. Larger files can be emailed to <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p></div></div>
<p class="mt-s"><button class="btn btn-primary" type="submit">Send application</button></p><p class="form-status" role="status" aria-live="polite"></p></form>'''
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div class="page-hero-grid"><div><h1>Work with Stier’s Construction</h1><p class="lead">We are hiring skilled professionals for marine construction, fabrication, concrete, excavating, welding and waterfront projects across Metro Detroit.</p></div>
<figure class="page-hero-media">{img('welders-frozen-shoreline', '(min-width:940px) 46vw, 92vw', prio=True, lazy=False)}</figure></div></div></section>
<section class="section"><div class="wrap content-grid"><div><h2 id="c-h">Apply today</h2><p class="measure">Send your details below. Resume is optional.</p><div class="mt-s">{form}</div></div>
<aside class="aside-sticky aside-stack"><div class="panel"><h3>Prefer to call?</h3><p>Reach Kevin at <a href="tel:{SITE['phone_e164']}">{SITE['phone']}</a>, Monday to Friday, 8am to 5pm.</p></div></aside></div></section>'''
    page('/careers/', 'Careers: Marine, Welding & Construction Jobs | Stier’s', 'Stier’s Construction is hiring skilled people for marine construction, fabrication, concrete, excavating and welding in Metro Detroit. Apply online.',
         body, trail=trail, bar=False, prio=0.5)

def thanks():
    trail = [('Home', '/'), ('Thank You', None)]
    steps = [('We Read It Right Away', 'Every submission comes straight to our inbox, photos and all.'),
             ('Kevin Calls or Emails You', 'To ask anything we need and talk through your project.'),
             ('You Get a Written Quote', 'No pressure, no obligation. Free, and specific to your site.')]
    steps_html = ''.join(f'<li><h3>{a}</h3><p>{c}</p></li>' for a, c in steps)
    links = [('michigan-permits-seawalls-docks-dredging', 'Wondering about permits?'),
             ('how-to-pay-for-a-waterfront-project', 'Planning how to pay for it?'),
             ('seasonal-waterfront-maintenance-checklist', 'Already own a seawall or dock?')]
    link_html = ''.join(
        f'<a class="wait-card" href="/blog/{slug}/"><b>{lead_in}</b><span>{POST_BY_SLUG[slug]["h1"]}</span></a>'
        for slug, lead_in in links
    )
    hero = f'''<section class="page-hero thanks-hero on-dark"><div class="wrap">{crumbs(trail)}
<div class="thanks-center-col">{CHECK_SVG}<h1>You’re All Set</h1>
<p class="lead">Your project details just landed in our inbox. We’ll follow up soon, usually the same business day.</p>
<p class="thanks-urgent">Project urgent? Call <a href="tel:{SITE['phone_e164']}">{SITE['phone']}</a>, Monday to Friday, 8am to 5pm.</p>
<div class="btn-row center"><a class="btn btn-primary" href="/projects/">See Our Project Photos</a><a class="btn btn-ghost" href="/">Back to Home</a></div></div>
<figure class="page-hero-media thanks-photo">{img('sheet-pile-excavator-canal-home', '(min-width:700px) 640px, 92vw', prio=True, lazy=False)}</figure></div></section>'''
    next_sec = f'''<section class="section thanks-page" aria-labelledby="wn-h"><div class="wrap"><div class="section-head"><h2 id="wn-h">What Happens Next</h2></div><ol class="steps">{steps_html}</ol></div></section>'''
    wait_sec = f'''<section class="section section-dark on-dark thanks-page" aria-labelledby="ww-h"><div class="wrap"><div class="section-head"><h2 id="ww-h">A Few Things Worth Reading</h2><p>While your quote comes together, here is what other waterfront owners ask us first.</p></div>
<div class="wait-links">{link_html}</div></div></section>'''
    figs = ''.join(f'<figure>{img(k, "(min-width:800px) 30vw, 46vw")}</figure>' for k in ('new-deck-over-seawall', 'boat-house-hoist-tarped-boat', 'welding-at-night-waterfront'))
    strip = f'''<section class="section section-alt thanks-page" aria-labelledby="wk-h"><div class="wrap"><div class="section-head"><h2 id="wk-h">A Look at Recent Work</h2></div><div class="strip">{figs}</div>
<p class="mt-m center"><a class="textlink" href="/projects/">See all project photos</a></p></div></section>'''
    body = hero + next_sec + wait_sec + strip
    page('/thank-you/', 'Thank You | Stier’s Marine & Construction', 'Thanks for contacting Stier’s Marine & Construction.', body, noindex=True, bar=False)

def not_found():
    svc = ''.join(f'<li><a href="/services/{s["slug"]}/"><b>{s["name"]}</b><span>{s["summary"]}</span></a></li>' for s in SERVICES[:6])
    body = f'''<section class="page-simple"><div class="wrap thanks nf"><p class="nf-code" aria-hidden="true">404</p><h1>We Could Not Find That Page</h1>
<p class="lead mt-s">The link may be out of date or the page may have moved. Here is where most people are headed:</p>
<div class="btn-row mt-m"><a class="btn btn-primary" href="/contact/">Get a free quote</a><a class="btn btn-outline" href="/services/">All services</a><a class="btn btn-outline" href="/projects/">Project photos</a><a class="btn btn-outline" href="/">Home</a></div>
<h2 class="nf-h">Popular Services</h2><ul class="related">{svc}</ul>
<p class="mt-m">Still stuck? Call <a href="tel:{SITE['phone_e164']}">{SITE['phone']}</a>, Monday to Friday, 8am to 5pm, or read our <a href="/blog/">waterfront guides</a>.</p></div></section>'''
    page('/404.html', 'Page not found | Stier’s Construction', 'Page not found.', body, noindex=True, bar=False)

# ============================================================ FINANCING
ENH_PAGE = 'https://www.enhancify.com/stiersconstruction'
FIN_FAQS = [
 ('Does checking my options affect my credit score?', '<p>Enhancify says that in most cases its lending partners run only a soft inquiry to show you options, and a soft inquiry does not affect your credit score. When you choose a loan and move forward, the lender is required to run a credit inquiry, and should tell you beforehand. Read the lender’s terms before you apply.</p>'),
 ('Do I have to accept an offer?', '<p>No. You can apply with one lender, several, or none. You are not obligated to accept any loan offer.</p>'),
 ('Who is the lender?', '<p>Enhancify is not a lender. It matches you with participating lenders, and each lender makes its own credit decision and sets the rate, fees and term. Stier’s Construction is not a lender and does not make credit decisions.</p>'),
 ('Does it cost anything to check my options?', '<p>Enhancify says it does not charge consumers to use its service. Lenders set their own terms and may charge fees, so read each offer carefully.</p>'),
 ('Should I get a quote first?', '<p>Yes, it helps. Your financing request usually starts from the price of the job, so <a href="/contact/">request a free quote</a> or call <a href="tel:%s">%s</a> first.</p>' % (SITE['phone_e164'], SITE['phone'])),
 ('The form did not load. What now?', '<p>Some browsers and ad blockers stop third-party forms from loading. You can open the <a href="%s" target="_blank" rel="noopener">financing page on Enhancify</a> instead, or call us.</p>' % ENH_PAGE),
]
def financing():
    trail = [('Home', '/'), ('Financing', None)]
    steps = [('Get a quote from us', 'Your financing request usually starts from the price of the job. <a href="/contact/">Request a free quote</a> if you do not have one yet.'),
             ('Answer a few questions', 'Use the form below. Enhancify matches you with participating lenders.'),
             ('Compare offers', 'Apply with the lender you like, or walk away. The lender makes the credit decision.'),
             ('Start your project', 'Funds approved through this page are for work with Stier’s Construction.')]
    steps_html = ''.join(f'<li><h3>{a}</h3><p>{c}</p></li>' for a, c in steps)
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div class="page-hero-grid"><div><h1>Financing for your waterfront project</h1>
<p class="lead">Spread the cost of a seawall, dock, deck, concrete or excavating job into monthly payments. Checking your options uses a soft credit check in most cases, which does not affect your credit score.</p>
<ul class="hero-checks"><li>Check options online</li><li>No obligation to accept an offer</li><li>For work with Stier’s Construction</li></ul>
<div class="btn-row"><a class="btn btn-primary" href="#apply">Check financing options</a>{tel('btn btn-ghost', 'Call ' + SITE['phone'], True)}</div></div>
<figure class="page-hero-media">{img('l-shaped-dock-choppy-water', '(min-width:940px) 46vw, 92vw', prio=True, lazy=False)}</figure></div></div></section>
<section class="section" aria-labelledby="how-h"><div class="wrap"><div class="section-head"><h2 id="how-h">How financing works</h2></div><ol class="steps">{steps_html}</ol></div></section>
<section id="apply" aria-labelledby="ap-h"><h2 id="ap-h" class="sr-only">Check your financing options</h2>
<div class="widget-wrap"><div id="fullpagewidget" data-color1="#C8202B" data-color2="#12323F" data-coBrandedColor="#FFFFFF" data-page="9934698" data-hideLink="0" data-src="https://www.enhancify.com/fullpagewidget/"><p class="widget-loading">Loading financing options...</p></div>
<noscript><p class="widget-loading">This form needs JavaScript. <a href="{ENH_PAGE}" target="_blank" rel="noopener">Open the financing page on Enhancify</a>.</p></noscript></div>
<div class="wrap section-tight"><p><a class="textlink" href="{ENH_PAGE}" target="_blank" rel="noopener">Prefer the full Enhancify page? Open it in a new tab</a></p>
<div class="mt-s">{note('<p><strong>Disclosure.</strong> The form above is provided by Enhancify.com, an independent marketplace that refers you to participating lenders. Stier’s Construction is not a lender and does not make credit decisions. Offers are subject to credit approval, and rates, terms and availability vary by lender. You are not required to accept any offer.</p>')}</div></div></section>
<section class="section" aria-labelledby="fq-h"><div class="wrap"><div class="section-head"><h2 id="fq-h">Financing questions</h2></div>{faq_html(FIN_FAQS)}</div></section>
{cta_band('Get your quote first', 'A quote tells you what the project costs, which is where every financing request starts. Quotes are free.')}'''
    page('/financing/', 'Financing for Seawalls, Docks & Waterfront Projects | Stier’s',
         'Spread the cost of a seawall, dock, deck or concrete project into monthly payments. Check financing options through Enhancify, subject to credit approval.',
         body, active='financing', trail=trail, prio=0.8, sm_images=[img_url('l-shaped-dock-choppy-water')])


# ============================================================ BLOG
import datetime
def fmt_date(d):
    y, m, dd = map(int, d.split('-'))
    return datetime.date(y, m, dd).strftime('%B %-d, %Y')
def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', re.sub(r'<[^>]+>', '', s).lower()).strip('-')

def post_row(p, sizes='(min-width:800px) 260px, 92vw', lazy=True):
    return f'''<li class="post-row"><a class="post-thumb" href="/blog/{p['slug']}/" tabindex="-1" aria-hidden="true">{img(p['hero'], sizes, lazy=lazy)}</a>
<div><p class="post-meta"><a href="/blog/#{slugify(p['cat'])}">{p['cat']}</a><span>{p['minutes']} min read</span></p><h3><a href="/blog/{p['slug']}/">{p['h1']}</a></h3><p>{p['desc']}</p></div></li>'''

def guides_for(service_slug, limit=4):
    ps = [p for p in POSTS if service_slug in p['services']]
    ps.sort(key=lambda p: (p['services'].index(service_slug), POSTS.index(p)))
    return ps[:limit]

def xsec_figure():
    return ('<figure class="post-fig"><div class="xsec-grid"><div class="xsec-scroll" tabindex="0" role="region" aria-label="Cross-section illustration of a waterfront lot">' + XSEC.replace('id="xsec-t"', 'id="xsec-t2"').replace('id="xsec-d"', 'id="xsec-d2"').replace('aria-labelledby="xsec-t xsec-d"', 'aria-labelledby="xsec-t2 xsec-d2"') +
            '</div></div><figcaption>Illustration of a typical seawall setup. Your site may differ.</figcaption></figure>')

def crumb_label(p):
    t = p['t'].split(':')[0].strip()
    if len(t) > 46: t = ' '.join(t.split()[:6]) + '...'
    return t

def blog_post(p):
    path = f'/blog/{p["slug"]}/'
    trail = [('Home', '/'), ('Blog', '/blog/'), (p['h1'], None)]
    body = p['body'].replace('[[xsec]]', xsec_figure())
    _n = [0]
    def _tw(m):
        _n[0] += 1
        return f'<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable table {_n[0]}">'
    body = re.sub(r'<div class="table-wrap">', _tw, body)
    heads = []
    def add_id(m):
        text = re.sub(r'<[^>]+>', '', m.group(1)); i = slugify(text); heads.append((i, tc(text)))
        return f'<h2 id="{i}">{m.group(1)}</h2>'
    body = re.sub(r'<h2>(.*?)</h2>', add_id, body, flags=re.S)
    toc = '<nav class="toc" aria-label="In this article"><h2 class="toc-h">In This Article</h2><ol>' + ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in heads) + '</ol></nav>'
    take = '<aside class="takeaways" aria-labelledby="kt-h"><h2 id="kt-h">Key Takeaways</h2><ul class="checklist">' + ''.join(f'<li>{t}</li>' for t in p['takeaways']) + '</ul></aside>'
    svcs = [BY_SLUG[s] for s in p['services']]
    aside = f'''<aside class="aside-sticky aside-stack" aria-label="Quote and related services"><div class="panel panel-dark"><h3>Get a Free Quote</h3><small>Mon to Fri, 8am to 5pm</small><a class="phone" href="tel:{SITE['phone_e164']}">{SITE['phone']}</a><a class="btn btn-primary" href="/contact/">Send Project Details</a><p class="fin-line">Financing available. <a href="/financing/">See options</a></p></div>
<div class="panel"><h3>Related Services</h3><ul class="related">{''.join(f'<li><a href="/services/{s["slug"]}/"><b>{s["name"]}</b><span>{s["summary"]}</span></a></li>' for s in svcs)}</ul></div></aside>'''
    meta = f'<p class="post-meta post-meta-hero"><a href="/blog/#{slugify(p["cat"])}">{p["cat"]}</a><span>Published {fmt_date(p["date"])}</span><span>{p["minutes"]} min read</span></p>'
    hero = f'''<section class="page-hero post-hero on-dark"><div class="wrap">{crumbs(trail[:2] + [(crumb_label(p), None)])}<div class="page-hero-grid"><div>{meta}<h1>{p['h1']}</h1><p class="lead">{p['desc']}</p></div>
<figure class="page-hero-media">{img(p['hero'], '(min-width:940px) 46vw, 92vw', prio=True, lazy=False)}</figure></div></div></section>'''
    rel = [POST_BY_SLUG[s] for s in p['related']]
    faq = f'<section class="section section-alt" aria-labelledby="pq-h"><div class="wrap"><div class="section-head"><h2 id="pq-h">Frequently Asked Questions</h2></div>{faq_html(p["faqs"])}</div></section>'
    more = f'<section class="section" aria-labelledby="km-h"><div class="wrap"><div class="section-head"><h2 id="km-h">Keep Reading</h2></div><ul class="post-list">{"".join(post_row(r) for r in rel)}</ul></div></section>'
    m0 = re.match(r'\s*(<p>.*?</p>)', body, flags=re.S)
    intro, rest = (m0.group(1), body[m0.end():]) if m0 else ('', body)
    article = f'<article class="main post-body"><div class="prose">{intro}{take}{toc}{rest}</div></article>'
    page_body = hero + f'<div class="section"><div class="wrap content-grid">{article}{aside}</div></div>' + faq + more + cta_band('Ready to Talk About Your Waterfront Project?')
    url = f'{URL}{path}'
    bp = {'@type': 'BlogPosting', '@id': f'{url}#article', 'headline': tc(p['h1']), 'description': p['desc'], 'image': [f'{URL}{img_url(p["hero"])}'],
          'datePublished': p['date'], 'dateModified': p['date'], 'author': {'@type': 'Organization', 'name': SITE['seo_name'], '@id': f'{URL}/#business'},
          'publisher': {'@id': f'{URL}/#business'}, 'mainEntityOfPage': {'@type': 'WebPage', '@id': url}, 'articleSection': p['cat'], 'wordCount': p['words'], 'inLanguage': 'en-US',
          'isPartOf': {'@id': f'{URL}/blog/#blog'}}
    page(path, p['t'], p['desc'], page_body, active='blog', trail=trail, ld=[bp, faq_ld(p['faqs'])], ptype='WebPage', prio=0.7, sm_images=[img_url(p['hero'])])

def blog_hub():
    trail = [('Home', '/'), ('Blog', None)]
    feat = POSTS[0]
    chips = ''.join(f'<li><a href="#{slugify(c)}">{c}</a></li>' for c in CATS if any(p['cat'] == c for p in POSTS))
    sections = ''
    for c in CATS:
        ps = [p for p in POSTS if p['cat'] == c and p is not feat]
        if not ps: continue
        sections += f'<section class="blog-cat" id="{slugify(c)}" aria-labelledby="{slugify(c)}-h"><h2 id="{slugify(c)}-h">{c}</h2><ul class="post-list">{"".join(post_row(p) for p in ps)}</ul></section>'
    body = f'''<section class="page-hero on-dark"><div class="wrap">{crumbs(trail)}<div style="padding-block:clamp(24px,4vw,56px) clamp(36px,5vw,64px)"><h1 style="max-width:22ch">Marine Construction Blog for Metro Detroit Waterfronts</h1>
<p class="lead mt-s" style="max-width:62ch">Plain-English guides on seawalls, docks, pilings, boat hoists, dredging, permits and waterfront living on Lake St. Clair and the Detroit River, from the crew at Stier’s Construction.</p>
<ul class="chips" aria-label="Topics">{chips}</ul></div></div></section>
<section class="section" aria-labelledby="ft-h"><div class="wrap"><h2 id="ft-h" class="sr-only">Featured Guide</h2><article class="feature"><a class="feature-img" href="/blog/{feat['slug']}/" tabindex="-1" aria-hidden="true">{img(feat['hero'], '(min-width:900px) 50vw, 92vw', prio=True, lazy=False)}</a>
<div><p class="post-meta"><a href="/blog/#{slugify(feat['cat'])}">{feat['cat']}</a><span>{feat['minutes']} min read</span><span>Featured Guide</span></p><h3><a href="/blog/{feat['slug']}/">{feat['h1']}</a></h3><p class="lead">{feat['desc']}</p><p><a class="btn btn-dark" href="/blog/{feat['slug']}/">Read the Guide</a></p></div></article></div></section>
<section class="section section-alt"><div class="wrap">{sections}</div></section>
{cta_band('Have a Question About Your Waterfront?', 'Send us your address and a few photos. Quotes are free, and we respond promptly to every inquiry.')}'''
    ld = [{'@type': 'Blog', '@id': f'{URL}/blog/#blog', 'name': 'Stier’s Marine & Construction Blog', 'url': f'{URL}/blog/', 'description': 'Guides on seawalls, docks, pilings, boat hoists, dredging, permits and waterfront living in Metro Detroit.',
           'publisher': {'@id': f'{URL}/#business'}, 'inLanguage': 'en-US',
           'blogPost': [{'@type': 'BlogPosting', 'headline': tc(p['h1']), 'url': f'{URL}/blog/{p["slug"]}/', 'datePublished': p['date']} for p in POSTS]}]
    page('/blog/', 'Marine Construction Blog: Seawall & Dock Guides | Stier’s', 'Guides on seawalls, docks, pilings, boat hoists, dredging, permits and waterfront living on Lake St. Clair and the Detroit River.',
         body, active='blog', trail=trail, ld=ld, ptype='CollectionPage', prio=0.9, sm_images=[img_url(feat['hero'])])

def blog_feed():
    items = ''.join(f"<item><title>{esc(tc(p['h1']))}</title><link>{URL}/blog/{p['slug']}/</link><guid isPermaLink=\"true\">{URL}/blog/{p['slug']}/</guid><pubDate>{datetime.datetime.strptime(p['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 08:00:00 -0400')}</pubDate><category>{esc(p['cat'])}</category><description>{esc(p['desc'])}</description></item>" for p in POSTS)
    open(f'{OUT}/blog/feed.xml', 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Stier’s Marine &amp; Construction Blog</title><link>{URL}/blog/</link><description>Guides on seawalls, docks, pilings, boat hoists, dredging, permits and waterfront living in Metro Detroit.</description><language>en-us</language><atom:link href="{URL}/blog/feed.xml" rel="self" type="application/rss+xml"/>{items}</channel></rss>')

# ============================================================ BUILD
home(); services_hub()
for s in SERVICES: service_page(s)
hi_tide_hub()
for _hp in HI_TIDE_PRODUCTS: hi_tide_product(_hp)
candock_hub()
for _cp in CANDOCK_PRODUCTS: candock_product(_cp)
blog_hub()
for _p in POSTS: blog_post(_p)
blog_feed()
projects(); financing(); about(); service_area()
for _t in TOWNS: town_page(_t)
contact(); careers(); thanks(); not_found()

# ---------- sitemap, robots, manifest, netlify ----------
def sm_entry(path, prio, images):
    imgs = ''.join(f'<image:image><image:loc>{URL}{i}</image:loc></image:image>' for i in dict.fromkeys(images))
    return f'<url><loc>{URL}{path}</loc><lastmod>{SITE["built"]}</lastmod><priority>{prio}</priority>{imgs}</url>'
open(f'{OUT}/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' + ''.join(sm_entry(*e) for e in sorted(SITEMAP, key=lambda e: (-e[1], e[0]))) + '</urlset>')
open(f'{OUT}/robots.txt', 'w').write(f'User-agent: *\nAllow: /\nDisallow: /thank-you/\n\nSitemap: {URL}/sitemap.xml\n')
json.dump({'name': 'Stier’s Marine & Construction', 'short_name': 'Stier’s', 'start_url': '/', 'display': 'standalone', 'background_color': '#0D2530', 'theme_color': '#0D2530',
           'icons': [{'src': '/assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': '/assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, open(f'{OUT}/site.webmanifest', 'w'), ensure_ascii=False)

redirects = [
 ('/all', '/services/'), ('/seawalls', '/services/seawalls/'), ('/docks-pilings', '/services/docks/'),
 ('/fabrication-install', '/services/welding-fabrication/'), ('/concrete', '/services/concrete/'), ('/excavating-grading', '/services/excavating-grading/'),
 ('/excavatinggrading', '/services/excavating-grading/'), ('/decks', '/services/decks/'), ('/boat-hoists', '/services/boat-hoists/'),
 ('/photos', '/projects/'), ('/gallery-5-1', '/projects/'), ('/new-page', '/services/seawalls/'), ('/new-page-1', '/services/welding-fabrication/'),
 ('/new-page-2', '/services/decks/'), ('/new-page-3', '/services/concrete/'), ('/cart', '/'),
]
# Guard: a redirect whose target equals its source (ignoring a trailing slash) loops forever on Netlify.
for _a, _b in redirects:
    assert _a.rstrip('/') != _b.rstrip('/'), f'redirect loop: {_a} -> {_b}'
open(f'{OUT}/_redirects', 'w').write('# Old Squarespace URLs -> new structure (301)\n' + ''.join(f'{a}  {b}  301!\n' for a, b in redirects))
CSP_BASE = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-src https://www.enhancify.com; frame-ancestors 'none'; base-uri 'self'; object-src 'none'"
CSP_FIN = "default-src 'self'; script-src 'self' https://www.enhancify.com; style-src 'self' 'unsafe-inline' https://www.enhancify.com https://fonts.googleapis.com; img-src 'self' data: https://www.enhancify.com https://cdn.enhancify.com; font-src 'self' https://fonts.gstatic.com https://www.enhancify.com; connect-src 'self' https://www.enhancify.com; form-action 'self' https://www.enhancify.com; frame-src https://www.enhancify.com; frame-ancestors 'none'; base-uri 'self'; object-src 'none'"
# Netlify merges header rules that match the same path, so each page gets exactly one CSP rule (no /* CSP).
csp_rules = ''.join(f"{p}\n  Content-Security-Policy: {CSP_FIN if p == '/financing/' else CSP_BASE}\n" for p in sorted({e[0] for e in SITEMAP} | {'/thank-you/'})) + f"/404.html\n  Content-Security-Policy: {CSP_BASE}\n"
open(f'{OUT}/_headers', 'w').write(f'''/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
{csp_rules}/assets/*
  Cache-Control: public, max-age=31536000, immutable
/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *
/assets/favicon.ico
  Cache-Control: public, max-age=86400
/assets/og-image.jpg
  Cache-Control: public, max-age=86400
/sitemap.xml
  Cache-Control: public, max-age=3600
''')
open(f'{ROOT}/netlify.toml', 'w').write('[build]\n  publish = "public"\n\n[build.processing]\n  skip_processing = true\n\n[functions]\n  directory = "netlify/functions"\n')
# Drop processed images that no page references (keeps the deploy lean)
_used = set()
for _root, _, _files in os.walk(OUT):
    for _f in _files:
        if _f.endswith(('.html', '.xml', '.webmanifest')):
            _used |= set(re.findall(r'/assets/img/([A-Za-z0-9_.\-]+\.webp)', open(os.path.join(_root, _f), encoding='utf-8').read()))
_removed = 0
for _f in os.listdir(f'{OUT}/assets/img'):
    if _f not in _used: os.remove(f'{OUT}/assets/img/{_f}'); _removed += 1
print('pruned', _removed, 'unused image files')
print('built', len(SITEMAP), 'indexable pages ->', OUT)
