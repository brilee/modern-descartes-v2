from collections import namedtuple, defaultdict
import datetime
import os
import subprocess

from jinja2 import  Environment, FileSystemLoader, select_autoescape
import mistune


ESSAY_DIR = "essays"
STATIC_DIR = "static"
STAGING_DIR = "staging"
TEMPLATE_DIR = "templates"

ALLOWED_EXTENSIONS = ('.md', '.txt', '.html')
MARKDOWN_EXTENSIONS = ('.md', '.txt')

BASIC_PAGES = (
    '404.html',
    'index.html',
)

JINJA_ENV = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml']))

compile_markdown = mistune.Markdown()

Essay = namedtuple('Essay', ['slug', 'title', 'date', 'content', 'category'])

def make_rss(compiled_essays):
    pass

def compile_html(template_name, output_file, **context):
    output_path = os.path.join(STAGING_DIR, output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    template = JINJA_ENV.get_template(template_name)
    compiled = template.render(**context)
    with open(output_path, 'w') as f:
        f.write(compiled)

def compile_essays():
    print("Processing essays...")
    all_essays = []
    category_names = os.listdir(ESSAY_DIR)
    for category in category_names:
        category_dir = os.path.join(ESSAY_DIR, category)
        if not os.path.isdir(category_dir):
            continue
        for essay in os.listdir(category_dir):
            (essay_shortname, extension) = os.path.splitext(essay)
            if not extension in ALLOWED_EXTENSIONS:
                continue

            with open(os.path.join(category_dir, essay), 'r') as f:
                essay_longname = f.readline().rstrip('\n')
                year, month, day = f.readline().rstrip('\n').split('/')
                essay_date = datetime.date(year=int(year), month=int(month),
                    day=int(day))
                essay_content = f.read()

            if extension in MARKDOWN_EXTENSIONS:
                essay_content = compile_markdown(essay_content)

            essay = Essay(slug=essay_shortname, title=essay_longname,
                date=essay_date, content=essay_content, category=category)
            all_essays.append(essay)

            compile_html('essay_detailed.html', 
                'essays/{}'.format(essay.slug), essay=essay)
    print("Compiled {} essays".format(len(all_essays)))
    return all_essays

def compile_all():
    assert STAGING_DIR not in ('/', '.', '..')
    subprocess.check_call('rm -r {}'.format(STAGING_DIR), shell=True)
    compile_html('404.html', '404.html')
    compile_html('index.html', 'index.html')
    all_essays = compile_essays()
    essays_sorted = sorted(all_essays, key=lambda e: e.date, reverse=True)
    essays_by_category = defaultdict(list)
    for essay in essays_sorted:
        essays_by_category[essay.category].append(essay)
    compile_html('essay_index.html', 'essays/index.html',
        essays_sorted=essays_sorted, essays_by_category=essays_by_category)
    make_rss(essays_sorted)
    subprocess.check_call('cp -r {static} {staging}/{static}'.format(
        static=STATIC_DIR, staging=STAGING_DIR), shell=True)

if __name__ == '__main__':
    compile_all()