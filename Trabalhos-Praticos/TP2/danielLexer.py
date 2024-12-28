from ply.lex import TOKEN
import ply.lex as lex

class MyLexer(object):

    def __init__(self):
        self.reserved_map = {r.lower(): r for r in self.reserved}
        self.lexer = lex.lex(module=self, debug=False)

    reserved = (
        # Keywords
        'BREAK', 'CASE', 'CONST', 'CONTINUE', 'DEFAULT', 'ELSE',
        'FOR', 'FUNC', 'IF', 'RETURN', 'STRUCT', 'SWITCH',
        'TYPE', 'VAR',

        # Types
        'INT', 'FLOAT', 'STRING', 'BOOL', 'TRUE', 'FALSE'
    )

    tokens = reserved + (
        # Identifiers and Literals
        'ID',
        'STRING_LITERAL',
        'NUMBER_LITERAL',

        # Arithmetic Operators
        'SUM', 'DIFFERENCE', 'PRODUCT', 'QUOTIENT', 'REMAINDER',

        # Bitwise Operators
        'BITWISEAND', 'BITWISEOR', 'BITWISEXOR', 'BITCLEAR',
        'LEFTSHIFT', 'RIGHTSHIFT',

        # Assignment Operators
        'PLUSEQUAL', 'MINUSEQUAL', 'STAREQUAL', 'DIVIDEEQUAL', 'PERCENTEQUAL',
        'PLUSPLUS', 'MINUSMINUS', 'BITWISEANDEQUAL', 'BITWISEOREQUAL',
        'BITWISEXOREQUAL', 'LEFTSHIFTEQUAL', 'RIGHTSHIFTEQUAL',
        'BITCLEAREQUAL', 'EQUALITY',

        # Comparison Operators
        'LESS', 'GREATER', 'EQUAL', 'CONDITIONALAND',
        'CONDITIONALOR', 'NOT', 'TILDE',

        # Additional Comparison Operators
        'NOTEQUAL', 'LESSOREQUAL', 'GREATEROREQUAL',
        'WALRUS', 'THREEDOTS',

        # Parentheses, Brackets, and Braces
        'LPAREN', 'LBRACKET', 'LBRACE',
        'RPAREN', 'RBRACKET', 'RBRACE',

        # Miscellaneous
        'COMMA', 'DOT',
        'SEMICOLON', 'COLON'
    )

    # Arithmetic Operators
    t_SUM = r'\+'
    t_DIFFERENCE = r'\-'
    t_PRODUCT = r'\*'
    t_QUOTIENT = r'\/'
    t_REMAINDER = r'\%'

    # Bitwise Operators
    t_BITWISEAND = r'\&'
    t_BITWISEOR = r'\|'
    t_BITWISEXOR = r'\^'
    t_BITCLEAR = r'\&\^'
    t_LEFTSHIFT = r'\<\<'
    t_RIGHTSHIFT = r'\>\>'

    # Assignment Operators
    t_PLUSEQUAL = r'\+\='
    t_MINUSEQUAL = r'\-\='
    t_STAREQUAL = r'\*\='
    t_DIVIDEEQUAL = r'\/\='
    t_PERCENTEQUAL = r'\%\='
    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'\-\-'
    t_BITWISEANDEQUAL = r'\&\='
    t_BITWISEOREQUAL = r'\|\='
    t_BITWISEXOREQUAL = r'\^\='
    t_LEFTSHIFTEQUAL = r'\<\<\='
    t_RIGHTSHIFTEQUAL = r'\>\>\='
    t_BITCLEAREQUAL = r'\&\^\='
    t_EQUALITY = r'\=\='

    # Comparison Operators
    t_LESS = r'\<'
    t_GREATER = r'\>'
    t_EQUAL = r'\='
    t_CONDITIONALAND = r'\&\&'
    t_CONDITIONALOR = r'\|\|'
    t_NOT = r'\!'
    t_TILDE = r'\~'

    # Additional Comparison Operators
    t_NOTEQUAL = r'\!\='
    t_LESSOREQUAL = r'\<\='
    t_GREATEROREQUAL = r'\>\='
    t_WALRUS = r'\:\='
    t_THREEDOTS = r'\.\.\.'

    # Parentheses, Brackets, and Braces
    t_LPAREN = r'\('
    t_LBRACKET = r'\['
    t_LBRACE = r'\{'
    t_RPAREN = r'\)'
    t_RBRACKET = r'\]'
    t_RBRACE = r'\}'

    # Miscellaneous
    t_COMMA = r'\,'
    t_DOT = r'\.'
    t_SEMICOLON = r'\;'
    t_COLON = r'\:'

    # -- Tokens --------------------------------------
    identifier = r'[a-zA-Z_][a-zA-Z_0-9]*'

    floatUni = r'\d+\.\d+'                      # 3.14 or 123.456
    floatDec = r'\.\d+'                         # .05 OR .945
    integer = r'\d+'                            # 314 or 123456
    number = r'(' + floatUni + '|' + floatDec + '|' + integer + r')'

    string = r'\"([^\\\n]|(\\.))*?\"'

    comment = r'(/\*(.|\n)*?\*/)|(//.*)'



    @TOKEN(identifier)
    def t_ID(self, t):
        t.type = self.reserved_map.get(t.value.lower(), 'ID')
        return t

    @TOKEN(number)
    def t_NUMBER_LITERAL(self, t):
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    @TOKEN(string)
    def t_STRING_LITERAL(self, t):
        t.value = t.value[1:-1]
        return t

    @TOKEN(comment)
    def t_COMMENT(self, t):
        pass

    t_ignore = ' \t'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def test(self):
        print("Type 'exit lexer' to stop the lexer.")

        while True:
            try:
                s = input('Enter expression: ')

                if s.lower() == 'exit lexer':
                    print("Exiting the lexer...")
                    break

                self.lexer.input(s)
                for token in self.lexer:
                    print(f"Token( Type: {token.type}, Value: {token.value} )")

            except EOFError:
                break

if __name__ == '__main__':
    lexer = MyLexer()
    lexer.test()