from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode does not have a tag")
        html = f'<{self.tag}{self.props_to_html()}>'
        for child in self.children:
            html += f'{child.to_html()}'
        html += f'</{self.tag}>'
        return html
