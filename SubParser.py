from bs4 import BeautifulSoup
from bs4 import element


def html(tokens):
    token = BeautifulSoup(tokens, 'xml')
    tag = []
    con = []
    iters = token
    while type(iters) != element.NavigableString and iters.contents:
        tag.append(iters.contents[0].name)
        con.append(iters.contents[0])
        iters = iters.contents[0]
    if "center" in tag:
        centering = 1
    else:
        centering = 0
    if "img" in tag:
        pos = tag.index("img")
        src = con[pos].get("src")
        width = con[pos].get("width")
        if width:
            width = int(width[0:len(width) - 1]) / 100
        else:
            width = 1
        return ["img", [src, width], centering]
    elif centering:
        pos = tag.index("center")
        text = con[pos].contents[0]
        return str(text)


if __name__ == '__main__':
    print("This can only be imported")
