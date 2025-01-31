from dataclasses import dataclass
from typing import Any, List, Optional, Dict

# Classe que representa um programa completo, contendo uma lista de declarações
# (funções, variáveis, etc.) e o número da linha onde o programa começa.
@dataclass
class Program:
    declarations: List[Any]
    lineno: int


# Declaração de função, contendo nome, parâmetros, tipo de retorno, corpo e o número da linha.
@dataclass
class FunctionDeclaration:
    name: str
    params: List[Any]
    return_type: str
    body: Any
    lineno: int


# Declaração de variável, que pode ter um tipo opcional (para inferência em declarações curtas),
# um inicializador opcional e o número da linha onde aparece.
@dataclass
class VariableDeclaration:
    name: str
    lineno: int
    var_type: Optional[str] = None  # None para inferência de tipo
    initializer: Optional[Any] = None


# Atribuição de valor a uma variável ou a outra expressão (por exemplo, a um acesso a array).
@dataclass
class Assignment:
    target: Any
    value: Any
    lineno: int


# Estrutura de controlo If, com a condição, o ramo "then" e opcionalmente o ramo "else".
@dataclass
class IfStatement:
    condition: Any
    then_branch: Any
    lineno: int
    else_branch: Optional[Any] = None


# Estrutura de controlo For, contendo a inicialização (init), condição, instrução de incremento (post)
# e o corpo do ciclo.
@dataclass
class ForStatement:
    init: Optional[Any]
    condition: Optional[Any]
    post: Optional[Any]
    body: Any
    lineno: int


# Estrutura de controlo Switch, com a expressão a ser avaliada, casos e um ramo opcional default.
@dataclass
class SwitchStatement:
    expression: Any
    cases: List[Any]
    lineno: int
    default: Optional[Any] = None


# Caso de um Switch, contendo o valor a ser comparado e o corpo (instruções do caso).
@dataclass
class SwitchCase:
    value: Any
    body: Any
    lineno: int


# Instrução de retorno, contendo um valor opcional e o número de linha.
@dataclass
class ReturnStatement:
    lineno: int
    value: Optional[Any] = None


# Instrução de break, usada para sair de loops ou switch.
@dataclass
class BreakStatement:
    lineno: int
    pass


# Instrução de continue, usada para avançar para a próxima iteração de um loop.
@dataclass
class ContinueStatement:
    lineno: int
    pass


# Instrução de expressão simples (chamada de função, operações aritméticas, etc.).
@dataclass
class ExpressionStatement:
    expression: Any
    lineno: int


# Operação binária (ex.: +, -, *, /), contendo operador, operandos e número de linha.
@dataclass
class BinaryOp:
    operator: str
    left: Any
    right: Any
    lineno: int


# Operação unária (ex.: -x, !x), contendo operador, operando e número de linha.
@dataclass
class UnaryOp:
    operator: str
    operand: Any
    lineno: int


# Representa um literal (ex.: número inteiro, string), contendo o valor, tipo e número de linha.
@dataclass
class Literal:
    value: Any
    type: str
    lineno: int


# Representa o acesso a uma variável, contendo o nome e número de linha.
@dataclass
class Variable:
    name: str
    lineno: int


# Chamada de função, contendo o nome da função, lista de argumentos e número de linha.
@dataclass
class FunctionCall:
    name: str
    arguments: List[Any]
    lineno: int


# Representa um tipo de array com tipo base (ex.: 'int') e lista de dimensões (ex.: int[3][4]).
@dataclass
class ArrayType:
    base_type: str
    dimensions: List[int]
    lineno: int


# Acesso a um array, contendo o array em si e a lista de índices (expressões) para cada dimensão.
@dataclass
class ArrayAccess:
    array: Any
    indices: List[Any]
    lineno: int


# Atribuição a um array, semelhante a Assignment, mas específica para elementos de array.
@dataclass
class ArrayAssignment:
    array: Any
    indices: List[Any]
    value: Any
    lineno: int


# Inicializador de array, contendo a lista de elementos (que podem ser inic. aninhados) 
# e as dimensões do array.
@dataclass
class ArrayInitializer:
    elements: List[Any]
    dimensions: List[int]
    lineno: int


# Representa um símbolo na tabela de símbolos, que pode ser variável ou função.
@dataclass
class Symbol:
    name: str
    type: str
    is_function: bool = False
    params: Optional[List[Dict[str, str]]] = None
    return_type: Optional[str] = None
