# -*- coding: utf-8 -*-
import re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from posts_a import POSTS_A, EGLE_GL, EGLE_OHWM, USACE_LEVELS
from posts_b import POSTS_B
from posts_c import POSTS_C
from posts_d import POSTS_D
from extras_a import EXTRAS_A
from extras_b import EXTRAS_B

EXTRAS = {**EXTRAS_A, **EXTRAS_B}
CATS = ['Seawalls', 'Docks, Pilings and Hoists', 'Permits and Regulations', 'Dredging', 'Michigan Waterfront Living', 'Concrete, Decks and Steel']

def _insert_extra(body, extra):
    """Insert extra sections before the closing call to action (last paragraph linking to /contact/)."""
    pos = body.rfind('/contact/')
    idx = body.rfind('<p>', 0, pos)
    pre = body[:idx].rstrip()
    if pre.endswith('</h2>'):
        idx = pre.rfind('<h2>')
    return body[:idx] + extra + '\n' + body[idx:]

POSTS = []
for p in POSTS_A + POSTS_B + POSTS_C + POSTS_D:
    q = dict(p)
    body = q['body']
    if q['slug'] in EXTRAS:
        body = _insert_extra(body, EXTRAS[q['slug']])
    body = body.replace('href="EGLE_OHWM"', f'href="{EGLE_OHWM}"').replace('href="EGLE_GL"', f'href="{EGLE_GL}"').replace('href="USACE_LEVELS"', f'href="{USACE_LEVELS}"')
    q['body'] = body
    q['words'] = len(re.sub(r'<[^>]+>', ' ', body).split())
    q['minutes'] = max(3, round(q['words'] / 220))
    POSTS.append(q)
HERO = {'seawall-guide-metro-detroit':'sheet-pile-excavator-canal-home','vinyl-vs-steel-vs-concrete-seawalls':'sheet-pile-staging-seawall','signs-your-seawall-is-failing':'demolition-excavator-canal',
 'seawall-anatomy-tie-rods-caps-french-drains':'vibratory-hammer-steel-pile','michigan-permits-seawalls-docks-dredging':'barge-open-water','floating-vs-fixed-docks':'l-shaped-dock-choppy-water',
 'wood-vs-steel-pilings':'excavator-barge-timber-pilings','how-to-choose-a-boat-hoist':'boat-house-hoist-tarped-boat','boat-hoist-maintenance-checklist':'welder-under-dock',
 'dredging-101-canals-marinas-boat-wells':'barge-excavator-canal','michigan-winter-dock-seawall-damage':'winter-dock-edge','great-lakes-water-levels-waterfront-property':'wood-dock-yellow-flag',
 'buying-waterfront-home-inspection-checklist':'boat-lift-covered-slip','waterfront-concrete-freeze-thaw':'new-concrete-patio','composite-vs-wood-vs-trex-decks':'red-stained-log-cabin-deck',
 'marine-steel-corrosion-welding-fabrication':'welding-at-night-waterfront','seasonal-waterfront-maintenance-checklist':'dock-boxes-moored-boat','how-to-pay-for-a-waterfront-project':'new-deck-over-seawall','lake-st-clair-detroit-river-st-clair-river-waterfront-differences':'pipe-pilings-barge-sunset'}
for _p in POSTS: _p['hero'] = HERO[_p['slug']]
BLOG_T = {'seawall-guide-metro-detroit':'Seawall Guide for Metro Detroit','vinyl-vs-steel-vs-concrete-seawalls':'Vinyl vs. Steel vs. Concrete Seawalls','signs-your-seawall-is-failing':'7 Signs Your Seawall Is Failing',
 'seawall-anatomy-tie-rods-caps-french-drains':'Seawall Anatomy Explained','michigan-permits-seawalls-docks-dredging':'Michigan Seawall & Dock Permits','floating-vs-fixed-docks':'Floating vs. Fixed Docks',
 'wood-vs-steel-pilings':'Wood vs. Steel Pilings','how-to-choose-a-boat-hoist':'How to Choose a Boat Hoist','boat-hoist-maintenance-checklist':'Boat Hoist Maintenance Checklist',
 'dredging-101-canals-marinas-boat-wells':'Dredging 101 for Canals & Boat Wells','michigan-winter-dock-seawall-damage':'Michigan Winter Dock & Seawall Damage','great-lakes-water-levels-waterfront-property':'Great Lakes Water Levels Guide',
 'buying-waterfront-home-inspection-checklist':'Waterfront Home Buyer Checklist','waterfront-concrete-freeze-thaw':'Waterfront Concrete & Freeze-Thaw','composite-vs-wood-vs-trex-decks':'Composite vs. Wood vs. Trex Decks',
 'marine-steel-corrosion-welding-fabrication':'Marine Steel & Corrosion Guide','seasonal-waterfront-maintenance-checklist':'Waterfront Maintenance Checklist','how-to-pay-for-a-waterfront-project':'How to Pay for a Waterfront Project',
 'lake-st-clair-detroit-river-st-clair-river-waterfront-differences':'Metro Detroit Waterways Compared'}
for _p in POSTS: _p['t'] = BLOG_T[_p['slug']]
# pillar first, then the rest in authored order
POST_BY_SLUG = {p['slug']: p for p in POSTS}
