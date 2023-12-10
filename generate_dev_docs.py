# Script for generating some of documents in `dev-docs` from Misago's code
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Union

HOOKS_MODULES = ("misago.oauth2.hooks",)

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
    with open(PLUGINS_HOOKS_PATH / "reference.md", "w") as fp:
        fp.write("# Built-in hook reference")
        fp.write("\n\n")
        fp.write(
            "This document contains a list of all standard plugin hooks existing in Misago."
        )
        fp.write("\n\n")
        fp.write("Hooks instances are importable from the following Python modules:")

        fp.write("\n")
        for module_name in sorted(hooks_data):
            fp.write(f"\n- [`{module_name}`](#{slugify_name(module_name)})")

        for module_name, module_hooks in hooks_data.items():
            fp.write("\n\n\n")
            fp.write(f"## `{module_name}`")
            fp.write("\n\n")
            fp.write(f"`{module_name}` defines the following hooks:")
            fp.write("\n")

            for module_hook in sorted(module_hooks):
                fp.write(f"\n- [`{module_hook}`](./{slugify_name(module_hook)}.md)")


def generate_hook_reference(import_from: str, hook_name: str, hook_module: ast.Module):
    hook_filename = f"{slugify_name(hook_name)}.md"

    module_docstring = None
    module_classes = {}
    for item in hook_module.body:
        if isinstance(item, ast.ClassDef):
            module_classes[item.name] = item

        if (
            isinstance(item, ast.Expr)
            and item.value
            and isinstance(item.value, ast.Constant)
            and isinstance(item.value.value, str)
        ):
            if module_docstring is not None:
                raise ValueError(
                    f"'{hook_name}': module with hook defines multiple docstrings."
                )
            module_docstring = parse_hook_docstring(item.value.value)

    hook_type: str | None = None
    hook_ast: ast.ClassDef | None = None
    hook_action_ast: ast.ClassDef | None = None
    hook_filter_ast: ast.ClassDef | None = None
    for class_name, class_ast in module_classes.items():
        class_hook_type = is_class_base_hook(class_ast)
        if class_hook_type:
            hook_ast = class_ast
            hook_type = class_hook_type
        elif is_class_protocol(class_ast):
            if class_name.endswith("HookAction"):
                hook_action_ast = class_ast
            elif class_name.endswith("HookFilter"):
                hook_filter_ast = class_ast

    with open(PLUGINS_HOOKS_PATH / hook_filename, "w") as fp:
        fp.write(f"# `{hook_name}`")

        if module_docstring and module_docstring.description:
            fp.write("\n\n")
            fp.write(module_docstring.description)

        if hook_type == "FILTER":
            fp.write("\n\n")
            fp.write(f"`{hook_name}` is a **filter** hook.")
        if hook_type == "ACTION":
            fp.write("\n\n")
            fp.write(f"`{hook_name}` is an **action** hook.")

        fp.write("\n\n\n")
        fp.write("## Location")
        fp.write("\n\n")
        fp.write(f"This hook can be imported from `{import_from}`:")
        fp.write("\n\n")
        fp.write("```python")
        fp.write("\n")
        fp.write("# exaple_plugin/register_hooks.py")
        fp.write("\n")
        fp.write(f"from {import_from} import {hook_name}")
        fp.write("\n\n")
        fp.write(f"from .override_{hook_name} import {hook_name}")
        fp.write("\n")
        fp.write("```")

        if hook_filter_ast:
            fp.write("\n\n\n")
            fp.write("## Filter")

        if hook_action_ast:
            fp.write("\n\n\n")
            fp.write("## Action")
        
        if module_docstring and module_docstring.examples:
            for example_title, example_text in module_docstring.examples.items():
                fp.write("\n\n\n")
                fp.write(f"## {example_title}")
                fp.write("\n\n")
                fp.write(example_text)


def is_class_base_hook(class_def: ast.ClassDef) -> str | None:
    if not class_def.bases:
        return None

    for base in class_def.bases:
        if (
            isinstance(base, ast.Subscript)
            and isinstance(base.value, ast.Name)
            and isinstance(base.value.id, str)
        ):
            if base.value.id == "FilterHook":
                return "FILTER"
            if base.value.id == "ActionHook":
                return "ACTION"

    return None


def is_class_protocol(class_def: ast.ClassDef) -> bool:
    if not class_def.bases or len(class_def.bases) != 1:
        return False

    return (
        isinstance(class_def.bases[0], ast.Name)
        and isinstance(class_def.bases[0].id, str)
        and class_def.bases[0].id == "Protocol"
    )


@dataclass
class HookDocstring:
    description: str | None
    examples: dict[str, str] | None


def parse_hook_docstring(docstring: str) -> HookDocstring:
    description: str | None = None
    examples: dict[str, str] = {}

    for block in split_docstring(docstring):
        if (
            block[:5].strip().startswith("# ")
            and block.lstrip("# ").lower().startswith("example")
        ):
            example_name = block[:block.index("\n")].strip("# ")
            example_block = block[block.index("\n"):].strip()
            examples[example_name] = example_block
        elif not block[:5].strip().startswith("# "):
            description = block

    return HookDocstring(description=description, examples=examples or None)


def split_docstring(docstring: str) -> list[str]:
    blocks: list[str] = []
    block: str = ""
    in_code = False
    for line in docstring.strip().splitlines():
        if in_code:
            if line == "```":
                in_code = False
            block += line
        else:
            if line.startswith("```"):
                in_code = True
                block += line

            elif line.startswith("# "):
                if block:
                    blocks.append(block.strip())
                block = line

            else:
                block += line

        block += "\n"

    if block:
        blocks.append(block)

    return blocks


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
            raise ValueError(f"'{file_path}': '{item.module}' could not be imported.")

        all_imports[import_name] = parse_python_file(import_path)

    for name in all_names:
        if name not in all_imports:
            raise ValueError(f"'{file_path}': import for '{name}' could not be found.")

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
