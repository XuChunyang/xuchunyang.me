import glob
import re
import os
import subprocess
import collections
from datetime import datetime

import jinja2
import mistune
import yaml


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    autoescape=True,
)
template = env.get_template('post.html')


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang=None):
        if lang:
            cmd = f'emacs -Q --batch -l colorize.el --lang {lang}'
            output = subprocess.check_output(cmd.split(), input=code.encode())
            output = output.decode()
            return f'\n{output}\n'
        else:
            return f'\n<pre>{mistune.escape(code)}</pre>\n'


def md2html(markdown_file):
    html_file = re.sub('\.md$', '/index.html', markdown_file)
    _dir = os.path.dirname(html_file)
    if not os.path.exists(_dir):
        os.mkdir(_dir)
    with open(markdown_file) as in_file, open(html_file, 'w') as out_file:
        text = in_file.read()
        if text.startswith('---'):
            end = text.find('---', 3)
            yaml_text = text[3:end]
            d = yaml.load(yaml_text, yaml.Loader)
            title = d['title']
            created = d['created']
            markdown = text[end+3:]
            content = mistune.markdown(markdown, renderer=HighlightRenderer())
            html = template.render(content=content, title=title, created=created)
            out_file.write(html)
        else:
            raise Exception('The Markdown file lacks a yaml header')

def index():
    markdown_file = 'index.md'
    html_file = 'index.html'
    with open(markdown_file) as in_file, open(html_file, 'w') as out_file:
        text = in_file.read()
        if text.startswith('---'):
            end = text.find('---', 3)
            yaml_text = text[3:end]
            d = yaml.load(yaml_text, yaml.Loader)
            title = d['title']
            markdown = text[end+3:]
            content = mistune.markdown(markdown, renderer=HighlightRenderer())
            template = env.get_template('index.html')
            html = template.render(content=content, title=title, posts=get_posts())
            out_file.write(html)
        else:
            raise Exception('The Markdown file lacks a yaml header')

Post = collections.namedtuple('Post', 'title url created updated')

def get_posts():
    posts = []
    for md in glob.glob('blog/*.md'):
        url = '/' + re.sub('\.md$', '/', md)
        with open(md) as f:
            text = f.read()
            end = text.find('---', 3)
            yaml_text = text[3:end]
            d = yaml.load(yaml_text, yaml.Loader)
            title = d['title']
            created = d['created']
            updated = d.get('updated')
        posts.append(Post(title, url, created, updated))
    return posts

if __name__ == '__main__':
    print('Processing index.md ...')
    index()
    for md in glob.glob('blog/*.md'):
        print(f'Processing {md} ...')
        md2html(md)
