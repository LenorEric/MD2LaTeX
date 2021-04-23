# MD2LaTeX
LenorEric

## 前言

​		或许你常常遇到这种情况：人生总是有无数的报告要写，它们还没有复杂到使用LaTeX的地步，但你又不想用Word来解决。或许是因为Word糟糕的文字排版，或许是因为来回不定的图片位置，或许是因为麻烦的目录格式与页眉页脚，或许是因为其不稳定和设备兼容性差。但无论如何，你打算使用Markdown。可MD对打印并不友好，无论是因为其忽大忽小的字体，或者一律左对齐的标题和正文。你期望可以直接在Markdown中进行简单的编辑，并且可以收获一份打印友好型的文档。

​		所以你采用了Pandoc将其转换，可生成的东西不仅复杂，而且不支持中文。那怎么办呢？不如来试试MD2Latex by Lenor吧。

## 使用要求

​		每个人有不同的写作习惯，但是写作习惯的多样性和最终转换的效果并不可以兼得。毕竟越支持多样的习惯，就代表最终生成的东西越复杂。
​		因此，在这里做出如下规定，如果你和Lenor一样使用的是Typora，并且拥有良好的写作习惯、以及写的的确是报告而不是什么其他很妖的东西，那么大部分东西对你而言都不会有问题：

1. 在第一行，用一个一级标题作为文档的总标题。

2. 在第二行，用一个普通正文作为作者名。如需多行作者名，用\\\\隔开。
3. MD正文中二级标题对应LaTeX中的一级标题。正文最多可拥有三个标题等级，即最多使用到LaTeX的三级标题。
5. 标题等级请使用“#”作为标识符。除了总标题外，其余的一级标题将被识别为LaTeX中的\\part
5. 除行末外，不要有两个及以上的连续空格，否则会被识别为单个空格。
6. 插入图片请使用\<img src=path width=percent>的格式。如没有\<center>标签，转换后的图片不会自动居中。通常转换后的表格默认居中（因为MD中表格只能居中）。
7. 如果表格、图片需要插入编号，请在其紧接下来的一行用\<center>\</center>标签加入名称，且不加编号。
8. 行末双空格换行将没有首行缩进，而空行换行则有。
9. 在标识符如\>（区块）后加入一个空格。
10. 请不要使用可能导致歧义的写法，或不符合规范的写法。
11. 切换不同的环境时，请保证至少有一个空行。
12. 如果一个内容转换失败，这很可能是由于过度使用了HTML代码，或使用了不存在与LaTeX中的写法。
13. 请尽可能地减少使用嵌套。

## 软件架构

<center><img src=".//img//SoftArch.png" width="90%"></center>

## MD-AST规则

​		MD中的每一个环境对应一条MD-AST。其中，一条MD-AST由一个列表（或元组）构成，结构为：

[Type, Properties, Content]。其中，Type为一字符串，Properties为一字典，Content为一列表。根据其类型的不同， 有着不同的Properties和Content规则。注意，大部分不同环境之间可以在Content中相互嵌套。

​		以下是目前已经规定的MD-AST规则：

> 目标种类：普通文本
>
> Type：“PlainText”
>
> Properties：{}
> Content：[ContentString]

> 目标种类：图片
>
> Type:"Image"
>
> Properties:{"Centering": [0/1]}
>
> Content:[Source, Width, Caption]

> 目标种类：表格
>
> Type:"Tabular"
>
> Properties:{"Align":"\[l/c/r]……"}
>
> Content:[[Cell,……]，……]
>
> 备注：表头记得用\\textbf{Cell}加粗哦

> 目标种类：有序列表
>
> Type:"Enumerate"
>
> Properties:{}
>
> Content:[Line, ……]

> 目标种类：无序列表
>
> Type: "Itemize"
>
> Properties:{}
>
> Content:[Line,……]

> 目标种类：区块
>
> Type:"Quotation"
>
> Properties:{}
>
> Content:[Line,……]
>
> 备注：在Markdown中区块将被翻译为LaTeX中的引用

> 目标种类：公式
>
> Type:"$$"
>
> Properties:{}
>
> Content:[Line,……]

## LaTeX-ST规则

​		为了方便起见，使用LaTeX-ST作为中间语言传入主程序，再由主程序转为LaTeX标准语法。这样做的理由是保证拓展性的同时，可以由主程序进行首行缩进等操作。LaTeX-ST的规则极为接近LaTeX语法，每一个LaTeX-ST代表一行多多行LaTeX语句。通常其结构为：

[[Type, Content],……]。其中，Type和Content均为一字符串。Content为LaTeX中的语法内容。

​		以下是已经规定的Type种类：

> "Cmd": 即单独使用一条\Command来表达的指令
>
> "Env": 即需要使用\\begin{Environment} \\end{Environment}来表达的环境
>
> "Text": 即一个普通的字符串

