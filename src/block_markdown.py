from textnode import *
from enum import Enum
import textwrap

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
    
def block_to_block_type(block):
    def is_heading(first_line):
        i = 0
        n = len(first_line)
        
        while i < n and first_line[i] == "#":
            i += 1
        if i == 0 or i > 6:
            return False  
        if i >= n or first_line[i] != " ":
            return False
        return True
        
        
    def is_code(lines):
        if len(lines) == 1:
            if len(lines[0]) <= 6:
                return False
            if lines[0].startswith("```") and lines[0].endswith("```"):
                return True
        if lines[0] == "```"and lines[-1] == "```":
            return True
        return False
        
    
    def unordered_quote_checker(lines):
        res = True
        for line in lines:
            if not line.startswith(">"):
                res = False
        return res
            
    
    def unordered_list_checker(lines):
        res = True
        for line in lines:
            if not line.startswith("- "):
                res = False
        return res
            
    def ordered_list_checker(lines):
        for i, line in enumerate(lines, start=1):
            dot = line.find(".")
            if dot == -1:
                return False
            num = line[:dot]
            if not num.isdigit() or num != str(i):
                return False
            if dot + 1 >= len(line) or line[dot + 1] != " ":
                return False
        return True  
    
    lines = [ln.lstrip() for ln in block.splitlines()] 
    
    if not lines:
        return BlockType.PARAGRAPH
    
    if is_code(lines):
        return BlockType.CODE
    
    if is_heading(lines[0]):
        return BlockType.HEADING
    
    if unordered_quote_checker(lines):
            return BlockType.QUOTE
        
    if unordered_list_checker(lines):
            return BlockType.UNORDERED_LIST
        
    if ordered_list_checker(lines):
            return BlockType.ORDERED_LIST
        
    else:
        return BlockType.PARAGRAPH 
            

def markdown_to_blocks(markdown):
    blocks = markdown.strip().split("\n\n")
    res = []
    for block in blocks:
        if block.strip() != "":
            res.append(textwrap.dedent(block).strip())
    return res




