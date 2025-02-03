import textwrap
import ast
import os

SYSTEM_PROMPT = """
You are an expert AI assistant that specializes in providing Python code to solve the task/problem at hand provided by the user.

You can use Python code freely, including the following available functions:

<|functions_schema|>
{{functions_schema}}
<|end_functions_schema|>

The following dangerous builtins are restricted for security:
- exec
- eval
- execfile
- compile
- importlib
- input
- exit

Think step by step and provide your reasoning, outside of the function calls.
You can write Python code and use the available functions. Provide all your python code in a SINGLE markdown code block like the following:

```python
result = example_function(arg1, "string")
result2 = example_function2(result, arg2)
```

DO NOT use print() statements AT ALL. Avoid mutating variables whenever possible.
""".strip()

def extract_tool_docstrings(tools_folder):
    tool_descriptions = []

    # Walk through all files in the tools folder
    for filename in os.listdir(tools_folder):
        if filename.endswith('.py'):
            file_path = os.path.join(tools_folder, filename)
            
            with open(file_path, 'r') as file:
                script_contents = file.read()
            
            # Parse the script into an AST
            module = ast.parse(script_contents)
            
            # Iterate through all function definitions
            for node in ast.walk(module):
                if isinstance(node, ast.FunctionDef):
                    # Check for @tool decorator
                    if any(isinstance(decorator, ast.Name) and decorator.id == 'tool' for decorator in node.decorator_list):
                        # Get function signature
                        args = []
                        for arg in node.args.args:
                            arg_name = arg.arg
                            arg_annotation = ast.unparse(arg.annotation) if arg.annotation else 'Any'
                            args.append(f"{arg_name}: {arg_annotation}")
                        
                        signature = f"def {node.name}({', '.join(args)}):"
                        
                        # Extract docstring
                        docstring = ast.get_docstring(node) or "No description provided."
                        
                        # Compile function description
                        tool_description = f"{signature}\n    \"\"\"\n    {textwrap.indent(docstring, '    ')}\n    \"\"\""
                        tool_descriptions.append(tool_description)
    
    # Combine all tool descriptions
    return "tool_descriptions = \"\"\"\n" + "\n\n".join(tool_descriptions) + "\n\"\"\""