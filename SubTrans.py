def divider(AST):
    if AST[0] == 'Enumerate' or AST[0] == 'Itemize':
        return transList(AST)
    elif AST[0] == 'Image':
        return transImage(AST)


def template(AST):
    LaTeX_ST = AST
    return LaTeX_ST


def transPlainText(AST):
    LaTeX_ST = []
    lines = AST[2]
    for line in lines:
        LaTeX_ST.append(['Text', line])
    return LaTeX_ST


def transImage(AST):
    LaTeX_ST = []
    begin = ['Env', ["figure", '[ht]']]
    LaTeX_ST.append(begin)
    if AST[1]["Centering"]:
        LaTeX_ST.append(["Cmd", "\centering"])
    include = "\includegraphics[width=" + str(AST[2][1]) + "\textwidth]{" + AST[2][0] + "}"
    LaTeX_ST.append(["Cmd", include])
    if AST[2][2] != '':
        caption = '\caption{' + AST[2][2] + '}'
        LaTeX_ST.append(['Cmd', caption])
    LaTeX_ST.append(['Env', ['\end{figure}']])
    return LaTeX_ST


def transTabular(AST):
    _table = {
        'hline': ['Cmd', '\hline']
    }
    LaTeX_ST = [['Env', ["table", '[ht]']], ["Cmd", "\centering"]]
    align = AST[1]["Align"]
    coll = []
    for i in range(len(align)):
        coll.append('|')
        coll.append(align[i])
    coll.append('|')
    begin = ['Env', ['tabular', '{' + ' '.join(coll) + '}']]
    LaTeX_ST.append(begin)
    LaTeX_ST.append(_table['hline'])
    AST[2][0] = ["\\textbf{" + str(cell) + "}" for cell in AST[2][0]]
    for line in AST[2]:
        cells = ' & '.join([str(cell) for cell in line]) + " \\"
        LaTeX_ST.append(['Text', cells])
        LaTeX_ST.append(_table['hline'])
    LaTeX_ST.append(['Env', ['\end{tabular}']])
    LaTeX_ST.append(['Env', ['\end{figure}']])
    return LaTeX_ST


def transQuotation(AST):
    LaTeX_ST = [['Env', ["quotation", '']]]
    for line in AST[2]:
        LaTeX_ST.append(['Text', str(line)])
    LaTeX_ST.append(['Env', ['\end{quotation}']])
    return LaTeX_ST


def transList(AST):
    if AST[0] == 'Enumerate':
        _type = 'enumerate'
    else:
        _type = 'itemize'
    LaTeX_ST = [['Env', [_type, '']]]
    for line in AST[2]:
        if type(line) == list:
            LaTeX_ST += divider(line)
        else:
            LaTeX_ST.append(['Cmd', '\item ' + str(line)])
    LaTeX_ST.append(['Env', ['\end{' + _type + '}']])
    return LaTeX_ST


def transFormula(AST):
    def isZh(c):
        if u'\u4e00' <= c <= u'\u9fff':
            return True
        return False

    def findZh(str):
        s = e = 0
        for i in range(len(str)):
            if isZh(str[i]):
                e = i
                if s == 0:
                    s = i
        return [s, e]

    LaTeX_ST = []
    for line in AST[2]:
        text = line
        index = findZh(line)
        if index[0] != index[1]:
            text = ''
            for i in range(index[0]):
                text += line[i]
            text += ("\mbox{" + line[index[0]:index[1] + 1] + "}")
            for i in range(index[1] + 1, len(line)):
                text += line[i]
        LaTeX_ST.append(['Text', text])
    return LaTeX_ST

# tabular=[
#     "Tabular",
#     {"Align":"lrrl"},
#     [
#         [1,2,3,4],
#         [5,6,7,8]
#     ]
# ]

# quotation=[ 
#     "Quotation",
#     {},
#     [
#         "@@@","$$$"
#     ]
# ]

# Enumerate=[ 
#     'Enumerate',
#     {},
#     ["12",'23','34']
# ]

# dollarDollar=[ 
#     '$$',
#     {},
#     [
#         "$$",
#         '\\frac{aaa}{我是中文}',
#         'a_{我是中文啊}',
#         '$$'
#     ]
# ]
# print(transTabular(tabular))
# print(transQuotation(quotation))
# print(transList(Enumerate))
# print(transItemize(Enumerate))
# print(findZh("12@中文12$2"))
# print('123456'[0:2])
# print(transFormula(dollarDollar))
