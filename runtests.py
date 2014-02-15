def runtests():
    import os
    import shutil
    import sys

    test_runner_path = os.path.dirname(__file__)
    project_template_path = os.path.join(
        test_runner_path, 'misago/project_template/project_name')

    test_project_path = os.path.join(test_runner_path, "testproject")
    if not os.path.exists(test_project_path):
        shutil.copytree(project_template_path, test_project_path)

        settings_path = os.path.join(test_project_path, "settings.py")
        with open(settings_path, "r") as py_file:
            settings_file = py_file.read().replace("{{ project_name }}",
                                                   "testproject")
            settings_file = settings_file.replace("{{ secret_key }}",
                                                   "t3stpr0j3ct")

        with open(settings_path, "w") as py_file:
            py_file.write(settings_file)

    os.environ["DJANGO_SETTINGS_MODULE"] = "testproject.settings"

    from south.management.commands import test
    sys.exit(test.Command().execute(verbosity=1))
