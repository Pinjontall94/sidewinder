from textnode import TextNode, TextType
from htmlnode import HTMLNode

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
print(dummy_text_node)
print(dummy_html_node)
