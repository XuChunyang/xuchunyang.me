import glob
import re
import subprocess

import jinja2
import mistune
import yaml


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    autoescape=True,
)
template = env.get_template('base.html')


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
    html_file = re.sub('\.md$', '.html', markdown_file)
    with open(markdown_file) as in_file, open(html_file, 'w') as out_file:
        text = in_file.read()
        if text.startswith('---'):
            end = text.find('---', 3)
            yaml_text = text[3:end]
            d = yaml.load(yaml_text, yaml.Loader)
            title = d['title']
            markdown = text[end+3:]
            content = mistune.markdown(markdown, renderer=HighlightRenderer())
            html = template.render(content=content, title=title)
            out_file.write(html)
        else:
            raise Exception('The Markdown file lacks a yaml header')


if __name__ == '__main__':
    mds = ['index.md'] + glob.glob('blog/*.md')
    for md in mds:
        print(f'Processing {md}...')
        md2html(md)
