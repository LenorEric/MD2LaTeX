import re
import SubParser as SP


def envRecognizer(tokens):
    if tokens[0] == "#":
        return ["Part"]
    elif tokens[0] == "##":
        return ["Section", 1]
    elif tokens[0] == "###":
        return ["Section", 2]
    elif tokens[0] == "####":
        return ["Section", 3]
    # elif tokens[0] == ">":
    #     return ["Quotation"]
    elif tokens[0][0] == "<":
        return ["Special", "HTML"]
    # elif tokens[0] == "|":
    #     return ["Special", "Tabular"]
    # elif tokens[0] == "*" or tokens[0] == "+" or tokens[0] == "-":
    #     return ["Itemize"]
    # elif re.match('[1-9]+\.', tokens[0]):
    #     return ["Enumerate"]
    # elif tokens[0] == "$$":
    #     return ["Special", "$$"]
    else:
        return ["PlainText"]


def parser(tokens, types):
    if types == "HTML":
        return SP.html(tokens)


if __name__ == '__main__':
    print("This can only be imported")
