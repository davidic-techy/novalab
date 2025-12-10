import ast

class CodeValidator:
    """
    Static analysis to ensure code safety and quality.
    """
    FORBIDDEN_IMPORTS = ['os', 'sys', 'subprocess', 'shutil']

    @staticmethod
    def validate_python(code_string):
        """
        Parses the code into an Abstract Syntax Tree (AST) to check for banned imports.
        Returns (is_safe, error_message).
        """
        try:
            tree = ast.parse(code_string)
        except SyntaxError as e:
            return False, f"Syntax Error: {e}"

        for node in ast.walk(tree):
            # Check for 'import x'
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in CodeValidator.FORBIDDEN_IMPORTS:
                        return False, f"Importing '{alias.name}' is forbidden in NovaLab."
            
            # Check for 'from x import y'
            elif isinstance(node, ast.ImportFrom):
                if node.module in CodeValidator.FORBIDDEN_IMPORTS:
                    return False, f"Importing from '{node.module}' is forbidden."

        return True, "Code is safe."