class PromptsHubError(Exception):
    """Base class for PromptsHub exceptions."""

class CategoryNotFoundError(PromptsHubError):
    pass

class ConnectionError(PromptsHubError):
    pass


class NotFoundError(PromptsHubError):
    pass

class CategoryNotFoundError(PromptsHubError):
    pass

class PromptNotFoundError(PromptsHubError):
    pass

class PromptMissingVariablesError(PromptsHubError):
    def __init__(self, missing_variables):
        self.missing_variables = missing_variables
        super().__init__(f"Missing variables: {', '.join(missing_variables)}")

class NoValidModelError(PromptsHubError):
    pass

class NotConnectedError(PromptsHubError):
    pass

