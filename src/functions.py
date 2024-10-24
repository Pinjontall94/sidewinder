from typing import List
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import LeafNode


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


class ParserStringType(Enum):
    NORMAL = "normal"
    DELIMITED = "delimited"


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    """Convert a raw markdown string into a list of consituent text nodes."""
    result_nodes = []
    delimiter_width = 2 if text_type == "bold" else 1
    for node in old_nodes:
        word_list = node.text.split()
        new_normal_text, new_delimited_text = "", ""
        parser_mode = ParserStringType.NORMAL
        for word in word_list:
            word_beginning = word[:delimiter_width]  # i.e. "**hello" -> "**"
            word_end = word[-delimiter_width:]       # "hello`" -> "`"
            word_edges = [word_beginning, word_end]
            if delimiter not in word_edges and parser_mode == ParserStringType.NORMAL:
                new_normal_text += word
            elif delimiter not in word_edges and parser_mode == ParserStringType.DELIMITED:
                new_delimited_text += word
            elif word_beginning == delimiter and parser_mode == ParserStringType.NORMAL:
                # Guard case for instances where delimited text isn't at the beginning
                if new_normal_text:
                    result_nodes.append(TextNode(new_normal_text, TextType.NORMAL))
                    new_normal_text = ""  # refresh the normal_text buffer variable
                parser_mode = ParserStringType.DELIMITED
                new_delimited_text += word[delimiter_width:]  # slice off the delimiter
            elif word_end == delimiter and parser_mode == ParserStringType.DELIMITED:
                result_nodes.append(TextNode(new_delimited_text, text_type))
                new_delimited_text = ""  # refresh the delimited_text buffer
                parser_mode = ParserStringType.NORMAL
                
