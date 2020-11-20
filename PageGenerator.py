from ProcessClass import CLASSES


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
