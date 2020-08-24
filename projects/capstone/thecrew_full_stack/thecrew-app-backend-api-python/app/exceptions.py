class ValidationError(ValueError):
    def __init__(self, field, code, description):
        self.field = field
        self.code = code
        self.description = description

    def __repr__(self):
        return f'<ValidationError {self.field} {self.code}>'


class ValidationsError(Exception):
    def __init__(self, message, errors=[]):
        self.message = message
        self.errors = errors if errors else []

    def add_error(self, field, code, description):
        self.errors.append(ValidationError(field, code, description))

    def has_errors(self):
        return bool(self.errors)

    def get_error(self, field, code):
        return next(filter(lambda x: x.field == field and x.code == code,
                           self.errors), None)

    def __repr__(self):
        return f'<ValidationsError {self.message}; errors={self.errors}>'
