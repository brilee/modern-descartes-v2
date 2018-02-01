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