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