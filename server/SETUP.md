# Skola MySQL on Dan’s cPanel (GoDaddy)

Do this on **https://…:2083/** (cPanel), not in phpMyAdmin first.
The long phpMyAdmin URL with `cpsess…` is a login session — it expires. Use **cPanel → phpMyAdmin**.

Dan’s US/university data stays in MySQL **`skola`**. Polish school votes go in **`szkola_pl`**. Polish university (later) is **`uczelnia_pl`**. Do not import this schema into `skola`.

## 1. Create the database

1. cPanel → **MySQL Databases**
2. Create database: `szkola_pl` (ASCII, no ł)
3. Create a user with the same name, strong password, **copy it now**
4. **Add User To Database** → ALL PRIVILEGES on `szkola_pl` only
5. Leave `qadmin` / `quser` on `skola` alone

## 2. Import the schema

1. cPanel → **phpMyAdmin** → click **`szkola_pl`** (not `skola`)
2. **Import** → `schema.sql` (this folder)

## 3. Put PHP on the website (not in the panel)

cPanel → **File Manager** → `public_html/G0/` (Dan’s folder for Karol). Do **not** replace `index.html` (Ground Zero). Upload:

- `api.php`
- `config.php` (copy of `config.example.php`, fill in the four values)
- leave `config.example.php` out if you want

`config.php` must not be world-readable if the host allows tightening permissions (0640).

## 4. What Karol needs back

Not the cPanel URL. The **https website URL** where `api.php` answers, e.g.

```
https://nerdwar.one/G0/api.php?action=ping
```

should return `{"ok":true}`. Then the rating page can POST votes there.

Password stays on the server. Do not paste it into chat.
