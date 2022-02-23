import typer
import markdown
import frontmatter
import http.server
import socketserver

from functools import partial
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from bs4 import BeautifulSoup
from distutils.dir_util import copy_tree


BUILD_DIR = "build"
STATIC_DIR = "static"

app = typer.Typer(help="Build beautiful CV from Markdown file")

env = Environment(
    loader=PackageLoader("cvraft", "templates"),
    autoescape=select_autoescape(),
)


@app.command()
def build(file_path: Path, static_path: Path = typer.Option(None), prettify: bool = typer.Option(default=False)):
    typer.echo(f"Building your CV from {file_path.absolute()}")
    cv = frontmatter.load(file_path.absolute())
    template = env.get_template("cv.html")
    md = markdown.markdown(cv.content, extensions=["attr_list", 'tables', 'cvraft.extension'])
    # Create build directory
    build_dir = Path(".") / BUILD_DIR
    build_dir.mkdir(exist_ok=True)
    # Output HTML from Markdown
    with open(build_dir / "index.html", "w") as f:
        html = template.render(content=md, **cv)
        if prettify:
            html = BeautifulSoup(html, 'html.parser').prettify(formatter='html5')
        f.write(html)
    # Copy static resources
    static_path = file_path.parent / STATIC_DIR
    if static_path.exists():
        copy_tree(str(static_path), str(build_dir / STATIC_DIR))


@app.command()
def serve():
    PORT = 9000
    directory = Path(".") / BUILD_DIR
    Handler = partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


if __name__ == "__main__":
    app()
