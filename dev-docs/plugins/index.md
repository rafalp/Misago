# Plugin guide

Misago implements a plugin system that enables customization and extension of the core functionality of the software.


## Installing plugins

The default Misago setup supports installing plugins from both PyPI and the filesystem.


### Installing a plugin from PyPI

To install a plugin from PyPI, first, create a `pip-install.txt` file in your Misago's `plugins` directory.

Inside this file, specify each plugin to install from PyPI on a separate line:

```
# pip-install.txt
misago-first-plugin
misago-other-plugin~=3.0
```

`pip-install.txt` a [PIP requirements file](https://pip.pypa.io/en/stable/reference/requirements-file-format/), but Misago only supports specifying package names and their versions (and comments). Other features like package URLs or installation options are not supported.

To install the specified plugins, [rebuild and restart the Docker container](./#rebuilding-misago-docker-image-to-install-plugins).


### Installing a plugin from the filesystem

To install a plugin from the filesystem, place its directory in your Misago's `plugins` directory.

A plugin must be a directory containing a Python package with a `misago_plugin.py` file:

```
example-plugin/
    example_plugin/
        __init__.py
        misago_plugin.py
```

A valid plugin has:

- `example-plugin`: a directory containing all the plugin's files.
- `example_plugin`: a Python package (and a Django application) that Misago will import.
- `__init__.py`: a file that makes the `example_plugin` directory a Python package.
- `misago_plugin.py`: a file that makes the `example_plugin` directory a Misago plugin.

The `example-plugin` directory may include a `pyproject.toml` or `requirements.txt` file to define the plugin's dependencies. It could also include a hidden `.git` directory if the plugin was cloned from a Git repository.

Plugins following the above file structure are automatically discovered and installed during [the Misago Docker image build](./#rebuilding-misago-docker-image-to-install-plugins).


## Rebuilding Misago Docker image to install plugins

Plugins are installed during the Misago Docker image build.

If you are using [`misago-docker`](https://github.com/rafalp/misago-docker) to run your site, use the `./appctl rebuild` command.

If you are using the [local development setup](https://github.com/rafalp/misago), run the `./dev rebuild` command instead.


## Creating a custom plugin

If you are interested in creating a custom plugin, please see the [plugin tutorial](./tutorial.md).

Once you have your basic plugin up and running, the [extending Misago](./extending-misago.md) document contains a list of all available extension points.


## Creating custom threads filters

Plugins can add custom filtering options to threads lists:

[Custom threads filters](./threads-filters.md)


## Adding new choices to the "index page" setting

Plugins can register custom views as new choices in the "index page" setting:

[Custom index pages](./forum-index.md)
