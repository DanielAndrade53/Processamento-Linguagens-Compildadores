import os

from ply import yacc
import sys
import re


from danielLexer import MyLexer

class MyParser(object):

    def __init__(self):
        self.lexer = MyLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, debug=False)
        self.parser.assembly = ''
        self.parser.vars = {}
        self.parser.exito = True
        self.parser.error = ''
        self.parser.stackPointer = 0
        self.parser.store_counter = 0
        self.parser.instructions = []
        self.parser.ifelse_counter = 0

    # ------------------------------------------------

    # Program-Definition

    def p_Program_1(self, p):
        '''Program : DeclarationList'''
        self.parser.assembly = f'START\n{p[1]}STOP'

    def p_Program_2(self, p):
        '''Program : '''
        self.parser.assembly = ''

    def p_DeclarationList_1(self, p):
        '''DeclarationList : Declaration'''
        p[0] = f'{p[1]}'

    def p_DeclarationList_2(self, p):
        '''DeclarationList : Declaration DeclarationList'''
        p[0] = f'{p[1]}{p[2]}'

    def p_Declaration_1(self, p):
        '''Declaration : VarDecl SEMICOLON'''
        p[0] = f'{p[1]}'

    def p_Declaration_2(self, p):
        '''Declaration : ArrayDecl SEMICOLON'''
        p[0] = f'{p[1]}'

    def p_Declaration_3(self, p):
        '''Declaration : ConstDecl SEMICOLON'''
        p[0] = f'{p[1]}'

    def p_Declaration_5(self, p):
        '''Declaration : FunctionDecl SEMICOLON'''
        p[0] = f'{p[1]}'

    def p_Declaration_6(self, p):
        '''Declaration : IfStmt SEMICOLON'''
        p[0] = f'{p[1]}'

    def p_Declaration_7(self, p):
        '''Declaration : ForStmt SEMICOLON'''
        p[0] = f'{p[1]}'

    def p_Declaration_8(self, p):
        '''Declaration : Assignment SEMICOLON'''
        p[0] = f'{p[1]}'

    # Variable-Declarator

    # x := 5
    def p_VarDecl_1(self, p):
        '''VarDecl : ShortVarDecl'''
        p[0] = f'{p[1]}'

    # var x int = 4
    def p_VarDecl_2(self, p):
        '''VarDecl : VAR VarSpec'''
        p[0] = f'{p[2]}'

    # x := 5
    def p_shortVarDecl_1(self, p):
        '''ShortVarDecl : IdentifierList WALRUS ExpressionList'''
        p[0] = f'{p[1]}{p[3]}'

    # x int = 4
    def p_VarSpec_1(self, p):
        '''VarSpec : IdentifierList Type EQUAL ExpressionList'''
        p[0] = f'{p[1]}{p[2]}{p[4]}'

    # x int
    def p_VarSpec_2(self, p):
        '''VarSpec : IdentifierList Type'''

        result = ''

        tam = len(p[1]) // 8  # Integer division to get the number of iterations

        for i in range(tam):
            result += f'PUSHI 0\nPUSHI 0\n'  # Default value 0
            result += f'STOREG {self.parser.store_counter}\n'
            self.parser.store_counter += 1

        p[0] = result

    # x = 4
    def p_VarSpec_3(self, p):
        '''VarSpec : IdentifierList EQUAL ExpressionList'''
        p[0] = f'{p[1]}{p[3]}'

    # Identifiers-Declarator

    def p_IdentifierList_1(self, p):
        '''IdentifierList : Identifier'''
        p[0] = f'{p[1]}'

    def p_IdentifierList_2(self, p):
        '''IdentifierList : Identifier COMMA IdentifierList'''
        p[0] = f'{p[1]}{p[3]}'

    def p_Identifier_1(self, p):
        '''Identifier : ID'''

        varName = p[1]

        if varName not in self.parser.vars:
            self.parser.vars[varName] = (self.parser.stackPointer, varName)
            p[0] = f'PUSHI 0\n'
            self.parser.stackPointer += 1
        else:
            p[0] = f'ERR "ALREADY IN SELF.PARSER.VARS"\n'
            # self.parser.exito = False


    # Expression-Declarator

    def p_ExpressionList_1(self, p):
        '''ExpressionList : Expression'''
        p[0] = f'{p[1]}'


    def p_ExpressionList_2(self, p):
        '''ExpressionList : Expression COMMA ExpressionList'''
        p[0] = f'{p[1]}{p[3]}'

    def p_Expression_1(self, p):
        '''Expression : NUMBER_LITERAL'''
        p[0] = f'PUSHI {int(p[1])}\nSTOREG {self.parser.store_counter}\n'
        self.parser.store_counter += 1

    def p_Expression_2(self, p):
        '''Expression : STRING_LITERAL'''
        p[0] = f'PUSHS "{str(p[1])}"\nSTOREG {self.parser.store_counter}\n'
        self.parser.store_counter += 1

    # aqui troca-se p1 p2 p3 por p1 p3 p2 para fazer x y add
    def p_Expression_3(self, p):
        '''Expression : Expression BinaryOp Expression'''
        p[0] = f'{p[1]}{p[3]}{p[2]}'

    # Type-Declarator

    def p_Type_1(self, p):
        '''Type : INT'''
        p[0] = f''

    def p_Type_2(self, p):
         '''Type : FLOAT'''
         p[0] = f''

    def p_Type_3(self, p):
        '''Type : STRING'''
        p[0] = f''

    def p_Type_4(self, p):
        '''Type : BOOL'''
        p[0] = f''

    # Binary-Operator-Declarator

    def p_BinaryOp_1(self, p):
        '''BinaryOp : SUM'''
        p[0] = f'ADD\n'

    def p_BinaryOp_2(self, p):
        '''BinaryOp : DIFFERENCE'''
        p[0] = f'SUB\n'

    def p_BinaryOp_3(self, p):
        '''BinaryOp : PRODUCT'''
        p[0] = f'MUL\n'

    def p_BinaryOp_4(self, p):
        '''BinaryOp : QUOTIENT'''
        p[0] = f'DIV\n'

    # Constant-Declarator (por fazer)

    def p_ConstDecl_1(self, p):
        '''ConstDecl : CONST ConstSpec'''
        p[0] = f'{p[2]}'

    def p_ConstSpec_1(self, p):
        '''ConstSpec : IdentifierList'''

        result = ''

        tam = len(p[1]) // 8  # Integer division to get the number of iterations

        for i in range(tam):
            result += f'PUSHI 0\nPUSHI 0\n'  # Default value 0
            result += f'STOREG {self.parser.store_counter}\n'
            self.parser.store_counter += 1

        p[0] = result

    def p_ConstSpec_2(self, p):
        '''ConstSpec : IdentifierList Type EQUAL ExpressionList'''
        p[0] = f'{p[1]}{p[2]}{p[4]}'

    def p_ConstSpec_3(self, p):
        '''ConstSpec : IdentifierList EQUAL ExpressionList'''
        p[0] = f'{p[1]}{p[3]}'








    # Functions-Declarator (por fazer)

    def p_FunctionDecl_1(self, p):
        '''FunctionDecl : FUNC FunctionName Signature FunctionBody'''
        p[0] = f'{p[2]}{p[3]}{p[4]}'

    def p_FunctionDecl_2(self, p):
        '''FunctionDecl : FUNC FunctionName Signature'''
        p[0] = f'{p[2]}{p[3]}'

    def p_FunctionName_1(self, p):
        '''FunctionName : ID'''
        p[0] = f'JUMP {p[1]}\n{p[1]}:NOP\n'

    def p_Signature_1(self, p):
        '''Signature : LPAREN ParameterList RPAREN'''
        p[0] = f'{p[2]}'

    def p_Signature_2(self, p):
        '''Signature : LPAREN RPAREN'''
        p[0] = f''

    def p_FunctionBody_1(self, p):
        '''FunctionBody : Block'''
        p[0] = f'{p[1]}'

    def p_ParameterList_1(self, p):
        '''ParameterList : ParameterDecl'''
        p[0] = f'{p[1]}'

    def p_ParameterList_2(self, p):
        '''ParameterList : ParameterDecl COMMA ParameterList'''
        p[0] = f'{p[1]}{p[3]}'

    def p_ParameterDecl_1(self, p):
        '''ParameterDecl : IdentifierList Type'''
        p[0] = f'{p[1]}{p[2]}'













    # If-Statement-Declarator

    def p_IfStmt_1(self, p):
        '''IfStmt : IF IfElseExpressionRel Block'''
        p[0] = f'{p[2]}then:NOP\n{p[3]}JUMP end{self.parser.ifelse_counter}\nelse{self.parser.ifelse_counter}:NOP\nend{self.parser.ifelse_counter}:NOP\n'

    def p_IfStmt_2(self, p):
        '''IfStmt : IF IfElseExpressionRel Block ELSE Block'''
        p[0] = f'{p[2]}then: NOP\n{p[3]}JUMP end{self.parser.ifelse_counter}\nelse{self.parser.ifelse_counter}:NOP\n{p[5]}end{self.parser.ifelse_counter}:NOP\n'

    def p_IfStmt_3(self, p):
        '''IfStmt : IF IfElseExpressionRel Block ELSE IfStmt'''
        self.parser.ifelse_counter += 1
        p[0] = f'{p[2]}then: NOP\n{p[3]}JUMP end{self.parser.ifelse_counter}\nelse1:NOP\n{p[5]}end{self.parser.ifelse_counter}:NOP\n'

    def p_IfElseExpressionRel_1(self, p):
        '''IfElseExpressionRel : ID Relation ID'''
        var1 = p[1]
        var1Value = self.parser.vars[var1][0]
        var2 = p[3]
        var2Value = self.parser.vars[var2][0]
        p[0] = f'PUSHG {var1Value}\nPUSHG {var2Value}\n{p[2]}\nJZ else{self.parser.ifelse_counter}\n'

    def p_IfElseExpressionRel_2(self, p):
        '''IfElseExpressionRel : NUMBER_LITERAL Relation NUMBER_LITERAL'''
        p[0] = f'PUSHI {int(p[1])}\nPUSHI {int(p[3])}\n{p[2]}\nJZ else{self.parser.ifelse_counter}\n'

    def p_IfElseExpressionRel_3(self, p):
        '''IfElseExpressionRel : NUMBER_LITERAL Relation ID'''
        var2 = p[3]
        var2Value = self.parser.vars[var2][0]
        p[0] = f'PUSHI {int(p[1])}\nPUSHG {var2Value}\n{p[2]}\nJZ else{self.parser.ifelse_counter}\n'

    def p_IfElseExpressionRel_4(self, p):
        '''IfElseExpressionRel : ID Relation NUMBER_LITERAL'''
        var1 = p[1]
        var1Value = self.parser.vars[var1][0]
        p[0] = f'PUSHG {var1Value}\nPUSHI {int(p[3])}\n{p[2]}\nJZ else{self.parser.ifelse_counter}\n'

    def p_Relation_1(self, p):
        '''Relation : LESS'''
        p[0] = f'INF'
        self.parser.ifelse_counter += 1

    def p_Relation_2(self, p):
        '''Relation : GREATER'''
        p[0] = f'SUP'
        self.parser.ifelse_counter += 1


    def p_Relation_3(self, p):
        '''Relation : LESSOREQUAL'''
        p[0] = f'INFEQ'
        self.parser.ifelse_counter += 1

    def p_Relation_4(self, p):
        '''Relation : GREATEROREQUAL'''
        p[0] = f'SUPEQ'
        self.parser.ifelse_counter += 1

    def p_Relation_5(self, p):
        '''Relation : EQUALITY'''
        p[0] = f'NOT'
        self.parser.ifelse_counter += 1

    def p_Relation_6(self, p):
        '''Relation : REMAINDER'''
        p[0] = f'MOD'
        self.parser.ifelse_counter += 1


































    # For-Statement-Declarator

    def p_ForStmt_1(self, p):
        '''ForStmt : FOR Condition Block'''
        p[0] = f'{p[2]}{p[3]}'

    # for i=0, i < 5, i++ {} ;
    def p_ForStmt_2(self, p):
        '''ForStmt : FOR InitStmt SEMICOLON Condition SEMICOLON PostStmt Block'''
        p[0] = f'{p[2]}{p[4]}{p[6]}{p[7]}'

    def p_ForStmt_3(self, p):
        '''ForStmt : FOR Block'''
        p[0] = f'{p[2]}'

    def p_Condition_1(self, p):
        '''Condition : ForExpressionRel'''
        p[0] = f'{p[1]}'

    def p_ForExpressionRel_1(self, p):
        '''ForExpressionRel : ID Relation ID'''
        var1 = p[1]
        var1Value = self.parser.vars[var1][0]
        var2 = p[3]
        var2Value = self.parser.vars[var2][0]
        p[0] = f'PUSHG {var1Value}\nPUSHG {var2Value}\n{p[2]}\n'

    def p_ForExpressionRel_2(self, p):
        '''ForExpressionRel : NUMBER_LITERAL Relation NUMBER_LITERAL'''
        p[0] = f'PUSHI {int(p[1])}\nPUSHI {int(p[3])}\n{p[2]}\n'

    def p_ForExpressionRel_3(self, p):
        '''ForExpressionRel : NUMBER_LITERAL Relation ID'''
        var2 = p[3]
        var2Value = self.parser.vars[var2][0]
        p[0] = f'PUSHI {int(p[1])}\nPUSHG {var2Value}\n{p[2]}\n'

    def p_ForExpressionRel_4(self, p):
        '''ForExpressionRel : ID Relation NUMBER_LITERAL'''
        var1 = p[1]
        var1Value = self.parser.vars[var1][0]
        p[0] = f'PUSHG {var1Value}\nPUSHI {int(p[3])}\n{p[2]}\n'

    def p_InitStmt_1(self, p):
        '''InitStmt : SimpleStmt'''
        p[0] = f'{p[1]}'

    def p_PostStmt_1(self, p):
        '''PostStmt : SimpleStmt'''
        p[0] = f'{p[1]}'











    # Block-Declarator

    def p_Block_1(self, p):
        '''Block : LBRACE StatementList RBRACE'''
        p[0] = f'{p[2]}'

    def p_StatementList_1(self, p):
        '''StatementList : Statement'''
        p[0] = f'{p[1]}'

    def p_StatementList_2(self, p):
        '''StatementList : Statement COMMA StatementList'''
        p[0] = f'{p[1]}{p[3]}'

    # Statement-Declarator

    def p_Statement_1(self, p):
        '''Statement : Declaration'''
        p[0] = f'{p[1]}'

    def p_Statement_2(self, p):
        '''Statement : SimpleStmt'''
        p[0] = f'{p[1]}'

    def p_Statement_3(self, p):
        '''Statement : ReturnStmt'''
        p[0] = f'RETURN {p[1]}\n'

    def p_Statement_4(self, p):
        '''Statement : BreakStmt'''
        p[0] = f'BREAK {p[1]}\n'

    def p_Statement_5(self, p):
        '''Statement : ContinueStmt'''
        p[0] = f'CONTINUE {p[1]}\n'

    def p_Statement_6(self, p):
        '''Statement : Block'''
        p[0] = f'{p[1]}'

    def p_Statement_7(self, p):
        '''Statement : IfStmt'''
        p[0] = f'{p[1]}'

    def p_Statement_8(self, p):
        '''Statement : ForStmt'''
        p[0] = f'{p[1]}'






    # Simple-Statement-Declarator

    def p_SimpleStmt_1(self, p):
        '''SimpleStmt : EmptyStmt'''
        p[0] = f'{p[1]}'

    def p_SimpleStmt_2(self, p):
        '''SimpleStmt : IncDecStmt'''
        p[0] = f'{p[1]}'

    """def p_SimpleStmt_4(self, p):
        '''SimpleStmt : ID WALRUS NUMBER_LITERAL'''
        p[0] = f'PUSHI 0\nPUSHI {p[3]}\nSTOREG {self.parser.store_counter}\n'
        self.parser.store_counter += 1"""

    def p_SimpleStmt_3(self, p):
        '''SimpleStmt : Assignment'''
        p[0] = f'{p[1]}'





    def p_EmptyStmt_1(self, p):
        '''EmptyStmt : '''
        p[0] = f''




    def p_IncDecStmt_1(self, p):
        '''IncDecStmt : Expression PLUSPLUS'''
        p[0] = f'{p[1]}\nPUSHI 1\nADD\n'

    def p_IncDecStmt_2(self, p):
        '''IncDecStmt : Expression MINUSMINUS'''
        p[0] = f'{p[1]}\nPUSHI 1\nSUB\n'


    # Return-Statement-Declarator

    def p_ReturnStmt_1(self, p):
        '''ReturnStmt : RETURN'''
        p[0] = f''

    def p_ReturnStmt_2(self, p):
        '''ReturnStmt : RETURN Expression'''
        p[0] = f'{p[2]}'

    # Break-Statement-Declarator

    def p_BreakStmt_1(self, p):
        '''BreakStmt : BREAK'''
        p[0] = f''

    def p_BreakStmt_2(self, p):
        '''BreakStmt : BREAK Label'''
        p[0] = f'{p[2]}'

    def p_Label_1(self, p):
        '''Label : ID'''
        p[0] = f'{p[1]}'

    # Continue-Statement-Declarator

    def p_ContinueStmt_1(self, p):
        '''ContinueStmt : CONTINUE'''
        p[0] = f''

    def p_ContinueStmt_2(self, p):
        '''ContinueStmt : CONTINUE Label'''
        p[0] = f'{p[2]}'

    # Assignment-Statement-Declarator

    def p_Assignment_1(self, p):
        '''Assignment : ID EQUAL Expression'''
        varName = p[1]
        if varName in self.parser.vars:
            p[0] = f'{p[3]}STOREG {self.parser.vars[varName][0]}\n'
        else:
            p[0] = f'ERR "VARIAVEL NÃO DECLARADA"\n'
            # self.parser.exito = False

    def p_Assignment_2(self, p):
        '''Assignment : ID EQUAL ID BinaryOp ID'''
        varName = p[1]
        var1 = p[3]
        var2 = p[5]
        if varName in self.parser.vars:
            p[0] = f'PUSHG {self.parser.vars[var1][0]}\nPUSHG {self.parser.vars[var2][0]}\n{p[4]}STOREG {self.parser.vars[varName][0]}\n'
        else:
            p[0] = f'ERR "VARIAVEL NÃO DECLARADA"\n'
            # self.parser.exito = False

    # ---------------------------------------------------------

    # Array-Declarator (por fazer)

    # var x = [3]int{1,2,3}

    def p_ArrayDecl_1(self, p):
        '''ArrayDecl : VAR IdentifierList EQUAL ArraySpec'''
        p[0] = f'{p[2]}{p[4]}'

        # x := [3]int{1,2,3}

    def p_ArrayDecl_2(self, p):
        '''ArrayDecl : IdentifierList WALRUS ArraySpec'''
        p[0] = f'{p[1]}{p[3]}'

        # [3]int{1,2,3}

    def p_ArraySpec_1(self, p):
        '''ArraySpec : LBRACKET NUMBER_LITERAL RBRACKET Type ArrayBody'''
        # array_length = p[2]
        # self.parser.is_array = True
        # self.parser.array_length = array_length
        p[0] = f'{p[4]}{p[5]}'

        # {1,2,3}

    def p_ArrayBody_1(self, p):
        '''ArrayBody : Block'''
        p[0] = f'{p[1]}'

    def p_error(self, p):
        if p:
            print(f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}")
        else:
            print("Syntax error: unexpected end of file (EOF)")
        self.parser.exito = False


# melhorar isto
if __name__ == '__main__':
    myparser = MyParser()

    if len(sys.argv) >= 2:
        input_file_name = sys.argv[1]
        if not re.match(r'.*\.plc$', input_file_name):
            print("Error: not a .plc file")
            sys.exit(1)

        try:
            with open(input_file_name, 'r') as file:
                content = file.read()
                myparser.parser.parse(content)

                if myparser.parser.exito:
                    print("Parsing sucessful!")
                    print(myparser.parser.vars)
                    print("Generated Assembly: ")
                    print(myparser.parser.assembly)

                    file.close()
                    outputFileName = f'{os.path.splitext(input_file_name)[0]}.vm'

                    with open(outputFileName, 'w') as output_file:
                        output_file.write(myparser.parser.assembly)
                        print(f'Assembly written to {outputFileName}')

                else:
                    print("Parsing failed!")
                    print(myparser.parser.error)


        except FileNotFoundError:
            print(f'Error: file {input_file_name} not found')
            sys.exit(1)

    else:
        print("Not enough arguments")
        sys.exit(1)
