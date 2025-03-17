class HtmlNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        text = ""
        for key, value in self.props.items():
            text += f' {key}="{value}"'
        return text

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"
