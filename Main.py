# -*- coding: UTF-8 -*-

import Recognizer
import Translator
from sys import exit

fileName = "test.md"

headers = (
    "\\documentclass{ctexart}",
    "",
    "\\usepackage[hmargin=1.25in,vmargin=1in]{geometry}",
    "\\usepackage{graphicx}",
    "\\usepackage{float}",
    "\\usepackage{CJKulem}",
    ""
)

docHeaders = (
    "\\maketitle",
    "",
    "\\tableofcontents",
    "",
    "\\thispagestyle{empty}",
    "\\newpage",
    "\\pagestyle{plain}",
    "\\setcounter{page}{1}",
    ""
)

title = ""
author = ""


def makeLine(line):
    for i in range(line):
        print()
        latexFile.write('\n')


def fPrintln(*args):
    word = ''.join(map(str, args))
    word = (max(len(stack) - 1, 0) + sectionLevel) * "    " + word
    print(word)
    latexFile.write(word)
    latexFile.write('\n')


class MDFile:
    data = ""
    point = -1

    def remain(self):
        if self.point + 1 == len(self.data):
            return False
        else:
            return True

    def fReadln(self):
        self.point += 1
        return self.data[self.point]

    def fReadNextln(self):
        self.point += 1
        while self.data[self.point] == "":
            self.point += 1
        return self.data[self.point]


stack = []
sectionLevel = 0


def newEnv(env, pro=""):
    stack.append(env)
    if pro == "":
        fPrintln("\\begin{", env, '}')
    else:
        fPrintln("\\begin{", env, "}[", pro, ']')


def endEnv():
    fPrintln("\\end{", stack.pop(), '}')


def compositorPrinter(LaTeX_SP):
    for line in LaTeX_SP:
        if line[0] == "Cmd":
            fPrintln(line[1])
        elif line[0] == "Env":
            if len(line[1]) == 1:
                endEnv()
            else:
                newEnv(line[1][0], line[1][1])
        elif line[0] == "Text":
            fPrintln(line[1])


ret = [
    ["Env", ["figure", "ht"]],
    ["Cmd", "\\centering"],
    ["Cmd", "\includegraphics[width=0.5\textwidth]{img//img3.png}"],
    ["Cmd", "\caption{软件流程图}"],
    ["Env", ["figure"]]
]


def process():
    def specialProcesser(tokens, preEnv):
        parse = Recognizer.parser(tokens, preEnv)
        LaTeX_SP = Translator.trans(parse)
        compositorPrinter(ret)

    buffer = md.fReadln()
    if buffer == "":
        makeLine(1)
        return
    env = Recognizer.envRecognizer(buffer.split())
    if env[0] == "Special":
        specialProcesser(buffer, env[1])
    elif env[0] == "Section":
        global sectionLevel
        sectionLevel = env[1] - 1
        if env[1] == 1:
            makeLine(1)
            fPrintln("\\section{", ' '.join(buffer.split()[1:]), "}")
        elif env[1] == 2:
            fPrintln("\\subsection{", ' '.join(buffer.split()[1:]), "}")
        elif env[1] == 3:
            fPrintln("\\subsubsection{", ' '.join(buffer.split()[1:]), "}")
        sectionLevel += 1
    elif env[0] == "PlainText":
        fPrintln(Translator.textRenderer(buffer))
    elif env[0] == "Part":
        sectionLevel = 0
        fPrintln("\\part{", ' '.join(buffer.split()[1:]), "}")


if __name__ == '__main__':
    if fileName == "":
        fileName = input()
    if fileName[len(fileName) - 3:] != '.md':
        print("请提供一个.md文件")
    else:
        fileName = fileName[:len(fileName) - 3]
    try:
        mdFile = open(fileName + '.md', "r", encoding="utf-8")
        mdData = mdFile.read().splitlines()
        mdFile.close()
        md = MDFile()
        md.data = mdData
    except IOError:
        print("找不到文件")
        exit()
    latexFile = open(fileName + '.tex', "w", encoding="utf-8")
    for ele in headers:
        fPrintln(ele)
    title = md.fReadln().split()
    if title[0] == '#':
        title = ' '.join(title[1:len(title)])
    else:
        title = ' '.join(title)
    author = md.fReadNextln()
    fPrintln("\\title{", title, "}")
    fPrintln("\\author{", author, '}')
    makeLine(1)
    fPrintln("\\date{\\today}")
    makeLine(2)

    newEnv("document")
    for ele in docHeaders:
        fPrintln(ele)

    while md.remain():
        process()

    sectionLevel = 0
    while stack:
        endEnv()
    latexFile.close()
