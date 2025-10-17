import re


# Abstract class
class Parser:
    def parse(self, data: str) -> (float, str):
        raise NotImplementedError("Calling abstract Parse method!")


class ChaseParser(Parser):
    regex_pattern = r"\$(\d+(?:\.\d+)?) transaction with (.+)"
    def parse(data: str) -> (float, str):
        match = re.search(ChaseParser.regex_pattern, data)

        if not match:
            raise ValueError(f"Couldn't parse chase email with subject: {data}")

        amount = float(match.group(1))
        merchant = match.group(2)
        return (amount, merchant)

# Client code that uses any parser
def parseEmailData(parser: Parser, data: str) -> (float, str):
    if not hasattr(parser, 'parse') or not callable(parser.parse):
        raise TypeError("Parser must have a callable 'parse' method.")

    result = parser.parse(data)
    return result
