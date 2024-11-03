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


def split_nodes_image(nodes):
    result_nodes = []
    for node in nodes:
        image = extract_markdown_images(node.text)
        if not image:
            # If no images, simply pass node to result list
            result_nodes.append(node)
        else:
            # Only grab first image; for multiple images per node, use recursion
            alt_text, image_url = image[0][0], image[0][1]
            split_nodes_list = []
            split_text = node.text.split(f"![{alt_text}]({image_url})", 1)
            if len(split_text) == 2 and not split_text[0]:
                # Case: image in beginning of the node
                # Append image node, then text node
                split_nodes_list.extend(
                    [
                        TextNode(alt_text, TextType.IMAGE, image_url),
                        TextNode(split_text[1], TextType.TEXT),
                    ]
                )
            elif len(split_text) == 2 and not split_text[1]:
                # Case: image in the end of the node
                split_nodes_list.extend(
                    [
                        TextNode(split_text[0], TextType.TEXT),
                        TextNode(alt_text, TextType.IMAGE, image_url),
                    ]
                )
            elif len(split_text) == 2 and split_text[0] and split_text[1]:
                # Case: image in the middle
                split_nodes_list.extend(
                    [
                        TextNode(split_text[0], TextType.TEXT),
                        TextNode(alt_text, TextType.IMAGE, image_url),
                        TextNode(split_text[1], TextType.TEXT),
                    ]
                )
            else:
                raise ValueError(
                        "Invalid node passed to split_nodes_image: ",
                        node
                        )
        result_nodes.extend(split_nodes_list)
    return result_nodes


def split_nodes_link(nodes):
    result_nodes = []
    for node in nodes:
        link = extract_markdown_links(node.text)
        if not link:
            # If no links, simply pass node to result list
            result_nodes.append(node)
        else:
            # Only grab first link; for multiple links per node, use recursion
            link_text, link_url = link[0][0], link[0][1]
            split_nodes_list = []
            split_text = node.text.split(f"[{link_text}]({link_url})", 1)
            if len(split_text) == 2 and not split_text[0]:
                # Case: link in beginning of the node
                # Append link node, then text node
                split_nodes_list.extend(
                    [
                        TextNode(link_text, TextType.LINK, link_url),
                        TextNode(split_text[1], TextType.TEXT),
                    ]
                )
            elif len(split_text) == 2 and not split_text[1]:
                # Case: link in the end of the node
                split_nodes_list.extend(
                    [
                        TextNode(split_text[0], TextType.TEXT),
                        TextNode(link_text, TextType.LINK, link_url),
                    ]
                )
            elif len(split_text) == 2 and split_text[0] and split_text[1]:
                # Case: link in the middle
                split_nodes_list.extend(
                    [
                        TextNode(split_text[0], TextType.TEXT),
                        TextNode(link_text, TextType.LINK, link_url),
                        TextNode(split_text[1], TextType.TEXT),
                    ]
                )
            else:
                raise ValueError(
                        "Invalid node passed to split_nodes_link: ",
                        node
                        )
            result_nodes.extend(split_nodes_list)
    return result_nodes
