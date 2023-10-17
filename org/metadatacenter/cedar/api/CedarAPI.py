class CedarAPI():
    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key

    def get_field_api(self):
        from org.metadatacenter.cedar.api.CedarFieldAPI import CedarFieldAPI
        return CedarFieldAPI(self.host, self.api_key)

    def get_element_api(self):
        from org.metadatacenter.cedar.api.CedarElementAPI import CedarElementAPI
        return CedarElementAPI(self.host, self.api_key)

    def get_template_api(self):
        from org.metadatacenter.cedar.api.CedarTemplateAPI import CedarTemplateAPI
        return CedarTemplateAPI(self.host, self.api_key)

    def get_folder_content_api(self):
        from org.metadatacenter.cedar.api.CedarFolderContentAPI import CedarFolderContentAPI
        return CedarFolderContentAPI(self.host, self.api_key)

    def get_category_api(self):
        from org.metadatacenter.cedar.api.CedarCategoryAPI import CedarCategoryAPI
        return CedarCategoryAPI(self.host, self.api_key)

    def get_command_api(self):
        from org.metadatacenter.cedar.api.CedarCommandAPI import CedarCommandAPI
        return CedarCommandAPI(self.host, self.api_key)
