import argparse
import os

from enex2md.enex_parser import parse_enex_file
from enex2md.markdown_convertor import convert_note_2_markdown


def convert_file(input_filepath, yinxiang_markdown_only, output_directory):
    notes = parse_enex_file(input_filepath)
    for note in notes:
        if yinxiang_markdown_only and not note.is_yinxiang_markdown():
            continue

        markdown = convert_note_2_markdown(note)
        if markdown is not None:
            output_filename = os.path.join(output_directory, note.title + ".md")
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)
            with open(output_filename, "w", encoding="utf-8") as fd:
                fd.write(markdown)
            print("Success: %s" % output_filename)
        else:
            print("Error: can not convert note(%s) to markdown in file(%s)" % (note.title, input_filepath))


def convert_directory(input_directory, yinxiang_markdown_only, output_directory):
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".enex"):
                filepath = os.path.join(root, file)
                rel_path = os.path.dirname(os.path.relpath(filepath, input_directory))
                output_dir = os.path.join(output_directory, rel_path)
                convert_file(filepath, yinxiang_markdown_only, output_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="A *.enex file or a directory containing many *.enex files")
    parser.add_argument("--yinxiang-markdown-only", default=False, action="store_true")
    parser.add_argument("-o", "--output", help="output directory", default="markdown_out")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("Error: input is not exists.")
        exit(-1)

    if not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)

    if os.path.isdir(args.input):
        convert_directory(args.input, args.yinxiang_markdown_only, args.output)
    elif os.path.isfile(args.input):
        convert_file(args.input, args.yinxiang_markdown_only, args.output)
    else:
        print(parser.usage)


if __name__ == '__main__':
    main()
