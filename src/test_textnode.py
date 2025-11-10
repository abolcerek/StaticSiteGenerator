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
        
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
])


    def test_single_inline_code(self):
        nodes = [TextNode("a `code` b", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            out,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" b", TextType.TEXT),
            ],
        )

    def test_multiple_inline_code_segments(self):
        nodes = [TextNode("`x` and `y`", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            out,
            [
                TextNode("x", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("y", TextType.CODE),
            ],
        )

    def test_unmatched_raises(self):
        nodes = [TextNode("start `no end", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)


    def test_italic_underscore(self):
        nodes = [TextNode("pre _mid_ post", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(
            out,
            [
                TextNode("pre ", TextType.TEXT),
                TextNode("mid", TextType.ITALIC),
                TextNode(" post", TextType.TEXT),
            ],
        )

    def test_bold_double_asterisks(self):
        nodes = [TextNode("a **b** c **d**", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" c ", TextType.TEXT),
                TextNode("d", TextType.BOLD),
            ],
        )

    def test_empty_inner_content(self):
        nodes = [TextNode("a **** b", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("", TextType.BOLD),
                TextNode(" b", TextType.TEXT),
            ],
        )

    def test_leading_trailing_segments(self):
        nodes = [TextNode("**bold**end", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            out,
            [
                TextNode("bold", TextType.BOLD),
                TextNode("end", TextType.TEXT),
            ],
        )



    def test_split_nodes_delimiter_at_edges(self):
        src = "`edge`rest"
        node = TextNode(src, TextType.TEXT)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        # First node should be CODE with 'edge'
        self.assertGreaterEqual(len(out), 1)
        self.assertEqual(out[0].text_type, TextType.CODE)
        self.assertEqual(out[0].text, "edge")


if __name__ == "__main__":
    unittest.main()