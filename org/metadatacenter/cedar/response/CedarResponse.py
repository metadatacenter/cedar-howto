class CedarResponse:
    def __init__(self, status_code, status_message, response_body):
        self.status_code = status_code
        self.status_message = status_message
        self.response_body = response_body

    def __str__(self):
        return f"Status Code: {self.status_code}, Status Message: {self.status_message}, Response Body: {self.response_body}"