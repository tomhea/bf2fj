class CompilerException(Exception):
    pass


class InnerException(CompilerException):
    pass


class CharDoesntMatchHandler(InnerException):
    pass


class BrainfuckCodeException(CompilerException):
    pass


class BrainfuckUnbalancedBrackets(BrainfuckCodeException):
    pass
