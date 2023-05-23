from threading import Lock


class Singleton:
    """
    Thread-safe implementation of Singleton.
    """

    _instance = None
    """Instances of our objects."""

    _lock = Lock()
    """
    A lock object that will be used to synchronize threads during first access to the Singleton.
    """

    def __new__(cls, *args, **kwarg):
        if cls._instance is None:
            with cls._lock:
                cls._instance = super().__new__(cls)
        return cls._instance
