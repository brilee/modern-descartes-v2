## Essays / static content on [www.moderndescartes.com](https://www.moderndescartes.com)

This is a static site generator that compiles a set of markdown files, generates HTML, and then uses firebase to serve content.

# Instructions to myself
```
python3 -m venv .
source bin/activate
pip install -r requirements.txt
```

[Install pandoc](https://pandoc.org/installing.html)

# How to compile/deploy
```
python3 make.py
firebase deploy
```

If you change anything about the compilation step, do a manual check over essays exercising various features - in particular:
    - fractal plants (javascript embedded snippets)
    - probability manipulations (heavy TeX)
    - hyperloglog (code blocks)
    - bitpacking compression (tables)
    - convnet edge detection (images)
