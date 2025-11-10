from textnode import *
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
            continue
        val = old_node.text.split(delimiter)
        if len(val) == 1:
            res.append(old_node)
            continue
        elif len(val) % 2 == 0:
            raise Exception("invalid Markdown syntax")
        built = []
        for i in range(len(val)):
            piece = val[i]
            if i % 2 == 1:
                node_type = text_type
            else:
                node_type = TextType.TEXT     
            built.append(TextNode(piece, node_type))  
        if built and built[0].text_type == TextType.TEXT and built[0].text == "": 
            built.pop(0)  
        if built and built[-1].text_type == TextType.TEXT and built[-1].text == "":
            built.pop()
        res.extend(built)        
    return res
    