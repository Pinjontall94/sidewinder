class HTMLNode:
    def __init__(
            self,
            tag=None,
            value=None,
            children=None,
            props=None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode(\n\t<{self.tag}>,\n\t{self.value},\n\tchildren: {self.children},\n\tprops: {self.props}\n)"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_repr = ''
        for key, val in self.props.items():
            props_repr += f' {key}="{val}"'  # leading space is important!
        return props_repr


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        return f"<{self.tag}>{self.value}</{self.tag}>"
