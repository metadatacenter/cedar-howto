from enum import Enum


class CedarResourceType(Enum):
    FOLDER = {
        'value': 'folder',
        'prefix': 'folders',
        'atType': None,
    }
    FIELD = {
        'value': 'field',
        'prefix': 'template-fields',
        'atType': 'https://schema.metadatacenter.org/core/TemplateField'
    }
    ELEMENT = {
        'value': 'element',
        'prefix': 'template-elements',
        'atType': 'https://schema.metadatacenter.org/core/TemplateElement'
    }
    TEMPLATE = {
        'value': 'template',
        'prefix': 'templates',
        'atType': 'https://schema.metadatacenter.org/core/Template'
    }
    INSTANCE = {
        'value': 'instance',
        'prefix': 'template-instances',
        'atType': None
    }
    CATEGORY = {
        'value': 'category',
        'prefix': 'categories',
        'atType': None
    }
    NONE = {
        'value': None,
        'prefix': None,
        'atType': None
    }
