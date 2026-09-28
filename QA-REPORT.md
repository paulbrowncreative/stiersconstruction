# Stier's Construction: content parity and copy QA

## 1. Old site vs. new site (content parity)
I re-crawled all 13 pages of the live stiersconstruction.com and compared every text item against the new build.

**Carried over (all present):**
- All 10 services, with every list item from the old pages (installation, repair, maintenance, removal, hauling, finishes, materials). Dredging and pilings were buried under the old Seawalls page and now have their own pages.
- Boat hoist types and published size ranges, plus cable, motor and welding maintenance descriptions (added a "Lift Types Explained" section from the old text).
- Concrete finishes, deck materials (composite, wood, Trex, pool), excavating, grading, hauling and demolition details.
- Kevin and Chris bios (including Stier's Enterprise), contact details, hours, Instagram and Facebook, both Google review quotes, careers page and form, contact form fields (name, phone, email, address, message, photos/videos).
- Old-site phrases restored where they were missing: "protect from erosion and structural damage," "regular maintenance helps prevent costly repairs," "visually appealing," the piling anchoring/support wording, Trex "eco-friendliness," the elevator/4-point/8-point/PWC/boat house descriptions, "dual perspective," "honest work, clear communication," the contact-page welcome line and "Not seeing what you are looking for? Send us a message."
- Photos: 54 of the old site's 90 images. Left out on purpose: 4 logo or blank files, 2 personal photos, unrelated screenshots and duplicates.

**Not carried over on purpose:**
- "Certified team" (old home page). No certification is named anywhere, so it is left out until you can say which ones.
- Typos ("Maintenane," "bushed," "finsh," "Drive way") are corrected. Cart icon, broken menu links and dead pages removed (redirected).
- JobTread web forms replaced by Netlify Forms. Tell me if you want JobTread kept.

## 2. Grammar, spelling and title case
- Title case applied to all headings, page titles, buttons, menu and footer labels (1,638 elements checked, 0 exceptions found). Small words (a, an, and, of, the, to, for...) stay lowercase; acronyms and units (PWC, EGLE, MIG, ft) are preserved.
- Spell-check across every page: only real terms flagged (riprap, flatwork, snowmelt...). No repeated words or a/an errors.
- One unverified claim removed: "Welding is where Stier's started" (now "Welding is central to what we do").

## 3. Blog
- 18 articles, about 12,000 words, six topics: seawalls, docks/pilings/hoists, permits, dredging, Michigan waterfront living, concrete/decks/steel.
- Facts checked against EGLE (permit and OHWM pages), the U.S. Army Corps Detroit District (water levels) and Michigan building-department guidance (42-inch footings). Anything not verified is worded generally.
- Written as company articles (author: Stier's Construction). **Have Kevin read them before publishing**, especially statements about how Stier's works.
- No prices, rates, lifespans or guarantees appear anywhere.

## 4. Local service-area pages (added)
- 19 town pages at `/service-area/<town>/` plus a rebuilt `/service-area/` hub grouped by waterway (Lake St. Clair, St. Clair River, Detroit River, Lake Erie and tributaries).
- Each page has its own facts (county, waterway, nearby parks and features, current or depth data where a public source exists), its own service priorities, a town-specific FAQ, waterway-specific permit guidance, nearby-town links and matching blog guides. Pages share only the permit boilerplate for the same waterway (highest 6-word overlap between any two pages: 26%).
- Sources used: EGLE (permits, ordinary high-water marks), NOAA Coast Pilot (St. Clair River currents), U.S. Army Corps Detroit District, Wayne County, city and township sites, Great Lakes Scuttlebutt and the Blue Water Area CVB.
- Honest exception: Grosse Pointe Woods has no Lake St. Clair shoreline of its own, so its page focuses on concrete, decks, excavating and steel and says so.
- Every town is also in the footer, the home page and the LocalBusiness schema (`areaServed` as City entities).
- New blog article: how Lake St. Clair, the St. Clair River, the Detroit River and Lake Erie differ, linking to all 19 towns.
- No claim is made that Stier's has completed projects in any specific town.

## 5. Technical SEO and functional audit (final pass)
**Method:** crawled all 59 built pages; validated HTML with the W3C Nu validator; ran Lighthouse (mobile, throttled) on 8 page types; ran axe accessibility on desktop and mobile; tested every interactive feature in a real browser under the production security headers.

**Results**
- Lighthouse mobile: Performance 97 to 99, Accessibility 100, Best Practices 100, SEO 100 on home, service, blog post, blog hub, town page, services hub and contact. Layout shift 0, blocking time 0 to 20 ms, LCP about 2.0 to 2.5 s (simulated slow 4G).
- W3C HTML validation: 0 errors on all 59 pages (7 found and fixed: `figcaption` inside links on the home mosaic, and the Netlify honeypot attribute, now `data-netlify-honeypot`).
- Every indexable page: unique title (max 65 chars) and description (70 to 160), self-referencing absolute canonical, OG and Twitter tags, one h1, no skipped heading levels, all images with alt text and dimensions, no duplicate IDs, no dangling ARIA references.
- Sitemap: 57 URLs, all indexable, none noindex, matches canonicals. Robots.txt allows everything except `/thank-you/`. RSS feed valid.
- Structured data: 100% parse cleanly; BlogPosting has headline, dates, author, publisher, image; FAQ markup matches visible FAQs; breadcrumb positions correct; business node includes region-only address (no street address supplied).
- Redirects: all 16 old URLs map to live pages with no chains. A `/services` to `/services/` rule was removed because it could create a redirect loop on Netlify.
- Links: 0 broken internal links or images; every page has 3+ inbound internal links; all internal links use the canonical trailing slash.
- Accessibility (axe): 0 violations on every page except the third-party Enhancify widget (missing labels and low-contrast small print inside their widget).
- Tested working: mobile menu, Services dropdown, cross-section hover, gallery filters and lightbox, sticky financing button, financing popup and Enhancify iframe under CSP, financing widget page, quote and careers form markup and validation.

**Could not verify from here**
- Live Netlify behavior: form submissions and notifications, headers and redirects actually applied, HTTPS/HSTS, domain setup, Google indexing.
- Facebook (400) and Instagram (429) links block automated checks; the U.S. Army Corps water-levels page did not respond from this environment. All three are correct as published by their owners.

## 6. Mobile menu "See All Services" failure (diagnosed and fixed)
- **Cause:** an earlier build shipped a redirect rule `/services  /services/  301!`. Netlify treats `/services` and `/services/` as the same path, so `/services/` redirected to itself forever ("too many redirects", page will not load). Every link to the services page was affected, including See All Services in the menu.
- **Reproduced** with Netlify's own redirect engine (Netlify CLI): old rule = endless 301 loop; current build = 200.
- **Fixed** in the audit pass (rule removed) and **guarded**: `build.py` now fails the build if any redirect points at itself.
- **Verified** against Netlify's engine: 81 internal paths return 200 (unknown URLs return the custom 404); every old Squarespace URL resolves in a single redirect.
- **Action for the site owner:** re-deploy the latest zip. Deploys made from earlier zips still contain the looping rule.

## 7. Final pass: brand in titles, buttons, SEO
- **Titles:** every SEO title (title tag, og:title, twitter:title) now ends with "| Stier’s Marine & Construction" (home page leads with it). og:site_name, the business and website schema name, blog author and the web manifest use the same name; "Stier’s Construction" and "Stier’s Welding & Construction" are kept as alternate names in the schema. Titles are set in `TITLE_MAP` in `build.py` (pages), `areas/towns.py` (towns) and `blog/blog_data.py` (`BLOG_T`).
- **Buttons and links:** 97 automated click checks pass under Netlify's own redirect and header engine: header, dropdown (every item), logo, hero CTAs, all 10 cross-section pins and legend links, photo tiles, FAQ toggles, sticky financing button, popup Open/Close/Escape, footer and social icons, gallery filters and lightbox, blog TOC and category chips, financing anchor, quote and careers forms (empty submit blocked, valid submit POSTs form-name and fields to /thank-you/), full mobile menu, mobile bar, mobile popup.
- **SEO:** 59 pages, 0 W3C errors, 0 axe violations (outside the third-party widget), all canonicals/sitemap/schema checks pass, every fragment link resolves, Lighthouse mobile 99/100/100/100.
- **Still using "Stier’s Construction" in visible page copy** (footer, form text, body copy) and "Welding & Construction" in the logo text. Only SEO metadata was changed.

## 8. Form email backend
- New function `netlify/functions/submission-created.js` emails every quote and careers submission to kevin@stiers-construction.com (reply-to = sender, photos and resume attached, HTML escaped, spam-trap submissions ignored). Netlify Forms keeps a backup copy.
- Tested: 12 unit tests (recipient, subject, escaping, attachments, download failure fallback, missing key, provider errors, forged calls, bad input) and an end-to-end run under Netlify's real function runtime against a mock email provider (quote and careers delivered to kevin@stiers-construction.com, spam trap ignored).
- Not testable from here: delivery through the real email provider. It needs a Resend API key and a deploy via Git or CLI (drag-and-drop does not deploy functions). See README.

## 9. Upload limit set to 4.2 MB
- Netlify's form upload limit is 4.2 MB (verified by the site owner). The quote and careers forms now say so, and the browser blocks anything over 4,200,000 bytes in total across all attached files with a clear message. Tested: 3 MB and exactly 4.2 MB pass; 4.2 MB plus one byte, 5 MB, two 3 MB photos and a 5 MB resume are blocked. Videos and larger files are directed to kevin@stiers-construction.com.

## 10. Final pass: bugs found and fixed
| Issue found | Fix |
|---|---|
| On phones 350px wide or narrower (e.g. iPhone SE), the "Welding & Construction" logo text ran under the Menu button | Logo subtitle hides and logo shrinks below 360px; verified no overlap at every width from 300 to 430px |
| With JavaScript off, the mobile menu could not open, so navigation was unreachable | No-JS fallback shows the full menu in the page; desktop dropdown already worked without JS |
| Service and town page headings wrapped to 6 lines at tablet-landscape widths (about 1024px) | Heading size and width tuned for mid-width screens |
| 8 processed photos were shipped but never used (2 MB) | Build now removes any image no page references |
| CSS and JavaScript were not minified | Minified at build (optional `pip install rcssmin rjsmin`); JS re-verified |
| Upload limit text still said 8 MB | Set to 4.2 MB everywhere (previous pass) |

**Verified after the fixes:** 112 layout checks (14 page types x 8 widths from 320 to 1920px) with no overflow, clipping, broken images, wrapped headers or small tap targets; 97/97 button and link checks under Netlify's engine; 82 internal paths and 199 asset URLs all return 200; W3C 0 errors on 59 pages; axe clean; Lighthouse mobile 98 to 100 on every category; function tests 12/12; spelling, title case and repeated-word scans clean.

**Could not verify from here:** Firefox and Safari (only Chromium available); real email delivery (needs Resend key and Git/CLI deploy); Netlify applying the `_headers` cache rules (Netlify's local dev server overrides Cache-Control, real Netlify honors it); Google indexing.

## 11. Thank-you page redesign
Replaced the plain confirmation text with a full page matching the site's design system: dark hero with an animated checkmark, a "What Happens Next" 3-step section, a customer-review trust section, and a "Recent Work" photo strip.

**Bug found and fixed during the redesign:** one photo in the new strip (a portrait-oriented boat-hoist shot forced into a landscape crop) rendered as a blank tile in Chromium despite loading successfully (correct dimensions, no network errors, correct computed styles) — isolated via direct pixel comparison and a minimal reproduction, then resolved by swapping in a landscape-oriented photo rather than fighting the underlying rendering edge case. Re-verified all three photos render correctly afterward.

**Verified:**
- W3C HTML validation: 0 errors
- axe accessibility: 0 violations, desktop and mobile
- Lighthouse mobile (2 runs): Performance 97–99, Accessibility 100, Best Practices 100, SEO 69 (expected — Lighthouse always flags `noindex` pages regardless of intent; this page is correctly excluded from search since it only appears after a form submission)
- All links/buttons tested and working: project-photos CTA, home CTA, phone tel: link, gallery link, breadcrumb
- `prefers-reduced-motion` correctly disables the checkmark animation
- No layout overflow, desktop or mobile; full-site QA re-run afterward with no regressions elsewhere

## 12. Thank-you page: copy update and centering fix
Per request: changed the headline ("Thanks, We Got Your Message" → "You're All Set") and subhead, replaced the "While You Wait" testimonial section with "A Few Things Worth Reading" (three links into the permits, financing, and maintenance guides most relevant right after requesting a quote), and rebuilt the page as a single centered column end to end.

**Bug found and fixed during this pass:** the headline's box was narrower than its container (inherited `max-width: 20ch` from the shared page-hero style) with no auto margins, so at some widths (768px confirmed) the box itself sat flush left while only the text inside it was centered — the heading looked shifted left even though every other element was centered correctly. Fixed by adding explicit `margin: 0 auto` to the constrained-width heading and lead paragraph.

**Verified:** measured the horizontal center offset of every major element (icon, heading, subhead, urgent line, buttons, photo, both section headings, steps, new reading cards, strip heading) at 11 widths from 320px to 1920px — all read exactly 0px offset, no overflow at any width. W3C: 0 errors. axe: 0 violations at desktop, tablet, and mobile widths. All links tested, including the three new guide links. Full-site regression scan re-run afterward with no issues on any other page. Function tests: 12/12 passing.

## 13. Review font size mismatch fixed
Kevin's review ("Kevin did a great job...") had a `q-sm` modifier class applying a smaller font size and lighter weight than the first review, unintentionally making it read as less prominent. Removed the modifier so both reviews share identical styling.

**Verified:** computed font-size and font-weight now match exactly at every breakpoint (29.6px/600 desktop, 25.2px/600 tablet, 20.7px/600 mobile). No overflow on mobile with the now-larger second quote. Full-site regression scan, W3C validation, and function tests re-run with no issues.

## 14. Financing button: made sticky/constant, and a real collision bug fixed
Per request: removed the scroll-triggered appear/disappear behavior entirely (previously invisible until scrolling 500px, then hidden again over the footer) so the button is now visible immediately on load and stays visible through the entire page, footer included.

**Bug found while implementing this:** my first attempt also raised the button's position (`bottom: 20px` → `104px`) on the assumption that "too low" meant the corner offset itself, not just the delayed appearance. This caused a genuine new problem — at that height the fixed button directly overlapped the homepage hero's own "Get a Free Quote" button, and further testing showed the pill-shaped button (with visible text label, ~217px wide) collided with real interactive elements — the hero's own CTA button on 5 of 8 tested pages, and the project gallery's filter buttons — because the site has no outer page margin at all in the common 900–1200px viewport-width range, so a wide fixed-position element at the left edge has nowhere safe to sit without overlapping in-flow content at many scroll positions.

**Fix:** reverted the corner offset to a standard, safe position (20px), and converted the button from a wide text pill into a compact 56px circular icon button (calculator icon, with `aria-label` and `title` for accessibility) so its footprint no longer intrudes into the content column at any tested width.

**Verified:** 65 automated checks across 9 page types, 6 viewport heights (700–1080px), and 5 widths (900–1920px, including the narrowest width the button appears at) — zero collisions with any button or link anywhere. Confirmed the button is visible with full opacity on load, mid-scroll, and at the very bottom of the footer on every page it appears on. Confirmed it still correctly hides only while its own dialog is open, and is still correctly excluded from `/financing/`, `/contact/`, and `/careers/`. Dialog open/close, Escape-to-close, and iframe loading re-tested and working. axe: 0 violations. W3C: 0 errors. Full-site regression scan and function tests re-run with no issues.
