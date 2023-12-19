# Plugin manifest reference

A frozen dataclass with plugin's metadata.


## Optional arguments

### `name: str`

A string with the plugin name. Limited to 100 characters.


### `description: str`

A string with the plugin description. Limited to 250 characters.


### `license: str`

A string with the plugin license. Limited to 50 characters.


### `icon: str`

A string with the plugin icon. Must be a valid Font Awesome icon CSS name, e.g., `fa fa-icon` or `fas fa-other-icon`.


### `color: str`

A string with the plugin icon's color. Must be a color hex format prefixed with `#`, e.g., `#efefef`.


### `version: str`

A string with the plugin version. Limited to 50 characters.


### `author: str`

A string with the plugin author's name. Limited to 150 characters.


### `homepage: str`

A string with the URL to the plugin's homepage.


### `sponsor: str`

A string with the URL to a page with sponsorship instructions or a donation form.


### `help: str`

A string with the URL to the plugin's help page or a support forum.


### `bugs: str`

A string with the URL to the plugin's bug reporting tool.


### `repo: str`

A string with the URL to the plugin's code repository.


## Example

The code below shows a `misago_plugin.py` file with a plugin manifest with all fields filled in:

```python
from misago import MisagoPlugin


manifest = MisagoPlugin(
    name="Example plugin with complete manifest",
    description="This plugin has all fields in its manifest filled in.",
    license="GNU GPL v2",
    icon="fa fa-wrench",
    color="#9b59b6",
    version="0.1DEV",
    author="Rafał Pitoń",
    homepage="https://misago-project.org",
    sponsor="https://github.com/sponsors/rafalp",
    help="https://misago-project.org/c/support/30/",
    bugs="https://misago-project.org/c/bug-reports/29/",
    repo="https://github.com/rafalp/misago",
)
```