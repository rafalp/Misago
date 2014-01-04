class WarningsTracker(object):
    def __init__(self, warning_level):
        self.warning_level = warning_level

    def is_warning_active(self, warning):
        if self.warning_level > 0 and not warning.canceled:
            self.warning_level -= 1
            return True
        else:
            return False

    def is_warning_expired(self, warning):
        return not self.is_warning_active(warning)
