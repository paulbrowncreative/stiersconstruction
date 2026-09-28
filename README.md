# Stier's Construction: deploy guide

## What is in this zip
- `public/` : the finished website. This is the only folder Netlify needs. It already contains `_headers`, `_redirects`, `robots.txt`, `sitemap.xml`, the blog feed and all images.
- `netlify.toml` : tells Netlify to publish `public/` (used for Git or CLI deploys).
- `build.py`, `content.py`, `blog/`, `areas/`, `src/` : the source that generates `public/` (only needed if you edit content).
- `README.md`, `QA-REPORT.md` : instructions and the QA notes.

## Deploy (fastest): Netlify drag-and-drop
1. Unzip `stiers-construction-website.zip`.
2. In Netlify: Add new site > Deploy manually > drag the `public` folder in.
3. Redirects and security/cache headers are inside `public/`, so they apply on drag-and-drop.

## Deploy via Git (for ongoing edits)
Put everything from the zip in a repo. `netlify.toml` publishes `public/` with no build command. To change content: edit `content.py`, `build.py`, `blog/`, `areas/` or `src/`, run `python3 build.py`, and commit `public/`.

## Form emails: silent backend (sends every submission to kevin@stiers-construction.com)
Both forms (quote and careers) are Netlify Forms. A serverless function, `netlify/functions/submission-created.js`, runs automatically on every real (non-spam) submission and emails it to `kevin@stiers-construction.com` with the sender as reply-to, and attaches any uploaded photos or resume. Visitors see no change. Netlify also keeps a copy of every submission in the dashboard as a backup.

**Important: drag-and-drop deploys do not include functions.** Deploy with Git or the Netlify CLI:
1. One-time email setup: create a free account at resend.com (sign up with kevin@stiers-construction.com) and create an API key. To send from your own domain, add the DNS records Resend gives you and use `forms@stiers-construction.com`. While testing you can use `onboarding@resend.dev`, which Resend delivers only to the account owner's own address.
2. Install the CLI and log in: `npm i -g netlify-cli`, then `netlify login`.
3. From this folder run `netlify link` (choose your existing site), then set the variables:
   - `netlify env:set RESEND_API_KEY re_your_key`
   - `netlify env:set MAIL_FROM "Stier's Website <forms@stiers-construction.com>"`
   - Optional: `netlify env:set MAIL_TO someone@else.com` (default is kevin@stiers-construction.com)
   - Optional but recommended: `netlify env:set NETLIFY_API_TOKEN <personal access token>` (lets the function confirm each submission is real)
4. Deploy with `netlify deploy --prod`. It uses `netlify.toml` to publish `public/` and the function. Git-based deploys work the same way once the variables are set.
5. Send one test submission from each form and confirm both emails arrive. If they do not, open Netlify > Logs > Functions > submission-created.

If the variables are missing nothing breaks: the submission is still saved in Netlify Forms and the function logs a warning. Run the function tests any time with `node tests/submission-created.test.js`.

## After first deploy
- Domains: set `www.stiersconstruction.com` as primary and let Netlify redirect the apex. Canonicals/sitemap already assume `https://www.stiersconstruction.com`.
- Forms: Site configuration > Forms > Notifications: add email notification for `quote` and `careers` (submissions are also stored in Netlify).
- Submit `https://www.stiersconstruction.com/sitemap.xml` in Google Search Console; keep the Google Business Profile name, phone and hours identical to the site.
- Analytics: no tag installed. Click/form events already push to `dataLayer` (`phone_click`, `email_click`, `quote_cta_click`, `generate_lead`). If you add GA/GTM, update the Content-Security-Policy in `_headers` to allow it.

## Financing (Enhancify)
- `/financing/` embeds Enhancify's Full Page Widget (page id 9934698). The widget script loads only when the section nears the screen, and only on this page.
- `_headers` gives `/financing/` a Content-Security-Policy that also allows Enhancify, Google Fonts and cdn.enhancify.com. Every other page keeps the strict policy. Each page has exactly one CSP rule, so don't add a blanket `/*` CSP rule, or it will merge with the financing one and block the widget.
- If Enhancify changes hosts or the widget stops loading, check the browser console for CSP messages and update `CSP_FIN` in `build.py`.
- The widget colours are set in `build.py` (`data-color1`, `data-color2`).
- Events: `financing_widget_load`, `financing_link_click`.

## Sticky financing button (Enhancify "Real Widget" replacement)
- Enhancify's Real Widget is a button that opens your co-branded page in a popup iframe. We rebuilt it with our own accessible dialog instead of loading their script (their popup's close control is a plain div, with no keyboard access or dialog semantics).
- Desktop: a "Financing options" pill at bottom-left appears after scrolling, hides over the footer and while the popup is open. Mobile: a third "Financing" button in the bottom bar. Neither appears on /financing/, /contact/, /careers/.
- The iframe loads only after a click. Source URL is `FIN_FRAME_SRC` in `build.py`. The CSP allows `frame-src https://www.enhancify.com`.
- Event: `financing_widget_open` (source: sticky_button or mobile_bar).

## Blog
- 18 articles in `blog/posts_a.py`, `posts_b.py`, `posts_c.py`, with deeper sections in `extras_a.py` / `extras_b.py`. `blog/blog_data.py` merges them.
- To add an article: copy a post dict, give it a slug, category, hero image key (from `src/data/images.json`), takeaways, body, FAQs and related slugs, then run `python3 build.py`.
- Every article gets: table of contents, key takeaways, FAQ, BlogPosting + FAQPage + Breadcrumb schema, related guides, sitemap entry and an RSS item (`/blog/feed.xml`).
- Service pages and the home page automatically link to matching articles.
- All dates are the build date (2026-09-20). Change `date` per post to stagger publication.

## Headlines
`build.py` title-cases headings, page titles, buttons, nav and footer labels automatically (`tc()` / `postprocess()`), so write source copy in normal case.

## Build tools
`python3 build.py` needs only Python 3 (no other packages). For minified CSS and JavaScript, first run `pip install rcssmin rjsmin`; without them the site still builds, just unminified.

## Local pages
- Town data lives in `areas/towns.py`. To add a town: copy a dict, set slug, county, water type, hero image key, two paragraphs, three facts, service list, FAQ and neighbors, then run `python3 build.py`.
- Keep facts specific and sourced. Do not add a town without unique local details.

## Confirm before launch
- Email domain (`stiers-construction.com` vs `stiersconstruction.com`).
- Add licence/insurance statements only if true. Add a street address and city list only if you want them public.
- Whether you pull permits for clients; whether "own trucks" wording is right.
- Privacy policy page (forms collect personal data).
