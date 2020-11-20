from ProcessClass import CLASSES


class LatexParser():
    def __init__(self):
        self.texsoup = None
        self.parsed_text = []
        self.parse_state = False

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
