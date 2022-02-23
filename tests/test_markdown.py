import markdown
import pytest

from cvraft.extension import CvraftExtension


@pytest.mark.parametrize("case", ['single-header', 'multiple-headers', 'multi-level-headers'])
def test_each_header_generates_a_wrapping_section(input_md, expected_html):
    html = markdown.markdown(input_md, extensions=[CvraftExtension()])
    assert html == expected_html
