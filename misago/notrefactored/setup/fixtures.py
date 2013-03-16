from django.utils.importlib import import_module

def load_app_fixtures(app):
    """
    See if application has fixtures module defining load_fixtures function
    If it does, execute that function
    """
    app += '.fixtures'
    try:
        fixture = import_module(app)
        fixture.load_fixtures()
        return True
    except (ImportError, AttributeError):
        return False
    except Exception as e:
        print 'Could not load fixtures from %s:\n%s' % (app, e)
        return False


def update_app_fixtures(app):
    """
    See if application has fixtures module defining update_fixtures function
    If it does, execute that function
    """
    app += '.fixtures'
    try:
        fixture = import_module(app)
        fixture.update_fixtures()
        return True
    except (ImportError, AttributeError):
        return False
    except Exception as e:
        print 'Could not update fixtures from %s:\n%s' % (app, e)
        return False
