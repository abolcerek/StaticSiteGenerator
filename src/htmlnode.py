class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        str = ""
        for key, value in self.props.items():
            str += key + "=" + value + " "
        return str
    
    def __repr__(self):
        str = ""
        str = "HTMLNode(" + self.tag + ", " + self.value + ", " + self.children + self.props + ")"
        return str

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
        
    def to_html(self):
        if self.value == None:
            raise ValueError(f'All leaf nodes must have a value')
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag == None:
            raise ValueError
        elif self.children == None:
            raise ValueError(f'All parent nodes much have children')
        for child in self.children:
            return f"<{self.tag}>{child.to_html()}</{self.tag}>"
        
        
        
        