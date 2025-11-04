class MovieAPIException(Exception):
    """Base exception - todas herdam desta"""

    pass


class MovieNotFoundError(MovieAPIException):
    """Filme não encontrado no banco ou OMDB"""

    pass


class MovieAlreadyExistsError(MovieAPIException):
    """Tentativa de criar filme duplicado"""

    pass


class ExternalAPIError(MovieAPIException):
    """Erro ao chamar API externa (OMDB)"""

    pass
