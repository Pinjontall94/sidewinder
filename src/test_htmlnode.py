import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    node = HTMLNode(
        tag="a",
        value="does the name gooby ring a bell?",
        children=None,
        props={
            "href": "https://www.google.com",
            "target": "_blank",
        }
    )

    def test_props_to_html(self):
        # NOTE: the leading space before 'href' is significant
        self.assertEqual(self.node.props_to_html(),
                         ' href="https://www.google.com" target="_blank"')

    def test_node_repr(self):
        self.assertEqual(
            str(self.node),
            'HTMLNode(\n\t<a>,\n\tdoes the name gooby ring a bell?,\n\tchildren: None,\n\tprops: {\'href\': \'https://www.google.com\', \'target\': \'_blank\'}\n)'
        )


class TestLeafNode(unittest.TestCase):
    leaf = LeafNode("p", "henlo")
    leaf2 = LeafNode(None, "howdy")

    def test_children(self):
        self.assertIsNone(self.leaf.children)

    def test_value(self):
        self.assertEqual(self.leaf.value, "henlo")

    def test_to_html(self):
        self.assertEqual(self.leaf.to_html(), "<p>henlo</p>")
    
    def test_to_html_none_tag(self):
        self.assertEqual(self.leaf2.to_html(), "howdy")


class TestParentNode(unittest.TestCase):
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    node_nest = ParentNode(
        "span",
        [
            ParentNode(
                "p",
                [
                    LeafNode("b", "i'm shouting"),
                    LeafNode(None, "i'm normal"),
                    LeafNode("i", "i'm spicy")
                ])
        ]
    )

    node_empty = ParentNode("div", children=[])

    def test_no_value(self):
        self.assertIsNone(self.node.value)

    def test_children(self):
        self.assertIsNotNone(self.node.children)

    def test_to_html(self):
        self.assertEqual(
            self.node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
    
    def test_to_html_nested(self):
        self.assertEqual(
            self.node_nest.to_html(),
            "<span><p><b>i'm shouting</b>i'm normal<i>i'm spicy</i></p></span>"
        )
    
    def test_to_html_empty(self):
        self.assertEqual(
            self.node_empty.to_html(),
            "<div></div>"
        )


if __name__ == "__main__":
    unittest.main()
