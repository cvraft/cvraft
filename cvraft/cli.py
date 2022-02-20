import typer
import markdown
import frontmatter
import http.server
import socketserver

from functools import partial
from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape
from bs4 import BeautifulSoup

from .extension import CvraftExtension


BUILD_DIR = "build"

app = typer.Typer(help="Build beautiful CV from Markdown file")

env = Environment(
    loader=PackageLoader("cvraft", "templates"),
    autoescape=select_autoescape(),
)


@app.command()
def build(file_path: Path, prettify: bool = typer.Option(default=False)):
    typer.echo(f"Building your CV from {file_path.absolute()}")
    cv = frontmatter.load(file_path.absolute())
    template = env.get_template("cv.html")
    md = markdown.markdown(cv.content, extensions=["attr_list", CvraftExtension()])
    # Create build directory
    build_dir = Path(".") / BUILD_DIR
    build_dir.mkdir(exist_ok=True)
    with open(build_dir / "index.html", "w") as f:
        html = template.render(content=md, name=cv["name"]) 
        if prettify:
            html = BeautifulSoup(html, 'html.parser').prettify(formatter='html5')
        f.write(html)


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
