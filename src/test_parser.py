import unittest
from parser import text_node_to_html_node, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_nodes
from textnode import TextNode, TextType


class TestParser(unittest.TestCase):
    def test_tn_to_hn_normal(self):
        text_node = TextNode("Hello world", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), 'Hello world')

    def test_tn_to_hn_bold(self):
        text_node = TextNode("Hello world", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<b>Hello world</b>')

    def test_tn_to_hn_italic(self):
        text_node = TextNode("Hello world", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<i>Hello world</i>')

    def test_tn_to_hn_code(self):
        text_node = TextNode("Hello world", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<code>Hello world</code>')

    def test_tn_to_hn_link(self):
        text_node = TextNode("Hello world", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="https://google.com">Hello world</a>')

    def test_tn_to_hn_image(self):
        text_node = TextNode("Hello world", TextType.IMAGE, "https://google.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<img src="https://google.com" alt="Hello world"></img>')

    def test_tn_to_hn_assert_exception(self):
        text_node = TextNode("something", None)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(text_node)
        self.assertTrue('Unexpected text type:' in str(context.exception))

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected[i])

    def test_split_nodes_delimiter_2(self):
        node = TextNode("`This is text with a code block word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a code block word", TextType.CODE),
        ]
        for i in range(0, len(new_nodes)):
            self.assertEqual(new_nodes[i], expected[i])

    def test_split_nodes_delimiter_malformed_md(self):
        node = TextNode("`This is text with a code block word", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue('Malformed MD' in str(context.exception))

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![images](https://i.imgur.com/zjjcJKZ.png) and another ![second images](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("images", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second images", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with an [images](https://i.imgur.com/zjjcJKZ.png) and another [second images](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("images", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second images", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        nodes = text_to_nodes(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan images](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan images", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
