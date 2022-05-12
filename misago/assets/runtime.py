import os

from ..conf import settings


def read_runtime(runtime_path: str) -> str:
    full_runtime_path = os.path.join(settings.static_root, runtime_path)
    with open(full_runtime_path, encoding="utf-8") as fp:
        runtime = fp.read()
        return update_runtime_map_url(runtime, runtime_path)


def update_runtime_map_url(runtime: str, runtime_path: str) -> str:
    lines = runtime.splitlines()
    if is_line_with_source_mapping(lines[-1], runtime_path):
        lines[-1] = f"//# sourceMappingURL=/static/{runtime_path}.map"

    return "\n".join(lines)


SOURCE_MAPPING_URL = "sourceMappingURL"


def is_line_with_source_mapping(line: str, runtime_path: str) -> bool:
    line = line.strip()
    if line.startswith("//"):
        line = line[2:].strip()
    else:
        return False

    if line.startswith("#"):
        line = line[1:].strip()
    else:
        return False

    if line.startswith(SOURCE_MAPPING_URL):
        line = line[len(SOURCE_MAPPING_URL) :].strip()
    else:
        return False

    if line.startswith("="):
        line = line[1:].strip()
    else:
        return False

    if line.endswith(".map"):
        line = line[:-4]
    else:
        return False

    filename = runtime_path.split("/")[-1]

    return line == filename
