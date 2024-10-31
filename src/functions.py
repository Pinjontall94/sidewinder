from typing import List
from textnode import TextNode, TextType
from htmlnode import LeafNode
import re


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Convert intermediate text node reprs to html nodes."""
    match text_node.text_type:
        case "normal":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case "image":
            return LeafNode(
                "img",
                value=None,
                props={
                    "src": text_node.url,
                    "alt": text_node.text,
                },
            )
        case _:
            raise ValueError(f"Invalid TextType value: {text_node.text_type}")


def split_nodes_delimiter(
    nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    result_nodes = []
    for node in nodes:
        split_nodes_list = []
        split_text = node.text.split(delimiter)
        for index, text in enumerate(split_text):
            if len(split_text) % 2 == 0:
                raise ValueError(f"Unterminated markdown text in node: {node}")
            elif not text:
                # Case: Delimited text in beginning, index 0 == ""
                pass
            elif index % 2 != 0:
                # Case: delimited text
                # NOTE: when modifying for nested delimiters, don't just append as text_type
                # use .find() or .index() to determine outer and inner nesting
                # NOTE: Could implement nested with recursive call and eliminating delimiter
                # and text_type args in favor of {delim -> type} dict
                split_nodes_list.append(TextNode(text, text_type))
            else:
                # Case: non-delimited text
                split_nodes_list.append(TextNode(text, TextType.TEXT))
        result_nodes.extend(split_nodes_list)
    return result_nodes


def extract_markdown_images(text):
    try:
        return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    except Exception as e:
        print(f"extract_markdown_images error: {e}")


def extract_markdown_links(text):
    try:
        return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    except Exception as e:
        print(f"extract_markdown_links error: {e}")
