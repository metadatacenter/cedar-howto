from org.metadatacenter.testdata.ResourceHandler import ResourceHandler


class TemplateHandler(ResourceHandler):
    def __init__(self):
        super().__init__('templates', 'templates/empty-template.json')
