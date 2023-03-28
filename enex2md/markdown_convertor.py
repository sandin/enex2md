from bs4 import BeautifulSoup
from urllib import parse


def convert_note_2_markdown(note):
    if note.is_yinxiang_markdown():
        return _extract_yinxiang_markdown(note.content)
    else:
        return ""  # TODO


def _extract_yinxiang_markdown(content):
    note_dom = BeautifulSoup(content, "html.parser").find("en-note")
    last_dir = note_dom.contents[-1]
    if "display:none" in last_dir.attrs.get("style", ""):
        markdown_content = parse.unquote(last_dir.text)
        return markdown_content
    return ""




