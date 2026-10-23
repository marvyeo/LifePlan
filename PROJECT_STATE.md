# Life Plan Dashboard — Project State

> **Next chat name: `Life Plan Dashboard ver 3`**
> Claude: your FIRST reply in a new chat must start with "Rename this chat to: **Life Plan Dashboard ver 3**" (you can't rename chats yourself). In your first commit this session, bump the number here by 1.

**State version:** 2 (Sprint 13.1 hub shell built 2026-10-23, chat "Life Plan Dashboard ver 2"; v1 was the Sprint 7 build)
**Maintenance rule:** When ported to a new chat, name it "Life Plan Dashboard ver X". Update this file in the same commit as any change. `git pull` before working.

| Item | Value |
|---|---|
| Repo | `marvyeo/LifePlan` (public) |
| Live URL | https://marvyeo.github.io/LifePlan/ (demo data: `?demo`) |
| Stack | `index.html` (vanilla JS, own CSS), `sw.js` (network-first, `lifeplan-v5`), `manifest.json`, `icons/` |
| Auth | Shared OAuth client `669494100250-…`. Scope `drive.file` first; "Grant read-only access" switches to `drive.readonly`. Redirect sign-in fallback for iPhone home-screen use (needs the URL in Authorized redirect URIs). |
| Writes | **Nothing.** Read-only by design. |
| Role | **Hub (Sprint 13).** Life Plan is the one installed app: launcher for all apps plus the due dashboard. Manifest `scope: "/"`, `start_url: "/LifePlan/"`, `id: "/LifePlan/"`. |

## ⚙ Session Rules (every chat that works on this app follows these)

**1. Pick the cheapest model that can do the job.** At the start of every session Claude names the model it recommends and the estimated size (below). If the chat is on a pricier model than needed, Claude says so before starting.

| Model | Use for |
|---|---|
| **Haiku** | State-file edits, text or label changes, small data packs, lookups, "where is X" questions |
| **Sonnet** (default) | Features, bug fixes, refactors, data processing (e.g. novel volumes, PullList), most app work |
| **Opus** | Only for new-app builds, cross-app architecture, or a bug Sonnet has failed on twice. Claude says why before using it |

**2. Every push updates this file in the same commit.** No exceptions, including PR branches and one-line fixes.
- `git pull` before starting, so you build on the latest state.
- Add a dated line to the change log (what changed and why, in plain words) and update any section the change made wrong.
- If a session ends without a push, nothing changes here.

**3. Size the work first, and plan the pause points.**
- Before starting, Claude lists the steps and sizes the job: **S** (under ~20k tokens), **M** (~20–60k), **L** (over ~60k).
- **M and L jobs are split into checkpoints.** Each checkpoint ends with a commit and a state update, so a cut-off session loses nothing.
- **Pause** when usage is around half the window, when the chat has grown long (heavy file reads, ~30+ turns), or before a step that won't finish in what's left. Claude can't see the remaining credit directly, so on L jobs it asks Marvin to check usage at each checkpoint.
- **On pause,** Claude writes a `▶ RESUME HERE` block at the top of this file: what's done, the exact next step, branch and files, and the first command to run. It also gives Marvin a one-line restart prompt ("Continue <App> ver X from RESUME HERE"). The next session starts from that block and deletes it once the step is done.

**4. Chat naming.** Use the **Next chat name** line at the top of this file; tell Marvin in the first reply, then bump it.

## Hub shell (Sprint 13.1, built 2026-10-23)
- **Config:** `HUB` array in `index.html` (app, name, url, feed flag, note). Icons are `icons/apps/<app>.png`, copied from `design/make_icons.py` output (so the shell works offline). Feed apps are also in `SOURCES`; FoodGuide (Makan Map), NovelReader and VacationGuru are **tiles only** (no due feed).
- **Phone (<900px):** bottom nav with two tabs, **Due** (the existing dashboard, red badge = attention count) and **Apps** (tile grid with due counts). Tab remembered (`lp-tab`). Tapping a tile opens the app in the same window.
- **Desktop (>=900px):** two panes. Left = app list (plus "All apps"); click selects, right = that app's due items with an **Open** button. Tiles-only apps show a short note. Selection remembered (`lp-sel`).
- **Polish:** `viewport-fit=cover` with safe-area insets on header, nav and toast; `100dvh` for the sign-in screen and the sticky left pane; 44px touch targets on touch devices.
- **Not done yet (13.2-13.5):** "← Life Plan" button in each app, iOS redirect sign-in and home-screen hint per app, shared sign-in across apps, deep links from due items. Feed items still open with `target=_blank`; 13.5 changes that.

## Sources (config array `SOURCES` in index.html)
| App | File | Notes |
|---|---|---|
| TV World | `tvworld-data.json` | episode, release (movies), due-date (monthly refresh) |
| Financial Planner | `financialplanner-data.json` | bill-due, cap-alert, rules-update |
| ChoreWheel | `chorewheel-data.json` | chore (overdue dated today, high) |
| ComicsTracker | `comicstracker-data.json` | release |
| MCC Inventory | `mcc-inventory-items.json` | low-stock (dated on last save); legacy raw array = no items |

File lookup: id remembered per device, else newest file by name. "Pick missing files" opens Google Picker for files `drive.file` can't see (e.g. a file the other household account created).

## Views
- **Attention:** past-dated items that are high priority or action types (bill, due-date, chore, low-stock, cap-alert, rules-update), plus high-priority action items dated today. Past episodes and releases drop off.
- **7 days / 30 days:** grouped by day; headline summarises counts by type.
- App filter chips (remembered). Sources panel shows item count, last saved, and a **stale** warning after 7 days, since `upcoming[]` only refreshes when an app saves.
- Last good result cached in localStorage; auto-refresh on return after 10 minutes.

## Known: two apps use other Google Cloud projects
TV World (client `678456232174-…`) and MCC Inventory (client `676510183503-…`, full `drive` scope) aren't on the shared client, so under `drive.file` Life Plan can't find their files by name. Fix: **Pick missing files** once. The grant is stored with the Google account and works on every device. Moving those apps to the shared client isn't worth it, because they'd lose sight of their own existing files.

## Open items
- [x] Tile URLs confirmed by Marvin 2026-10-23 (FoodGuide, NovelReader, VacationGuru match the `HUB` array).
- [ ] After 13.1 is live: Android clean reinstall (uninstall all apps, clear site data, install only Life Plan). This is roadmap checkpoint 13.6.
- [ ] Marvin: enable Pages; add `https://marvyeo.github.io/LifePlan/` to Authorized redirect URIs (for iPhone).
- [x] First run 2026-10-21: TV World and MCC Inventory not found (different OAuth projects). Resolution: Pick missing files.

## Change log
- **v1.0 (2026-10-21):** Initial build (Sprint 7).
- **2026-10-21:** ecosystem icon set added (`design/`); VacationGuru glyph changed to a suitcase (the paper plane looked like Telegram).
- **2026-10-22:** manifest id set to `/LifePlan/` (the old `./` made Android treat all apps as one).
- **2026-10-22:** added Session Rules and `CLAUDE.md`. NovelReader's icons were generated from `design/make_icons.py` (glyph already defined) and shipped in its repo.

- **2026-10-23:** Sprint 13.1: hub shell (tile launcher, phone bottom nav, desktop two-pane, safe-area and 44px targets), manifest scope `/`, `sw.js` cache `lifeplan-v5` now also caches `icons/apps/`.

## Ecosystem icon set (2026-10-21)
`design/make_icons.py` generates every app's icon in one style (dark tile, line glyph in the app colour, same stroke and safe zone). `python3 design/make_icons.py out` writes `out/<app>/icon-192.png`, `icon-512.png`, `apple-touch-icon.png` and `out/preview.png`. To add an app: add it to `APPS` (name, colour) and write a `g_<app>` glyph function.
