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
            self._finalize_site()

    def _finalize_site(self):
        iterations = 0
        while self._unsorted_list:
            iterations += 1
            if iterations > 512:
                message = ("%s site hierarchy is invalid or too complex "
                           "to resolve. pages left: %s" % self._unsorted_list)
                raise ValueError(message)

            for index, page in enumerate(self._unsorted_list):
                if page['after']:
                    page_added = self._insert_page(page, after=page['after'])
                elif page['before']:
                    page_added = self._insert_page(page, before=page['before'])
                else:
                    page_added = self._insert_page(page)

                if page_added:
                    del self._unsorted_list[index]
                    break

    def _insert_page(self, inserted_page, after=None, before=None):
        if after:
            new_sorted_list = []
            for index, page in enumerate(self._sorted_list):
                new_sorted_list.append(page)
                if page['link'] == after:
                    new_sorted_list.append(inserted_page)
                    self._sorted_list = new_sorted_list
                    return True
            else:
                return False
        elif before:
            new_sorted_list = []
            for index, page in enumerate(self._sorted_list):
                if page['link'] == before:
                    new_sorted_list.append(inserted_page)
                    new_sorted_list.append(page)
                    self._sorted_list = new_sorted_list
                    return True
                else:
                    new_sorted_list.append(page)
            else:
                return False
        else:
            self._sorted_list.append(inserted_page)
            return True

    def add_page(self, link, name, icon=None, after=None, before=None,
                 visible_if=None, badge=None):
        if self._finalized:
            message = ("%s site was initialized already and no longer "
                       "accepts new pages")
            raise RuntimeError(message % self.name)

        if after and before:
            raise ValueError("after and before arguments are exclusive")

        self._unsorted_list.append({
            'link': link,
            'name': name,
            'icon': icon,
            'after': after,
            'before': before,
            'badge': badge,
            'visible_if': visible_if,
            })

    def _active_link_name(self, request):
        namespace = request.resolver_match.namespace
        url_name = request.resolver_match.url_name

        if namespace:
            active_link = '%s:%s' % (namespace, url_name)
        else:
            active_link = url_name
        return active_link

    def get_pages(self, request, profile=None):
        self.assert_site_is_finalized()
        active_link = self._active_link_name(request)
        visible_pages = []

        if profile:
            test_args = (request, profile)
        else:
            test_args = (request,)

        for page_definition in self._sorted_list:
            page = page_definition.copy()

            is_visible = True
            if page['visible_if']:
                is_visible = page['visible_if'](*test_args)

            if is_visible:
                if page['badge']:
                    page['badge'] = page['badge'](*test_args)
                page['is_active'] = active_link.startswith(page['link'])
                visible_pages.append(page)
        return visible_pages

    def get_default_link(self):
        self.assert_site_is_finalized()
        return self._sorted_list[0]['link']


usercp = Site('usercp')
users_list = Site('users list')
user_profile = Site('user profile')
