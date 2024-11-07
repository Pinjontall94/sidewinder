from typing import List
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
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
        if node.text_type != "text":
            # Previously delimited nodes can just be added to the result list
            result_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            for index, text in enumerate(split_text):
                if len(split_text) % 2 == 0:
                    raise ValueError(f"Unterminated markdown text in node: {node}")
                elif not text:
                    # Case: Delimited text in beginning, index 0 == ""
                    pass
                elif index % 2 != 0:
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
        split_nodes_list = []
        if not image:
            # If no images, simply pass node to result list
            result_nodes.append(node)
        else:
            # Only grab first image; for multiple images per node, use recursion
            alt_text, image_url = image[0][0], image[0][1]
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
                raise ValueError("Invalid node passed to split_nodes_image: ", node)
        # import pdb; pdb.set_trace()
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
                raise ValueError("Invalid node passed to split_nodes_link: ", node)
            result_nodes.extend(split_nodes_list)
    return result_nodes


def text_to_text_nodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    delimiter_type_map = {
        "**": TextType.BOLD,
        "*": TextType.ITALIC,
        "`": TextType.CODE,
    }
    for delimiter, text_type in delimiter_type_map.items():
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, text_type)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes


def markdown_to_blocks(markdown: str) -> List[str]:
    markdown_lines = markdown.split("\n")
    markdown_lines = [line.strip() for line in markdown_lines]
    result, block_text = [], []
    in_multiline_block = False
    for index, line in enumerate(markdown_lines):
        print("index: ", index, "line:\n", line)
        if line and not in_multiline_block and not markdown_lines[index + 1]:
            # Case: isolated line of text followed by empty line
            result.append(line)
        elif line and in_multiline_block and index == len(markdown_lines) - 1:
            # Case: last line of block ends the markdown text
            block_text.append(line)
            result.append("\n".join(block_text))
            block_text = []
            in_multiline_block = False
        elif line and not in_multiline_block and markdown_lines[index + 1]:
            # Case: first line of a multiline block
            block_text.append(line)
            in_multiline_block = True
        elif line and in_multiline_block and markdown_lines[index + 1]:
            # Case: line within the first and last lines of a block
            block_text.append(line)
        elif line and in_multiline_block and not markdown_lines[index + 1]:
            # Case: last line of a multiline block
            block_text.append(line)
            result.append("\n".join(block_text))
            block_text = []  # Clear the block_text list for any new blocks
            in_multiline_block = False
        elif not line:
            # Case: empty line between blocks and isolated lines
            pass
        else:
            raise Exception(f"markdown_to_blocks error: invalid line {line}")
    return result


def block_to_block_type(block: List[str]) -> str:
    "Returns a string representing an enum of the passed block's markdown type."
    # NOTE: This code assumes well-formed markdown is passed, so it sacrifices
    # complexity of checking every line of a block for code readability
    block_lines = block.split("\n")
    if len(block_lines) > 1:
        first_line, last_line = block_lines[0], block_lines[-1]
    else:
        first_line, last_line = block, block

    if re.findall(r"^#{1,6} ", first_line):
        # Case: 1 to 6 starting pound signs, followed by a space
        return "heading"
    elif re.findall(r"^```", first_line) and re.findall(r"^```", last_line):
        # Case: ```optional_language
        #       monospaced code
        #       ```
        return "code"
    elif re.findall(r"^> ", first_line):
        # Case: > Block of
        #       > quoted text
        return "quote"
    elif re.findall(r"^\* ", first_line):
        # Case: * A list
        #       * of unordered items
        return "unordered_list"
    elif re.findall(r"^\d\. ", first_line):
        # Case: 1. A list
        #       2. Where each item
        #       3. Has a numbered order
        for index, line in enumerate(block_lines):
            num = int(re.findall(r"^\d\. ", line)[0][0])  # Turn match: "1. " into int 1
            if (index == 0 and num != 1) or (index != num - 1):
                raise ValueError(
                    f"block_to_block_type error: malformed line passed {line}"
                )
        return "ordered_list"
    else:
        return "paragraph"


def markdown_to_html_node(markdown: str) -> ParentNode:
    # Split markdown into blocks
    block_list = markdown_to_blocks(markdown)
    # Loop over blocks
    for block in block_list:
        block_type = block_to_block_type(block)
        #   Depending on type, create new HTMLNode with appropriate data
        #   Assign correct HTMLNode children to the block node
        #     use text_node_to_html_node in text_to_children(text)
        #     ^ returns List[HTMLNode] (repr of inline markdown)

        # Make one ParentNode(tag="div") with all the processed blocks
        # as its children
        pass

    return ParentNode(tag="div", children=None)
