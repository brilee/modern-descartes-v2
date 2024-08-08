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
firebase logout && firebase login
firebase deploy
```

# Analytics

[goatcounter](https://moderndescartes.goatcounter.com/)

If you change anything about the compilation step, do a manual check over essays exercising various features - in particular:

    - why did/does brain exist (links) 
    - fractal plants (javascript embedded snippets)
    - probability manipulations (heavy TeX)
    - mcts deep dive (code blocks)
    - bitpacking compression, factobattery (tables)
    - convnet edge detection (images)
