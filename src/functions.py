from typing import List
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from bs4 import BeautifulSoup
import os
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


def text_to_children(text: str) -> List[HTMLNode]:
    text_nodes = text_to_text_nodes(text)
    result = []
    for node in text_nodes:
        if node.text_type == "text":
            result.append(LeafNode(None, node.text))
        else:
            result.append(text_node_to_html_node(node))
    return result


def markdown_to_html_node(markdown: str) -> ParentNode:
    # Split markdown into blocks
    block_list = markdown_to_blocks(markdown)
    # Loop over blocks
    children = []
    for block in block_list:
        block_type = block_to_block_type(block)
        block_lines = block.split("\n")
        #   Depending on type, create new HTMLNode with appropriate data
        match block_type:
            case "heading":
                heading = block_lines[0]
                hashes = heading.split(" ")[0]
                num_hashtags = 0
                for hashtag in hashes:
                    num_hashtags += 1
                trimmed_heading = heading[num_hashtags + 1 :]
                children.append(LeafNode(f"h{num_hashtags}", trimmed_heading))
            case "code":
                middle_of_block = "\n".join(block_lines[1:-1])
                children.append(ParentNode("pre", [LeafNode("code", middle_of_block)]))
            case "quote":
                trimmed_block = "\n".join([line[2:] for line in block_lines])
                children.append(
                    ParentNode(
                        "blockquote", ParentNode("p", text_to_children(trimmed_block))
                    )
                )
            case "unordered_list":
                list_elements = []
                for line in block_lines:
                    trimmed_line = line[2:]  # * ^from here onward
                    processed_nodes = text_to_children(trimmed_line)
                    if len(processed_nodes) == 1 and isinstance(
                        processed_nodes[0], str
                    ):
                        # If processed_nodes is just one string of plain text
                        new_li = LeafNode("li", processed_nodes[0])
                    else:
                        new_li = ParentNode("li", processed_nodes)
                    list_elements.append(new_li)
                children.append(ParentNode("ul", list_elements))
            case "ordered_list":
                list_elements = []
                for line in block_lines:
                    trimmed_line = line[3:]  # 1. ^from here onward
                    processed_nodes = text_to_children(trimmed_line)
                    if len(processed_nodes) == 1 and isinstance(
                        processed_nodes[0], str
                    ):
                        # If processed_nodes is just one string of plain text
                        new_li = LeafNode("li", processed_nodes[0])
                    else:
                        new_li = ParentNode("li", processed_nodes)
                    list_elements.append(new_li)
                children.append(ParentNode("ol", list_elements))
            case _:
                # Treat any other block as a paragraph automatically
                children.append(ParentNode("p", text_to_children(block)))
    return ParentNode("div", children)


def extract_title(markup, extension):
    markup_lines = markup.split("\n")
    if extension == ".md":
        title_pattern = r"(?<=^#\s).*"
    elif extension == ".html":
        title_pattern = r"(?<=<title>).*(?=<\/title>)"
    else:
        raise ValueError("Invalid markup type")
    for line in markup_lines:
        if match := re.findall(title_pattern, line):
            # Grab the first match and remove surrounding whitespace
            return match[0].strip()
    # If no title is found, raise an exception here
    raise EOFError("No title found in markup passed")


def generate_page(markup_path, template_path, html_path):
    print(f"Making page from {markup_path} to {html_path} with {template_path}")
    _, extension = os.path.splitext(markup_path)
    with open(markup_path, "r") as file:
        markup = file.read()
    with open(template_path, "r") as file:
        template = [line.rstrip() for line in file]

    # Dispatch processing based on markup extension
    if extension == ".md":
        title = extract_title(markup, extension)
        content_html = markdown_to_html_node(markup).to_html()
    elif extension == ".html":
        soup = BeautifulSoup(markup, "html.parser")
        title = soup.title.get_text()
        content_html = str(soup.body.encode_contents(), "utf-8")

    html = []
    for line in template:
        if match := re.findall(r"{{ Title }}", line):
            line = line.replace(match[0], title)
            html.append(line)
        elif match := re.findall(r"{{ Content }}", line):
            line = line.replace(match[0], content_html)
            html.append(line)
        else:
            html.append(line)
    formatted_html = BeautifulSoup("\n".join(html)).prettify(formatter="html5")

    if os.path.exists(os.path.dirname(html_path)):
        with open(html_path, "w") as file:
            for line in formatted_html:
                file.write(line)


def generate_page_recursive(content_path, template_path, dest_path):
    for item in os.listdir(content_path):
        item_path = os.path.join(content_path, item)
        if os.path.isfile(item_path):
            item_html = os.path.splitext(item)[0] + ".html"
            generate_page(item_path, template_path, os.path.join(dest_path, item_html))
        elif not os.path.isdir(item_path):
            raise Exception(f"Item {item} is neither file nor directory.")
        else:
            # Must be a directory in this case
            new_dest_dir = os.path.join(dest_path, item)
            os.mkdir(new_dest_dir)
            generate_page_recursive(item_path, template_path, new_dest_dir)
