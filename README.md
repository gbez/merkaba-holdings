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
