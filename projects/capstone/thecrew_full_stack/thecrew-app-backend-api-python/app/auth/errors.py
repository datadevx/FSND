class AuthError(Exception):
    def __init__(self, code, description, status_code):
        self.code = code
        self.description = description
        self.status_code = status_code

    def __repr__(self):
        return f'<AuthError {self.code}: {self.description}>'
