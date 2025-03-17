import unittest

from src.htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank", }
        node = HtmlNode(props=props)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_with_none(self):
        node = HtmlNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_empty(self):
        props = {}
        node = HtmlNode(props=props)
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
