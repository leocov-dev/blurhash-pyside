__version__: str

def decode(
    blurhash: str,
    width: int,
    height: int,
) -> list[int]: ...
def encode(
    image: list[int],
    width: int,
    height: int,
    x: int,
    y: int,
) -> str: ...
