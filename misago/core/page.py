class Page(object):
    """
    Misago page utility

    Allows for adding custom views to "sectioned" pages like
    User Control Panel, Users List or Threads Lists
    """

    def __init__(self, name):
        self._finalized = False
        self.name = name
        self._unsorted_list = []
        self._sorted_list = []

    def assert_is_finalized(self):
        if not self._finalized:
            self._finalized = True
            self._finalize()

    def _finalize(self):
        iterations = 0
        while self._unsorted_list:
            iterations += 1
            if iterations > 512:
                message = (
                    "%s page hierarchy is invalid or too complex  to resolve. Sections left: %s"
                )
                raise ValueError(message % self._unsorted_list)

            for index, section in enumerate(self._unsorted_list):
                if section['after']:
                    section_added = self._insert_section(section, after=section['after'])
                elif section['before']:
                    section_added = self._insert_section(section, before=section['before'])
                else:
                    section_added = self._insert_section(section)

                if section_added:
                    del self._unsorted_list[index]
                    break

    def _insert_section(self, inserted_section, after=None, before=None):
        if after:
            new_sorted_list = []
            for section in self._sorted_list:
                new_sorted_list.append(section)
                if section['link'] == after:
                    new_sorted_list.append(inserted_section)
                    self._sorted_list = new_sorted_list
                    return True
            else:
                return False
        elif before:
            new_sorted_list = []
            for section in self._sorted_list:
                if section['link'] == before:
                    new_sorted_list.append(inserted_section)
                    new_sorted_list.append(section)
                    self._sorted_list = new_sorted_list
                    return True
                else:
                    new_sorted_list.append(section)
            else:
                return False
        else:
            self._sorted_list.append(inserted_section)
            return True

    def add_section(
            self, link, after=None, before=None, visible_if=None, get_metadata=None, **kwargs
    ):
        if self._finalized:
            message = "%s page was initialized already and no longer accepts new sections"
            raise RuntimeError(message % self.name)

        if after and before:
            raise ValueError("after and before arguments are exclusive")

        kwargs.update({
            'link': link,
            'after': after,
            'before': before,
            'visible_if': visible_if,
            'get_metadata': get_metadata,
        })

        self._unsorted_list.append(kwargs)

    def _active_link_name(self, request):
        namespace = request.resolver_match.namespace
        url_name = request.resolver_match.url_name

        if namespace:
            active_link = '%s:%s' % (namespace, url_name)
        else:
            active_link = url_name
        return active_link

    def get_sections(self, request, *args):
        self.assert_is_finalized()
        active_link = self._active_link_name(request)
        visible_sections = []

        for section_definition in self._sorted_list:
            section = section_definition.copy()

            is_visible = True
            if section['visible_if']:
                is_visible = section['visible_if'](request, *args)

            if is_visible:
                if section['get_metadata']:
                    section['metadata'] = section['get_metadata'](request, *args)
                section['is_active'] = active_link.startswith(section['link'])
                visible_sections.append(section)
        return visible_sections

    def get_default_link(self):
        self.assert_is_finalized()
        return self._sorted_list[0]['link']
