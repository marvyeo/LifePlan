# Life Plan Dashboard — Project State

**State version:** 1 (built 2026-10-21 by the conductor chat "Life Plan Roadmap ver 2", Sprint 7)
**Next chat name:** `Life Plan Dashboard ver 2`
**Maintenance rule:** When ported to a new chat, name it "Life Plan Dashboard ver X". Update this file in the same commit as any change. `git pull` before working.

| Item | Value |
|---|---|
| Repo | `marvyeo/LifePlan` (public) |
| Live URL | https://marvyeo.github.io/LifePlan/ (demo data: `?demo`) |
| Stack | `index.html` (vanilla JS, own CSS), `sw.js` (network-first, `lifeplan-v1`), `manifest.json`, `icons/` |
| Auth | Shared OAuth client `669494100250-…`. Scope `drive.file` first; "Grant read-only access" switches to `drive.readonly`. Redirect sign-in fallback for iPhone home-screen use (needs the URL in Authorized redirect URIs). |
| Writes | **Nothing.** Read-only by design. |

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
- [ ] Marvin: enable Pages; add `https://marvyeo.github.io/LifePlan/` to Authorized redirect URIs (for iPhone).
- [x] First run 2026-10-21: TV World and MCC Inventory not found (different OAuth projects). Resolution: Pick missing files.

## Change log
- **v1.0 (2026-10-21):** Initial build (Sprint 7).

## Ecosystem icon set (2026-10-21)
`design/make_icons.py` generates every app's icon in one style (dark tile, line glyph in the app colour, same stroke and safe zone). `python3 design/make_icons.py out` writes `out/<app>/icon-192.png`, `icon-512.png`, `apple-touch-icon.png` and `out/preview.png`. To add an app: add it to `APPS` (name, colour) and write a `g_<app>` glyph function.
