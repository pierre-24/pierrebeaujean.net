import pathlib
import sass

from static_website.base import File


class ScssStylesheet(File):
    def __init__(self, src: pathlib.Path, dest: pathlib.Path):
        super().__init__(dest)
        self.src = src

    def generate(self):
        if not self.src.is_file():
            raise FileNotFoundError(self.src)

        with self.path.open('w') as f:
            f.write(sass.compile(filename=str(self.src), output_style='compressed'))
