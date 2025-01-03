class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode(\n\t<{self.tag}>,\n\t{self.value},\n\tchildren: {self.children},\n\tprops: {self.props}\n)"

    def to_html(self):
        raise NotImplementedError("Raw HTMLNode found: ", self.tag)

    def props_to_html(self):
        props_repr = ""
        for key, val in self.props.items():
            props_repr += f' {key}="{val}"'  # leading space is important!
        return props_repr


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.tag is None:
            return f"{self.value}"
        elif self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            props_text = ""
            for key, val in self.props.items():
                props_text += f'{key}="{val}" '
            return f"<{self.tag} {props_text}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None) -> None:
        super().__init__(tag, value=None, children=children, props=props)
        if self.tag is None:
            raise ValueError("ParentNode 'tag' field cannot be None")
        elif self.children is None:
            raise ValueError("ParentNode 'children' field must contain a list")
        else:
            pass

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.children):
            raise StopIteration
        child_node = self.children[self.index]
        self.index += 1
        return child_node

    def to_html(self):
        parent_close_tag = f"</{self.tag}>"
        if self.props:
            props_text = ""
            for key, val in self.props.items():
                props_text += f'{key}="{val}" '
                parent_open_tag = f"<{self.tag} {props_text}>"
        else:
            parent_open_tag = f"<{self.tag}>"
        inner_html = ""
        for leaf in self.children:
            inner_html += leaf.to_html()
        return parent_open_tag + inner_html + parent_close_tag
