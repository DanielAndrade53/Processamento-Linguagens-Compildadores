import ply.yacc as yacc
from cparser.lexer import tokens

from c_ast.ast_nodes import (
    Program,
    FunctionDeclaration,
    VariableDeclaration,
    ArrayType,
    ArrayInitializer,
    ContinueStatement,
    BreakStatement,
    ExpressionStatement,
    IfStatement,
    ForStatement,
    SwitchStatement,
    SwitchCase,
    ReturnStatement,
    BinaryOp,
    UnaryOp,
    Variable,
    FunctionCall,
    ArrayAccess,
    Assignment,
    ArrayAssignment,
    Literal,
)

# ----- Precedência de operadores e outras configurações do parser -----
# A tupla 'precedence' informa ao PLY como desempatar conflitos de parsing,
# definindo a precedência e associatividade (left, right) de cada token.
precedence = (
    ("left", "CONDITIONALOR"),
    ("left", "CONDITIONALAND"),
    ("left", "EQUALITY", "NOTEQUAL"),
    ("left", "LESS", "LESSOREQUAL", "GREATER", "GREATEROREQUAL"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE", "MODULO"),
    ("right", "NOT"),
    ("right", "UMINUS"),
)

# ----- Regras principais de análise sintática (gramática) -----

# Programa completo: Conjunto de declarações globais
def p_program(p):
    "program : global_declarations"
    # Cria um nó de AST Program contendo as declarações e o número de linha
    p[0] = Program(declarations=p[1], lineno=p.lineno(1))

# Múltiplas declarações globais (concatenadas em lista)
def p_global_declarations_multiple(p):
    "global_declarations : global_declarations global_declaration"
    p[0] = p[1] + [p[2]]

# Única declaração global
def p_global_declarations_single(p):
    "global_declarations : global_declaration"
    p[0] = [p[1]]

# Declaração global de função
def p_global_declaration_func(p):
    "global_declaration : function_declaration"
    p[0] = p[1]

# Declaração global de variável (normal ou curta)
def p_global_declaration_var(p):
    """global_declaration : var_declaration
                          | short_var_declaration"""
    p[0] = p[1]

# ----- Declarações de Função -----

def p_function_declaration(p):
    """
    function_declaration : FUNC ID LPAREN parameters_opt RPAREN type block
    """
    # Cria um nó FunctionDeclaration com o nome, parâmetros, tipo de retorno,
    # corpo (bloco) e a linha correspondente.
    p[0] = FunctionDeclaration(
        name=p[2],
        params=p[4],
        return_type=p[6],
        body=p[7],
        lineno=p.lineno(1),
    )

# Parâmetros opcionais (caso vazio)
def p_parameters_opt(p):
    "parameters_opt : parameters"
    p[0] = p[1]

# Se não houver parâmetros, retorna lista vazia
def p_parameters_empty(p):
    "parameters : empty"
    p[0] = []

# Múltiplos parâmetros (separados por vírgulas)
def p_parameters_multiple(p):
    "parameters : parameters COMMA parameter"
    p[0] = p[1] + [p[3]]

# Um único parâmetro
def p_parameters_single(p):
    "parameters : parameter"
    p[0] = [p[1]]

# Definição de um parâmetro (nome + tipo)
def p_parameter(p):
    "parameter : ID type"
    p[0] = {"name": p[1], "type": p[2]}

# Bloco de código: { ... }
def p_block(p):
    "block : LBRACE block_contents RBRACE"
    p[0] = p[2]

# Bloco vazio: { }
def p_block_empty(p):
    "block : LBRACE RBRACE"
    p[0] = []

def p_block_contents(p):
    "block_contents : statements"
    p[0] = p[1]

# ----- Declarações / Instruções -----

# Múltiplas instruções
def p_statements_multiple(p):
    "statements : statements statement"
    p[0] = p[1] + [p[2]]

# Única instrução
def p_statements_single(p):
    "statements : statement"
    p[0] = [p[1]]

# Tipos de instruções possíveis
def p_statement(p):
    """statement : var_declaration
                 | short_var_declaration
                 | expression_statement
                 | if_statement
                 | for_statement
                 | switch_statement
                 | return_statement
                 | assignment"""
    p[0] = p[1]

# Instrução de continue
def p_statement_continue(p):
    "statement : CONTINUE SEMICOLON"
    p[0] = ContinueStatement(lineno=p.lineno(1))

# Instrução de break
def p_statement_break(p):
    "statement : BREAK SEMICOLON"
    p[0] = BreakStatement(lineno=p.lineno(1))

# Instrução de expressão (terminada com ponto-e-vírgula)
def p_expression_statement(p):
    "expression_statement : expression SEMICOLON"
    p[0] = ExpressionStatement(
        expression=p[1],
        lineno=p.lineno(2)
    )

# ----- If Statements -----

def p_if_statement(p):
    "if_statement : IF expression block else_clause"
    p[0] = IfStatement(
        condition=p[2],
        then_branch=p[3],
        else_branch=p[4],
        lineno=p.lineno(1)
    )

def p_else_clause_if(p):
    "else_clause : ELSE if_statement"
    p[0] = p[2]

def p_else_clause_block(p):
    "else_clause : ELSE block"
    p[0] = p[2]

def p_else_clause_empty(p):
    "else_clause : empty"
    p[0] = None

# ----- For Statements -----

def p_for_statement(p):
    """
    for_statement : FOR for_init SEMICOLON expression SEMICOLON for_post block
    """
    # for ( init ; condition ; post ) { block }
    p[0] = ForStatement(
        init=p[2],
        condition=p[4],
        post=p[6],
        body=p[7],
        lineno=p.lineno(1)
    )

# for ( expression ) { block } => estilo "for" simplificado
def p_for_statement_expression(p):
    "for_statement : FOR expression block"
    p[0] = ForStatement(init=None, condition=p[2], post=None, body=p[3], lineno=p.lineno(1))

# for ( block ) => estilo "for sem condição" (equivalente a loop infinito)
def p_for_while_statement(p):
    "for_statement : FOR block"
    p[0] = ForStatement(init=None, condition=None, post=None, body=p[2], lineno=p.lineno(1))

# Inicialização curta dentro do "for" (i := 0)
def p_for_init_short_var(p):
    "for_init : ID WALRUS expression"
    p[0] = VariableDeclaration(name=p[1], var_type=None, initializer=p[3], lineno=p.lineno(2))

# Declaração de variável no "for" (var i int = 0)
def p_for_init_var_declaration(p):
    "for_init : VAR ID type EQUAL expression"
    p[0] = VariableDeclaration(name=p[2], var_type=p[3], initializer=p[5], lineno=p.lineno(1))

# Post (ou step) no "for" pode ser assignment
def p_for_post_assignment(p):
    "for_post : assignment"
    p[0] = p[1]

# Ou pode ser uma expressão
def p_for_post_expression(p):
    "for_post : expression"
    p[0] = p[1]

# ----- Switch Statements -----

def p_switch_statement(p):
    """
    switch_statement : SWITCH expression LBRACE switch_cases default_clause RBRACE
    """
    p[0] = SwitchStatement(expression=p[2], cases=p[4], default=p[5], lineno=p.lineno(1))

def p_switch_cases_multiple(p):
    "switch_cases : switch_cases switch_case"
    p[0] = p[1] + [p[2]]

def p_switch_cases_single(p):
    "switch_cases : switch_case"
    p[0] = [p[1]]

def p_switch_case(p):
    "switch_case : CASE expression COLON statements"
    p[0] = SwitchCase(value=p[2], body=p[4], lineno=p.lineno(1))

def p_default_clause_with_statements(p):
    "default_clause : DEFAULT COLON statements"
    p[0] = p[3]

def p_default_clause_empty(p):
    "default_clause : empty"
    p[0] = None

# ----- Instrução de retorno -----

def p_return_statement(p):
    "return_statement : RETURN expression_opt SEMICOLON"
    p[0] = ReturnStatement(value=p[2], lineno=p.lineno(1))

def p_expression_opt(p):
    """expression_opt : expression
                      | empty"""
    p[0] = p[1]

# ----- Declarações de Variáveis -----

def p_var_declaration_array_init(p):
    "var_declaration : VAR ID array_type EQUAL array_initializer SEMICOLON"
    p[0] = VariableDeclaration(name=p[2], var_type=p[3], initializer=p[5], lineno=p.lineno(1))

def p_var_declaration_array_noinit(p):
    "var_declaration : VAR ID array_type SEMICOLON"
    p[0] = VariableDeclaration(name=p[2], var_type=p[3], initializer=None, lineno=p.lineno(1))

def p_var_declaration_array_short(p):
    "var_declaration : ID WALRUS array_type array_initializer SEMICOLON"
    p[0] = VariableDeclaration(name=p[1], var_type=p[3], initializer=p[4], lineno=p.lineno(2))
    
def p_var_declaration_init(p):
    "var_declaration : VAR ID type EQUAL expression SEMICOLON"
    p[0] = VariableDeclaration(name=p[2], var_type=p[3], initializer=p[5], lineno=p.lineno(1))

def p_var_declaration_noinit(p):
    "var_declaration : VAR ID type SEMICOLON"
    p[0] = VariableDeclaration(name=p[2], var_type=p[3], initializer=None, lineno=p.lineno(1))

def p_short_var_declaration(p):
    "short_var_declaration : ID WALRUS expression SEMICOLON"
    p[0] = VariableDeclaration(name=p[1], var_type=None, initializer=p[3], lineno=p.lineno(2))

# ----- Tipos de Array -----

def p_array_type_first_dimension(p):
    "array_type : type LBRACKET NUMBER_LITERAL RBRACKET"
    # Exemplo: int[10]
    p[0] = ArrayType(base_type=p[1], dimensions=[p[3]], lineno=p.lineno(1))

def p_array_type_more_dimensions(p):
    "array_type : array_type LBRACKET NUMBER_LITERAL RBRACKET"
    # Exemplo: int[10][5]
    p[1].dimensions.append(p[3])
    p[0] = p[1]

def p_array_type_first_empty(p):
    "array_type : type LBRACKET RBRACKET"
    # Exemplo: int[]
    # None usado como dimensão desconhecida
    p[0] = ArrayType(base_type=p[1], dimensions=[None], lineno=p.lineno(1))

def p_array_type_more_empty(p):
    "array_type : array_type LBRACKET RBRACKET"
    p[1].dimensions.append(None)
    p[0] = p[1]

# ----- Inicializadores de Array -----

def p_array_initializer_empty(p):
    "array_initializer : LBRACE RBRACE"
    # Exemplo: {}
    p[0] = ArrayInitializer(elements=[], dimensions=[0], lineno=p.lineno(1))

def p_array_initializer_flat(p):
    "array_initializer : LBRACE expression_list RBRACE"
    # Exemplo: {1, 2, 3}
    p[0] = ArrayInitializer(elements=p[2], dimensions=[len(p[2])], lineno=p.lineno(1))

def p_array_initializer_nested(p):
    "array_initializer : LBRACE nested_initializer_list RBRACE"
    # Exemplo: {{1,2},{3,4}}
    elements = p[2]
    if not elements:
        # Caso de {} aninhado
        p[0] = ArrayInitializer(elements=[], dimensions=[0], lineno=p.lineno(1))
        return
    dims = [len(elements)]
    if isinstance(elements[0], ArrayInitializer):
        # Se os elementos forem também ArrayInitializer, concatenar dimensões
        dims.extend(elements[0].dimensions)
    p[0] = ArrayInitializer(elements=elements, dimensions=dims, lineno=p.lineno(1))

def p_nested_initializer_list_single(p):
    "nested_initializer_list : array_initializer"
    p[0] = [p[1]]

def p_nested_initializer_list_multiple(p):
    "nested_initializer_list : nested_initializer_list COMMA array_initializer"
    p[0] = p[1] + [p[3]]

# ----- Acesso a Array -----

def p_array_access_first(p):
    "array_access : ID LBRACKET expression RBRACKET"
    # Exemplo: arr[2]
    p[0] = ArrayAccess(array=Variable(name=p[1], lineno=p.lineno(1)), indices=[p[3]], lineno=p.lineno(1))

def p_array_access_next(p):
    "array_access : array_access LBRACKET expression RBRACKET"
    # Exemplo: arr[2][3]
    p[1].indices.append(p[3])
    p[0] = p[1]

# ----- Atribuições -----

def p_simple_assignment(p):
    "assignment : ID EQUAL expression SEMICOLON"
    # Exemplo: x = 10;
    p[0] = Assignment(target=Variable(name=p[1], lineno=p.lineno(1)), value=p[3], lineno=p.lineno(2))

def p_array_element_assignment(p):
    "assignment : array_access EQUAL expression SEMICOLON"
    # Exemplo: arr[2] = 5;
    p[0] = ArrayAssignment(array=p[1].array, indices=p[1].indices, value=p[3], lineno=p.lineno(2))

def p_array_assignment(p):
    "assignment : ID EQUAL array_initializer SEMICOLON"
    # Exemplo: arr = {1,2,3};
    p[0] = Assignment(target=Variable(name=p[1], lineno=p.lineno(1)), value=p[3], lineno=p.lineno(2))

# ----- Expressões -----

def p_expression_binop(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MODULO expression
                  | expression EQUALITY expression
                  | expression NOTEQUAL expression
                  | expression GREATER expression
                  | expression LESS expression
                  | expression GREATEROREQUAL expression
                  | expression LESSOREQUAL expression
                  | expression CONDITIONALAND expression
                  | expression CONDITIONALOR expression"""
    # Operações binárias (Ex.: +, -, *, /, ==, !=, etc.)
    p[0] = BinaryOp(operator=p[2], left=p[1], right=p[3], lineno=p.lineno(2))

def p_expression_unaryop(p):
    """expression : NOT expression
                  | MINUS expression %prec UMINUS"""
    # Operadores unários (Ex.: !expr, -expr)
    p[0] = UnaryOp(operator=p[1], operand=p[2], lineno=p.lineno(1))

def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    # Expressão entre parênteses
    p[0] = p[2]

def p_expression_literal(p):
    "expression : literal"
    # Literal (número, string, bool)
    p[0] = p[1]

def p_expression_id(p):
    "expression : ID"
    # Variável
    p[0] = Variable(name=p[1], lineno=p.lineno(1))

def p_expression_array_access(p):
    "expression : array_access"
    # Acesso a array como expressão
    p[0] = p[1]

def p_expression_increment(p):
    "expression : ID INCREMENT"
    # i++
    p[0] = UnaryOp(operator="++", operand=Variable(name=p[1], lineno=p.lineno(1)), lineno=p.lineno(2))

def p_expression_decrement(p):
    "expression : ID DECREMENT"
    # i--
    p[0] = UnaryOp(operator="--", operand=Variable(name=p[1], lineno=p.lineno(1)), lineno=p.lineno(2))

def p_expression_function_call(p):
    "expression : function_call"
    # Chamada de função como expressão
    p[0] = p[1]

def p_function_call(p):
    "function_call : ID LPAREN arguments_opt RPAREN"
    p[0] = FunctionCall(name=p[1], arguments=p[3], lineno=p.lineno(1))

def p_arguments_opt(p):
    "arguments_opt : arguments"
    p[0] = p[1]

def p_arguments_empty(p):
    "arguments : empty"
    p[0] = []

def p_arguments_multiple(p):
    "arguments : arguments COMMA expression"
    p[0] = p[1] + [p[3]]

def p_arguments_single(p):
    "arguments : expression"
    p[0] = [p[1]]

def p_expression_list_multiple(p):
    "expression_list : expression_list COMMA expression"
    p[0] = p[1] + [p[3]]

def p_expression_list_single(p):
    "expression_list : expression"
    p[0] = [p[1]]

# ----- Literais -----

def p_literal_number(p):
    """literal : NUMBER_LITERAL"""
    # Determina se é int ou float
    if isinstance(p[1], int):
        p[0] = Literal(value=p[1], type="int", lineno=p.lineno(1))
    else:
        p[0] = Literal(value=p[1], type="float", lineno=p.lineno(1))

def p_literal_string(p):
    """literal : STRING_LITERAL"""
    p[0] = Literal(value=p[1], type="string", lineno=p.lineno(1))

def p_literal_boolean(p):
    """literal : BOOLEAN_LITERAL"""
    p[0] = Literal(value=p[1], type="bool", lineno=p.lineno(1))

# ----- Tipos Básicos -----
def p_basic_type(p):
    """type : INT 
            | FLOAT 
            | BOOL 
            | STRING 
            | VOID"""
    # Tipo base (int, float, bool, string, void)
    p[0] = p[1]

# Produção vazia (usada para representar opcionalidade)
def p_empty(p):
    "empty :"
    p[0] = None

# Função de tratamento de erros de parsing
def p_error(p):
    """
    Função simples de tratamento de erro do parser.
    """
    if not p:
        print("Syntax Error: Unexpected end of input")
        p.lexer.skip(1)
    else:
        print(f"Syntax Error at line {p.lineno}: Unexpected token {p.value}")
    parser.errok()

# Construção do parser
parser = yacc.yacc()
