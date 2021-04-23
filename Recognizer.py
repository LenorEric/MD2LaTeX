import re


def envRecognizer(tokens):
    if tokens[0] == "#":
        return ["part"]
    elif tokens[0] == "##":
        return ["Section", 0]
    elif tokens[0] == "###":
        return ["Section", 1]
    elif tokens[0] == "####":
        return ["Section", 2]
    elif tokens[0] == ">":
        return ["Quotation"]
    elif tokens[0] == "<":
        return ["Special", "HTML"]
    elif tokens[0] == "|":
        return ["Special", "Tabular"]
    elif tokens[0] == "*" or tokens[0] == "+" or tokens[0] == "-":
        return ["Itemize"]
    elif re.match('[1-9]+\.', tokens[0]):
        return ["Enumerate"]
    else:
        return ["PlainText"]


if __name__ == '__main__':
    print("This can only be imported")
