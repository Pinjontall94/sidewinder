import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    # def test_to_html(self):
    #     node = HTMLNode()
    #     self.assertIsNotNone(node.to_html())

    def test_props_to_html(self):
        test_a_prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=test_a_prop)
        # NOTE: the leading space before 'href' is significant
        self.assertEqual(node.props_to_html(),
                         ' href="https://www.google.com" target="_blank"')

    def test_node_repr(self):
        node = HTMLNode(
            tag="a",
            value="does the name gooby ring a bell?",
            children=None,
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            str(node), 
            'HTMLNode(\n\t<a>,\n\tdoes the name gooby ring a bell?,\n\tchildren: None,\n\tprops: {\'href\': \'https://www.google.com\', \'target\': \'_blank\'}\n)'
            )


class TestLeafNode(unittest.TestCase):
    leaf = LeafNode("p", "henlo")
    def test_children(self):
        self.assertIsNone(self.leaf.children)
    
    def test_value(self):
        self.assertEqual(self.leaf.value, "henlo")
    
    def test_to_html(self):
        self.assertEqual(self.leaf.to_html(), "<p>henlo</p>")

if __name__ == "__main__":
    unittest.main()
