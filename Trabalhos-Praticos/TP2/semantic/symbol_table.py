from contextlib import contextmanager
from typing import Dict, Generator, List, Optional
from c_ast.ast_nodes import Symbol

class SymbolTable:
    """
    Implementa uma tabela de símbolos simples, suportando contextos aninhados (nested scopes).
    Internamente, mantém uma stack (lista) de dicionários, onde cada dicionário representa um scope.
    """

    def __init__(self):
        # Iniciamos com um scope global (vazio).
        self.scopes: List[Dict[str, Symbol]] = [{}]

    @contextmanager
    def new_scope(self) -> Generator[None, None, None]:
        """
        Gerente de contexto (context manager) para lidar com a entrada e saída de um scope:
            with self.new_scope():
                # tudo aqui dentro está num novo scope
        """
        self.enter_scope()
        try:
            yield
        finally:
            self.exit_scope()

    def enter_scope(self):
        """
        Entrar num novo scope (push de um dicionário vazio).
        """
        self.scopes.append({})

    def exit_scope(self):
        """
        Sair do scope atual (pop), mantendo sempre pelo menos o scope global.
        """
        if len(self.scopes) > 1:
            self.scopes.pop()

    def define(self, name: str, symbol: Symbol) -> None:
        """
        Define um símbolo no scope atual (o mais interno).
        Lança uma exceção se o símbolo já existir nesse mesmo scope.
        """
        if name in self.scopes[-1]:
            raise Exception(f"Symbol '{name}' already defined in current scope")
        self.scopes[-1][name] = symbol

    def lookup(self, name: str) -> Optional[Symbol]:
        """
        Procura um símbolo de dentro para fora (do scope mais interno ao mais externo).
        Se encontrar, retorna o símbolo; caso contrário, retorna None.
        """
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
