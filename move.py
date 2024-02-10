from square import Square


class Move:
    def __init__(self, initial: Square, final: Square) -> None:
        self.initial = initial
        self.final = final

    def __eq__(self, __value: object) -> bool:
        return self.initial == __value.initial and self.final == __value.final
