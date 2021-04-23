# -*- coding: UTF-8 -*-

import Recognizer
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


def process():
    buffer = []
    ASTP = []
    buffer.append(md.fReadNextln())
    env = Recognizer.envRecognizer(buffer[len(buffer)-1].split())
    print(env)


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

    while stack:
        endEnv()
    latexFile.close()
