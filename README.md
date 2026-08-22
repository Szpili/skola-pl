# Polish-market Skola (GitHub Pages)

Visitor-facing site is Polish. Code comments and this README are English.

## Local preview

```bash
cd deploy/skola-pl-rynek
python3 -m http.server 8088
# open http://127.0.0.1:8088/
```

## Publish

From the physix repo:

```bash
deploy/push-skola-pl.sh
```

That creates (if needed) a public GitHub repo, pushes `main`, and turns on Pages from `main` at `/`. No custom domain until you add a `CNAME` file and DNS.

Until then the URL is `https://<github-user>.github.io/<repo>/`.
