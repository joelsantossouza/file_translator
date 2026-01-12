from typing import Any, Optional
from deep_translator import GoogleTranslator
from os.path import splitext


class ParseArgs:
    """Will split correctly the important arguments of input"""

    def __init__(self, args: list[str]) -> None:
        self.src_path: str = self.get_flag_value(
            "--src-file", args, crucial=True
        )
        self.filetype: str = splitext(self.src_path)[1]
        self.dst_path: str = self.get_flag_value(
            "--dst-file", args, crucial=True
        )

        self.src_lang: str = self.get_flag_value(
            "--src-lang", args, crucial=True
        )
        self.dst_lang: str = self.get_flag_value(
            "--dst-lang", args, crucial=True
        )

        self.translator: callable = self.get_flag_translator(
            "--translator", args, crucial=True
        )

    @staticmethod
    def get_flag_value(flag: any, lst: list[Any],
                       crucial: Optional[bool] = False) -> any:
        for i in range(len(lst) - 1):
            if lst[i] == flag:
                value: any = lst[i + 1]
                del lst[i + 1]
                return value
        if crucial:
            print(f"ERROR: You must provide a \'{flag}\' value!")
            exit(1)
        return None

    def get_flag_translator(self, flag: Any, lst: list[Any],
                            crucial: Optional[bool] = False) -> callable:
        translator: str = self.get_flag_value(flag, lst, crucial)
        if translator.lower() == "googletranslator":
            return GoogleTranslator(
                source=self.src_lang,
                target=self.dst_lang
            ).tranlate
        if crucial:
            print("ERROR: You must provide a valid translator!")
            exit(1)
        return None
