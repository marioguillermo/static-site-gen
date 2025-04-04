from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(self, tag, value: str, props: dict = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf node must have a value")

        if self.tag is None:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
