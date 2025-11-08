from enum import Enum

class TextType(Enum):
    p = "text (plain)"
    b = "**Bold text**"
    i = "_Italic text_"
    img = "![alt text](url)"
    a = "[anchor text](url)"
    
    
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url
        
        
    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False
    
    def __repr__(self):
        pass
        
        
    