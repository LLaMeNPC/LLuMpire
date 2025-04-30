from log import log

class ApiCallResult:

    def __init__(self, text, token_count) -> None:
        self.text = text
        self.token_count = token_count

    def get_result_text(self) -> str:
        return f"----- judgement:\n{self.text}\n----- token_count: {self.token_count}\n"

    def get_text(self) -> str:
        return self.text

    # Returns last character, asuming it is a one digit score value
    def get_judgement_value(self) -> int: 
        return int(self.text.strip().strip(",.-\"'")[-1])

    #def print(self) -> None:
    #    print(f"----- text:\n{self.text}\n")
    #    print(f"----- token_count: {self.token_count}\n")

class Api:

    def __init__(self) -> None:
        self.retry_num = 0
        self.request_num = 0

    def request(self, input) -> ApiCallResult:
        raise Exception("Api 'request' method not overwritten")

    def register_retry(self):
        self.retry_num += 1
        log("Request failed - retrying")
