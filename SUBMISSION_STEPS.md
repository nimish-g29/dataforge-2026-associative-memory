# Exactly what to do to submit

I can't create a GitHub account, push to a remote repo, or host a public URL on your behalf — those
need your credentials. Everything below is copy-paste-ready; it should take about 10 minutes.

## 1. Create the public repository

1. Go to https://github.com/new
2. Repository name: e.g. `dataforge-2026-associative-memory` (anything descriptive)
3. Set visibility to **Public** (required by the checklist)
4. Do **not** initialize with a README (you already have one) — leave it empty
5. Click **Create repository** and copy the URL it gives you, e.g.
   `https://github.com/YOUR-USERNAME/dataforge-2026-associative-memory.git`

## 2. Push these files

From the folder containing `index.html`, `README.md`, `dataforge-concept-summary.pdf`, and
`make_summary.py`:

```bash
cd path/to/this/folder
git init
git add .
git commit -m "DataForge 2026: associative memory / synaptic plasticity explainer"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/dataforge-2026-associative-memory.git
git push -u origin main
```

## 3. Turn on GitHub Pages (this gives you the public artifact URL)

1. In your repo on GitHub: **Settings → Pages**
2. Under "Build and deployment", set **Source** to `Deploy from a branch`
3. Branch: `main`, folder: `/ (root)` → **Save**
4. Wait ~1 minute, then refresh the page — GitHub shows your live URL, something like:
   `https://YOUR-USERNAME.github.io/dataforge-2026-associative-memory/`
5. Open it in an incognito/private window to confirm it loads **without sign-in** — this is a hard
   requirement.
6. Visit `.../index.html` and `.../dataforge-concept-summary.pdf` specifically and confirm both load.

## 4. Fill in the placeholders

Three files still have `PASTE-...-HERE` or `[YOUR NAME]` placeholders on purpose — search for them:

```bash
grep -rn "PASTE-\|YOUR-USERNAME\|YOUR NAME\|CHOOSE A LICENSE" .
```

Fill in:
- `README.md` — live artifact URL, repo URL, your name, your chosen license (MIT is a safe default for
  code; CC BY 4.0 is a safe default for the written content)
- `index.html` — the nav bar's "GitHub Repo" link currently does nothing (`href="#" onclick="return false;"`).
  Replace it with your real repo URL:
  ```html
  <a class="navpill" href="https://github.com/YOUR-USERNAME/dataforge-2026-associative-memory" target="_blank" rel="noopener">🔗 GitHub Repo</a>
  ```
- `README.md` §10 — replace the AI-disclosure placeholder paragraph with your own words. This matters:
  judges score whether *you* can defend the submission live, and a disclosure that reads as AI-written
  about AI assistance works against you. Write it yourself, in your own voice.

Commit and push the changes:
```bash
git add .
git commit -m "Fill in submission placeholders"
git push
```

## 5. Before you actually submit, verify

- [ ] Public artifact URL opens in an incognito window with no sign-in
- [ ] Repo is public (check by opening its URL logged out)
- [ ] `dataforge-concept-summary.pdf` opens from the live URL
- [ ] README renders correctly on the GitHub repo page (GitHub auto-renders `README.md`)
- [ ] Every `PASTE-`/`[YOUR NAME]`/`[CHOOSE A LICENSE]` placeholder is replaced
- [ ] You can, without notes, explain: the write/read rule, why interference is gradual not sudden, what
  changes when you move each slider, and where the Hebbian rule appears in BDH vs. this toy — a judge can
  and will ask you to trace this live
