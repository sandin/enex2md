from bs4 import BeautifulSoup
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import datetime
from typing import List


@dataclass
class Note(object):
    title: str
    created: datetime
    updated: datetime
    tags: List[str]
    note_attributes: dict
    content: str

    def is_yinxiang_markdown(self):
        return "content-class" in self.note_attributes \
            and self.note_attributes["content-class"] == "yinxiang.markdown"


def parse_enex_file(filename):
    notes = []
    with open(filename, "r", encoding="utf-8") as f:
        root = ET.fromstring(f.read())
        for note_elem in root:
            note = _parse_note(note_elem)
            notes.append(note)
    return notes


def _get_text_from_elem(elem, def_val=""):
    if elem is not None:
        return elem.text
    return def_val


def _parse_note(note_elem):
    title = _get_text_from_elem(note_elem.find("title"))
    created = _get_text_from_elem(note_elem.find("created"))
    updated = _get_text_from_elem(note_elem.find("updated"))
    content = _get_text_from_elem(note_elem.find("content"))

    tags = []
    for elem in note_elem.findall("tag"):
        tags.append(elem.text)

    attrs = {}
    attrs_elem = note_elem.find("note-attributes")
    for attr_elem in attrs_elem:
        attrs[attr_elem.tag] = attr_elem.text
    return Note(title, created, updated, tags, attrs, content)