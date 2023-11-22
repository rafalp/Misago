# Plugin guide

Misago implements a plugin system that enables developers to customize and extend the core functionality of the software. This plugin system itself extends existing Django applications mechanism.

> **Plugins vs forking Misago**
>
> It may seem simpler (and faster) to fork and customize Misago directly instead of developing plugins. While this is possible, the time required to later keep the fork in sync with new versions of Misago for every site update may quickly add up, resulting in a net loss of time.
>
> It is recommended to attempt achieving as much as possible through plugins. In situations where this is not feasible, consider [reaching out to the developers](https://misago-project.org/c/development/31/) before resorting to forking. Misago's current extension points are not exhaustive, and new ones may be added in future releases based on user feedback.


## Plugin installation

To install a plugin, place its directory in the standard 'plugins' directory within your Misago setup.

Example plugin directory must contain a valid Python package, including a `misago_plugin.py` file. For example:

```
- minimal-plugin
  - minimal_plugin
    - __init__.py
    - misago_plugin.py
```

The graph above shows the file structure of a minimal valid plugin:

- `minimal-plugin`: a directory that contains all plugin files.
- `minimal_plugin`: a Python package (and a Django application) that Misago will import.
- `__init__.py`: a file that marks `minimal_plugin` directory as a Python package.
- `misago_plugin.py`: a file that marks `minimal_plugin` directory as a Misago plugin.

The  `minimal-plugin` and `minimal_plugin` directories can contain additional files and directories. The `minimal-plugin` directory may include a `pyproject.toml` or `requirements.txt` file to define the plugin's dependencies. It could also include a hidden `.git` directory if plugin was cloned from a Git repository.

Plugins following the above file structure are discovered and installed automatically at the Misago's Docker image build time.


## Writing custom plugin

- django applications mechanism
- plugin structure
- plugins vs. forking


## Hooks

- how to hooks
- hook reference