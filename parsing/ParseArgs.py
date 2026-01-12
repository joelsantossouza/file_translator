from typing import Any
from deep_translator import GoogleTranslator
from os.path import splitext


class ParseArgs:
    """Will split correctly the important arguments of input"""

    def __init__(self, args: list[str]) -> None:
        self.src_path: str = self.get_flag_value("--src-file", args)
        self.filetype: str = splitext(self.src_path)[1]
        self.dst_path: str = self.get_flag_value("--dst-file", args)

        self.src_lang: str = self.get_flag_value("--src-lang", args)
        self.dst_lang: str = self.get_flag_value("--dst-lang", args)

        self.translator: callable = self.get_flag_translator(
            "--translator", args
        )

    @staticmethod
    def get_flag_value(flag: any, lst: list[Any]) -> any:
        for i in range(len(lst) - 1):
            if lst[i] == flag:
                value: any = lst[i + 1]
                del lst[i + 1]
                return value
        return None

    def get_flag_translator(self, flag: Any, lst: list[Any]) -> callable:
        translator: str = self.get_flag_value(flag, lst)
        if translator.lower == "googletranslator":
            return GoogleTranslator(
                source=self.src_lang,
                target=self.dst_lang
            ).tranlate
        return None
