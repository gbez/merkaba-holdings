# Merkaba Holdings Website

A simple, one-page static website for Merkaba Holdings LLC, written in plain HTML, CSS, and JavaScript. It needs no build tools or frameworks.

## Files

```
index.html        All of the page content (text, sections, contact info)
css/styles.css    All of the styling. Colors and fonts are set at the top.
js/main.js        Mobile menu and the footer year
images/           Logo, photos, and other images
.nojekyll         Tells GitHub Pages to serve the files as-is
```

## Previewing locally

Double-click `index.html` to open it in your browser. After you edit a file, save it and refresh the browser.

## Filling in your details

Anything in **[square brackets]** in `index.html` is a placeholder to replace. To find them all, search the file for `[` in your editor. The main ones are:

- **About Me:** your name, background, location, and education
- **Criteria:** revenue and EBITDA ranges, location, and industries
- **For Brokers:** your response time
- **Contact:** email, phone, and LinkedIn URL

For the phone link, write the number with digits only: `href="tel:+12025551234"`.

## Adding your photo

1. Put your photo in the `images` folder, for example `images/headshot.jpg`. A portrait (taller than wide) looks best.
2. In `index.html`, find `headshot-placeholder.svg` and change it to `headshot.jpg`.

## Changing colors or fonts

Open `css/styles.css`. The `:root` block at the top holds every color and font the site uses. Change a value there and it updates across the whole site.

## Using the Clarendon font for every visitor

The site's `--font-heading` and `--font-body` variables are already set to use **Clarendon**. No browser or operating system ships the real Clarendon, so until you self-host it (below), every visitor sees a fallback slab serif instead — on a Mac or iPhone that fallback is Apple's own "Superclarendon" (a close visual match, no license needed), and everywhere else it falls back further to Georgia.

Clarendon is a commercial typeface (owned by Monotype), not a free Google Font, so it can't be linked from a free CDN the way the previous fonts were. To make it render for every visitor, you need to license it and self-host the files. Two ways to do that:

**Option A: Buy desktop/web-embedding font files and self-host them**

1. Buy a license that includes web-embedding rights, for example from [fonts.com](https://www.fonts.com) or [MyFonts](https://www.myfonts.com) (search "Clarendon" — Monotype's own release is called "Clarendon LT Std" or "Clarendon URW"). Make sure the license covers web use, not just desktop/print.
2. Download the `.woff2` and `.woff` files for at least the Regular and Bold weights (some vendors generate these for you; others sell only `.otf`/`.ttf`, which you can convert at [transfonter.org](https://transfonter.org)).
3. Create a `fonts` folder in this project (next to `css`, `images`, `js`) and place the files there, named:
   ```
   fonts/Clarendon-Regular.woff2
   fonts/Clarendon-Regular.woff
   fonts/Clarendon-Bold.woff2
   fonts/Clarendon-Bold.woff
   ```
4. Open `css/styles.css` and find the commented-out `@font-face` block near the top (right above the `:root` block). Delete the `/*` and `*/` around it to enable it.
5. Save, refresh the browser, and Clarendon will now load for all visitors, with the system font as an instant fallback while it downloads.

**Option B: Use Adobe Fonts (no file management)**

1. If you or your organization has a Creative Cloud subscription, go to [fonts.adobe.com](https://fonts.adobe.com) and search "Clarendon URW" (Adobe's licensed web version of Clarendon).
2. Add it to a web project and copy the `<link>` snippet Adobe gives you (it looks like `<link rel="stylesheet" href="https://use.typekit.net/xxxxxxx.css">`).
3. Paste that `<link>` into `index.html`, right above `<link rel="stylesheet" href="css/styles.css">`.
4. In `css/styles.css`, change `--font-heading` and `--font-body` to start with the exact family name Adobe shows on the font's page (usually `"clarendon-urw"`), keeping the rest of the fallback list as-is.

Either option is a one-time setup; the site's CSS is already pointed at `"Clarendon"` and needs no other changes once the font is available.

## Editing common things

- **Add an FAQ:** copy one `<details>...</details>` block in the FAQ section and change the text.
- **Add an industry:** add a line like `<li>New Industry</li>` in the `tag-list`.
- **Remove a section:** delete everything from its opening `<section>` tag to its closing `</section>` tag, and remove its link from the `<nav>`.

## Publishing on GitHub Pages

1. Create a new repository on GitHub, for example `merkaba-holdings`.
2. Upload all the files in this folder, keeping the same folder structure, either through the GitHub website or with git:
   ```
   git init
   git add .
   git commit -m "Initial website"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/merkaba-holdings.git
   git push -u origin main
   ```
3. On GitHub, go to **Settings → Pages**. Under "Build and deployment", pick **Deploy from a branch**, then choose `main` and `/ (root)`, and click Save.
4. After a minute or two, your site will be live at `https://YOUR-USERNAME.github.io/merkaba-holdings/`.

**Custom domain (optional):** If you buy a domain like `merkabaholdings.com`, enter it under **Settings → Pages → Custom domain**, then follow GitHub's instructions for updating your domain's DNS records.
