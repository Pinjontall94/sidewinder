import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from functions import text_node_to_html_node, split_nodes_delimiter


class TestTextNodeToHTMLNode(unittest.TestCase):
    normal_node = TextNode("i'm normal", TextType.NORMAL)
    bold_node = TextNode("i'm super srs rn", TextType.BOLD)
    italic_node = TextNode("i'm spicy", TextType.ITALIC)
    code_node = TextNode("beep boop i'm code", TextType.CODE)
    link_node = TextNode(
        "i'm a link to google", TextType.LINK, "https://www.google.com"
    )
    image_node = TextNode(
        "i'm alt text", TextType.IMAGE, "https://picsum.photos/200/200"
    )

    def test_normal(self):
        self.assertEqual(
            text_node_to_html_node(self.normal_node).to_html(),
            LeafNode(None, "i'm normal").to_html(),
        )

    def test_bold(self):
        self.assertEqual(
            text_node_to_html_node(self.bold_node).to_html(),
            LeafNode("b", "i'm super srs rn").to_html(),
        )

    def test_italic(self):
        self.assertEqual(
            text_node_to_html_node(self.italic_node).to_html(),
            LeafNode("i", "i'm spicy").to_html(),
        )

    def test_code(self):
        self.assertEqual(
            text_node_to_html_node(self.code_node).to_html(),
            LeafNode("code", "beep boop i'm code").to_html(),
        )

    def test_link(self):
        self.assertEqual(
            text_node_to_html_node(self.link_node).to_html(),
            LeafNode(
                "a", "i'm a link to google", props={"href": "https://www.google.com"}
            ).to_html(),
        )

    def test_image(self):
        self.assertEqual(
            text_node_to_html_node(self.image_node).to_html(),
            LeafNode(
                "img",
                value=None,
                props={"src": "https://picsum.photos/200/200", "alt": "i'm alt text"},
            ).to_html(),
        )


class TestSplitNodesDelimiter(unittest.TestCase):
    node_italic = TextNode("this is *a lot of sarcastic* business", TextType.TEXT)
    node_bold = TextNode("this is **some serious** business", TextType.TEXT)
    node_code = TextNode("this is `beep boop` business", TextType.TEXT)
    split_node_italic = split_nodes_delimiter([node_italic], "*", TextType.ITALIC)
    split_node_bold = split_nodes_delimiter([node_bold], "**", TextType.BOLD)
    split_node_code = split_nodes_delimiter([node_code], "`", TextType.CODE)

    def test_italic(self):
        self.assertEqual(
            self.split_node_italic,
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("a lot of sarcastic", TextType.ITALIC),
                TextNode(" business", TextType.TEXT),
            ],
        )

    def test_bold(self):
        self.assertEqual(
            self.split_node_bold,
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("some serious", TextType.BOLD),
                TextNode(" business", TextType.TEXT),
            ],
        )

    def test_code(self):
        self.assertEqual(
            self.split_node_code,
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("beep boop", TextType.CODE),
                TextNode(" business", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
