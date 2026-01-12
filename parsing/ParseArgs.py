class ParseArgs:
    """Will split correctly the important arguments of input"""

    def __init__(self, args: list[str]) -> None:
        self.src_path: str = self.get_flag_value("--src-file", args)
        self.dst_path: str = self.get_flag_value("--dst-file", args)

        self.src_lang: str = self.get_flag_value("--src-lang", args)
        self.dst_lang: str = self.get_flag_value("--dst-lang", args)

    @staticmethod
    def get_flag_value(flag: any, lst: list) -> any:
        for i in range(len(lst) - 1):
            if lst[i] == flag:
                value: any = lst[i + 1]
                del lst[i + 1]
                return value
        return None
