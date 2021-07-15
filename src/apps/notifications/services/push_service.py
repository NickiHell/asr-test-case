class PushServiceUseCase(object):
    def __init__(self, text: str) -> None:
        self._text: str = text
