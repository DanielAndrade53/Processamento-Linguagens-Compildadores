class ASTPrettyPrinter:
    def __init__(self):
        # Construtor vazio, não requer configuração inicial específica
        pass

    def pretty_print_ast(self, node, indent=0):
        """
        Imprime recursivamente, de forma organizada, um nó de AST (Abstract Syntax Tree)
        e os seus filhos.

        Args:
            node: O nó da AST a ser impresso.
            indent: Nível de indentação atual (por omissão: 0).
        """
        # Caso o nó seja None, imprime e retorna
        if node is None:
            print(" " * indent + "None")
            return

        # Caso o nó seja uma lista (vários nós ou instruções)
        if isinstance(node, list):
            for item in node:
                self.pretty_print_ast(item, indent)
            return

        # Obtém o nome da classe do nó (por exemplo, IfStatement, ForStatement, etc.)
        node_type = node.__class__.__name__

        # Imprime o tipo do nó com indentação
        print(" " * indent + f"{node_type}:")
        indent += 2  # Aumenta a indentação para as propriedades filhas

        # Se o nó for um dicionário (pouco comum neste contexto, mas pode acontecer)
        # obtemos os seus itens. Caso contrário, se for um objeto, obtemos o seu dicionário interno.
        if isinstance(node, dict):
            items = node.items()
        else:
            items = node.__dict__.items()

        # Itera sobre cada campo e valor do nó
        for field_name, field_value in items:
            # Imprime o nome do campo com indentação
            print(" " * indent + f"{field_name}:", end=" ")

            # Para campos de tipos primitivos (str, int, float, bool)
            # imprimimos diretamente o valor.
            if isinstance(field_value, (str, int, float, bool)):
                print(field_value)

            # Se o campo for uma lista
            elif isinstance(field_value, list):
                # Se for lista vazia, imprime "[]"
                if not field_value:
                    print("[]")
                # Se todos os elementos da lista forem primitivos, imprime a lista diretamente
                elif all(isinstance(item, (str, int, float, bool)) for item in field_value):
                    print(field_value)
                else:
                    # Para listas com nós de AST, fazemos chamadas recursivas
                    print()
                    for item in field_value:
                        self.pretty_print_ast(item, indent + 2)

            # Se o campo for um dicionário, chamamos a função recursivamente
            elif isinstance(field_value, dict):
                print()
                self.pretty_print_ast(field_value, indent + 2)

            else:
                # Para nós filhos (que são instâncias de outras classes),
                # chamamos a função recursivamente para imprimir os seus campos.
                print()
                self.pretty_print_ast(field_value, indent + 2)
