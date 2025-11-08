import unittest

from textnode import *
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node3, node4)
        node5 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node6 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node3, node4)
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_textnode_eq_with_non_textnode_raises(self):
        node = TextNode("x", TextType.TEXT)
        class Dummy:
            pass
        # __eq__ expects the other object to have .text/.text_type/.url; when missing, it should raise
        with self.assertRaises(AttributeError):
            _ = (node == Dummy())

    def test_text_node_to_html_node_link_and_image_shapes(self):
        link = TextNode("link text", TextType.LINK)
        link_html = link.text_node_to_html_node()
        # LINK mapping currently returns a LeafNode with props as a dict containing 'href'
        self.assertIsInstance(link_html, LeafNode)
        self.assertEqual(link_html.tag, 'a')
        self.assertIsInstance(link_html.props, dict)
        self.assertIn('href', link_html.props)

        image = TextNode("", TextType.IMAGE)
        image_html = image.text_node_to_html_node()
        # IMAGE mapping currently returns a LeafNode with props as a list of dicts
        self.assertIsInstance(image_html.props, list)
        keys = set()
        for p in image_html.props:
            if isinstance(p, dict):
                keys.update(p.keys())
        self.assertIn('src', keys)
        self.assertIn('alt', keys)


if __name__ == "__main__":
    unittest.main()