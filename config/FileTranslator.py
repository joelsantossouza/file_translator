from abc import ABC, abstractmethod


class FileTranslator(ABC):
    """Abstract base class for file translations"""

    def __init__(self, translator: callable) -> None:
        self.__translator: callable = translator

    @abstractmethod
    def translate(self, dst_path: str, src_path: str) -> None:
        ...
