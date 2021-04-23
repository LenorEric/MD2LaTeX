def transImage(AST):
    LaTeX_SP = []
    begin = ['Env', ["figure", '[ht]']]
    LaTeX_SP.append(begin)
    if AST[1]["Centering"]:
        LaTeX_SP.append(["Cmd", "\centering"])
    include = "\includegraphics[width=" + str(AST[2][1]) + "\\textwidth]{" + AST[2][0] + "}"
    LaTeX_SP.append(["Cmd", include])
    if AST[2][2] != '':
        caption = '\caption{' + AST[2][2] + '}'
        LaTeX_SP.append(['Cmd', caption])
    LaTeX_SP.append(['Env', 'figure'])
    return LaTeX_SP


if __name__ == '__main__':
    print("This can only be imported")
