import ast
import re
import builtins

# Helper to remove comments and docstrings from Python code
def remove_comments_and_docstrings(source):
    def visit_node(node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            if (doc := ast.get_docstring(node)) is not None:
                node.body = node.body[1:]  # remove docstring
        for child in ast.iter_child_nodes(node):
            visit_node(child)
    try:
        tree = ast.parse(source)
        visit_node(tree)
        return ast.unparse(tree)
    except:
        return source  # Fallback if AST parsing fails

# AST transformer to rename only variable names
class RenameIdentifiers(ast.NodeTransformer):
    def __init__(self):
        self.counter = 0
        self.mapping = {}
        self.builtins = set(dir(builtins))
        self.function_names = set()

    def visit_FunctionDef(self, node):
        self.function_names.add(node.name)

        # Rename function arguments
        for arg in node.args.args:
            if arg.arg not in self.mapping:
                self.mapping[arg.arg] = f'var_{self.counter}'
                self.counter += 1
            arg.arg = self.mapping[arg.arg]

        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Load, ast.Store, ast.Del)):
            if (
                node.id not in self.builtins and
                node.id not in self.function_names
            ):
                if node.id not in self.mapping:
                    self.mapping[node.id] = f'var_{self.counter}'
                    self.counter += 1
                node.id = self.mapping[node.id]
        return node

# Cleaning function that works on files (used in CLI or Flask)
def clean_code(input_path, output_path):
    with open(input_path, 'r') as infile:
        code = infile.read()

    cleaned_code = clean_code_from_string(code)

    with open(output_path, 'w') as outfile:
        outfile.write(cleaned_code)

# New: Cleaning function that works directly on code strings (used by matchers)
def clean_code_from_string(code_str):
    code = re.sub(r'#.*', '', code_str)
    code = remove_comments_and_docstrings(code)

    try:
        tree = ast.parse(code)
        transformer = RenameIdentifiers()
        transformed_tree = transformer.visit(tree)
        ast.fix_missing_locations(transformed_tree)
        code = ast.unparse(transformed_tree)
    except Exception as e:
        print(f"AST parsing error: {e}")

    cleaned_code = '\n'.join([line for line in code.splitlines() if line.strip()])
    return cleaned_code
