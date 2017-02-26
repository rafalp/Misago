class AdminBaseMixin(object):
    """
    Admin mixin abstraciton used for configuring admin CRUD views.

    Takes following attributes:

    model - Model instance
    root_link - name of link leading to root action (eg. list of all items
    templates_dir - directory with templates
    message_404 - string used in "requested item not found" messages
    """
    model = None
    root_link = None
    templates_dir = None
    message_404 = None

    def get_model(self):
        """basic method for retrieving Model, used in cases such as User model."""
        return self.model
