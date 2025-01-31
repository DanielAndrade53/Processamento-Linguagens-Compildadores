from c_ast.ast_nodes import (
    ArrayInitializer,
    VariableDeclaration,
    FunctionDeclaration,
    ArrayType,
    BinaryOp,
    Literal,
    Variable,
    ExpressionStatement,
    FunctionCall,
    ArrayAssignment,
    ArrayAccess,
    ReturnStatement,
    IfStatement,
    ForStatement,
    SwitchStatement,
    BreakStatement,
    ContinueStatement,
    Assignment,
    UnaryOp,
    Program
)


class CodeGenerator:
    """
    A classe CodeGenerator percorre uma AST semanticamente válida e produz código assembly.
    Assumimos que todas as verificações semânticas (tipagem, escopo, etc.) já foram feitas,
    e que cada nó de expressão possui um atributo 'inferred_type'.
    """

    def __init__(self):
        # Lista de instruções assembly geradas
        self.assembly = []

        # Informação de contexto / escopo
        self.current_scope = "global"  # Escopo atual (p.e., global ou nome de função)
        self.label_counter = 0         # Contador para geração de rótulos únicos

        # Variáveis globais e locais
        self.global_vars = {}  # Dicionário: nome_variável -> {address, type}
        self.local_vars = {}   # Dicionário: nome_variável -> {offset, type, ...} para a função atual

        # Função atualmente em visita
        self.current_function = None

        # Endereços / offsets para armazenamento
        self.next_global_addr = 0
        self.next_local_offset = 0

        # Contador de parâmetros de função
        self.param_count = 0

        # Stacks para controlo de loops / switches (break/continue)
        self.break_stack = []     # Stack de tuplos (tipo, end_label)
        self.continue_stack = []  # Stack de rótulos de 'continue' para loops

        # Tipos de retorno de funções (preenchido ao visitar declarações de função)
        self.return_types = {}

    def init_builtins(self):
        """
        Inicializa funções internas (built-in) conhecidas e os seus tipos de retorno,
        para que o gerador de código consiga lidar corretamente com chamadas a estas funções.
        """
        self.return_types["print"] = "void"
        self.return_types["read"] = "string"
        self.return_types["toInt"] = "int"
        self.return_types["toFloat"] = "float"
        self.return_types["toStr"] = "string"
        self.return_types["len"] = "int"

    def visit(self, node):
        """
        Função central de despacho de visitas.
        Invoca dinamicamente o método 'visit_<nome_da_classe>' baseado no tipo de nó da AST.
        """
        if node is None:
            return None
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        Chamado se não existir um método específico de visita para o tipo de nó.
        """
        raise Exception(f"Nenhum método visit_{type(node).__name__} definido")

    def reset_local_context(self):
        """
        Limpa / reinicia as variáveis locais ao entrar numa nova função,
        preparando para analisar a sua lista de variáveis.
        """
        self.local_vars = {}
        self.next_local_offset = 0
        self.param_count = 0

    def emit(self, instruction, comment=None):
        """
        Adiciona uma instrução à lista self.assembly, com um comentário opcional.
        O comentário aparece no código gerado, facilitando a depuração.
        """
        if comment:
            self.assembly.append(f"\t{instruction}\t// {comment}")
        else:
            self.assembly.append(f"\t{instruction}")

    def generate_label(self, prefix="L"):
        """
        Gera um rótulo único (ex.: L1, L2, ...) para uso em instruções de salto (branch/loops).
        """
        self.label_counter += 1
        return f"{prefix}{self.label_counter}"

    def count_local_vars(self, statements):
        """
        Conta quantas variáveis locais são declaradas num corpo de função,
        para saber quanta memória deve ser reservada na stack local.
        """
        count = 0
        if not statements:
            return 0
        # Se statements for uma lista, percorre; caso contrário, põe numa lista e percorre
        for stmt in statements if isinstance(statements, list) else [statements]:
            if isinstance(stmt, VariableDeclaration):
                count += 1
        return count

    def generate_code(self, ast) -> str:
        """
        Orquestra a geração de código para toda a AST:
        1) Inicializa as funções built-in
        2) Visita o nó raiz Program
        3) Retorna o texto das instruções assembly unidas por nova linha
        """
        self.init_builtins()
        self.visit(ast)
        return "\n".join(self.assembly)

    # ---------------------------------------------------------------------
    # Métodos de visita de alto nível (Program, Função, etc.)
    # ---------------------------------------------------------------------

    def visit_Program(self, node: Program):
        """
        Visita o nó principal Program.
        1) Recolhe tipos de retorno de cada função
        2) Aloca e gera código para variáveis globais
        3) Emite 'start' + chamada opcional para main
        4) Emite 'stop'
        5) Gera código para cada declaração de função
        """
        # 1) Recolher tipos de retorno das funções
        for decl in node.declarations:
            if isinstance(decl, FunctionDeclaration):
                self.return_types[decl.name] = decl.return_type

        # 2) Declarar variáveis globais
        self.emit("// Global variable declarations")
        for decl in node.declarations:
            if isinstance(decl, VariableDeclaration):
                addr = self.next_global_addr
                self.global_vars[decl.name] = {"address": addr, "type": decl.var_type}
                self.next_global_addr += 1
                self.visit_global_var_decl(decl)

        # 3) Iniciar programa + chamada opcional a main
        self.emit("start", "Program start")
        if "main" in self.return_types:
            self.emit("pusha main", "Call main function")
            self.emit("call")

        # 4) Finalizar programa
        self.emit("stop", "Program end")

        # 5) Gerar código para funções
        for decl in node.declarations:
            if isinstance(decl, FunctionDeclaration):
                self.visit(decl)

    def visit_global_var_decl(self, node: VariableDeclaration):
        """
        Lida com uma declaração global de variável (incluindo arrays):
        Aloca memória, inicializa se necessário e guarda o endereço global.
        """
        addr = self.global_vars[node.name]["address"]
        self.emit(f"// Global variable {node.name} at address {addr}")

        # Se o tipo for array
        if isinstance(node.var_type, ArrayType):
            if node.initializer:
                # Calcula o tamanho total a partir das dimensões
                total_size = 1
                for dim in node.initializer.dimensions:
                    total_size *= dim
                self.emit(f"alloc {total_size}", f"Allocate array of total size {total_size}")

                # Inicializa cada elemento, se presente
                if node.initializer.elements:
                    for i, elem in enumerate(node.initializer.elements):
                        if isinstance(elem, ArrayInitializer):
                            # Caso de array aninhado
                            for j, nested_elem in enumerate(elem.elements):
                                self.emit("dup 1")  # Duplica a referência ao array
                                offset = i * node.initializer.dimensions[1] + j
                                self.emit(f"pushi {offset}")
                                self.visit(nested_elem)
                                self.emit("storen")
                        else:
                            # Array simples (1D)
                            self.emit("dup 1")
                            self.emit(f"pushi {i}")
                            self.visit(elem)
                            self.emit("storen")
            else:
                # Sem inicializador => alocar espaço padrão
                total_size = 1
                for dim in node.var_type.dimensions:
                    if dim is not None:
                        total_size *= dim
                self.emit(f"alloc {total_size}")

        # Se for variável simples (não-array)
        elif node.initializer:
            self.visit(node.initializer)
        else:
            # Inicialização por omissão
            if node.var_type == "float":
                self.emit("pushf 0.0")
            elif node.var_type == "string":
                self.emit('pushs ""')
            else:
                self.emit("pushi 0")

        self.emit(f"storeg {addr}")

    def visit_FunctionDeclaration(self, node: FunctionDeclaration):
        """
        Gera código para uma função:
        1) Limpa o contexto de variáveis locais
        2) Reserva espaço para variáveis locais
        3) Emite o corpo da função
        4) Se a função for void, emite um return
        """
        self.current_function = node
        self.reset_local_context()

        # Processa parâmetros: armazena-os em local_vars
        for i, param in enumerate(node.params, start=1):
            self.local_vars[param["name"]] = {
                "offset": i,
                "type": param["type"],
                "param": True,
                "param_num": i,
            }

        # Contagem das variáveis locais no corpo
        local_var_count = self.count_local_vars(node.body)

        # Emite o rótulo da função
        self.emit(f"\n{node.name}:", f"Function {node.name} declaration")

        # Prólogo (reserva espaço para variáveis locais)
        if local_var_count > 0:
            self.emit(
                f"pushn {local_var_count}",
                f"Reserve space for {local_var_count} local variables",
            )

        # Visita o corpo (que pode ser lista de statements ou único statement)
        if isinstance(node.body, list):
            for stmt in node.body:
                self.visit(stmt)
        else:
            self.visit(node.body)

        # Se for void, garante um return
        if node.return_type == "void":
            self.emit("return", "Return from void function")

        self.current_function = None

    def visit_VariableDeclaration(self, node: VariableDeclaration):
        """
        Lida com declaração de variável local (com inicializador opcional).
        """
        if self.current_function:
            # É variável local
            offset = self.next_local_offset
            self.local_vars[node.name] = {"offset": offset, "type": node.var_type}
            self.next_local_offset += 1

            # Se for array
            if isinstance(node.var_type, ArrayType):
                if node.initializer:
                    self.visit_array_initializer(node.initializer, node.initializer.dimensions)
                else:
                    # Aloca para array com dimensões conhecidas
                    total_size = 1
                    for dim in node.var_type.dimensions:
                        if dim is not None:
                            total_size *= dim
                    self.emit(f"alloc {total_size}")

            elif node.initializer:
                # Inicializador simples
                self.visit(node.initializer)
            else:
                # Inicialização por omissão
                if node.var_type == "float":
                    self.emit("pushf 0.0")
                elif node.var_type == "string":
                    self.emit('pushs ""')
                else:
                    self.emit("pushi 0")

            self.emit(f"storel {offset}")

    def visit_array_initializer(self, initializer: ArrayInitializer, dimensions, current_dim=0):
        """
        Inicializa um array multidimensional num único bloco contíguo.
        'Flatten' (achatar) os inicializadores aninhados e aloca.
        """
        # Se o 'initializer' não for ArrayInitializer (pode ser Literal), apenas visita-o.
        if not isinstance(initializer, ArrayInitializer):
            self.visit(initializer)
            return

        actual_dimensions = initializer.dimensions
        total_size = 1
        for dim in actual_dimensions:
            total_size *= dim

        # Alocar bloco único
        self.emit(f"alloc {total_size}")

        # 'Flatten' todos os elementos e armazena
        flat_elements = self._flatten_array_initializer(initializer)
        for i, elem in enumerate(flat_elements):
            self.emit("dup 1")
            self.emit(f"pushi {i}")
            self.visit(elem)
            self.emit("storen")

    def _flatten_array_initializer(self, initializer: ArrayInitializer):
        """
        Função auxiliar para achatar inicializadores de array aninhados num só nível de lista.
        """
        if not isinstance(initializer, ArrayInitializer):
            return [initializer]
        flattened = []
        for elem in initializer.elements:
            if isinstance(elem, ArrayInitializer):
                flattened.extend(self._flatten_array_initializer(elem))
            else:
                flattened.append(elem)
        return flattened

    # ---------------------------------------------------------------------
    #  Visita de nós de instrução (Assignment, If, For, Switch, etc.)
    # ---------------------------------------------------------------------

    def visit_Assignment(self, node: Assignment):
        """
        Atribuição a uma variável simples:
        1) Avalia o lado direito (value)
        2) Armazena no alvo (global ou local)
        """
        self.visit(node.value)
        var_name = node.target.name
        if var_name in self.global_vars:
            addr = self.global_vars[var_name]["address"]
            self.emit(f"storeg {addr}")
        else:
            offset = self.local_vars[var_name]["offset"]
            self.emit(f"storel {offset}")

    def visit_ArrayAssignment(self, node: ArrayAssignment):
        """
        Atribuição a um elemento de array:
        1) Dá stack a referência base do array
        2) Calcula o índice linear
        3) Avalia o valor
        4) Usa 'storen' para armazenar no local correto
        """
        # Dá stack á referência do array
        self.visit(node.array)

        # Calcula índice linear
        array_type = node.array.inferred_type
        if isinstance(array_type, ArrayType):
            self.calculate_array_index(array_type.dimensions, node.indices)
        else:
            # Fallback para array de dimensão única ou cenário de erro semântico
            self.visit(node.index)

        # Avalia o valor e armazena
        self.visit(node.value)
        self.emit("storen")

    def calculate_array_index(self, dimensions, indices):
        """
        Calcula o índice linear para acesso a um array multidimensional.
        Ex.: para array[M][N], o acesso [i][j] => i * N + j
        """
        if len(dimensions) != len(indices):
            # O analisador semântico já deve ter verificado isto
            return

        steps = []
        step = 1
        # Constrói lista 'steps' de trás para a frente
        for dim in reversed(dimensions[1:]):
            steps.append(step)
            step *= dim
        steps.append(step)
        steps.reverse()

        first = True
        for s, idx_node in zip(steps, indices):
            self.visit(idx_node)
            if s != 1:
                self.emit(f"pushi {s}")
                self.emit("mul")
            if not first:
                self.emit("add")
            first = False

    def visit_BinaryOp(self, node: BinaryOp):
        """
        Avalia operandos esquerdo e direito, depois emite a instrução correspondente.
        Utiliza node.left.inferred_type, node.right.inferred_type e node.inferred_type
        para selecção da instrução final (int, float, string, etc.).
        """
        self.visit(node.left)
        self.visit(node.right)

        left_type = node.left.inferred_type
        right_type = node.right.inferred_type
        operator = node.operator

        # Mapeamento da instrução
        self._emit_binary_op(operator, left_type, right_type, node.inferred_type)

    def _emit_binary_op(self, operator, left_type, right_type, result_type):
        """
        Função auxiliar para escolher a instrução assembly adequada
        a uma dada operação binária.
        """
        op_map = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "div",
            "%": "mod",
            "<": "inf",
            "<=": "infeq",
            ">": "sup",
            ">=": "supeq",
            "==": "equal",
            "!=": "equal\n\tnot",
            "&&": "and",
            "||": "or",
        }

        float_op_map = {
            "+": "fadd",
            "-": "fsub",
            "*": "fmul",
            "/": "fdiv",
            "<": "finf",
            "<=": "finfeq",
            ">": "fsup",
            ">=": "fsupeq",
        }

        # Concatenar strings com +
        if left_type == "string" and right_type == "string" and operator == "+":
            self.emit("swap")
            self.emit("concat")
            return

        # Se o resultado for float, usar instruções float
        if result_type == "float":
            # Converter operandos int em float, se necessário
            if left_type == "int":
                self.emit("itof")
            if right_type == "int":
                self.emit("itof")
            # Usar float_op_map se disponível, senão fallback
            self.emit(float_op_map.get(operator, op_map[operator]))
        elif result_type == "string":
            # (Normalmente só para + entre strings, já tratado acima)
            pass
        else:
            # Caso contrário, operações int / bool
            inst = op_map.get(operator)
            if inst:
                self.emit(inst)

    def visit_UnaryOp(self, node: UnaryOp):
        """
        Lida com operadores unários: '-', '!', '++', '--'.
        Pressupõe que a análise semântica validou o uso.
        """
        op = node.operator
        if op in ["++", "--"]:
            # Pré-incremento/decremento
            var_name = node.operand.name
            self.visit(node.operand)  # Stack o valor atual
            self.emit("pushi 1")
            if op == "++":
                self.emit("add")
            else:
                self.emit("sub")

            # Armazena de volta
            if var_name in self.global_vars:
                addr = self.global_vars[var_name]["address"]
                self.emit(f"storeg {addr}")
            else:
                offset = self.local_vars[var_name]["offset"]
                self.emit(f"storel {offset}")

        elif op == "-":
            # Negação aritmética
            self.emit("pushi 0")
            self.visit(node.operand)
            self.emit("sub")
        elif op == "!":
            # Negação lógica
            self.visit(node.operand)
            self.emit("not")

    def visit_Literal(self, node: Literal):
        """
        Dá stack do literal (int, float, string, bool).
        """
        if node.inferred_type == "int":
            self.emit(f"pushi {node.value}")
        elif node.inferred_type == "float":
            self.emit(f"pushf {node.value}")
        elif node.inferred_type == "string":
            self.emit(f'pushs "{node.value}"')
        elif node.inferred_type == "bool":
            self.emit(f"pushi {1 if node.value else 0}")

    def visit_Variable(self, node: Variable):
        """
        Dá stack ao valor de uma variável (global ou local).
        Se for parâmetro de função, lida com offsets de FP conforme a convenção usada.
        """
        var_name = node.name
        if var_name in self.global_vars:
            addr = self.global_vars[var_name]["address"]
            self.emit(f"pushg {addr}")
        elif var_name in self.local_vars:
            var_info = self.local_vars[var_name]
            if var_info.get("param"):
                # Parâmetro de função, offset pode ser negativo em certas convenções
                param_num = var_info["param_num"]
                self.emit("pushfp", f"Access param {var_name}")
                self.emit(f"load -{param_num}", f"Load param at offset -{param_num}")
            else:
                # Variável local normal
                offset = var_info["offset"]
                self.emit(f"pushl {offset}")

    def visit_ArrayAccess(self, node: ArrayAccess):
        """
        Acesso a elemento de array (que pode ser multidimensional):
        1) Stack á referência base
        2) Calcula o índice linear
        3) Usa 'loadn' para ler o valor
        """
        self.visit(node.array)
        array_type = node.array.inferred_type
        if not isinstance(array_type, ArrayType):
            return  # O analisador semântico terá reportado erro antes

        # Calcula índice linear
        self.calculate_array_index(array_type.dimensions, node.indices)

        # Carrega valor (loadn)
        self.emit("loadn")

    def visit_FunctionCall(self, node: FunctionCall):
        """
        Chamadas de função:
        1) Avaliar argumentos (em ordem inversa para dar stack corretamente)
        2) pusha <function_name>
        3) call
        4) Se a função retorna valor mas o chamador é um ExpressionStatement,
           descarta-se (pop 1).
        """
        # Se for função built-in, tratar separadamente
        if node.name in ["print", "read", "toInt", "toFloat", "toStr", "len"]:
            self.visit_builtin_function_call(node)
            return

        # Dá stack aos argumentos em ordem inversa
        for arg in reversed(node.arguments):
            self.visit(arg)

        self.emit(f"pusha {node.name}")
        self.emit("call")

        # Verifica se retorna valor
        returns_value = (node.inferred_type != "void")
        parent = getattr(self, "current_statement", None)
        is_expression_stmt = isinstance(parent, ExpressionStatement)

        # Se retorna valor mas está a ser usado como statement, faz pop
        if returns_value and is_expression_stmt:
            self.emit("pop 1")

    def visit_builtin_function_call(self, node: FunctionCall):
        """
        Trata separadamente as funções internas (built-in).
        """
        if node.name == "print":
            # Imprimir cada argumento
            for arg in node.arguments:
                arg_type = arg.inferred_type
                if arg_type is None:
                    arg_type = "int"  # Fallback

                # Caso hipotético de imprimir um array
                if isinstance(arg_type, ArrayType):
                    self.visit(arg)
                    self.emit("writeln")  # Exemplo simples
                else:
                    self.visit(arg)
                    if arg_type == "float":
                        self.emit("writef")
                    elif arg_type == "string":
                        self.emit("writes")
                    else:
                        self.emit("writei")

            # Se há argumentos e o último não for void, salta linha
            if node.arguments and node.arguments[-1].inferred_type != "void":
                self.emit("writeln")

        elif node.name == "read":
            self.emit("read")

        elif node.name == "toInt":
            self.visit(node.arguments[0])
            arg_type = node.arguments[0].inferred_type
            if arg_type == "float":
                self.emit("ftoi")
            elif arg_type == "string":
                self.emit("atoi")

        elif node.name == "toFloat":
            self.visit(node.arguments[0])
            arg_type = node.arguments[0].inferred_type
            if arg_type == "int":
                self.emit("itof")
            elif arg_type == "string":
                self.emit("atof")

        elif node.name == "toStr":
            self.visit(node.arguments[0])
            arg_type = node.arguments[0].inferred_type
            if arg_type == "int":
                self.emit("stri")
            elif arg_type == "float":
                self.emit("strf")

        elif node.name == "len":
            self.visit(node.arguments[0])
            arg_type = node.arguments[0].inferred_type
            if isinstance(arg_type, ArrayType):
                # Para multidimensional, poderíamos retornar a 1ª dimensão
                self.emit(f"pushi {arg_type.dimensions[0]}")
            elif arg_type == "string":
                self.emit("strlen")
            else:
                pass  # Caso improvável, analisador semântico teria tratado

    def visit_ReturnStatement(self, node: ReturnStatement):
        """
        Instrução de retorno de função. Se houver valor, adiciona-o á primeiro.
        """
        if node.value:
            self.visit(node.value)
        self.emit("return")

    def visit_ExpressionStatement(self, node: ExpressionStatement):
        """
        Visita uma expressão usada como statement.
        Guarda em 'current_statement' para detetar se uma chamada de função
        tem o valor de retorno não utilizado (caso em que faremos pop).
        """
        self.current_statement = node
        self.visit(node.expression)
        self.current_statement = None

    def visit_IfStatement(self, node: IfStatement):
        """
        Estrutura: if <cond> then <then_branch> else <else_branch>
        """
        else_label = self.generate_label("else")
        end_label = self.generate_label("endif")

        self.visit(node.condition)
        self.emit(f"jz {else_label}")

        if isinstance(node.then_branch, list):
            for stmt in node.then_branch:
                self.visit(stmt)
        else:
            self.visit(node.then_branch)

        self.emit(f"jump {end_label}")
        self.emit(f"{else_label}:")
        if node.else_branch:
            if isinstance(node.else_branch, list):
                for stmt in node.else_branch:
                    self.visit(stmt)
            else:
                self.visit(node.else_branch)

        self.emit(f"{end_label}:")

    def visit_ForStatement(self, node: ForStatement):
        """
        Estrutura: for (<init>; <cond>; <post>) { body }
        Utiliza stacks de rótulos para tratar break/continue.
        """
        start_label = self.generate_label("for")
        continue_label = self.generate_label("continue")
        end_label = self.generate_label("endfor")

        # Inicialização
        if node.init:
            self.visit(node.init)

        # Dá stack contexto de loop
        self.break_stack.append(("loop", end_label))
        self.continue_stack.append(continue_label)

        self.emit(f"{start_label}:")

        if node.condition:
            self.visit(node.condition)
            self.emit(f"jz {end_label}")

        if isinstance(node.body, list):
            for stmt in node.body:
                self.visit(stmt)
        else:
            self.visit(node.body)

        self.emit(f"{continue_label}:")

        if node.post:
            self.visit(node.post)

        self.emit(f"jump {start_label}")
        self.emit(f"{end_label}:")

        # Sai do contexto de loop
        self.break_stack.pop()
        self.continue_stack.pop()

    def visit_BreakStatement(self, node: BreakStatement):
        """
        Lida com instruções de break para loops e switch.
        Sai do constructo mais interno (loop ou switch).
        """
        if not self.break_stack:
            raise Exception("Break statement fora de loop ou switch")
            
        # Obtém o rótulo de fim do constructo mais interno
        _, end_label = self.break_stack[-1]
        self.emit(f"jump {end_label}")

    def visit_ContinueStatement(self, node: ContinueStatement):
        """
        Lida com instruções de continue em loops,
        usando a stack de 'continue_stack'.
        """
        if not self.continue_stack:
            raise Exception("Continue statement fora de loop")
            
        continue_label = self.continue_stack[-1]
        self.emit(f"jump {continue_label}")

    def visit_SwitchStatement(self, node: SwitchStatement):
        """
        Estrutura: switch <expr> { case <val>: ...; default: ... }
        Suporta instruções break e execução fall-through.
        Conserve o valor do switch para cada comparação de caso.
        """
        end_label = self.generate_label("endswitch")
        
        # Dá stack ao contexto de switch
        self.break_stack.append(("switch", end_label))

        # Avalia a expressão do switch apenas uma vez
        self.visit(node.expression)

        case_matched = False
        next_case_label = None

        for i, case in enumerate(node.cases):
            # Para cada caso, gera um rótulo para possível fall-through
            if i > 0:
                self.emit(f"{next_case_label}:")

            next_case_label = self.generate_label("case") if i < len(node.cases) - 1 else None

            # Duplica o valor do switch para comparar
            self.emit("dup 1")
            self.visit(case.value)
            self.emit("equal")

            # Se não corresponder e não for o último caso, salta para o próximo
            if next_case_label:
                self.emit(f"jz {next_case_label}")
            else:
                # Último caso: se não corresponder, salta para default
                default_label = self.generate_label("default")
                self.emit(f"jz {default_label}")

            # Caso corresponde -> executa o corpo
            # self.emit("pop 1")  # Remove o resultado da comparação
            if isinstance(case.body, list):
                for stmt in case.body:
                    self.visit(stmt)
            else:
                self.visit(case.body)

            # Falha intencional sem jump => fall-through

        # Caso default, se existir
        if node.default:
            if next_case_label:
                self.emit(f"{next_case_label}:")
            self.emit(f"{default_label}:")
            if isinstance(node.default, list):
                for stmt in node.default:
                    self.visit(stmt)
            else:
                self.visit(node.default)
        elif next_case_label:
            # Sem default, mas precisamos de um rótulo para o último salto
            self.emit(f"{next_case_label}:")
            self.emit(f"{default_label}:")

        # Marca o fim do switch
        self.emit(f"{end_label}:")

        # Tira o valor do switch da stack (se ainda existir)
        self.emit("pop 1")

        # Sai do contexto de switch
        self.break_stack.pop()
