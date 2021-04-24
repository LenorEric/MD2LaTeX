def divider(AST):
    if AST[0] == 'Enumerate' or AST[0] == 'Itemize':
        return transList(AST)
    elif AST[0] == 'Image':
        return transImage(AST)

def template(AST):
    LaTeXST = AST
    return LaTeXST


def transPlainText(AST):
    LaTeXST = []
    lines = AST[2]
    for line in lines:
        LaTeXST.append(['Text', line])
    return LaTeXST


def transImage(AST):
    LaTeXST = []
    begin = ['Env', ["figure", '[ht]']]
    LaTeXST.append(begin)
    if AST[1]["Centering"]:
        LaTeXST.append(["Cmd", "\centering"])
    include = "\includegraphics[width=" + str(AST[2][1]) + "\textwidth]{" + AST[2][0] + "}"
    LaTeXST.append(["Cmd", include])
    if AST[2][2] != '':
        caption = '\caption{' + AST[2][2] + '}'
        LaTeXST.append(['Cmd', caption])
    LaTeXST.append(['Env', ['\end{figure}']])
    return LaTeXST


def transTabular(AST):
    _table = {
        'hline': ['Cmd', '\hline']
    }
    LaTeXST = [['Env', ["table", '[ht]']], ["Cmd", "\centering"]]
    align = AST[1]["Align"]
    coll = []
    for i in range(len(align)):
        coll.append('|')
        coll.append(align[i])
    coll.append('|')
    begin = ['Env', ['tabular', '{' + ' '.join(coll) + '}']]
    LaTeXST.append(begin)
    LaTeXST.append(_table['hline'])
    AST[2][0] = ["\\textbf{" + str(cell) + "}" for cell in AST[2][0]]
    for line in AST[2]:
        cells = ' & '.join([str(cell) for cell in line]) + " \\"
        LaTeXST.append(['Text', cells])
        LaTeXST.append(_table['hline'])
    LaTeXST.append(['Env', ['\end{tabular}']])
    LaTeXST.append(['Env', ['\end{figure}']])
    return LaTeXST




def transQuotation(AST):
    LaTeXST = [['Env', ["quotation", '']]]
    for line in AST[2]:
        LaTeXST.append(['Text', str(line)])
    LaTeXST.append(['Env', ['\end{quotation}']])
    return LaTeXST


def transList(AST):
    if AST[0] == 'Enumerate':
        _type = 'enumerate'
    else:
        _type = 'itemize'
    LaTeXST = [['Env', [_type, '']]]
    for line in AST[2]:
        if type(line) == list:
            LateXST += divider(line)
        else:
            LaTeXST.append(['Cmd', '\item ' + str(line)])
    LaTeXST.append(['Env', ['\end{' + _type + '}']])
    return LaTeXST


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

    LaTeXST = []
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
        LaTeXST.append(['Text', text])
    return LaTeXST

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
