import unittest
from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
