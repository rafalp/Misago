class Site(object):
    """
    Misago user sites controller

    Allows for adding custom views to User CP, Users Lists and User Profile
    """
    def __init__(self, name):
        self._finalized = False
        self.name = name
        self._unsorted_list = []
        self._sorted_list = []

    def assert_site_is_finalized(self):
        if not self._finalized:
            self._finalized = True
            self.finalize_site()

    def finalize_site(self):
        iterations = 0
        while self._unsorted_list:
            iterations += 1
            if iterations > 512:
                message = ("%s site hierarchy is invalid or too complex "
                           "to resolve. pages left: %s" % self._unsorted_list)
                raise ValueError(message)

            for index, page in enumerate(self._unsorted_list):
                pass

    def add_page(self, link, name, icon=None, after=None, before=None):
        if self._finalized:
            message = ("%s site was initialized already and no longer "
                       "accepts new pages")
            raise RuntimeError(message % self.name)

        self._sorted_list.append({
            'link': link,
            'name': name,
            'icon': icon,
            'after': after,
            'before': before,
            })


usercp_actions = Site('usercp_actions')
users_list_tabs = Site('users_list')
user_profile_tabs = Site('user_profile')
