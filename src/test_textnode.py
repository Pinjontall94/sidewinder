import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_italic(self):
        node = TextNode("this is a text node", TextType.ITALIC)
        node2 = TextNode("this is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
    
    def test_eq_normal(self):
        node = TextNode("this is a text node", TextType.NORMAL)
        node2 = TextNode("this is a text node", TextType.NORMAL)
        self.assertEqual(node, node2)
    
    def test_ne_url(self):
        node = TextNode("this is a text node", TextType.NORMAL, "index.html")
        node2 = TextNode("this is a text node", TextType.NORMAL, "articles/page1.html")
        self.assertNotEqual(node, node2)
    
    def test_ne_text_type(self):
        node = TextNode("this is a text node", TextType.NORMAL)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
