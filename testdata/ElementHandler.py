from testdata.ResourceHandler import ResourceHandler


class ElementHandler(ResourceHandler):
    def __init__(self):
        super().__init__('template-elements', 'elements/empty-element.json')
