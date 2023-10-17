from enum import Enum


class CedarPublicationStatusFilter(Enum):
    DRAFT = {
        'value': 'bibo:draft'
    }
    PUBLISHED = {
        'value': 'bibo:published'
    }
    ALL = {
        'value': 'all'
    }
