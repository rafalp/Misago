# Creating a custom plugin

Welcome to the plugin tutorial! In this tutorial, you will implement a "Users Online" plugin that displays a block containing a list of users currently online for site administrators on Misago's categories page. Additionally, this plugin will add a new page displaying all users currently online.

This exercise will cover all the basics of plugin development:

- Setting up a development environment for creating a new plugin.
- Getting a practical experience with Django templates, views, URLs, and the ORM.
- Using template outlets to include new HTML on existing pages.
- Adding a new page to the site.


## Django basics are required

Because Misago plugins are Django apps, knowledge of Django basics is necessary for plugin development.

If you don't know what Django apps are, how to use its ORM, create templates, views, or URLs, please see the ["First steps"](https://docs.djangoproject.com/en/5.0/#first-steps) section of the Django documentation. It provides a gentle and quick introduction to these concepts, which will be essential later.


## Misago development environment

To begin plugin development, clone the [Misago GitHub](https://github.com/rafalp/Misago) repository and run the `./dev init` command in your terminal. This will build the necessary Docker containers, install Python dependencies, and initialize the database. Once the command completes, you can start the development server using the `docker compose up` command.

Once the development server starts, visit http://127.0.0.1:8000/ in your browser to see your Misago site. You can sign in to the admin account using the `admin` and `password` credentials.

The `./dev` utility provides more commands than `init`. Run it without any arguments to get the list of all available commands.


## Initializing a minimal plugin

Look at the contents of the `plugins` directory. Misago's main repository comes with a few plugins already pre-installed. These plugins exist mainly to test the plugin system's features, but `minimal-plugin`, `full-manifest-plugin`, and the `misago-pypi-plugin` specified in the `pip-install.txt` file can be used as quick references for plugin developers.

Stop your development environment if it's running (`ctrl + c` or `cmd + c` in the terminal). Now, let's create a new directory for in `plugins` and name it `misago-users-online-plugin`. Inside of it, create another directory and name `misago_users_online_plugin`. Within this last directory, create two empty Python files: `__init__.py` and `misago_plugin.py`. Final directories structure should look like this:

```
misago-users-online-plugin/
    misago_users_online_plugin/
        __init__.py
        misago_plugin.py
```

This is the file structure of a minimal valid plugin that Misago will discover and load:

- `misago-users-online-plugin`: a directory containing all the plugin's files.
- `misago_users_online_plugin`: a Python package (and a Django application) that Misago will import.
- `__init__.py`: a file that makes the `misago_users_online_plugin` directory a Python package.
- `misago_plugin.py`: a file that makes the `misago_users_online_plugin` directory a Misago plugin.

It's important that the final plugin name and its Python package name are so close to each other. After the plugin is released to PyPI, Misago will build its imported Python package name from its PyPI name specified in the `pip-install.txt` file, using the `name.lower().replace("-", "_")` function. For example, the [Misago PyPI Plugin](https://pypi.org/project/misago-pypi-plugin/) is installable from PyPI as `misago-pypi-plugin`, but its Python package is named `misago_pypi_plugin` because that's the name Misago will try to include based on the `pip-install.txt` file contents.

The `misago-users-online-plugin` directory can contain additional files and directories. For example, it can include a `pyproject.toml` file with plugin's Python package data and dependencies. It can also include `requirements.txt` and `requirements-dev.txt` PIP requirements files. Requirements specified in those files will be installed during the Docker image build time. It is also possible (and recommended) to begin plugin development by creating a repository for it on GitHub or another code hosting platform and then cloning it to the `plugins` directory.


## Plugin list in admin control panel

Misago's admin control panel has a "Plugins" page that displays a list of all installed plugins on your Misago site. To access the admin control panel, start the development server with the `docker compose up` command and visit http://127.0.0.1:8000/admincp/ in your browser. You will see a login page for the Misago admin control panel. Log in using the `admin` username and `password` password.

After logging in, find the "Plugins" link in the menu on the left and click on it. The list of plugins should include our new plugin as "Misago-Users-Online-Plugin". If it's not there, make sure you've restarted the development server and that the plugin structure is correct.


## Adding a plugin manifest

Misago will display a message next to our plugin that it's missing a manifest in its `misago_plugin.py` file. The plugin manifest is an instance of the `MisagoPlugin` data class populated with the plugin's data.

Let's update the `misago_plugin.py` file to include a basic manifest for our plugin:

```python
# misago_users_online_plugin/misago_plugin.py
from misago import MisagoPlugin


manifest = MisagoPlugin(
    name="Users Online",
    description="Displays users online list on the categories page.",
)
```

Save the updated file and refresh the admin's plugins page. Our plugin will now be displayed as "Users Online", along with a brief description of its functionality.

The `MisagoPlugin` class allows plugin authors to specify additional information about their plugins. Refer to the [plugin manifest reference](./plugin-manifest-reference.md) document for a comprehensive list of available fields.