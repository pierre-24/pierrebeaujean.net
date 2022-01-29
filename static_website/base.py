import pathlib
import shutil
from typing import List

import jinja2
import yaml
import markdown


class File:
    """A file that will be generated"""

    def __init__(self, path: pathlib.Path):
        self.path = path

    def generate(self):
        raise NotImplementedError()


class Directory(File):
    """A directory"""

    def generate(self):
        self.path.mkdir()


class Asset(File):
    """Asset, copied directly
    """

    def __init__(self, source: pathlib.Path, dest: pathlib.Path):
        self.source = source

        super().__init__(dest)

    def generate(self):
        shutil.copy(self.source, self.path)


class NoJekyll(File):
    def __init__(self, build_dir: pathlib.Path = '.'):

        super().__init__(build_dir / '.nojekyll')

    def generate(self):
        dest = self.path
        dest.touch()


class ContextGenerator:

    def __call__(self) -> dict:
        raise NotImplementedError()


class RawContext(ContextGenerator):
    def __init__(self, context: dict):
        self.context = context

    def __call__(self) -> dict:
        return self.context


class YamlContext(ContextGenerator):
    def __init__(self, path: pathlib.Path):
        self.path = path

    def __call__(self) -> dict:
        if not self.path.is_file():
            raise FileNotFoundError(self.path)

        with self.path.open() as f:
            return yaml.load(f, Loader=yaml.Loader)


class MarkdownContext(ContextGenerator):
    def __init__(self, var: str, path: pathlib.Path):
        self.path = path
        self.var = var

    def __call__(self) -> dict:
        if not self.path.is_file():
            raise FileNotFoundError(self.path)

        with self.path.open() as f:
            return {self.var: markdown.markdown(f.read())}


class TemplateFile(File):
    """Given the appropriate context, render the template"""

    def __init__(
            self,
            template: str,
            context: List[ContextGenerator],
            env: jinja2.Environment,
            dest: pathlib.Path):

        super().__init__(dest)
        self.template = template
        self.context = context
        self.env = env

    def generate(self):
        # open template
        t = self.env.get_template(self.template)

        # generate context
        context = {}
        for c in self.context:
            context.update(**c())

        # write up
        with self.path.open('w') as f:
            f.write(t.render(**context))
