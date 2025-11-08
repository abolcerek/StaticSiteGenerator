import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node2 = HTMLNode("a", "Some random anchor text", None,  {"href": "https://www.google.com"})
        node3 = HTMLNode("a", "Some random anchor text", None,  {"href": "https://boot.dev"})
        node = HTMLNode("p", "Some random text", [node2, node3],  None)
        self.assertNotEqual(node, node2)
        print(node2.props_to_html())
        node4 = HTMLNode("a", "Some random anchor text", None,  {"href": "https://www.google.com"})
        node5 = HTMLNode("a", "Some random anchor text", None,  {"href": "https://www.google.com"})
        self.assertEqual(node4.props_to_html(), node5.props_to_html())
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_props_to_html_with_none_raises(self):
        node = HTMLNode('p', 'v', None, None)
        # props_to_html calls .items() on props; when props is None this should raise
        with self.assertRaises(AttributeError):
            node.props_to_html()

    def test_parent_with_multiple_children_returns_first_child_only(self):
        # Current ParentNode.to_html returns the rendering for the first child only
        c1 = LeafNode('b', '1')
        c2 = LeafNode('i', '2')
        p = ParentNode('div', [c1, c2])
        # Document current behavior: only the first child's HTML is included
        self.assertEqual(p.to_html(), '<div><b>1</b></div>')

def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )


if __name__ == "__main__":
    unittest.main()