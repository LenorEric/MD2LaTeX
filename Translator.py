import SubTrans as ST
import mistune
from bs4 import BeautifulSoup
import re

md = mistune.Markdown(escape=False)


def textRenderer(text):
    while text[0] == " " or text[0] == "\u200b" or text[0] == "\t":
        text = text[1:]
    if text[len(text)-2:len(text)] == "  ":
        text += " \\newline"
    text = "".join(map(str, BeautifulSoup(md(text), 'xml').contents[0].contents))
    replaceRules = (
        (r"\n", ""),
        (r"</a>", ""),
        (r'<a href=".*">', r""),
        (r"</\w*>", r"}"),
        (r"<strong>", r"\\textbf{"),
        (r"<em>", r"\\textsl{"),
        (r"<del>", r"\\sout{"),
        (r"<u>", r"\\underline{"),
        (r"_", r"\\_"),
        (r"\^", r"\\^")
    )
    for rule in replaceRules:
        text = re.sub(rule[0], rule[1], text)
    return text


def trans(AST):
    return ST.divider(AST)


if __name__ == '__main__':
    print("This can only be imported")
