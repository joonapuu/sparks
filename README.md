# Sparks — card webapp

A mobile-first webapp that shows cards from 14 categories (~60 each, 839 cards total). Pick a category, then tap through cards in random order.

## Files

- `sparks.html` — the entire app in one self-contained file (HTML + CSS + JS + all 839 cards + the app icon inlined as a data URI). This is the only file you need to run or deploy.
- `cards.js` — the same card data as a standalone JS file, for reference/editing.
- `raw_notes.txt` — the original raw text from your Apple Notes, preserved as a backup.
- `parse.py` — regenerates `cards.js` **and** re-inlines the data into `sparks.html`. Run `python3 parse.py` after editing the raw notes.
- `icon.png` / `icon-180.png` — the Sparks app icon (1024×1024 master and 180×180 for iOS home screen). Already inlined inside `sparks.html` as a data URI, so they're only needed if you deploy the whole folder or want to edit the art.
- `make_icon.py` — regenerates the icons. Edit the colors in the script, run `python3 make_icon.py`, and it will also auto-re-inline `icon-180.png` as the apple-touch-icon data URI inside `sparks.html`.

Everything you need to deploy is just `sparks.html` on its own — it has no external dependencies.

## Run it locally first

Double-click `sparks.html` to open in Safari or Chrome — the app runs locally with no server needed. Once you're happy, deploy to the web using one of the options below.

## Deploy — Option A: Netlify (easiest, recommended)

1. Go to https://app.netlify.com/drop
2. Drag **just `sparks.html`** onto the drop zone (or the whole folder — either works).
3. Netlify gives you a URL like `https://quirky-name-12345.netlify.app`. Done.
4. (Optional) Sign in to rename the site or attach a custom domain.

No git, no terminal — this is the fastest path to a live URL.

## Deploy — Option B: GitHub Pages

1. Create a new public GitHub repo (e.g., `sparks-cards`).
2. Upload `sparks.html` to the root of the repo (use the GitHub web UI: "Add file → Upload files").
3. In the repo, go to **Settings → Pages**.
4. Under "Build and deployment", set **Source** to "Deploy from a branch", then select `main` / `(root)` and Save.
5. Wait ~30 seconds. Your site will be live at `https://<your-username>.github.io/sparks-cards/`.

## Add to your iPhone home screen

Once you have a URL:

1. Open the URL in Safari on your iPhone.
2. Tap the Share button (the square with an arrow pointing up).
3. Scroll down and tap **Add to Home Screen**.
4. Name it "Sparks" and tap Add.

You now have an app icon that opens fullscreen with no Safari chrome — it behaves like a native app.

## How it works

- **Picker screen**: a grid of 14 colored tiles, one per category. Each tile shows its card count.
- **Card screen**: full-bleed in the category's color. Tap anywhere (except the back button or progress indicator) to advance to the next card. Progress is shown in the top-right as `12 / 60`.
- **Finish screen**: when you've seen every card in the current shuffle, you get a "Shuffle again" button or can pick a different category.
- Cards are reshuffled each time you enter a category or tap "Shuffle again" (Fisher-Yates shuffle).

Keyboard shortcuts (for desktop previewing): Space / → / Enter to advance, Esc to go back.

## Editing cards

If you want to add, remove, or edit cards, the easiest path is:

1. Open `raw_notes.txt` in any text editor.
2. Keep the `=== CATEGORY: Name ===` delimiters and the "Question?\nDescription" format (blank line between cards).
3. Save.
4. In the `sparks-cards` folder, run: `python3 parse.py`
5. This rewrites `cards.js`. Redeploy (drag to Netlify again, or push to GitHub).

Alternatively, you can edit `cards.js` directly — it's just JSON inside a variable assignment.

## Customizing the colors

Open `sparks.html`, search for `const THEMES = {`, and change any hex color. Redeploy.
