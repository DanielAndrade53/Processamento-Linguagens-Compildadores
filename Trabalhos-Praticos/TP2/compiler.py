from cparser.parser import parser
from cparser.lexer import lexer
from semantic.semantic_analyzer import SemanticAnalyzer
from codegen.code_generator import CodeGenerator
from c_ast.ast_pretty_printer import ASTPrettyPrinter
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filepath>")
        sys.exit(1)

    try:
        with open(sys.argv[1], "r") as file:
            source = file.read()

        print("\nParsing -------------------")

        ast = parser.parse(source, lexer, debug=False)
        if not ast:
            print()
            raise ValueError("Parsing failed")

        print("Parsing successful!")

        print("\nAnalyzing -------------------")
        ast = SemanticAnalyzer().analyze(ast)
        print("Semantic analysis successful!")

        print("\nAST -------------------")
        ASTPrettyPrinter().pretty_print_ast(ast)

        print("\nGenerating code -------------------")
        print()
        code = CodeGenerator().generate_code(ast)
        print(code)

        output_filename = sys.argv[1].replace(".go", ".vm")

        with open(output_filename, "w") as output_file:
            output_file.write(code)

        print(f"\nCode written to {output_filename}")

        print("\nCompilation successful!")

    except FileNotFoundError:
        print(f"\nError: File '{sys.argv[1]}' not found")
    except Exception as e:
        print(f"\nCompilation failed: {str(e)}")
