# Script for generating some of documents in `dev-docs` from Misago's code
import ast
from pathlib import Path

HOOKS_MODULES = (
    "misago.oauth2.hooks",
)

BASE_PATH = Path(__file__).parent
DOCS_PATH = BASE_PATH / "dev-docs"
PLUGINS_PATH = DOCS_PATH / "plugins"
PLUGINS_HOOKS_PATH = PLUGINS_PATH / "hooks"


def main():
    generate_hooks_reference()


def generate_hooks_reference():
    hooks_data: dict[str, dict[str, ast.Module]] = {}
    for hooks_module in HOOKS_MODULES:
        init_path = module_path_to_init_path(hooks_module)
        hooks_data[hooks_module] = get_all_modules(init_path)

    generate_hooks_reference_index(hooks_data)

    for import_from, module_hooks in hooks_data.items():
        for hook_name, hook_module in module_hooks.items():
            generate_hook_reference(import_from, hook_name, hook_module)


def generate_hooks_reference_index(hooks_data: dict[str, dict[str, ast.Module]]):
    with open(PLUGINS_HOOKS_PATH / "index.md", "w") as fp:
        fp.write("# Hook reference")
        fp.write("\n\n")
        fp.write("This document contains a list of all standard plugin hooks existing in Misago.")
        fp.write("\n\n")
        fp.write("Hooks instances are importable from the following Python modules:")

        fp.write("\n")
        for module_name in sorted(hooks_data):
            fp.write(f"\n- [`{module_name}`](#{slugify_name(module_name)})")

        for module_name, module_hooks in hooks_data.items():
            fp.write("\n\n\n")
            fp.write(f"## `{module_name}`")
            fp.write("\n\n")
            fp.write(f"`{module_name}` exports the following hooks:")
            fp.write("\n")

            for module_hook in sorted(module_hooks):
                fp.write(f"\n- [`{module_hook}`](./{slugify_name(module_hook)}.md)")


def generate_hook_reference(import_from: str, hook_name: str, hook_module: ast.Module):
    hook_filename = f"{slugify_name(hook_name)}.md"
    with open(PLUGINS_HOOKS_PATH / hook_filename, "w") as fp:
        fp.write(f"# `{hook_name}` hook")
        fp.write("\n\n")
        fp.write(f"This hook can be imported from `{import_from}`:")
        fp.write("\n\n")
        fp.write("```python")
        fp.write("\n")
        fp.write("# In your plugin's app.py...")
        fp.write("\n")
        fp.write(f"from {import_from} import {hook_name}")
        fp.write("\n")
        fp.write("```")


def get_all_modules(file_path: str) -> dict[str, ast.Module]:
    all_names: list[str] = []
    all_imports: dict[str, ast.Module] = {}

    file_ast: ast.Module = parse_python_file(file_path)
    for item in file_ast.body:
        if not isinstance(item, ast.Assign):
            continue  # Skip non-value assignment

        if not item.targets or not item.value:
            continue  # Skip value assignment without targets

        if item.targets[0].id != "__all__":
            continue  # Skip variables that aren't __all__

        if not isinstance(item.value, (ast.List, ast.Tuple)):
            continue  # Skip non-list or tuple

        for item_value in item.value.elts:
            if not isinstance(item_value, ast.Constant):
                raise ValueError(f"'{file_path}': '__all__' items must be constants.")
            if not isinstance(item_value.value, str):
                raise ValueError(f"'{file_path}': '__all__' items must be strings.")
            
            all_names.append(item_value.value)
    
    for item in file_ast.body:
        if not isinstance(item, ast.ImportFrom):
            continue  # Skip non-value assignment

        if len(item.names) != 1:
            continue
        
        import_name = item.names[0].name
        if import_name not in all_names:
            continue

        import_path = Path(file_path).parent / f"{item.module}.py"
        if not import_path.is_file():
            raise ValueError(
                f"'{file_path}': '{item.module}' could not be imported."
            )
        
        all_imports[import_name] = parse_python_file(import_path)
    
    for name in all_names:
        if name not in all_imports:
            raise ValueError(
                f"'{file_path}': import for '{name}' could not be found."
            )

    return {name: all_imports[name] for name in sorted(all_names)}


def parse_python_file(file_path: Path) -> ast.Module:
    with open(file_path, "r") as fp:
        return ast.parse(fp.read())


def module_path_to_init_path(module_path: str) -> Path:
    base_path = Path(BASE_PATH, *module_path.split("."), "__init__.py")
    if not base_path.is_file():
        raise ValueError(f"'{base_path}' doesn't exist or is not a file.")
    return base_path


def slugify_name(py_name: str) -> str:
    return py_name.replace(".", "-").replace("_", "-")


if __name__ == "__main__":
    main()
