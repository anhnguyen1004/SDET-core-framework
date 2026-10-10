class DatabaseClientError(Exception):
    """Raised when the database client is not properly initialized or query fails."""


class FileReadError(Exception):
    """Raised when a file cannot be found or read."""


class FileSaveError(Exception):
    """Raised when a file cannot be saved."""


class DataProcessingError(Exception):
    """Raised when data processing (e.g. filtering) encounters an unexpected error."""
