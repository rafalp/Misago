from django.utils.importlib import import_module

def load_app_fixtures(app):
    """
    See if application has fixtures module defining load_fixtures function
    If it does, execute that function
    """
    app += '.fixtures'
    try:
        fixture = import_module(app)
        fixture.load_fixture()
        return True
    except (ImportError, AttributeError):
        return False