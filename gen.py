import pathlib
import shutil
from datetime import datetime

import jinja2
import markdown

from static_website import base, custom


def markdown_filter(txt) -> str:
    return markdown.markdown(txt)


def main():
    # JINJA context:
    template_loader = jinja2.FileSystemLoader(searchpath='./templates')
    env = jinja2.Environment(loader=template_loader)
    env.filters['markdown'] = markdown_filter

    # build dir
    build_dir = pathlib.Path('build')
    if build_dir.exists():
        shutil.rmtree(build_dir)

    build_dir.mkdir()

    # common context
    common_context = base.YamlContext(pathlib.Path('./src/common_context.yml'))

    # index
    base.TemplateFile('index.html', [
        common_context,
        # build context
        base.RawContext({
            'build_context': datetime.now().strftime('This page was generated on %B %d, %Y'),
            'lang': 'en'
        }),
        # specific context
        base.MarkdownContext('introduction', pathlib.Path('src/en/introduction.md')),
        base.MarkdownContext('employment', pathlib.Path('src/en/employment.md')),
        base.YamlContext(pathlib.Path('./src/publications.yml')),
        base.YamlContext(pathlib.Path('./src/en/skills.yml')),
        base.MarkdownContext('interests', pathlib.Path('src/en/interests.md')),
        base.YamlContext(pathlib.Path('./src/en/pathway.yml')),
        base.MarkdownContext('footer', pathlib.Path('src/en/footer.md'))
    ], env, build_dir / 'index.html').generate()

    # french
    base.TemplateFile('fr.html', [
        common_context,
        # build context
        base.RawContext({
            'build_context': datetime.now().strftime('Page générée le %d/%m/%Y'),
            'lang': 'fr'
        }),
        # specific context
        base.MarkdownContext('introduction', pathlib.Path('src/fr/introduction.md')),
        base.MarkdownContext('employment', pathlib.Path('src/fr/employment.md')),
        base.YamlContext(pathlib.Path('./src/publications.yml')),
        base.MarkdownContext('mediation', pathlib.Path('src/fr/mediation.md')),
        base.YamlContext(pathlib.Path('./src/fr/zds.yml')),
        base.YamlContext(pathlib.Path('./src/fr/skills.yml')),
        base.MarkdownContext('interests', pathlib.Path('src/fr/interests.md')),
        base.YamlContext(pathlib.Path('./src/fr/pathway.yml')),
        base.MarkdownContext('footer', pathlib.Path('src/fr/footer.md'))
    ], env, build_dir / 'fr.html').generate()

    # assets
    base.Asset(pathlib.Path('./src/assets/me.jpg'), build_dir / 'me.jpg').generate()
    custom.ScssStylesheet(pathlib.Path('src/assets/style.scss'), build_dir / 'style.css').generate()
    base.Asset(pathlib.Path('./src/assets/favicon.svg'), build_dir / 'favicon.svg').generate()

    # GH pages
    base.NoJekyll(build_dir).generate()
    base.Asset(pathlib.Path('./src/assets/CNAME'), build_dir / 'CNAME').generate()


if __name__ == '__main__':
    main()
