from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import split_nodes_delimiter, text_node_to_html_node

node_invalid = TextNode("this is **a load of invalid markdown", TextType.TEXT)
new_nodes = split_nodes_delimiter([node_invalid], "**", TextType.BOLD)
for node in new_nodes:
    print(node)
