# -*- coding: UTF-8 -*-

import re
from sys import exit

fileName = "test.md"

headers = (
    "\\documentclass{ctexart}",
    "\n",
    "\\usepackage[hmargin=1.25in,vmargin=1in]{geometry}",
    "\\usepackage{graphicx}",
    "\\usepackage{float}",
    "\\usepackage{CJKulem}",
    "\n"
)

docHeaders = (
    "\\maketitle",
    "\n",
    "\\tableofcontents",
    "\n",
    "\\thispagestyle{empty}",
    "\\newpage",
    "\\pagestyle{plain}",
    "\\setcounter{page}{1}"
)

title = ""
author = ""


def makeLine(line):
    for i in range(line):
        print()
        latexFile.write('\n')


def fPrintln(*args):
    word = ''.join(map(str, args))
    word = (max(len(stack) - 1, 0) + sectionCount) * "    " + word
    print(word)
    latexFile.write(word)
    latexFile.write('\n')


class MDFile:
    data = ""
    point = 0

    def fReadln(self):
        self.point += 1
        return self.data[self.point - 1]


stack = []
sectionCount = 0


def newEnv(env):
    stack.append(env)
    fPrintln("\\begin{", env, '}')


def endEnv():
    fPrintln("\\end{", stack.pop(), '}')


if __name__ == '__main__':
    if fileName == "":
        fileName = input()
    if fileName[len(fileName) - 3:] != '.md':
        print("请提供一个.md文件")
    else:
        fileName = fileName[:len(fileName) - 3]
    try:
        mdFile = open(fileName + '.md', "r", encoding="utf-8")
        mdData = mdFile.read().split("\n")
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
    author = md.fReadln()
    fPrintln("\\title{", title, "}")
    fPrintln("\\author{", author, '}')
    makeLine(1)
    fPrintln("\\date{\\today}")
    makeLine(2)

    newEnv("document")
    for ele in docHeaders:
        fPrintln(ele)

    while stack:
        endEnv()
    latexFile.close()
