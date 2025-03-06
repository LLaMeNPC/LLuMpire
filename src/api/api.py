
class ApiCallResult:

    def __init__(self, text, token_count) -> None:
        self.text = text
        self.token_count = token_count

    def get_result_text(self) -> str:
        return f"----- text:\n{self.text}\n----- token_count: {self.token_count}\n"

    #def print(self) -> None:
    #    print(f"----- text:\n{self.text}\n")
    #    print(f"----- token_count: {self.token_count}\n")

class Api:

    def __init__(self) -> None:
        pass

    def request(self, input) -> ApiCallResult:
        raise Exception("Api 'request' method not overwritten")


