from tree_sitter import Language, Parser
import tree_sitter_python as tspython


class Grammar:
    def __init__(self, language: str):
        if language != "python":
            raise ValueError("not supported")
        self._language = Language(tspython.language())
        self._parser = Parser(self._language)

    def parse(self, program: bytes):
        tree = self._parser.parse(program)
        print(tree)

    def list_classes(self, program: bytes) -> list[str]:
        query = self._language.query("(class_definition name: (identifier) @class_name)")
        tree = self._parser.parse(program)
        captures = query.captures(tree.root_node)
        classes = []

        for capture in captures["class_name"]:
            class_name = capture.text.decode("utf-8")
            classes.append(class_name)
        return classes

    def list_functions(self, program: bytes) -> list[str]:
        query = self._language.query("(function_definition name: (identifier) @function_name)")
        tree = self._parser.parse(program)
        captures = query.captures(tree.root_node)
        functions = []

        for capture in captures["function_name"]:
            method = capture.text.decode("utf-8")
            functions.append(method)
        return functions
