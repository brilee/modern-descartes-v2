import atexit
from collections import namedtuple, defaultdict
import datetime
import os
import subprocess

import feedgenerator
from jinja2 import Environment, FileSystemLoader, select_autoescape
import watchdog
import watchdog.events
import watchdog.observers


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

def is_public_essay(essay_path):
    dirpath, filename = os.path.split(essay_path)
    (essay_shortname, extension) = os.path.splitext(filename)
    if extension not in ALLOWED_EXTENSIONS:
        return False
    if filename[0] == '_':
        return False
    return True


def make_rss(compiled_essays: list[Essay]):

    feed = feedgenerator.Atom1Feed(
        title="Modern Descartes - Essays by Brian Lee",
        link=os.path.join(WEBSITE_URL, ESSAY_WEBDIR),
        description="I seek, therefore I am")
    for essay in compiled_essays[:10]:
        feed.add_item(
            title=essay.title,
            link=os.path.join(WEBSITE_URL, ESSAY_WEBDIR, essay.slug),
            description=compile_html('rss_item.txt', essay=essay),
            pubdate=essay.date)
    with open(os.path.join(STAGING_DIR, ESSAY_WEBDIR, 'rss.xml'), 'w') as f:
        feed.write(f, 'utf-8')


def compile_html(template_name, **context):
    default_context = {"ESSAY_WEBDIR": ESSAY_WEBDIR}
    default_context.update(**context)
    template = JINJA_ENV.get_template(template_name)
    compiled = template.render(**default_context)
    return compiled


def compile_and_write_html(template_name: str, output_file: str, **context):
    compiled = compile_html(template_name, **context)
    output_path = os.path.join(STAGING_DIR, output_file)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
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
        "pandoc -f markdown -t html --mathjax --shift-heading-level-by=1",
        stdout=subprocess.PIPE,
        input=essay_content.encode('utf8'),
        shell=True)
    essay_content = result.stdout.decode('utf8')

    return Essay(slug=essay_shortname, title=essay_longname,
                 date=essay_date, content=essay_content, tags=tags)


def compile_essay(essay_path) -> list[Essay]:
    if not is_public_essay(essay_path):
        return []

    try:
        essay = parse_essay(essay_path)
        compile_and_write_html('essay_detailed.html',
            'essays/{}/index.html'.format(essay.slug), essay=essay)
        return [essay]
    except Exception as e:
        print('Failed to process {}'.format(essay_path))
        print(type(e), e)
    return []


def compile_essays() -> list[Essay]:
    print("Processing essays...")
    all_essays = []
    for dirpath, _, filenames in os.walk(ESSAY_DIR):
        for filename in filenames:
            all_essays.extend(compile_essay(os.path.join(dirpath, filename)))

    print("Compiled {} essays".format(len(all_essays)))
    return all_essays

def compile_all():
    assert STAGING_DIR not in ('/', '.', '..', '')
    subprocess.run('[ -d {} ] && rm -r {}'.format(STAGING_DIR, STAGING_DIR), shell=True, stderr=subprocess.STDOUT)
    compile_and_write_html('404.html', '404.html')
    compile_and_write_html('index.html', 'index.html')
    all_essays = compile_essays()
    essays_sorted = sorted(all_essays, key=lambda e: e.date, reverse=True)
    essays_by_tag = defaultdict(list)
    for essay in essays_sorted:
        for tag in essay.tags:
            essays_by_tag[tag].append(essay)
    compile_and_write_html('essay_index.html', 'essays/index.html',
        essays_sorted=essays_sorted, tags=essays_by_tag)
    for tag, essays_with_tag in essays_by_tag.items():
        compile_and_write_html('essay_tag.html', 'essays/tags/{}/index.html'.format(tag.replace(' ', '_')),
            tag=tag, essays_with_tag=essays_with_tag)
    make_rss(essays_sorted)
    subprocess.run('cp -r -p {static} {staging}/{static}'.format(
        static=STATIC_DIR, staging=STAGING_DIR), shell=True)


class RecompileEssayHandler(watchdog.events.LoggingEventHandler):
    def dispatch(self, event):
        essay_path = os.fsdecode(event.src_path)
        if is_public_essay(essay_path):
            print(f'Recompiling {essay_path}...', end="")
            compile_essay(essay_path)
            print('done.')
        else:
            print(f"Ignoring {essay_path}")


if __name__ == '__main__':
    compile_all()
    webserver = subprocess.Popen(['python', '-m', 'http.server', '8888', '-d', 'staging'])
    atexit.register(webserver.kill)
    event_handler = RecompileEssayHandler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, ESSAY_DIR, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()