import os

from TexSoup import TexSoup

TEX_PATH = os.getcwd() + "/main.tex"


def add_tabs(tab_count, string):
    for i in range(tab_count):
        string = "\t" + string
    return string


class PageGenerator():
    def __init__(self, charset="utf-8", stylesheet_path="stylesheet.css"):
        self._html_lines = []
        self._parsed_text = []
        self._charset = charset
        self._stylesheet_path = stylesheet_path

    def search_unique_item(self, search_key):
        # TODO: raise an error if iterm if found more than once
        for (item, key) in self._parsed_text:
            if key == search_key:
                return item
        return None  # TODO: raise a real error here

    def generate_head(self):
        title = self.search_unique_item("title")

        lines_to_append = [
            "<!DOCKTYPE html>",
            "<html>",
            "  <head>",
            f"    <meta charset=\"{self._charset}\" />",
            f"    <link rel=\"stylesheet\" href=\"{self._stylesheet_path}\" />",
            f"    <title>{title}</title>",
            "  </head>"
        ]

        self._html_lines += lines_to_append

    def process_text(self, parsed_text):
        print(parsed_text)
        self._parsed_text = parsed_text

        self.generate_head()
        self.tabs_count = 1

        self._html_lines.append(add_tabs(self.tabs_count, "<body>"))

        for (content, process_key) in self._parsed_text:
            html_content = CLASSES[process_key].turn_to_body_html(content)
            if html_content:
                self._html_lines.append(add_tabs(self.tabs_count, html_content))

        self._html_lines.append(add_tabs(self.tabs_count, "</body>"))
        self.tabs_count -= 1

        self._html_lines.append(add_tabs(self.tabs_count, "</html>"))

        print(self._html_lines)

    def create_page(self, page_name):
        with open(page_name, "x") as file:
            for line in self._html_lines:
                file.write(line + "\n")


class ProcessClass():
    def __init__(self, name, condition, content,
                 turn_to_body_html=lambda x: None):
        self.name = name
        self.condition = condition
        self.content = content
        self.turn_to_body_html = turn_to_body_html


CLASSES = {
    "title": ProcessClass("title",
                          lambda line: line.startswith("\\title"),
                          lambda line: line.split("{")[1].split("}")[0]),
    "author": ProcessClass("author",
                           lambda line: line.startswith("\\author"),
                           lambda line: line.split("{")[1].split("}")[0]),
    "date": ProcessClass("date",
                         lambda line: line.startswith("\\date"),
                         lambda line: line.split("{")[1].split("}")[0]),
    "section": ProcessClass("section",
                            lambda line: line.startswith("\\section"),
                            lambda line: line.split("{")[1].split("}")[0],
                            lambda content: f"<h1>{content}</h1>"),
    "subsection": ProcessClass("subsection",
                               lambda line: line.startswith("\\subsection"),
                               lambda line: line.split("{")[1].split("}")[0],
                               lambda content: f"<h2>{content}</h2>"),
    "comment": ProcessClass("comment",
                            lambda line: line.startswith("%"),
                            lambda line: None,),
    "blank_line": ProcessClass("blank_line",
                               lambda line: line.startswith("\n"),
                               lambda line: None),
    "mics": ProcessClass("misc",
                         lambda line: (line.startswith("\\documentclass")
                                       or line.startswith("\\usepackage")
                                       or line.startswith("\\geometry")
                                       or line.startswith("\\setcounter")
                                       or line.startswith("\\renewcommand")
                                       or line.startswith("\\begin")
                                       or line.startswith("\\end")
                                       or line.startswith("\\shorthandoff")
                                       or line.startswith("\\newpage")),
                         lambda line: None),
    "plain_text": ProcessClass("plain_text",
                               lambda line: True,
                               lambda line: line,
                               # TODO: remove all functional tags (bold, texit etc)
                               lambda content: f"<p>{content}</p>"),
}


class LatexParser():
    def __init__(self):
        self.texsoup = None
        self.parsed_text = []
        self.parse_state = False

    def parse_latex_texsoup(self, latex_file_path):
        with open(latex_file_path, 'r') as tex_file:
            # print(tex_file.read())
            # print(tex_file.read())
            texsoup = TexSoup(tex_file.read())
            # readlines might be of use to get each line independantly
            print(texsoup.section.name)

    def parse_line(self, line):
        found_class = False
        for class_key in CLASSES.keys():
            if found_class:
                continue
            if CLASSES[class_key].condition(line):
                found_class = True
                content = CLASSES[class_key].content(line)
                if content:
                    return(content, class_key)

    def parse_latex_custom(self, latex_file_path):
        assert not self.parse_state

        with open(latex_file_path, 'r') as tex_file:
            lines = tex_file.readlines()
            # print(lines)
            for line in lines:
                item = self.parse_line(line)
                if item:
                    self.parsed_text.append(item)
        self.parse_state = True

    def return_parsed_text(self):
        assert self.parse_state
        return self.parsed_text


if __name__ == "__main__":
    latex_parser = LatexParser()
    page_generator = PageGenerator()
    latex_parser.parse_latex_custom(TEX_PATH)
    parsed_text = latex_parser.return_parsed_text()
    page_generator.process_text(parsed_text)
    page_generator.create_page("test.html")
