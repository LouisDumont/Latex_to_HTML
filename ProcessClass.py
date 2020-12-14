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
                            lambda line: None),
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
