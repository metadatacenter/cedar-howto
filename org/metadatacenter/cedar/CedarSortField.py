from enum import Enum


class CedarSortField(Enum):
    NAME_ASC = {
        'value': 'name'
    }
    NAME_DESC = {
        'value': '-name'
    }
    NAME = NAME_ASC

    CREATED_ON_TS_ASC = {
        'value': 'createdOnTS'
    }
    CREATED_ON_TS_DESC = {
        'value': '-createdOnTS'
    }
    CREATED_ON_TS = CREATED_ON_TS_ASC

    LAST_UPDATED_ON_TS_ASC = {
        'value': 'lastUpdatedOnTS'
    }
    LAST_UPDATED_ON_TS_DESC = {
        'value': '-lastUpdatedOnTS'
    }
    LAST_UPDATED_ON_TS = LAST_UPDATED_ON_TS_ASC
