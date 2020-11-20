import os

from LatexParser import LatexParser
from PageGenerator import PageGenerator

TEX_PATH = os.getcwd() + "/main.tex"

if __name__ == "__main__":
    latex_parser = LatexParser()
    page_generator = PageGenerator()
    latex_parser.parse_latex_custom(TEX_PATH)
    parsed_text = latex_parser.return_parsed_text()
    page_generator.process_text(parsed_text)
    page_generator.create_page("test2.html")
