from collections import namedtuple, defaultdict
import datetime
import os
import subprocess
import sys

import feedgenerator
from jinja2 import Environment, FileSystemLoader, select_autoescape


WEBSITE_URL = 'https://www.moderndescartes.com'
# Where to look for various files
ESSAY_DIR = "essays"
STATIC_DIR = "static"
STAGING_DIR = "staging"
TEMPLATE_DIR = "templates"

ESSAY_WEBDIR = "essays"

ALLOWED_EXTENSIONS = ('.md', '.txt', '.html')

BASIC_PAGES = (
    '404.html',
    'index.html',
)

JINJA_ENV = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml']))

Essay = namedtuple('Essay', ['slug', 'title', 'date', 'content', 'tags'])

def make_rss(compiled_essays):

    feed = feedgenerator.Atom1Feed(
        title="Modern Descartes - Essays by Brian Lee",
        link=os.path.join(WEBSITE_URL, ESSAY_WEBDIR),
        description="I seek, therefore I am")
    for essay in compiled_essays[:10]:
        feed.add_item(
            title=essay.title,
            link=os.path.join(WEBSITE_URL, ESSAY_WEBDIR, essay.slug),
            description=essay.content,
            pubdate=essay.date)
    with open(os.path.join(STAGING_DIR, ESSAY_WEBDIR, 'rss.xml'), 'w') as f:
        feed.write(f, 'utf-8')

def compile_html(template_name, output_file, **context):
    default_context = {"ESSAY_WEBDIR": ESSAY_WEBDIR}
    default_context.update(**context)
    output_path = os.path.join(STAGING_DIR, output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    template = JINJA_ENV.get_template(template_name)
    compiled = template.render(**default_context)
    with open(output_path, 'w') as f:
        f.write(compiled)

def parse_essay(essay_path):
    essay_shortname = os.path.splitext(os.path.basename(essay_path))[0]
    with open(essay_path, 'r') as f:
        essay_longname = f.readline().rstrip('\n')
        year, month, day = f.readline().rstrip('\n').split('/')
        tags = list(filter(bool, f.readline().rstrip('\n').split(',')))
        essay_date = datetime.date(year=int(year), month=int(month),
            day=int(day))
        essay_content = f.read()
    result = subprocess.run(
        "pandoc -f markdown -t html --mathjax",
        stdout=subprocess.PIPE,
        input=essay_content.encode('utf8'),
        shell=True)
    essay_content = result.stdout.decode('utf8')

    return Essay(slug=essay_shortname, title=essay_longname,
                 date=essay_date, content=essay_content, tags=tags)


def compile_essays():
    print("Processing essays...")
    all_essays = []
    for dirpath, _, filenames in os.walk(ESSAY_DIR):
        for filename in filenames:
            (essay_shortname, extension) = os.path.splitext(filename)
            essay_path = os.path.join(dirpath, filename)
            if extension not in ALLOWED_EXTENSIONS:
                continue
            if filename[0] == '_':
                continue
            try:
                essay = parse_essay(essay_path)
                all_essays.append(essay)
                compile_html('essay_detailed.html',
                    'essays/{}/index.html'.format(essay.slug), essay=essay)
            except Exception as e:
                print('Failed to process {}'.format(filename))
                print(type(e), e)

    print("Compiled {} essays".format(len(all_essays)))
    return all_essays

def compile_all(local=False):
    assert STAGING_DIR not in ('/', '.', '..', '')
    subprocess.check_call('rm -r {}'.format(STAGING_DIR), shell=True)
    compile_html('404.html', '404.html')
    compile_html('index.html', 'index.html')
    all_essays = compile_essays()
    essays_sorted = sorted(all_essays, key=lambda e: e.date, reverse=True)
    essays_by_tag = defaultdict(list)
    for essay in essays_sorted:
        for tag in essay.tags:
            essays_by_tag[tag].append(essay)
    compile_html('essay_index.html', 'essays/index.html',
        essays_sorted=essays_sorted, tags=essays_by_tag)
    for tag, essays_with_tag in essays_by_tag.items():
        compile_html('essay_tag.html', 'essays/tags/{}/index.html'.format(tag),
            tag=tag, essays_with_tag=essays_with_tag)
    make_rss(essays_sorted)
    subprocess.check_call('cp -r -p {static} {staging}/{static}'.format(
        static=STATIC_DIR, staging=STAGING_DIR), shell=True)
    if local:
        abs_dir = os.path.join(os.path.abspath('.'), STAGING_DIR)
        subprocess.check_call(['find', abs_dir,
            '-type', 'f', '-name', '*.html', '-exec',
            'sed', '-i', '', 's|href="/|href="{}/|g'.format(abs_dir), '{}', '+'])
        subprocess.check_call(['find', abs_dir,
            '-type', 'f', '-name', '*.html', '-exec',
            'sed', '-i', '', 's|src="/|src="{}/|g'.format(abs_dir), '{}', '+'])

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'local':
        compile_all(local=True)
        subprocess.call(['open', 'staging/index.html'])
    elif len(sys.argv) == 1:
        compile_all()
    else:
        print("Usage: python {} [local]".format(sys.argv[0]))
