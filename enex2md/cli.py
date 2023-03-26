import argparse
import os
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from urllib import parse


def check_if_is_yinxiang_markdown(note_elem):
    note_attrs_elem = note_elem.find("note-attributes")  # TODO: assert
    if note_attrs_elem is not None:
        content_class_elem = note_attrs_elem.find("content-class")
        if content_class_elem is not None:
            content_class = content_class_elem.text
            return content_class == "yinxiang.markdown"
    return False


def extract_yinxiang_markdown(content):
    note_dom = BeautifulSoup(content, "html.parser").find("en-note")
    last_dir = note_dom.contents[-1]
    if "display:none" in last_dir.attrs.get("style", ""):
        markdown_content = parse.unquote(last_dir.text)
        return markdown_content
    return ""


def convert_file_to_markdown(input_filepath, yinxiang_markdown_only, output_directory):
    with open(input_filepath, "r", encoding="utf-8") as f:
        root = ET.fromstring(f.read())
        note_elem = root[0]
        content_elem = note_elem.find("content")
        content = content_elem.text

        is_yinxiang_markdown = check_if_is_yinxiang_markdown(note_elem)
        if is_yinxiang_markdown:
            markdown = extract_yinxiang_markdown(content)
        else:
            if yinxiang_markdown_only:
                return
            markdown = ""  # TODO

        print("=========================")
        print(input_filepath)
        print(markdown[:10])
        output_filename = os.path.join(output_directory, os.path.basename(input_filepath))[:-5] + ".md"
        print(output_filename)
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(output_filename, "w", encoding="utf-8") as fd:
            fd.write(markdown)


def convert_directory_to_markdown(input_directory, yinxiang_markdown_only, output_directory):
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".enex"):
                filepath = os.path.join(root, file)
                rel_path = os.path.dirname(os.path.relpath(filepath, input_directory))
                output_dir = os.path.join(output_directory, rel_path)
                convert_file_to_markdown(filepath, yinxiang_markdown_only, output_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="A *.enex file or a directory containing many *.enex files")
    parser.add_argument("--yinxiang-markdown-only", default=True, action="store_true")
    parser.add_argument("-o", "--output", help="output directory", default="markdown_out")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("Error: input is not exists.")
        exit(-1)

    if not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)

    if os.path.isdir(args.input):
        convert_directory_to_markdown(args.input, args.yinxiang_markdown_only, args.output)
    elif os.path.isfile(args.input):
        convert_file_to_markdown(args.input, args.yinxiang_markdown_only, args.output)
    else:
        print(parser.usage)


if __name__ == '__main__':
    main()
