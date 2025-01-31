from typing import List, Optional, Any
from semantic.symbol_table import SymbolTable
from c_ast.ast_nodes import (
    ArrayAccess,
    ArrayAssignment,
    ArrayType,
    Symbol,
    Variable,
    ArrayInitializer,
    Literal,
    Program,
    FunctionDeclaration,
    VariableDeclaration,
    Assignment,
    IfStatement,
    ForStatement,
    SwitchStatement,
    ReturnStatement,
    BreakStatement,
    ContinueStatement,
    ExpressionStatement,
    BinaryOp,
    UnaryOp,
    FunctionCall,
)

class SemanticError(Exception):
    """
    Exceção para erros semânticos. 
    Permite associar uma mensagem e, opcionalmente, o nó da AST onde ocorreu o erro.
    """

    def __init__(self, message, node=None):
        self.node = node
        message = f"SemanticError: {message}"
        # Se o nó tiver número de linha (lineno), acrescentar essa informação à mensagem
        if node is not None and hasattr(node, "lineno") and node.lineno is not None:
            message += f" at line {node.lineno}"
        super().__init__(message)


class SemanticAnalyzer:
    """
    Analisador semântico que verifica:
      - Compatibilidade de tipos (e anota 'inferred_type' nos nós),
      - Definição e uso correto de símbolos (variáveis, funções),
      - Uso de instruções return compatíveis com o tipo de retorno da função,
      - Uso adequado de break/continue dentro de estruturas de repetição (loops).
    """

    def __init__(self):
        # Tabela de símbolos (SymbolTable) que mantém registo de variáveis e funções
        self.symbol_table = SymbolTable()

        # Nome da função atualmente em análise (ou None se estiver fora de qualquer função)
        self.current_function: Optional[str] = None

        # Indica se estamos dentro de um loop (para gerir break/continue)
        self.in_loop = False

        # Conjunto de tipos básicos aceites
        self.basic_types = {"int", "float", "bool", "string", "void"}

    def analyze(self, ast) -> Any:
        """
        Executa a análise semântica sobre a AST fornecida.
        1. Adiciona as funções built-in à tabela de símbolos.
        2. Percorre a AST com a função visit.
        3. Devolve a AST anotada (p.ex., com tipos inferidos).
        """
        if ast is None:
            return

        # Insere funções built-in na tabela de símbolos
        self.add_builtins()

        # Visita recursivamente a AST
        self.visit(ast)
        return ast

    def add_builtins(self):
        """
        Adiciona funções built-in (print, read, toInt, toFloat, toStr, len) como símbolos na tabela,
        cada uma marcada como is_function=True.
        """
        builtin_functions = [
            Symbol(name="print",   type="void",   is_function=True, params=[],                      return_type="void"),
            Symbol(name="read",    type="string", is_function=True, params=[],                      return_type="string"),
            Symbol(name="toInt",   type="int",    is_function=True, params=[{"name": "value", "type": "any"}], return_type="int"),
            Symbol(name="toFloat", type="float",  is_function=True, params=[{"name": "value", "type": "any"}], return_type="float"),
            Symbol(name="toStr",   type="string", is_function=True, params=[{"name": "value", "type": "any"}], return_type="string"),
            Symbol(name="len",     type="int",    is_function=True, params=[{"name": "value", "type": "any"}], return_type="int"),
        ]

        for func in builtin_functions:
            self.symbol_table.define(func.name, func)

    def visit(self, node) -> Optional[str]:
        """
        Método genérico de despacho de visita.
        Dado um nó da AST, encontra o método 'visit_<nome da classe do nó>' e invoca-o.
        """
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        Se não houver um método 'visit_X' específico para o tipo de nó, geramos um erro.
        """
        raise SemanticError(f"No visit method for node type: {type(node).__name__}")

    # ------------------------------------------------------------------------
    # MÉTODOS AUXILIARES
    # ------------------------------------------------------------------------

    def _visit_block(self, statements):
        """
        Auxiliar para visitar um bloco de instruções. 
        O bloco pode ser uma lista de instruções ou uma única instrução.
        """
        if isinstance(statements, list):
            for stmt in statements:
                self.visit(stmt)
        else:
            self.visit(statements)

    def type_compatible(self, source_type: Any, target_type: Any) -> bool:
        """
        Verifica se 'source_type' pode ser atribuído a 'target_type'.
        Trata:
          - Tipos de array,
          - Tipos básicos,
          - Parâmetro 'any' usado em funções built-in.
        """
        # Se o source_type for uma função (Symbol) obtida pelo nome, usar o seu return_type
        func_symbol = self.symbol_table.lookup(str(source_type))
        if func_symbol and func_symbol.is_function:
            source_type = func_symbol.return_type

        # Caso de arrays
        if isinstance(target_type, ArrayType):
            # É necessário que ambos sejam ArrayType com dimensões compatíveis e mesmo tipo base
            if not isinstance(source_type, ArrayType):
                return False
            if len(source_type.dimensions) != len(target_type.dimensions):
                return False
            # Verificar cada dimensão (quando não for None)
            for src_dim, tgt_dim in zip(source_type.dimensions, target_type.dimensions):
                if tgt_dim is not None and src_dim > tgt_dim:
                    return False
            return self.type_compatible(source_type.base_type, target_type.base_type)

        # 'any' é usado em alguns parâmetros de funções built-in (sem restrição de tipo)
        if target_type == "any":
            return True

        # Caso geral: verificar igualdade para tipos básicos
        return source_type == target_type

    # ------------------------------------------------------------------------
    # MÉTODOS DE VISITA
    # ------------------------------------------------------------------------

    def visit_Program(self, node: Program) -> None:
        """
        Visita cada declaração no nó Program (funções, variáveis globais, etc.).
        """
        for decl in node.declarations:
            self.visit(decl)

    def visit_FunctionDeclaration(self, node: FunctionDeclaration):
        """
        Declaração de função:
         1. Verifica se o tipo de retorno é válido.
         2. Cria um símbolo da função e regista-o na tabela de símbolos.
         3. Visita o corpo da função num novo scope (stack de scopes).
         4. Verifica se funções não-void têm pelo menos um return de nível superior.
        """
        # Verificar se o tipo de retorno é válido
        if node.return_type not in self.basic_types:
            raise SemanticError(
                f"Invalid return type '{node.return_type}'",
                node
            )

        # Definir um símbolo para a função
        func_symbol = Symbol(
            name=node.name,
            type=node.return_type,
            is_function=True,
            params=node.params,
            return_type=node.return_type,
        )
        self.symbol_table.define(node.name, func_symbol)

        # Variável para verificar se encontrámos um 'return' de nível superior
        found_return = False

        # Entrar num novo scope para a função
        with self.symbol_table.new_scope():
            self.current_function = node.name

            # Definir os parâmetros da função no scope
            for param in node.params:
                self.symbol_table.define(param["name"], Symbol(name=param["name"], type=param["type"]))

            # Se o corpo for lista de instruções, visitar cada uma
            if isinstance(node.body, list):
                for stmt in node.body:
                    self.visit(stmt)
                    # Verificar se esta instrução é um ReturnStatement
                    if isinstance(stmt, ReturnStatement):
                        found_return = True
            else:
                # Corpo único
                self.visit(node.body)
                if isinstance(node.body, ReturnStatement):
                    found_return = True

            self.current_function = None

        # Se a função não for 'void' e não tiver um return de topo, lança erro
        if node.return_type != "void" and not found_return:
            raise SemanticError(
                f"Function '{node.name}' must have a top-level return statement",
                node
            )

    def visit_VariableDeclaration(self, node: VariableDeclaration) -> None:
        """
        Declaração de variável (simples ou array).
        1. Verifica dimensões dos arrays (se definido).
        2. Verifica/infere o tipo da variável a partir do initializer (se existir).
        3. Garante que o tipo da inicialização é compatível com var_type.
        4. Define o símbolo na tabela.
        """
        # Se for um ArrayType, verificar se dimensões especificadas são > 0
        if isinstance(node.var_type, ArrayType):
            for i, dim in enumerate(node.var_type.dimensions):
                if dim is not None and dim <= 0:
                    raise SemanticError(f"Array dimension {i} must be positive", node)

        # Visitar o initializer (se existir) para descobrir ou confirmar o tipo
        init_type = None
        if node.initializer:
            init_type = self.visit(node.initializer)

        # Se var_type for explicitamente fornecido
        if node.var_type:
            if init_type:
                if not self.type_compatible(init_type, node.var_type):
                    raise SemanticError(
                        f"Type mismatch in variable '{node.name}' declaration: "
                        f"expected {node.var_type}, got {init_type}",
                        node
                    )
                # Se o array type tiver dimensões None, preencher com as dimensões obtidas do init_type
                if isinstance(node.var_type, ArrayType) and isinstance(init_type, ArrayType):
                    node.var_type.dimensions = [
                        init_type.dimensions[i] if d is None else d
                        for i, d in enumerate(node.var_type.dimensions)
                    ]
                    # Se ainda houver discrepâncias, lançar erro
                    if node.var_type.dimensions != init_type.dimensions:
                        raise SemanticError(
                            f"Array initializer dimensions do not match array type: "
                            f"expected {node.var_type.dimensions}, got {init_type.dimensions}",
                            node
                        )
        else:
            # Se var_type não for fornecido, inferir do initializer
            node.var_type = init_type

        # Registar a variável na tabela de símbolos
        var_symbol = Symbol(name=node.name, type=node.var_type)
        self.symbol_table.define(node.name, var_symbol)

        # Guardar o tipo final em node.inferred_type (opcional)
        node.inferred_type = node.var_type

    def visit_Assignment(self, node: Assignment) -> None:
        """
        Atribuição simples (target = value).
        1. Visita a variável destino e o valor.
        2. Verifica compatibilidade de tipos.
        3. Armazena o tipo resultante em node.inferred_type (normalmente igual ao tipo do destino).
        """
        target_type = self.visit(node.target)
        value_type = self.visit(node.value)

        if not self.type_compatible(value_type, target_type):
            raise SemanticError(
                f"Type mismatch in assignment: cannot assign {value_type} to {target_type}",
                node
            )

        node.inferred_type = target_type

    def visit_ArrayAssignment(self, node: ArrayAssignment) -> None:
        """
        Atribuição a elemento(s) de array: array[i][j] = valor.
        1. Verifica se 'array' é mesmo do tipo ArrayType.
        2. Verifica se número de índices coincide com o número de dimensões.
        3. Verifica se todos os índices são int.
        4. Verifica se o tipo do valor é compatível com o base_type do array.
        """
        array_type = self.visit(node.array)
        if not isinstance(array_type, ArrayType):
            raise SemanticError(f"Cannot index into non-array type {array_type}", node)

        if len(node.indices) != len(array_type.dimensions):
            raise SemanticError(
                f"Wrong number of dimensions in array assignment: expected {len(array_type.dimensions)}, got {len(node.indices)}", node
            )

        for i, index_expr in enumerate(node.indices):
            idx_type = self.visit(index_expr)
            if idx_type != "int":
                raise SemanticError(f"Array index {i} must be int, got {idx_type}", node)

        value_type = self.visit(node.value)
        if not self.type_compatible(value_type, array_type.base_type):
            raise SemanticError(
                f"Cannot assign value of type {value_type} to array element of type {array_type.base_type}", node
            )

        node.inferred_type = None  # Normalmente, array assignment não produz um tipo de expressão

    def visit_IfStatement(self, node: IfStatement) -> None:
        """
        Instrução if:
          - A condição tem de ser do tipo bool.
          - O corpo do then e do else é visitado (possivelmente em novos scopes).
        """
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            raise SemanticError(f"If condition must be boolean, got {cond_type}", node)

        # then_branch em novo scope
        with self.symbol_table.new_scope():
            self._visit_block(node.then_branch)

        # else_branch (se existir) em outro scope
        if node.else_branch is not None:
            with self.symbol_table.new_scope():
                self._visit_block(node.else_branch)

    def visit_ForStatement(self, node: ForStatement) -> None:
        """
        Instrução for:
          - init corre num scope (variável local se houver).
          - condition deve ser bool se existir.
          - body corre num contexto de loop (in_loop=True).
          - post (se houver) é visitado após o body.
        """
        with self.symbol_table.new_scope():
            if node.init:
                self.visit(node.init)

            if node.condition:
                cond_type = self.visit(node.condition)
                if cond_type != "bool":
                    raise SemanticError(f"For condition must be boolean, got {cond_type}", node)

            # Temporariamente marcamos in_loop = True para permitir break/continue
            prev_in_loop = self.in_loop
            self.in_loop = True

            self._visit_block(node.body)

            self.in_loop = prev_in_loop

            if node.post:
                self.visit(node.post)

    def visit_ReturnStatement(self, node: ReturnStatement) -> None:
        """
        Instrução return:
          - Tem de estar dentro de uma função.
          - Se a função não for void, tem de retornar um valor compatível.
          - Se a função for void, não pode retornar valor.
        """
        if not self.current_function:
            raise SemanticError("Return statement outside function", node)

        func_symbol = self.symbol_table.lookup(self.current_function)
        if not func_symbol:
            raise SemanticError(f"Cannot find current function {self.current_function}", node)

        if node.value:
            return_type = self.visit(node.value)
            if not self.type_compatible(return_type, func_symbol.return_type):
                raise SemanticError(
                    f"Return type mismatch: expected {func_symbol.return_type}, got {return_type}",
                    node
                )
            node.inferred_type = return_type
        else:
            # Não há valor no return
            if func_symbol.return_type != "void":
                raise SemanticError(
                    f"Function {self.current_function} must return a value of type {func_symbol.return_type}",
                    node
                )
            node.inferred_type = "void"

    def visit_BreakStatement(self, node: BreakStatement) -> None:
        """
        break só é válido dentro de loops.
        """
        if not self.in_loop:
            raise SemanticError("Break statement outside loop", node)

    def visit_ContinueStatement(self, node: ContinueStatement) -> None:
        """
        continue só é válido dentro de loops.
        """
        if not self.in_loop:
            raise SemanticError("Continue statement outside loop", node)

    def visit_BinaryOp(self, node: BinaryOp) -> str:
        """
        Operadores binários:
         - +, -, *, /, % => aritméticos
         - <, <=, >, >= => comparações
         - ==, != => igualdade/ desigualdade
         - &&, || => lógicos
        Verifica compatibilidade de tipos e define node.inferred_type.
        """
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        op = node.operator

        # Operadores aritméticos
        if op in {"+", "-", "*", "/", "%"}:
            # Exceção: concatenação de strings usando +
            if op == "+" and left_type == "string" and right_type == "string":
                node.inferred_type = "string"
                return node.inferred_type

            # Caso normal: ambos operandos têm de ser int ou float
            if left_type not in {"int", "float"} or right_type not in {"int", "float"}:
                raise SemanticError(
                    f"Arithmetic op '{op}' not supported between {left_type} and {right_type}",
                    node
                )
            # Se um deles for float, o resultado é float; caso contrário, int
            node.inferred_type = "float" if "float" in {left_type, right_type} else "int"
            return node.inferred_type

        # Operadores de comparação (<, <=, >, >=)
        elif op in {"<", "<=", ">", ">="}:
            if left_type not in {"int", "float"} or right_type not in {"int", "float"}:
                raise SemanticError(
                    f"Comparison '{op}' not supported between {left_type} and {right_type}",
                    node
                )
            node.inferred_type = "bool"
            return node.inferred_type

        # Operadores de igualdade (==, !=)
        elif op in {"==", "!="}:
            if not self.type_compatible(left_type, right_type):
                raise SemanticError(f"Cannot compare {left_type} and {right_type}", node)
            node.inferred_type = "bool"
            return node.inferred_type

        # Operadores lógicos (&&, ||)
        elif op in {"&&", "||"}:
            if left_type != "bool" or right_type != "bool":
                raise SemanticError(
                    f"Logical op '{op}' not supported between {left_type} and {right_type}",
                    node
                )
            node.inferred_type = "bool"
            return node.inferred_type

        raise SemanticError(f"Unrecognized binary operator: {op}", node)

    def visit_UnaryOp(self, node: UnaryOp) -> str:
        """
        Operadores unários: 
         - '!' (NOT lógico),
         - '-' (negativo aritmético),
         - '++', '--' (incremento/decremento).
        Verifica o tipo do operando e define node.inferred_type.
        """
        operand_type = self.visit(node.operand)
        op = node.operator

        if op == "!":
            if operand_type != "bool":
                raise SemanticError(f"Logical NOT requires bool, got {operand_type}", node)
            node.inferred_type = "bool"
            return node.inferred_type

        elif op == "-":
            if operand_type not in {"int", "float"}:
                raise SemanticError(f"Unary minus requires numeric type, got {operand_type}", node)
            node.inferred_type = operand_type
            return node.inferred_type

        elif op in {"++", "--"}:
            # i++, i-- => Têm de ser variáveis do tipo int
            if not isinstance(node.operand, Variable):
                raise SemanticError("Increment/decrement requires variable operand", node)
            if operand_type != "int":
                raise SemanticError(
                    f"Increment/decrement requires int operand, got {operand_type}",
                    node
                )
            node.inferred_type = "int"
            return node.inferred_type

        raise SemanticError(f"Unrecognized unary operator: {op}", node)

    def visit_Literal(self, node: Literal) -> str:
        """
        Visita literal (int, float, bool, string) e devolve o seu tipo.
        Armazena em node.inferred_type.
        """
        node.inferred_type = node.type
        return node.inferred_type

    def visit_Variable(self, node: Variable) -> str:
        """
        Visita uma variável: procura na tabela de símbolos e obtém o tipo.
        Armazena em node.inferred_type.
        """
        symbol = self.symbol_table.lookup(node.name)
        if not symbol:
            raise SemanticError(f"Undefined variable: {node.name}", node)
        node.inferred_type = symbol.type
        return node.inferred_type

    def visit_ArrayAccess(self, node: ArrayAccess) -> str:
        """
        Acesso a array: array[i][j]...
        - Verifica se 'array' é ArrayType
        - Verifica se o número de índices corresponde ao número de dimensões
        - Cada índice tem de ser int
        - O tipo resultante é o base_type do array
        """
        array_type = self.visit(node.array)
        if not isinstance(array_type, ArrayType):
            raise SemanticError(f"Cannot index into non-array type {array_type}", node)

        if len(node.indices) != len(array_type.dimensions):
            raise SemanticError(
                f"Wrong number of dimensions in array access: "
                f"expected {len(array_type.dimensions)}, got {len(node.indices)}", node
            )

        for i, idx_expr in enumerate(node.indices):
            idx_type = self.visit(idx_expr)
            if idx_type != "int":
                raise SemanticError(f"Array index {i} must be int, got {idx_type}", node)

        node.inferred_type = array_type.base_type
        return node.inferred_type

    def visit_FunctionCall(self, node: FunctionCall) -> str:
        """
        Chamada de função:
          1. Verificar se a função existe na tabela de símbolos (e se é função).
          2. Verificar contagem e tipos de argumentos.
          3. Retornar o tipo de retorno da função.
        """
        func_symbol = self.symbol_table.lookup(node.name)
        if not func_symbol:
            raise SemanticError(f"Undefined function: {node.name}", node)
        if not func_symbol.is_function:
            raise SemanticError(f"{node.name} is not a function", node)

        # Caso especial: print() pode ter vários argumentos de tipos variados
        if node.name == "print":
            for arg in node.arguments:
                arg_type = self.visit(arg)
                # Aceitamos vários tipos para print, não é feita verificação estrita
            node.inferred_type = "void"
            return node.inferred_type

        # Funções built-in com um único argumento (toInt, toFloat, toStr)
        if node.name in {"toInt", "toFloat", "toStr"}:
            if len(node.arguments) != 1:
                raise SemanticError(f"{node.name}() expects exactly one argument", node)
            arg_type = self.visit(node.arguments[0])
            if arg_type not in self.basic_types and arg_type != "string":
                raise SemanticError(f"Cannot convert type {arg_type} to {node.name}", node)
            node.inferred_type = func_symbol.return_type
            return node.inferred_type

        # Verificar número de argumentos para funções normais
        if len(node.arguments) != len(func_symbol.params):
            raise SemanticError(
                f"Function {node.name} expects {len(func_symbol.params)} arguments, got {len(node.arguments)}",
                node
            )

        # Verificar cada argumento
        for i, (arg, param) in enumerate(zip(node.arguments, func_symbol.params)):
            arg_type = self.visit(arg)
            # Se param["type"] == "any", não verificamos compatibilidade
            if param["type"] != "any" and not self.type_compatible(arg_type, param["type"]):
                raise SemanticError(
                    f"Type mismatch in argument {i+1} of {node.name}: "
                    f"expected {param['type']}, got {arg_type}",
                    node
                )

        node.inferred_type = func_symbol.return_type
        return node.inferred_type

    def visit_ArrayInitializer(self, node: ArrayInitializer) -> ArrayType:
        """
        Inicializador de array (Ex.: {{1,2},{3,4}}):
        1. Analisa recursivamente a estrutura para determinar dimensões e tipo base.
        2. Cria um ArrayType correspondente e armazena em node.inferred_type.
        """
        if not node.elements:
            raise SemanticError("Empty array initializer", node)

        dimensions, base_type = self._analyze_array_initializer_level(node.elements)
        arr_type = ArrayType(base_type=base_type, dimensions=dimensions, lineno=node.lineno)
        node.inferred_type = arr_type
        return arr_type

    def _analyze_array_initializer_level(self, elements: List[Any]):
        """
        Função recursiva para determinar dimensões e tipo base de um nível do array initializer.
        Retorna (lista_de_dimensões, tipo_base_string).
        """
        if not elements:
            return [], None

        # A primeira dimensão é o tamanho de 'elements'
        dimensions = [len(elements)]
        first = elements[0]

        # Se o primeiro elemento for outro ArrayInitializer, descer mais um nível
        if isinstance(first, ArrayInitializer):
            subdims, elem_type = self._analyze_array_initializer_level(first.elements)
            dimensions.extend(subdims)
        else:
            # Caso contrário, é um literal ou algo que tem um tipo
            elem_type = self.visit(first)

        # Verificar consistência nos elementos seguintes
        for elem in elements[1:]:
            if isinstance(first, ArrayInitializer) != isinstance(elem, ArrayInitializer):
                raise SemanticError("Inconsistent array structure in initializer", node=elem)

            if isinstance(elem, ArrayInitializer):
                subdims2, sub_type = self._analyze_array_initializer_level(elem.elements)
                if subdims2 != subdims or sub_type != elem_type:
                    raise SemanticError("Inconsistent dimensions or types in array initializer", node=elem)
            else:
                if self.visit(elem) != elem_type:
                    raise SemanticError("Inconsistent types in array initializer", node=elem)

        return dimensions, elem_type

    def visit_ExpressionStatement(self, node: ExpressionStatement) -> None:
        """
        Instrução que é apenas uma expressão (por exemplo, chamada de função sozinha).
        Basta visitar a expressão para validar.
        """
        self.visit(node.expression)

    def visit_SwitchStatement(self, node: SwitchStatement) -> None:
        """
        Instrução switch:
          1. Visita a expressão do switch para determinar o tipo base,
          2. Para cada case, verifica compatibilidade se for literal,
          3. Verifica duplicados nos case (para literais),
          4. Visita cada body em novo scope e marca in_loop=True para permitir break.
          5. Se houver default, visita o corpo.
        """
        switch_type = self.visit(node.expression)

        with self.symbol_table.new_scope():
            seen_values = set()

            for case in node.cases:
                case_type = self.visit(case.value)
                if not self.type_compatible(case_type, switch_type):
                    raise SemanticError(
                        f"Switch case type mismatch: cannot compare {switch_type} with {case_type}",
                        node=case
                    )

                # Se o case for literal, verificar duplicados
                case_val = case.value.value if isinstance(case.value, Literal) else None
                if case_val in seen_values:
                    raise SemanticError(f"Duplicate case value: {case_val}", node=case)
                if case_val is not None:
                    seen_values.add(case_val)

                # Neste contexto, consideramos o switch como loop-friendly para permitir break
                prev_in_loop = self.in_loop
                self.in_loop = True

                self._visit_block(case.body)

                self.in_loop = prev_in_loop

            # Visitar default (se existir)
            if node.default:
                self._visit_block(node.default)
