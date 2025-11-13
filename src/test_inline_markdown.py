import unittest
from inline_markdown import (
    split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
)
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_no_image(self):
        node = TextNode("This is text with no image.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is text with no image.", TextType.TEXT)],
            new_nodes
        )

    def test_image_at_start(self):
        node = TextNode("![image](https://example.com/img.png)This is text.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode("This is text.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_image_at_end(self):
        node = TextNode("This is text with an image at the end.![image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image at the end.", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            ],
            new_nodes
        )

    def test_multiple_images_and_text(self):
        node = TextNode("Text before ![img1](url1) text in middle ![img2](url2) text after.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode(" text in middle ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2"),
                TextNode(" text after.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_only_image(self):
        node = TextNode("![only image](https://example.com/single.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only image", TextType.IMAGE, "https://example.com/single.png"),
            ],
            new_nodes
        )

    # What about a node that isn't of type TEXT? How should your function handle that?
    def test_non_text_node(self):
        node = TextNode("This is a code block `print('hello')`", TextType.CODE)
        new_nodes = split_nodes_image([node])
        # What do you think should be the expected output here?
        # self.assertListEqual(
        #     [
        #         # Your expected TextNode list here
        #     ],
        #     new_nodes
        # )
        
        
    def test_extract_images_basic(self):
        s = "a ![alt](url) b ![x](y)"
        self.assertEqual(
            extract_markdown_images(s),
            [("alt", "url"), ("x", "y")]
        )

    def test_extract_images_ignores_links(self):
        s = "a [alt](url) b"
        self.assertEqual(extract_markdown_images(s), [])

    def test_extract_links_basic(self):
        s = "a [alt](url) b [x](y)"
        self.assertEqual(
            extract_markdown_links(s),
            [("alt", "url"), ("x", "y")]
        )

    def test_extract_links_ignores_images(self):
        s = "a ![alt](url)"
        self.assertEqual(extract_markdown_links(s), [])

    def test_split_nodes_image_simple(self):
        nodes = [TextNode("a ![alt](url) b", TextType.TEXT)]
        out = split_nodes_image(nodes)
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" b", TextType.TEXT),
        ])

    def test_split_nodes_image_multiple(self):
        nodes = [TextNode("x ![a](u) y ![b](v) z", TextType.TEXT)]
        out = split_nodes_image(nodes)
        self.assertEqual(out, [
            TextNode("x ", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "u"),
            TextNode(" y ", TextType.TEXT),
            TextNode("b", TextType.IMAGE, "v"),
            TextNode(" z", TextType.TEXT),
        ])

    def test_split_nodes_link_simple(self):
        nodes = [TextNode("a [alt](url) b", TextType.TEXT)]
        out = split_nodes_link(nodes)
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("alt", TextType.LINK, "url"),
            TextNode(" b", TextType.TEXT),
        ])

    def test_split_nodes_link_multiple(self):
        nodes = [TextNode("x [a](u) y [b](v) z", TextType.TEXT)]
        out = split_nodes_link(nodes)
        self.assertEqual(out, [
            TextNode("x ", TextType.TEXT),
            TextNode("a", TextType.LINK, "u"),
            TextNode(" y ", TextType.TEXT),
            TextNode("b", TextType.LINK, "v"),
            TextNode(" z", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_code(self):
        nodes = [TextNode("a `code` b", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" b", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_bold_double_asterisk(self):
        nodes = [TextNode("a **bold** b", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" b", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_italic_underscore(self):
        nodes = [TextNode("a _it_ b", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("it", TextType.ITALIC),
            TextNode(" b", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_ignores_non_text_nodes(self):
        nodes = [
            TextNode("a `code` b", TextType.TEXT),
            TextNode("c", TextType.LINK, "url"),
        ]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" b", TextType.TEXT),
            TextNode("c", TextType.LINK, "url"),
        ])

    def test_text_to_textnodes_integration(self):
        s = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        out = text_to_textnodes(s)
        self.assertEqual(out, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])
        
    # python
    def test_delimiters_inside_link_untouched(self):
        nodes = [TextNode("see [**bold** link](/u) and _not here_", TextType.TEXT)]
        out = split_nodes_link(nodes)
        out = split_nodes_image(out)
        out = split_nodes_delimiter(out, "**", TextType.BOLD)
        out = split_nodes_delimiter(out, "_", TextType.ITALIC)
        self.assertEqual(out, [
            TextNode("see ", TextType.TEXT),
            TextNode("**bold** link", TextType.LINK, "/u"),
            TextNode(" and ", TextType.TEXT),
            TextNode("not here", TextType.ITALIC),
        ])

    def test_delimiters_inside_image_untouched(self):
        nodes = [TextNode("pic ![__alt__ text](url) end", TextType.TEXT)]
        out = split_nodes_image(nodes)
        out = split_nodes_delimiter(out, "_", TextType.ITALIC)
        self.assertEqual(out, [
            TextNode("pic ", TextType.TEXT),
            TextNode("__alt__ text", TextType.IMAGE, "url"),
            TextNode(" end", TextType.TEXT),
        ])
        
    # python
    def test_unmatched_bold_raises(self):
        nodes = [TextNode("start **bold only", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

    def test_unmatched_code_raises(self):
        nodes = [TextNode("broken `code here", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)
            
    # python
    def test_single_asterisk_italic_with_bold(self):
        nodes = [TextNode("a *it* and **bold** b", TextType.TEXT)]
        out = split_nodes_delimiter(nodes, "`", TextType.CODE)  # no-op
        out = split_nodes_delimiter(out, "**", TextType.BOLD)
        out = split_nodes_delimiter(out, "*", TextType.ITALIC)
        self.assertEqual(out, [
            TextNode("a ", TextType.TEXT),
            TextNode("it", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" b", TextType.TEXT),
        ])
    
    def test_heading_simple(self):
        self.assertEqual(block_to_block_type("# Title"), BlockType.HEADING)

    def test_heading_six_hashes(self):
        self.assertEqual(block_to_block_type("###### Six"), BlockType.HEADING)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Seven"), BlockType.PARAGRAPH)

    def test_heading_missing_space(self):
        self.assertEqual(block_to_block_type("###NoSpace"), BlockType.PARAGRAPH)

    def test_code_fenced_multiline(self):
        block = "```\nprint('x')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_single_line_backticks_only(self):
        self.assertEqual(block_to_block_type("```"), BlockType.PARAGRAPH)

    def test_quote_all_lines_start_with_gt(self):
        block = "> a\n> b"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_mixed_lines(self):
        block = "> a\nb"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_valid(self):
        block = "- a\n- b"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("-a"), BlockType.PARAGRAPH)

    def test_ordered_list_valid(self):
        block = "1. a\n2. b\n3. c"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_skipped_number(self):
        block = "1. a\n3. b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_start(self):
        block = "0. a\n1. b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_must_start_at_one(self):
        block = "10. a\n11. b"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraph_fallback(self):
        self.assertEqual(block_to_block_type("just some text"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
