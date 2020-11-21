import os
import argparse

from LatexParser import LatexParser
from PageGenerator import PageGenerator

TEX_PATH = os.getcwd() + "/main.tex"

parser = argparse.ArgumentParser()
parser.add_argument('--tex_path', help='path to the .tex file to process')
parser.add_argument('--result_name',
                    help='Name of the result page (do not forget to add .html extension')

args = parser.parse_args()

TEX_PATH = os.getcwd() + "/" + args.tex_path
PAGE_NAME = args.result_name

latex_parser = LatexParser()
page_generator = PageGenerator()
latex_parser.parse_latex_custom(TEX_PATH)
parsed_text = latex_parser.return_parsed_text()
page_generator.process_text(parsed_text)
page_generator.create_page(PAGE_NAME)
