---
name: app-factory
description: >-
  Take a new Mac + iPhone app from idea to a live, listed product in one repeatable pipeline: name
  and domain check, creative direction, prototype, SwiftPM/XcodeGen scaffold with an MCP server and
  iCloud sync, a static product site on Cloudflare Pages, domains, redirects and email forwarding,
  required SEO and AI-search (GEO) setup, analytics, cross-listing on your other sites, TestFlight,
  and a signed, notarized Mac DMG with Sparkle auto-update. Use when the user says "new app",
  "start an app", "app factory", "set up a site for <app>", or registers a domain for a new product.
  Its SEO/AI-search checklist also audits any existing product site.
metadata:
  version: "1.0.0"
---

# App Factory

One procedure for taking a new app from idea to a live, listed, tracked product. It strings together
things you already have: your newest app, your newest product site, your shared footer and your
analytics setup. **Never invent a new site template, footer, analytics setup or hosting pattern for
one app.** Copy the newest sibling and change only what is specific to the new app. If the portfolio
is inconsistent, match the newest one and note the drift.

> **Hard rule: never submit to App Review.** No agent clicks Submit for Review or submits an app,
> version, build or in-app purchase to App Review, even when the draft is ready or someone relays an
> approval. Prepare everything up to a saved, ready draft, then stop and tell the owner. The owner
> submits.

## Studio profile (fill in once)

The pipeline refers to these values. Keep them in your agent's memory or a `STUDIO.md` next to your
repos, and look them up instead of asking every time.

| Key | Example | Used for |
|---|---|---|
| Studio name / legal name | `Acme Labs` / `Acme Labs, LLC` | footer, JSON-LD Organization, copyright |
| Owner name | `Sam Rivera` | JSON-LD Person, "picks are the owner's" |
| GitHub owner | `acme` | `acme/<app>`, `acme/<app>-site` |
| Bundle ID prefix | `com.acme` | `com.acme.<app>`, `iCloud.com.acme.<app>` |
| Apple Team ID | `ABCDE12345` | `project.yml`, profiles |
| Domain pattern | `.ai` primary, `.app` redirect | naming, DNS, redirects |
| Studio site | `https://acme.example` | shared JSON-LD ids, portfolio listing |
| Reference app / site | your newest app and its site repo | what to copy |
| Task tracker | any board with plans + activity log | step 1 and close-out |
| Inbox for forwarding | the owner's address | catch-all email routing |
| Secret store | a secrets CLI or the Keychain | API keys, never in chat or repos |
| License wording | e.g. "free and open source (MIT)" | site, README, llms.txt |

## Rules for every step

- **Track it.** Before work starts, create a top-priority task on the owner's tracker with the plan
  and a definition of done, and log each step as activity. The tracker holds plans and to-dos only.
- **Picks are the owner's.** Name, visual direction and anything bought need the owner's pick on
  options they have actually seen. Show 2 to 4 options with one recommended, keep working on the
  recommendation, and never act on a pick they haven't seen. Never buy a domain unless told to.
- **Be honest about status.** Until a signed build is downloadable, every surface says "Coming soon".
  Never write "Available" or link a download that doesn't exist.
- **Look things up before asking.** Registrar, DNS, analytics IDs and site lists are findable in the
  dashboards, receipts and memory. Ask the owner only for sign-ins and picks.
- **Brand each app as itself** (its own fonts, colors, icon). The studio appears only in the shared
  footer, the "More from <Studio>" block and an "A <Studio> product" line.
- **SEO and AI search are part of the build, not a follow-up.** The app isn't done until the
  checklist in step 8 passes on the live domain.
- **Secrets stay secret.** Pipe keys from the secret store into the command that needs them. Never
  print them, commit them or paste them into a tool argument.

## The pipeline

Work top to bottom. Steps 4 to 9 can overlap once the name is picked.

| # | Step | Output |
|---|---|---|
| 1 | Plan | Tracker task with plan + definition of done |
| 2 | Name | 8 to 10 candidates, domain + App Store check, one recommended; owner picks |
| 3 | Creative direction | 3 distinct directions (palette, type, UI style, icon idea), one recommended; owner picks |
| 4 | Prototype | Clickable HTML prototype of the real screens with the real data shape |
| 5 | App scaffold + repo | SwiftPM/XcodeGen project on the house pattern, private repo, first build |
| 6 | Standard Settings | The house share / feedback / rate / support set, copied from the reference app |
| 7 | Website + hosting | Static site from the house template on Cloudflare Pages, domains, redirects, email |
| 8 | SEO + AI search (required) | Every box below checked and verified live |
| 9 | Analytics | Consent-gated GA4, Search Console, Bing, IndexNow |
| 10 | List it everywhere | Studio site and every "More from <Studio>" footer |
| 11 | Ship builds | ASC record, TestFlight build, signed + notarized Mac DMG with Sparkle on the site, CI |
| 12 | Close out | Memory updated, task Done with proof, one summary to the owner |

### Order of merges (so nothing links to a 404)

1. Site deployed and the primary domain serving over HTTPS.
2. Then merge the footer and studio-site listing changes.
3. Then submit to Search Console / Bing and run the live SEO check.

---

## 2. Naming

1. Write 8 to 10 candidates with a one-line rationale each. If the studio has a naming family (a
   shared suffix or style), prefer names in it and offer a couple outside it too.
2. Check domains at your registrar (most WHOIS/RDAP endpoints are blocked from cloud sandboxes; use
   the registrar's search or API). Check whether the owner already holds any of them.
3. App Store clash: search `"<name>" app store` and `"<name>" app`. Drop names with a live app of the
   same or confusingly close name, or a company already using the main domain.
4. Present on a decision card (max 4) or a short table, one recommended.
5. After the pick, rename everything: bundle ID `<prefix>.<app>`, iCloud container
   `iCloud.<prefix>.<app>`, Keychain service, env vars. Save the name to memory.

## 4. Prototype

- Read the real data or workflow the app replaces first, so the prototype uses the real shape.
- One self-contained HTML file: Mac window and iPhone side by side, the 3 directions as token sets
  swapped on `<body data-dir>`, light and dark. Share it privately; later keep it in the app repo
  under `design/`.

## 5. App scaffold

Every app uses the same shape. Copy it from your newest app; don't design a new one per app.

- **SwiftPM + XcodeGen.** A local package with `<App>Kit` (models, store, sync, services, MCP) and
  `<App>UI` (theme, shared views); `project.yml` with `Apps/Mac` and `Apps/iPhone` targets (iPhone +
  iPad). Swift 6. Gate on-device model features with `#available`. `.xcodeproj` stays gitignored.
- **Local-first, no server.** Workspace JSON in Application Support, writes coordinated with
  `NSFileCoordinator` so the app and its MCP process can share it.
- **MCP server built in.** The same executable run with `--mcp` is a stdio JSON-RPC MCP server on the
  same store. Read tools carry `readOnlyHint`. Writes are gated by a "Let agents make changes"
  setting, and every agent write is shown in an activity list in the app. An Agents screen can save
  client configs (Claude Code, Codex, Gemini CLI) and install a matching Agent Skill.
- **Secrets in the Keychain**, never in the workspace or an iCloud payload. A key set by an agent is
  read from an env var of the MCP process, never from tool arguments.
- **iCloud sync** in the user's private CloudKit database, with the house iCloud Sync and
  Diagnostics settings below.
- **Mac ships outside the Mac App Store** as a Developer ID build with Sparkle (no sandbox needed if
  it launches local agent CLIs); iPhone ships through TestFlight / App Store.
- **Repo:** `<owner>/<app>`, private until release, `.gitignore` for `.build/`, `DerivedData/`,
  `*.xcodeproj/`. A cloud agent without a Swift toolchain dispatches the first compile to a Mac
  (a local agent session or CI) rather than skipping it.

### iCloud Sync and Diagnostics settings (copy, never redesign)

Pick one app as the canonical source and copy its code into every iCloud app, changing only the app
name, the workspace row and the theme. Every device that touches iCloud (iPhone, iPad and the Mac's
Settings) shows:

1. **iCloud Sync** section
   - `Apple Account`: Not checked / Connected / Unavailable
   - one app-specific row, e.g. `Mac workspace`: Found / Not found yet
   - `Last check`, `Last iCloud response`, and the snapshot's own timestamp when there is one
   - the error in plain words, or "iCloud has no … from your Mac yet. Open <App> on your Mac…"
   - **Check Now** ("Checking iCloud…" while busy), `accessibilityIdentifier("settings.checkSync")`
2. **Diagnostics** section
   - `Error code` row (selectable), formatted `"<NSError domain> (<code>)"`
   - **Share Sync Diagnostics** (`ShareLink`, `accessibilityIdentifier("settings.shareSyncDiagnostics")`)
     sharing plain text: `<App> <version> (<build>)`, account status, the workspace row, last check,
     last response, snapshot time, error code
   - footer: "Includes sync status and timestamps. Your content and account details are not included."
   - never include keys, tokens, account names or user content

CloudKit rules that go with it:

- **Check per-record results.** `modifyRecords(saving:…)` only throws for the whole request; a
  rejected record comes back in the per-record results. Read them and surface that error.
- **Only record "last shared" when the per-record save succeeded.**
- **Create every record type in the Development schema first.** Production can't create types; a new
  type fails per record with "Cannot create new type <Type> in production schema". Save each type
  once from a Debug build, or add the types in CloudKit Console.
- **Deploy the schema to Production before the first TestFlight or Developer ID build.** Debug builds
  write to Development, so a working Debug build proves nothing about Production. Verify by fetching
  a record from a release build.

## 6. Standard Settings set

Pick one app as the reference implementation and copy its code; change only the app name, URLs and
colors. A good default set, on Mac and iPhone/iPad:

1. **Rating.** A "Share Your Experience" row. iOS and Mac App Store builds call `requestReview()`
   once, a couple of seconds after the app is idle, after 5 successful core actions, and only in
   production App Store builds (`AppTransaction` environment `.production`), never TestFlight/Xcode.
2. **Mac reminder card** (direct-download builds). Counts successful core actions; shows after 5,
   only while idle with no sheet in front, then at most once every 7 days. Actions: share the app,
   send feedback, rate it, newsletter, community, more apps; each row shows a checkmark once clicked.
   It returns until every action is clicked or the person picks "Don't show again". A Settings row
   always reopens it.
3. **Two dismiss buttons on every prompt the app shows by itself:** a large "Later" pill at the right
   of the button row (comes back after the interval) and a smaller, readable "Don't show again" text
   button at the far left (permanent, stored per prompt, e.g. `<app>.prompt.<id>.neverShow`). The
   system review sheet gets nothing extra.
4. **Support row** to your support page or form.
5. **Done means:** unit tests for the reminder rules (milestone, 7-day wait, all boxes, Later returns,
   Don't show again is permanent and per prompt) and review eligibility, plus screenshots of the real
   Settings rows and card.

If the studio's policy is "no money collection", also grep the repo for tip, coffee, donate, sponsor,
paywall and storekit and make sure nothing collects money.

## 7. Website, hosting, domains and email

### Template

Copy your newest **static HTML/CSS** product site (`git archive HEAD | tar -x -C ../<app>-site`).
Keep unchanged: header (wordmark, section links, CTA pill), consent-gated analytics script, share
pill, footer (community + newsletter callouts, the "More from <Studio>" block with the new app left
out of its own site, studio pill, footer nav, year), `robots.txt`, `sitemap.xml`, `llms.txt`,
`404.html`, the IndexNow script and key file, and the Cloudflare Pages files below.

Pages: `/` (hero with a working preview of the app using sample data, never real personal numbers,
plus a light/dark toggle), `/download/` (installer, or "Coming soon" with what the first release
includes), `/mcp/` (client setup + tool table), `/help/` (FAQ + contact), `/compare/` (vs 2 to 3
alternatives), `/privacy/`, `404`.

Re-skin with the picked direction: replace only the `:root` tokens, fonts and the hero/preview.
Keep class names and layout. Self-host fonts as woff2 (`npm pack @fontsource-variable/<font>`); the
CSP is `font-src 'self'` and `style-src 'self'`, so no CDN fonts and no inline `style=""`. Render
the icon to PNG from SVG (512 icon, 64 favicon, 180 apple-touch, 96 webp for footers). Use a small
generator script for the shared head/header/footer instead of hand-editing every page.

Check before pushing: serve locally, screenshot at 1366 and 390 wide, no horizontal scroll, no
console errors, every preview control works, and `grep -ri <template app name>` only hits the
"More from" entry.

### Cloudflare layout

```
Registrar (nameservers → Cloudflare)
   │
Cloudflare zone (Free): DNS, Email Routing, Redirect Rules (www, secondary TLD → primary)
   │  custom domain
   ▼
Pages project "<app>"  ◀── GitHub <owner>/<app>-site, main = production
   │  functions/_middleware.js (consent cookie, /downloads/* from R2)
   ▼
R2 bucket "<app>-downloads" (installers over 25 MiB)
```

1. **Zones:** add `<app>.<primary>` and the secondary TLD on the Free plan; wait for Active.
2. **Pages project from GitHub:** project `<app>`, production branch `main`, framework None, output
   `.`, build command `node tools/indexnow.mjs sitemap.xml . --lastmod && rm tools/indexnow.mjs`,
   env `NODE_VERSION=22`. Check `https://<app>.pages.dev/` first. Production deploys only from main;
   never `wrangler pages deploy` to production from a local tree.
3. **Custom domain:** add the primary domain in the Pages project (the dashboard creates the CNAME;
   the API alone does not). For `www` and the secondary TLD: proxied `AAAA @ 100::` / `AAAA www 100::`
   plus a zone Redirect Rule → `concat("https://<app>.<primary>", http.request.uri.path)`, 301, keep
   query string.
4. **Installers:** Pages refuses files over 25 MiB and a repo full of DMGs gets huge. Small DMGs may
   be committed under `/downloads/`; anything bigger goes to R2 bucket `<app>-downloads`, bound as
   `DOWNLOADS`. Upload **before** pushing the appcast:
   `npx wrangler r2 object put <app>-downloads/<App>-<ver>.dmg --file <dmg> --remote --content-type application/x-apple-diskimage`.
5. **Email Routing:** enable, catch-all → the owner's inbox, plus `hello@<app>.<primary>`; same on the
   secondary TLD. Test from a *different* account than the destination (Gmail drops a forwarded copy
   of your own sent message).

Common blockers: dashboard writes made from page JavaScript get a WAF 403 (click through the UI or
use the Cloudflare API); DNS lookups and CDN fonts are often blocked from cloud sandboxes.

`_headers`:

```
/*
  Referrer-Policy: strict-origin-when-cross-origin
  X-Content-Type-Options: nosniff
  Content-Security-Policy: default-src 'self'; script-src 'self' https://www.googletagmanager.com; style-src 'self'; img-src 'self' https://*.google-analytics.com https://*.googletagmanager.com; font-src 'self'; connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'none'

/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable

/downloads/*
  Content-Disposition: attachment
  Content-Type: application/x-apple-diskimage

/appcast.xml
  Content-Type: application/rss+xml; charset=utf-8
  Cache-Control: public, max-age=300
```

`_redirects`:

```
/downloads /download/ 302
/downloads/ /download/ 302
/support /help/ 301
/support/ /help/ 301
```

`_routes.json`:

```json
{ "version": 1, "include": ["/analytics-consent.gif", "/downloads/*"], "exclude": [] }
```

`functions/_middleware.js`:

```js
// /analytics-consent.gif?choice=granted|denied sets the first-party consent cookie.
// /downloads/<file> streams installers from the R2 bucket bound as DOWNLOADS (when bound).
export async function onRequest({ request, env, next }) {
  const url = new URL(request.url);
  const path = url.pathname;

  if (path === '/analytics-consent.gif') {
    const choice = url.searchParams.get('choice');
    const response = await next();
    if (choice !== 'granted' && choice !== 'denied') return response;
    const out = new Response(response.body, response);
    out.headers.append('Set-Cookie', `analytics_consent=${choice}; Path=/; Max-Age=34560000; Secure; SameSite=Lax`);
    out.headers.set('Cache-Control', 'no-store');
    return out;
  }

  if (path.startsWith('/downloads/') && env.DOWNLOADS && path.length > '/downloads/'.length) {
    if (request.method !== 'GET' && request.method !== 'HEAD') return new Response('Method not allowed', { status: 405 });
    const key = decodeURIComponent(path.slice('/downloads/'.length));
    const object = await env.DOWNLOADS.get(key, { range: request.headers, onlyIf: request.headers });
    if (object === null) return next();
    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set('etag', object.httpEtag);
    headers.set('accept-ranges', 'bytes');
    headers.set('content-disposition', 'attachment');
    headers.set('cache-control', 'public, max-age=3600');
    if (/\.dmg$/i.test(key)) headers.set('content-type', 'application/x-apple-diskimage');
    else if (/\.zip$/i.test(key)) headers.set('content-type', 'application/zip');
    headers.set('x-content-type-options', 'nosniff');
    if (!('body' in object)) return new Response(null, { status: 304, headers });
    let status = 200;
    if (object.range && request.headers.has('range')) {
      const { offset = 0, length = object.size - offset } = object.range;
      headers.set('content-range', `bytes ${offset}-${offset + length - 1}/${object.size}`);
      headers.set('content-length', String(length));
      status = 206;
    } else {
      headers.set('content-length', String(object.size));
    }
    return new Response(request.method === 'HEAD' ? null : object.body, { status, headers });
  }

  return next();
}
```

## 8. SEO and AI search (required gate)

The same checklist audits an existing site: run it, fix what's missing, ship to main, verify live.

**On every page (head)**
- [ ] Unique `<title>` and meta description (app name + what it does).
- [ ] `<link rel="canonical">` with the absolute primary-domain URL, trailing-slash style matching the
      sitemap. Redirect domains never canonical.
- [ ] Open Graph (`og:title`, `og:description`, `og:url`, `og:type`, `og:image` 1200x630,
      `og:site_name`) and `twitter:card` summary_large_image with title, description, image.
- [ ] No `noindex` on public pages (only drafts, 404 and private tools).
- [ ] One `<h1>`; real text near the top says what the app is, who it's for and what it runs on.

**Structured data (JSON-LD)**
- [ ] `SoftwareApplication` with `@id` `https://<app>.<primary>/#app`: name, description,
      `applicationCategory`, `operatingSystem`, `isAccessibleForFree`, an offer (`PreOrder` while
      coming soon, `InStock` + `downloadUrl` once live), `publisher` and `author` → shared ids.
- [ ] Shared ids, identical on every studio site: Organization `<studio site>/#org` and Person
      `<studio site>/#owner`. Never invent new ids per site.
- [ ] `WebSite` + `WebPage` on each page, `BreadcrumbList` on subpages.
- [ ] `/help/` has a visible FAQ **and** `FAQPage` JSON-LD with the same words. Edit both together.
- [ ] Parse every JSON-LD block in the built HTML so none is broken.

**Crawl files (site root)**
- [ ] `robots.txt`: `User-agent: *` Allow, then a named group allowing AI crawlers (OAI-SearchBot,
      ChatGPT-User, GPTBot, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User,
      Google-Extended, GoogleOther, Applebot, Applebot-Extended, bingbot, Amazonbot,
      meta-externalagent, meta-externalfetcher, DuckAssistBot, MistralAI-User, CCBot, cohere-ai,
      YouBot), and the `Sitemap:` line. A named group ignores `*`, so any `Disallow` goes in both.
- [ ] `sitemap.xml`: every public page on the primary domain, with `lastmod`.
- [ ] `llms.txt`: one-line description, durable key facts (platforms, requirements, price, license,
      privacy model), a link list of every page, MCP setup if any, and the studio link. No version
      numbers.
- [ ] IndexNow: a key file at the root (generate once, never rename) and a build step that submits
      only changed pages on production builds of main and never fails the build.

**Pages AI answers cite**
- [ ] `/help/` FAQ: setup, privacy, requirements, price, support.
- [ ] `/compare/`: the app vs 2 to 3 named alternatives, a table, "Which one to choose", 3 questions
      (visible + FAQPage), sources with the date read. Competitor facts only from their own pages.

**Search engines and analytics (after the domain serves)**
- [ ] GA4 property with a consent-gated tag; mark download / App Store clicks as key events.
- [ ] Google Search Console URL-prefix property, verified by meta tag; sitemap submitted, status
      Success with the right page count.
- [ ] Bing Webmaster Tools (import from GSC or a meta tag); sitemap submitted and read.

**Off-site**
- [ ] GitHub topics on the public repo(s).
- [ ] Listed on the studio site, its `llms.txt`, and every "More from <Studio>" footer.

**Verify live (the gate).** Check the live domain, not the repo: `robots.txt`, `sitemap.xml`,
`llms.txt` and the IndexNow key return 200; view source of `/` and `/help/` for canonical, OG/X,
parsing JSON-LD and verification metas; the Pages build log shows the IndexNow step; GSC and Bing
show the sitemap read. Record the result on the task.

## 10. List it everywhere

- **Studio site:** model the change on the commit that listed the previous app
  (`git log -i --grep=<previous app>`) and match its wording and every file it touched (portfolio
  data, app cards, SEO JSON-LD, `llms.txt`, analytics product hosts, any chat-agent prompt).
- **"More from <Studio>" footers:** insert the new entry after the newest app on every sibling site,
  in the same markup, with the 96px icon. Script it once (a dict of repo → file holding the block)
  so each new app is one run. A site's own block leaves itself out.
- While not downloadable, the status reads "Coming soon". Merge these only after the new site is live.

## 11. Ship builds

The run is done only when: the App Store Connect record exists and a build is in TestFlight's internal
group; a signed, notarized Mac DMG downloads from the site; Sparkle auto-updates from the site's
appcast; the site deploys from main; CI has its workflows and secrets; every repo is pushed.
App Store listing content (description, keywords, screenshots) waits for the owner.

**Apple setup** (developer.apple.com and App Store Connect, owner's signed-in browser):
1. iCloud container `iCloud.<prefix>.<app>` (the portal adds `iCloud.`; type the rest).
2. Explicit bundle ID `<prefix>.<app>` with iCloud (CloudKit, that container) and Push. One ID
   serves the Mac and iPhone targets.
3. App Store Connect → New App: iOS (+ macOS only for the Mac App Store), name "<App>: <subtitle>"
   (30 chars, unique), that bundle ID, SKU `<app>`.
4. Profiles: "<App> Developer ID" (macOS, Developer ID Application certificate) and "<App> App Store"
   (iOS, Apple Distribution). Commit them under `signing/` (they hold no secrets).

The App Store Connect API (ES256 JWT, admin key) can register bundle IDs, capabilities and profiles,
but there's no container endpoint and `POST /apps` isn't allowed, so the container and the New App
form need the browser.

**Project changes** (`project.yml`): bundle ID, Team ID, automatic signing, AppIcon + AccentColor.
Mac: hardened runtime, release profile specifier, Sparkle package
(`https://github.com/sparkle-project/Sparkle`), Info.plist `SUFeedURL https://<app>.<primary>/appcast.xml`,
`SUPublicEDKey`, `SUEnableInstallerLauncherService`, `ITSAppUsesNonExemptEncryption false`, and the
`mach-lookup` temporary exception for `<bundle>-spks` / `<bundle>-spki`. iPhone: release profile,
`aps-environment: production`. Add a "Check for Updates…" menu item (off in Debug or without a key).
iOS icon is a full-bleed 1024 square with **no alpha**. Create the Sparkle key with
`generate_keys --account <prefix>.<app>` (private key stays in the login Keychain). Build both Release
configurations unsigned first (`CODE_SIGNING_ALLOWED=NO`).

**Scripts** (copy from the reference app, rename):

| File | Does |
|---|---|
| `scripts/release-ios.sh` | xcodegen → archive → export → upload → wait for processing → add to the internal TestFlight group |
| `scripts/asc.py` | ASC API helper: `latest-build`, `wait-build`, `internal-group` |
| `scripts/release-mac.sh <ver> --notes … [--publish]` | archive (Developer ID) → notarize + staple app → build DMG with the house installer art → sign, notarize, staple DMG → `generate_appcast` → stage DMG + appcast in the site repo → bump version; `--publish` pushes both repos and waits until the live feed and a byte-identical DMG are served |
| `RELEASING.md` | how to release, which credentials, the CI secrets table |

Run the iOS release first (Apple processing takes 5 to 30 minutes) and the Mac release while it waits.

**CI** (GitHub Actions on a macOS runner, `brew install xcodegen && xcodegen generate`):
`checks.yml` (tests + unsigned Release builds on push/PR), `mac-release.yml` (manual; checks out the
site repo with a fine-grained token, imports the Developer ID p12, runs `release-mac.sh --publish`),
`testflight.yml` (manual; imports the Distribution p12, runs `release-ios.sh`). Set secrets with
`gh secret set` piped from the secret store, never echoed. The owner creates the fine-grained site
token and exports the p12s; agents can't mint credentials. Pushing workflow files needs a credential
with `workflow` scope.

**Verify:** the build is VALID in the internal group; `curl -sI <site>/downloads/<App>-<ver>.dmg` is 200
`application/x-apple-diskimage` and its SHA-256 matches; the appcast lists the build with an
`sparkle:edSignature`; `spctl --assess --type open --context context:primary-signature` accepts the
DMG; it mounts, shows the app and Applications over the artwork, and launches; from the second
release on, an older build's Check for Updates… offers the new one; CI is green on main.

**Release day (coming soon → available):** site CTA becomes "Download for Mac", JSON-LD offer
`InStock` + `downloadUrl`; studio site and every footer entry switch to "Mac app available"; mark
the download key event in analytics; save the launch post idea where the owner keeps post drafts.

## 12. Close out

- Update memory: one entry per app (repos, domains, Pages project, R2 bucket, analytics ID, status)
  and any decision the owner made.
- Confirm the SEO and AI-search gate passed on the live domain. Don't close out until it does.
- Mark the task Done with proof: live URLs, merged commits or PRs, analytics ID, GSC + Bing sitemap
  status, screenshots.
- Send one summary: what's live, what's coming soon, and the single next action the owner owns.
