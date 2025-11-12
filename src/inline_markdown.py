from textnode import *
import re
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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    res = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
            continue
        image_tags = extract_markdown_images(old_node.text)
        if len(image_tags) == 0:
            res.append(old_node)
            continue
        text = old_node.text
        for groups in image_tags:
            image_alt = groups[0]
            image_url = groups[1]
            node = text.split(f"![{image_alt}]({image_url})", 1)
            if node[0] != "":
                res.append(TextNode(node[0], TextType.TEXT))
            res.append(TextNode(image_alt, TextType.IMAGE, image_url))
            text = node[1]
        if text:
            res.append(TextNode(text, TextType.TEXT))
    return res

def split_nodes_link(old_nodes):
    res = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            res.append(old_node)
            continue
        link_tags = extract_markdown_links(old_node.text)
        if len(link_tags) == 0:
            res.append(old_node)
            continue
        text = old_node.text
        for groups in link_tags:
            link_alt = groups[0]
            link_url = groups[1]
            node = text.split(f"[{link_alt}]({link_url})", 1)
            if node[0] != "":
                res.append(TextNode(node[0], TextType.TEXT))
            res.append(TextNode(link_alt, TextType.LINK, link_url))
            text = node[1]
        if text:
            res.append(TextNode(text, TextType.TEXT))
    return res


def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    val1 = split_nodes_image(node)
    val2 = split_nodes_link(val1)
    val3 = split_nodes_delimiter(val2, "`", TextType.CODE)
    val4 = split_nodes_delimiter(val3, "**", TextType.BOLD)
    val5 = split_nodes_delimiter(val4, "_", TextType.ITALIC)
    return(val5)

    


            
    
        