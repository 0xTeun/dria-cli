import os
import ast
import sys
import textwrap
import inspect
import importlib
import re
from typing import List, Dict, Any, Callable
from pathlib import Path
from dataclasses import dataclass
from exec_python import execute_python_code

@dataclass
class Tool:
    """Represents a tool function and its metadata."""
    func: Callable
    name: str
    signature: str
    docstring: str

class ToolManager:
    """Manages tool discovery and documentation with exec-python integration."""
    
    def __init__(self, tools_dir: str | Path):
        self.tools_dir = Path(tools_dir)
        if not self.tools_dir.exists():
            raise FileNotFoundError(f"Tools directory not found: {tools_dir}")
        
        # Initialize tools cache
        self._tools: Dict[str, Tool] = {}
        self._load_tools()

    def _load_tools(self) -> None:
        """Load all tool functions from the tools directory."""
        # Add tools directory to path for imports
        parent_dir = str(self.tools_dir.parent)
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
            
        for file_path in self.tools_dir.glob('**/*.py'):
            if file_path.name.startswith('__'):
                continue
                
            try:
                module_name = f"tools.{file_path.stem}"
                module = importlib.import_module(module_name)
                
                # Find all functions with @tool decorator
                for name, func in inspect.getmembers(module):
                    if inspect.isfunction(func) and hasattr(func, 'is_tool'):
                        self._add_tool(func)
                        
            except ImportError as e:
                print(f"Error importing {module_name}: {e}")

    def _add_tool(self, func: Callable) -> None:
        """Add a tool function to the manager."""
        source = inspect.getsource(func)
        module = ast.parse(source)
        function_def = module.body[0]
        
        args = []
        for arg in function_def.args.args:
            arg_name = arg.arg
            arg_annotation = ast.unparse(arg.annotation) if arg.annotation else 'Any'
            args.append(f"{arg_name}: {arg_annotation}")
        
        signature = f"def {func.__name__}({', '.join(args)}):"
        docstring = inspect.getdoc(func) or "No description provided."
        
        self._tools[func.__name__] = Tool(
            func=func,
            name=func.__name__,
            signature=signature,
            docstring=docstring
        )

    def get_tools_schema(self) -> str:
        """Generate documentation schema for all tools."""
        if not self._tools:
            return "tool_descriptions = \"\"\"\nNo tool functions found.\n\"\"\""
        
        tool_descriptions = []
        for tool in self._tools.values():
            description = (
                f"{tool.signature}\n"
                f"    \"\"\"\n"
                f"    {textwrap.indent(tool.docstring, '    ')}\n"
                f"    \"\"\""
            )
            tool_descriptions.append(description)
        
        return "tool_descriptions = \"\"\"\n" + "\n\n".join(tool_descriptions) + "\n\"\"\""

    def get_available_tools(self) -> List[Callable]:
        """Get list of all available tool functions for exec-python."""
        return [tool.func for tool in self._tools.values()]

    def execute_llm_response(self, response: str) -> Any:
        """
        Extract and execute Python code from LLM response using exec-python.
        
        Args:
            response: LLM response containing Python code block
            
        Returns:
            Execution results from exec-python
        """
        code_match = re.search(r'```python\n(.*?)```', response, re.DOTALL)
        
        if code_match:
            code = code_match.group(1).strip()
            function_results = execute_python_code(
                code=code,
                functions=self.get_available_tools()
            )
            print(function_results)
            return function_results
        
        return "No Python code found in response"