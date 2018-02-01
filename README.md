## Essays / static content on [moderndescartes.com](moderndescartes.com)

This is a static site generator that compiles a set of markdown files, generates HTML, and then pushes HTML/CSS/JS to a Google Cloud Storage bucket for serving. Configuration can be found in `config`

# Getting started
```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

# How to compile/deploy
python3 make.py
./push

# Not implemented yet:

- figure out how GCS does index.html
- figure out how to make GCS insensitive to trailing slash
- figure out how to develop locally
- figure out how to generate rss.xml
- manual testing: do a careful check over weird essays - in particular,
    - fractal plants (javascript embedded snippets)
    - 2n choose n (heavy TeX)
    - hyperloglog (code blocks)
    - bitpacking compression (tables)
    - convnet edge detection (images)
