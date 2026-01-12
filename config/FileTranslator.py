from abs import ABS, abstractmethod


class FileTranslator(ABS):
    """Abstract base class for file translations"""

    def __init__(self, translator: callable) -> None:
        self.__translator: callable = translator

    @abstractmethod
    def translate(self, dst_path: str, src_path: str) -> None:
        ...
