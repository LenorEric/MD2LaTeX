import SubTrans as ST


def textRenderer(text):
    while text[0] == " " or text[0] == "\u200b":
        text = text[1:]
    return text


def trans(AST):
    if AST[0] == "Image":
        return ST.transImage(AST)


if __name__ == '__main__':
    print("This can only be imported")
