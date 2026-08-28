# Skola landing (GitHub Pages)

Polish is the default (`/`). English is `/en/`. Code comments and this README are English.

Relative paths only — copy the whole tree to Dan’s server later; EN stays at `en/`.

## Local preview

```bash
cd deploy/skola-pl-rynek
python3 -m http.server 8088
# http://127.0.0.1:8088/      Polish
# http://127.0.0.1:8088/en/   English
```

## Publish

From the physix repo:

```bash
deploy/push-skola-pl.sh
```

Until a custom domain: `https://szpili.github.io/skola-pl/` and `https://szpili.github.io/skola-pl/en/`.

## MySQL (Dan’s cPanel)

Polish school votes: MySQL `szkola_pl` (not Dan’s US `skola`).
API: `https://nerdwar.one/G0/api.php` (`?action=ping` → `{"ok":true}`).
`rate.html` sets `window.SKOLA_API` to that URL. Password lives only in `G0/config.php` on the host.
Schema and PHP: [`server/SETUP.md`](server/SETUP.md).
