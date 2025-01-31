import ply.lex as lex
from ply.lex import TOKEN

# Lista de palavras reservadas (reserved words) usadas na linguagem
reserved = [
    # Palavras-chave
    "BREAK",
    "CASE",
    "CONTINUE",
    "DEFAULT",
    "ELSE",
    "FOR",
    "FUNC",
    "IF",
    "RETURN",
    "SWITCH",
    "VAR",
    # Tipos
    "INT",
    "FLOAT",
    "STRING",
    "BOOL",
    "VOID",
]

# Lista de nomes de tokens que inclui as palavras reservadas e outros símbolos
tokens = reserved + [
    # Operadores
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MODULO",
    "EQUALITY",
    "NOTEQUAL",
    "GREATER",
    "LESS",
    "GREATEROREQUAL",
    "LESSOREQUAL",
    "CONDITIONALAND",
    "CONDITIONALOR",
    "NOT",
    "EQUAL",
    "WALRUS",    # Operador de atribuição curta :=
    "INCREMENT", # ++
    "DECREMENT", # --
    # Delimitadores
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "LBRACKET",  # [
    "RBRACKET",  # ]
    "COMMA",
    "SEMICOLON",
    "COLON",
    # Literais
    "NUMBER_LITERAL",
    "STRING_LITERAL",
    "BOOLEAN_LITERAL",
    # Identificador
    "ID",
]

# Expressões regulares para tokens simples
t_PLUS            = r"\+"
t_MINUS           = r"-"
t_TIMES           = r"\*"
t_DIVIDE          = r"/"
t_MODULO          = r"%"
t_EQUALITY        = r"=="
t_NOTEQUAL        = r"!="
t_GREATER         = r">"
t_LESS            = r"<"
t_GREATEROREQUAL  = r">="
t_LESSOREQUAL     = r"<="
t_CONDITIONALAND  = r"&&"
t_CONDITIONALOR   = r"\|\|"
t_NOT             = r"!"
t_EQUAL           = r"="
t_WALRUS          = r":="
t_INCREMENT       = r"\+\+"
t_DECREMENT       = r"--"
t_LPAREN          = r"\("
t_RPAREN          = r"\)"
t_LBRACE          = r"\{"
t_RBRACE          = r"\}"
t_LBRACKET        = r"\["
t_RBRACKET        = r"\]"
t_COMMA           = r","
t_SEMICOLON       = r";"
t_COLON           = r":"

# Ignorar espaços e tabulações
t_ignore = " \t"

# Comentário de linha simples (//...), conta a nova linha para atualizar o número de linha
@TOKEN(r'//.*\n')
def t_COMMENT_SINGLE(t):
    t.lexer.lineno += 1

# Comentário de múltiplas linhas (/* ... */), conta todas as quebras de linha internas
@TOKEN(r'/\*([^*]|\*[^/])*\*/')
def t_COMMENT_MULTI(t):
    t.lexer.lineno += t.value.count('\n')


# Definição de literais booleanos (True/False)
@TOKEN(r"[Tt]rue|[Ff]alse")
def t_BOOLEAN_LITERAL(t):
    t.type = "BOOLEAN_LITERAL"
    t.value = True if t.value.lower() == "true" else False
    return t


# Definição de literais numéricos (inteiros ou floats)
@TOKEN(r"\d+(\.\d+)?")
def t_NUMBER_LITERAL(t):
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


# Definição de literais de string (entre aspas duplas)
@TOKEN(r"\"([^\\\n]|(\\.))*?\"")
def t_STRING_LITERAL(t):
    # Remove as aspas iniciais e finais
    t.value = t.value[1:-1]
    return t


# Definição de identificadores (ID) e verificação se são palavras reservadas
@TOKEN(r"[a-zA-Z_][a-zA-Z_0-9]*")
def t_ID(t):
    # Só aceitamos palavras reservadas se estiverem em letras minúsculas
    # e constarem na lista de reserved (em maiúsculas).
    t.type = t.value.upper() if (t.value.islower() and t.value.upper() in reserved) else "ID"
    return t


# Controlo de quebras de linha
@TOKEN(r"\n+")
def t_newline(t):
    t.lexer.lineno += len(t.value)


# Regra de erro: em caso de carácter ilegal, salta 1 posição e imprime mensagem
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)


# Construção do lexer (analisador léxico)
lexer = lex.lex(debug=False)

# Teste do lexer com um exemplo
if __name__ == "__main__":
    test_data = """
        func main() int {
            var arr int[10];
            for i := 0; i < 10; i++ {
                if arr[i] == 5 {
                    break;
                }
                continue;
            }
            return 0;
        }
    """
    lexer.input(test_data)
    for token in lexer:
        print(f"{token.type}, '{token.value}', {token.lineno}")
