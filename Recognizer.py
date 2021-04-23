import re
import SubParser as SP


def envRecognizer(tokens):
    if not(tokens):
        return ["PlainText"]
    if tokens[0] == "#":
        return ["Part"]
    elif tokens[0] == "##":
        return ["Section", 1]
    elif tokens[0] == "###":
        return ["Section", 2]
    elif tokens[0] == "####":
        return ["Section", 3]
    # elif tokens[0] == ">":
    #     return ["Special", "Quotation"]
    elif tokens[0][0] == "<":
        return ["Special", "HTML"]
    # elif tokens[0] == "|":
    #     return ["Special", "Tabular"]
    # elif tokens[0] == "*" or tokens[0] == "+" or tokens[0] == "-":
    #     return ["Special", "Itemize"]
    # elif re.match('[1-9]+\.', tokens[0]):
    #     return ["Special", "Enumerate"]
    # elif tokens[0] == "$$":
    #     return ["Special", "$$"]
    else:
        return ["PlainText"]


def parser(tokens, types):
    if types == "HTML":
        cont = SP.html(tokens[0])
        if cont[0] == "img" and len(tokens) > 1:
            if tokens[1] == "":
                return ["Image", {"Centering": cont[2]}, cont[1] + [""]]
            else:
                capt = SP.html(tokens[1])
                return ["Image", {"Centering": cont[2]}, cont[1] + [capt]]


if __name__ == '__main__':
    print("This can only be imported")
