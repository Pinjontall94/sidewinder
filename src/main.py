from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

dummy_text_node = TextNode("This is a text node",
                           TextType.BOLD, "https://www.boot.dev")
dummy_html_node = HTMLNode(
    tag="a",
    value="does the name gooby ring a bell?",
    children=None,
    props={
        "href": "https://www.google.com",
        "target": "_blank",
    }
)
leaf1 = LeafNode("p", "This is a paragraph of text.")
leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
print(dummy_text_node)
print(dummy_html_node)
print(leaf1.to_html())
print(leaf2.to_html())
