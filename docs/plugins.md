Plugins
=======

Misago implements plugin system that allows forum owners and developers to modify and extend their site without need for modifying Misago codebase.


Plugin file structure
---------------------

Plugins files should be organized into following (*optional):

```
plugin_directory
+- package_name
   +- migrations*
      +- __init__.py
   +- templates*
   +- __init__.py
   +- plugin.py
   +- cli.py*
   +- tables.py*
+- requirements.txt*
+- admin*
   +- src
      +- locale*
      +- styles*
         +- variables.scss*
         +- components.scss*
      +- plugin.tsx
+- client*
   +- src
      +- locale*
      +- styles*
         +- variables.scss*
         +- components.scss*
      +- plugin.tsx
```


Plugin manifests
----------------

Plugins can declare manifests which are additional information about the plugin.

To declare manifest, insert following code in your plugin's `__init__.py` module:

```python
__manifest__ = PluginManifest(
    name="Example plugin",
    description="Me example plugin",
    license="BSD-3",
    icon="fas fa-dice",
    color="0466c8",
    version="0.1.0",
    author="John Doe",
    homepage="https://misago-project.org",
    repo="https://github.com/rafalp/misago",
)
```

Every item of manifest is optional.

You can select any icon from [Font Awesome 5.15 free icon set](https://fontawesome.com/v5.15/icons?d=gallery).
