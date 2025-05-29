class APIResponse:

    def __init__(self, code=200, message='OK', data=None):
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return f"APIResponse(code={self.code}, message='{self.message}', data={self.data})"