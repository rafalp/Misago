from misago.conf.dbsettings import db_settings


def settings(request):
    return {'misago_settings': db_settings}
