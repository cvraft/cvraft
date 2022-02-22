import re
import xml.etree.ElementTree as etree

from markdown import Markdown
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class WrapSectionsProcessor(BlockProcessor):
    STATE_NAME = "wrapping-%s"
    RE = re.compile(r"(?:^|\n)(?P<level>#{1,7})(?P<header>(?:\\.|[^\\])*?)#*(?:\n|$)")

    def __init__(self, parser):
        super().__init__(parser)

    def test(self, parent: etree.ElementTree, block: str) -> None:
        m = self.RE.search(block)
        if m:
            level = m.group("level")
            return not self.parser.state.isstate(self.STATE_NAME % len(level))
        return False

    def run(self, parent: etree.ElementTree, blocks: list[str]) -> None:
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            level = m.group("level")
            self.parser.state.set(self.STATE_NAME % len(level))
            blocks_in_section = [block[m.start() : m.end()]]
            blocks.insert(0, block[m.end() :])

            NEXT_RE = re.compile(f"(?:^|\n)({level})[^#]+")

            cur = -1
            for i, b in enumerate(blocks):
                m2 = NEXT_RE.search(b)
                if m2:
                    blocks_in_section.append(b[: m2.start()])
                    break
                else:
                    cur = i

            if cur > -1:
                for i in range(cur + 1):
                    b = blocks.pop(0)
                    blocks_in_section.append(b)

            section = etree.SubElement(parent, "section")
            self.parser.parseBlocks(section, blocks_in_section)
            self.parser.state.reset()
            return True
        else:
            blocks.insert(0, block)
            return False


HEADER_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6", "h7"]


def is_header(tag: str):
    return tag.lower() in HEADER_TAGS


class SectionDataProcessor(Treeprocessor):
    SECTION_ID = "data-section-id"
    SECTION_CLASS = "data-section-class"
    PERIOD = "data-period"
    LOCATION = "data-location"
    DATE = "data-date"

    def run(self, root):
        for section in root.iter("section"):
            self._move_section_data_from_heading(section)

    def _move_section_data_from_heading(self, section):
        for child in section:
            if is_header(child.tag):
                position = 1
                if self.SECTION_ID in child.attrib:
                    section.attrib["id"] = child.attrib[self.SECTION_ID]
                    child.attrib.pop(self.SECTION_ID)
                if self.SECTION_CLASS in child.attrib:
                    section.attrib["class"] = child.attrib[self.SECTION_CLASS]
                    child.attrib.pop(self.SECTION_CLASS)
                if self.PERIOD in child.attrib:
                    el = self._create_span(child.attrib[self.PERIOD], "period")
                    section.insert(position, el)
                    position += 1
                    child.attrib.pop(self.PERIOD)
                if self.DATE in child.attrib:
                    el = self._create_span(child.attrib[self.DATE], "date")
                    section.insert(position, el)
                    position += 1
                    child.attrib.pop(self.DATE)
                if self.LOCATION in child.attrib:
                    el = self._create_span(child.attrib[self.LOCATION], "location")
                    section.insert(position, el)
                    position += 1
                    child.attrib.pop(self.LOCATION)
            elif child.tag == "section":
                self._move_section_data_from_heading(child)

    def _create_span(self, value, classes = None):
        el = etree.Element("span")
        el.attrib["class"] = classes
        el.text = value
        return el

class CvraftExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.parser.blockprocessors.register(
            WrapSectionsProcessor(md.parser), "wrap-sections", 75
        )
        md.treeprocessors.register(SectionDataProcessor(md), "section-data", 7)


# Recommend by Python Markdown: https://python-markdown.github.io/extensions/api/#dot_notation
def makeExtension(**kwargs):
    return CvraftExtension(**kwargs)
