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
    TEXT = "text"
    DELIMITED = "delimited"


def text_type_by_delimiter(delimiter: str) -> TextType:
    match delimiter:
        case "*":
            return TextType.ITALIC
        case "`":
            return TextType.CODE
        case "**":
            return TextType.BOLD
        case _:
            raise ValueError("Invalid delimiter passed: ", delimiter)


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    """Convert a raw markdown string into a list of consituent text nodes."""
    result_nodes = []
    delimiter_width = len(delimiter)
    for node in old_nodes:
        word_list = node.text.split()
        new_text, new_delimited_text = [], []
        parser_mode = ParserStringType.TEXT
        for index, word in enumerate(word_list):
            word_start = word[:delimiter_width]  # i.e. "**hello" -> "**"
            word_end = word[-delimiter_width:]  # "hello`" -> "`"
            word_edges = [word_start, word_end]
            if parser_mode == ParserStringType.TEXT and delimiter not in word_edges:
                new_text.append(word)
            elif parser_mode == ParserStringType.TEXT and delimiter in word_start:
                # Add the new text with a leading space before parsing delimited text
                result_nodes.append(
                    TextNode(" ".join(new_text.copy()) + " ", TextType.TEXT)
                )
                new_text, parser_mode = [], ParserStringType.DELIMITED
                if delimiter not in word_end:
                    new_delimited_text.append(word[delimiter_width:])
                else:
                    # Case: **^hello**, delim on both ends for one word
                    new_delimited_text.append(word[delimiter_width:-delimiter_width])
                    result_nodes.append(
                        TextNode(
                            " ".join(new_delimited_text.copy()),
                            text_type_by_delimiter(delimiter),
                        )
                    )
                    new_delimited_text, parser_mode = [], ParserStringType.TEXT
            elif (
                parser_mode == ParserStringType.DELIMITED
                and delimiter not in word_edges
                and index != len(word_list) - 1
            ):
                # Case: "these are some *italic ^words written* in markdown"
                new_delimited_text.append(word)
            elif parser_mode == ParserStringType.DELIMITED and delimiter in word_end:
                # Case: "these are some *italic words ^written* in markdown"
                new_delimited_text.append(word[:-delimiter_width])
                result_nodes.append(
                    TextNode(
                        " ".join(new_delimited_text.copy()),
                        text_type_by_delimiter(delimiter),
                    )
                )
                new_delimited_text, parser_mode = (
                    [],
                    ParserStringType.TEXT,
                )
            elif (
                parser_mode == ParserStringType.DELIMITED
                and index == len(word_list) - 1
            ):
                # Case: "this is **invalid ^markdown"
                raise Exception(
                    f"Invalid markdown, text delimited by {delimiter} not terminated by word: {word}"
                )
            else:
                raise Exception(
                    f"Invalid parser state:\nMode: {parser_mode}\tWord: {word}"
                )
        if new_text:
            result_nodes.append(
                TextNode(" " + " ".join(new_text.copy()), TextType.TEXT)
            )
            new_text = []
        return result_nodes
