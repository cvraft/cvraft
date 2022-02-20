import markdown

from cvraft.extension import CvraftExtension


def test_wrap_sections_1():
    content = """
# Introduction
Some introduction text

And a bit of overview
"""

    html = markdown.markdown(content, extensions=[CvraftExtension()])
    assert (
        html
        == "<div>\n<h1>Introduction</h1>\n<p>Some introduction text</p>\n<p>And a bit of overview</p>\n</div>"
    )


def test_wrap_sections_2():
    content = """
# Heading 1
# Heading 2
Some text come here
"""

    html = markdown.markdown(content, extensions=[CvraftExtension()])
    assert (
        html
        == "<div>\n<h1>Heading 1</h1>\n</div>\n<div>\n<h1>Heading 2</h1>\n<p>Some text come here</p>\n</div>"
    )


def test_multiple_heading_levels():
    content = """
# Heading 1

# Heading 2

##  Heading 2.1

Some text come here
"""

    html = markdown.markdown(content, extensions=[CvraftExtension()])
    assert (
        html
        == "<div>\n<h1>Heading 1</h1>\n</div>\n<div>\n<h1>Heading 2</h1>\n<div>\n<h2>Heading 2.1</h2>\n<p>Some text come here</p>\n</div>\n</div>"
    )
