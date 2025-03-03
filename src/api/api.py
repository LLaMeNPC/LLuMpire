
class api_call_result:

    def __init__(self, text, token_count) -> None:
        self.text = text
        self.token_count = token_count

    def print(self) -> None:
        print(f"----- text:\n{self.text}\n")
        print(f"----- token_count: {self.token_count}\n")

class api:

    def __init__(self) -> None:
        pass

    def request(self, input) -> api_call_result:
        raise Exception("Api 'request' method not overwritten")


