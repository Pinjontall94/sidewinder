import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from functions import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)


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


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = " ".join(
            (
                "This is text with ![the ferry building](https://unsplash.com/photos/w-palm-trees-in-front-of-clock-tower-HwCKc2ej_NM)",
                "and ![the golden gate bridge](https://unsplash.com/photos/a-view-of-the-golden-gate-bridge-in-the-fog-UdWZNa83lG8)",
            )
        )
        self.assertEqual(
            extract_markdown_images(text),
            [
                (
                    "the ferry building",
                    "https://unsplash.com/photos/w-palm-trees-in-front-of-clock-tower-HwCKc2ej_NM",
                ),
                (
                    "the golden gate bridge",
                    "https://unsplash.com/photos/a-view-of-the-golden-gate-bridge-in-the-fog-UdWZNa83lG8",
                ),
            ],
        )

    def test_extract_markdown_links(self):
        text = " ".join(
            (
                "This is text with [EFF](https://www.eff.org/)",
                "and [Codeberg](https://codeberg.org/) links",
            )
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("EFF", "https://www.eff.org/"), ("Codeberg", "https://codeberg.org/")],
        )


class TestSplitImagesLinks(unittest.TestCase):
    image_node_start = TextNode(
            "![the golden gate bridge](https://unsplash.com/photos/a-view-of-the-golden-gate-bridge-in-the-fog-UdWZNa83lG8) in all its glory",
            TextType.TEXT
            )

    image_node_middle = TextNode(
            "Behold:![the golden gate bridge](https://unsplash.com/photos/a-view-of-the-golden-gate-bridge-in-the-fog-UdWZNa83lG8) the bridge in fog",
            TextType.TEXT
            )

    image_node_end = TextNode(
            "Behold, ![the golden gate bridge](https://unsplash.com/photos/a-view-of-the-golden-gate-bridge-in-the-fog-UdWZNa83lG8)",
            TextType.TEXT
            )

    link_node_start = TextNode(
            "[Here's](https://gnu.org) a link to GNU",
            TextType.TEXT
            )

    link_node_middle = TextNode(
            "And a [link](https://eff.org) to EFF",
            TextType.TEXT
            )

    link_node_end = TextNode(
            "Have a link to [my website](http://catgirlwebinteractive.com/)",
            TextType.TEXT
            )

    def test_split_nodes_image_start(self):
        self.assertEqual(
                split_nodes_image([self.image_node_start]),
                [
                    TextNode(
                        "the golden gate bridge",
                        TextType.IMAGE,
                        "https://unsplash.com/photos/a-view-of-the-golden-gate-bridge-in-the-fog-UdWZNa83lG8"
                        ),
                    TextNode(" in all its glory", TextType.TEXT),
                ],
        )

    def test_split_nodes_image_middle(self):
        self.assertEqual(
                split_nodes_image([self.image_node_middle]),
                [
                    TextNode("Behold:", TextType.TEXT),
                    TextNode(
                        "the golden gate bridge",
                        TextType.IMAGE,
                        "https://unsplash.com/photos/a-view-of-the-golden-gate-bridge-in-the-fog-UdWZNa83lG8"
                        ),
                    TextNode(" the bridge in fog", TextType.TEXT),
                ],
        )

    def test_split_nodes_image_end(self):
        self.assertEqual(
                split_nodes_image([self.image_node_end]),
                [
                    TextNode("Behold, ", TextType.TEXT),
                    TextNode(
                        "the golden gate bridge",
                        TextType.IMAGE,
                        "https://unsplash.com/photos/a-view-of-the-golden-gate-bridge-in-the-fog-UdWZNa83lG8"
                        ),
                ],
        )

    def test_split_nodes_link_start(self):
        self.assertEqual(
                split_nodes_link([self.link_node_start]),
                [
                    TextNode("Here's", TextType.LINK, "https://gnu.org"),
                    TextNode(" a link to GNU", TextType.TEXT)
                ],
        )

    def test_split_nodes_link_middle(self):
        self.assertEqual(
                split_nodes_link([self.link_node_middle]),
                [
                    TextNode("And a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://eff.org"),
                    TextNode(" to EFF", TextType.TEXT),
                ],
        )

    def test_split_nodes_link_end(self):
        self.assertEqual(
                split_nodes_link([self.link_node_end]),
                [
                    TextNode("Have a link to ", TextType.TEXT),
                    TextNode("my website", TextType.LINK, "http://catgirlwebinteractive.com/"),
                ],
        )


if __name__ == "__main__":
    unittest.main()
