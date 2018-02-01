## Essays / static content on [moderndescartes.com](moderndescartes.com)

This is a static site generator that compiles a set of markdown files, generates HTML, and then pushes HTML/CSS/JS to a Google Cloud Storage bucket for serving. Configuration can be found in `config`

# Getting started
```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

Then, read docs at [https://cloud.google.com/storage/docs/hosting-static-website](https://cloud.google.com/storage/docs/hosting-static-website). In particular, you'll want to

- make a bucket with the name of your website. (and update config with the website URL)
- set DNS to point at `c.storage.googleapis.com.` with a CNAME (trailing dot not a typo). (Note: CNAME does not support the root domain (domain.com), but only subdomain.domain.com. You'll want to set an A record to forward domain.com to subdomain.domain.com)


# How to compile/deploy
python3 make.py
./push

# Not implemented yet:

- figure out how to develop locally
- figure out how to generate rss.xml
- manual testing: do a careful check over weird essays - in particular,
    - fractal plants (javascript embedded snippets)
    - 2n choose n (heavy TeX)
    - hyperloglog (code blocks)
    - bitpacking compression (tables)
    - convnet edge detection (images)
