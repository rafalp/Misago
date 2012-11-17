from django.conf import settings
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import resolve
from django.utils.importlib import import_module

"""
Clean admin path if it was defined, or leave variable empty if ACP is turned off.
"""
ADMIN_PATH = ''
if settings.ADMIN_PATH:
    ADMIN_PATH = settings.ADMIN_PATH
    while ADMIN_PATH[:1] == '/':
        ADMIN_PATH = ADMIN_PATH[1:]
    while ADMIN_PATH[-1:] == '/':
        ADMIN_PATH = ADMIN_PATH[:-1]
    ADMIN_PATH += '/'
    

"""
Admin lists sorter for admin sections and actions
"""
class SortList(object):
    def __init__(self, unsorted):
        self.unsorted = unsorted
        
    def sort(self):
        # Sort and return sorted list
        order = []
        cache = {}
        for item in self.unsorted:
            if item.after:
                try:
                    cache[item.after].append(item.id)
                except KeyError:
                    cache[item.after] = []
                    cache[item.after].append(item.id)
            else:
                order.append(item.id)
        while cache:
            for item in cache.keys():
                try:
                    target_index = order.index(item)
                    for new_item in cache[item]:
                        target_index += 1
                        order.insert(target_index, new_item)
                    del cache[item]
                except ValueError:
                    pass
        sorted = []
        for item in order:
            for object in self.unsorted:
                if item == object.id:
                    sorted.append(object)
                    break
        return sorted
        
            
"""
Admin site section
"""
class AdminSiteItem(object):
    def __init__(self, id, name, icon, target=None, route=None, help=None, after=None):
        self.id = id
        self.name = name
        self.help = help
        self.after = after
        self.icon = icon
        self.target = target
        self.route = route
        self.sorted = False
    
    
"""
Admin site action
"""
class AdminAction(AdminSiteItem):
    def __init__(self, section=None, actions=[], model=None, messages={}, urlpatterns=None, **kwargs):
        self.actions = actions
        self.section = section
        self.model = model
        self.messages = messages
        self.urlpatterns = urlpatterns
        super(AdminAction, self).__init__(**kwargs)
    
    def get_action_attr(self, id, attr):
        for action in self.actions:
            if action['id'] == id:
                return action[attr]
        return None
    
    def is_active(self, full_path, section=None):
        if section:
            action_path = '/%s%s/%s/' % (ADMIN_PATH, section, self.id)
        else:
            action_path = '/%s%s/' % (ADMIN_PATH, self.id)
        # Paths overlap = active action
        return len(action_path) <= full_path and full_path[:len(action_path)] == action_path


"""
Admin site section
"""
class AdminSection(AdminSiteItem):
    def __init__(self, section=None, **kwargs):
        self.actions = []
        self.last = None
        super(AdminSection, self).__init__(**kwargs)
        
    def get_routes(self):
        routes = []
        first_action = True
        for action in self.actions:
            if first_action:
                routes += patterns('', url('^', include(action.urlpatterns)))
                first_action = False
            else:
                routes += patterns('', url(('^%s/' % action.id), include(action.urlpatterns)))
        return routes
            
    def is_active(self, full_path):
        action_path = '/%s%s/' % (ADMIN_PATH, self.id)
        # Paths overlap = active action
        return len(action_path) <= full_path and full_path[:len(action_path)] == action_path


"""
Admin site class that knows ACP structure
"""
class AdminSite(object):
    actions_index = {}
    routes = []
    sections = []
    sections_index = {}
    
    def discover(self):
        """
        Build admin site structure
        """
        # Return discovered admin routes, so we dont repeat ourself
        if self.routes:
            return self.routes
        
        # Found actions
        actions = []
        
        # Orphan actions that have no section yet
        late_actions = []
        
        # Iterate over installed applications
        for app_name in settings.INSTALLED_APPS:
            try:
                app = import_module(app_name + '.admin')
                
                # Attempt to import sections
                try:
                    for section in app.ADMIN_SECTIONS:
                        self.sections.append(section)
                        self.sections_index[section.id] = section
                except AttributeError:
                    pass
                
                # Attempt to import actions
                try:
                    for action in app.ADMIN_ACTIONS:
                        self.actions_index[action.id] = action
                        if action.section in self.sections_index:
                            if not action.after:
                                 action.after = self.sections_index[action.section].last
                            actions.append(action)
                            self.sections_index[action.section].last = action.after
                        else:
                            late_actions.append(action)
                except AttributeError:
                    pass
            except ImportError:
                pass
                
        # So actions and late actions
        actions += late_actions
        
        # Sorth sections and actions
        sort_sections = SortList(self.sections)
        sort_actions = SortList(actions)
        self.sections = sort_sections.sort()
        actions = sort_actions.sort()
        
        # Put actions in sections
        for action in actions:
            self.sections_index[action.section].actions.append(action)
        
        # Return ready admin routing
        first_section = True
        for section in self.sections:
            if first_section:
                self.routes += patterns('', url('^', include(section.get_routes())))
                first_section = False
            else:
                self.routes += patterns('', url(('^%s/' % section.id), include(section.get_routes())))
        return self.routes
    
    def get_action(self, action):
        """
        Get admin action
        """
        return self.actions_index.get(action)
            
    def get_admin_index(self):
        """
        Return admin index route - first action of first section
        """
        return self.sections[0].actions[0].route
            
    def get_admin_navigation(self, request):
        """
        Find and return current admin navigation
        """
        sections = []
        actions = []
        active_section = False
        active_action = False
        
        # Loop sections, build list of sections and find active section
        for section in self.sections:
            is_active = section.is_active(request.path)
            sections.append({
                             'is_active': is_active,
                             'name': section.name,
                             'icon': section.icon,
                             'route': section.actions[0].route
                             })
            if is_active:
                active_section = section
        
        # If no section was found to be active, default to first one
        if not active_section:
            active_section = self.sections[0]
            sections[0]['is_active'] = True
            
        # Loop active section actions
        for action in active_section.actions:
            is_active = action.is_active(request.path, active_section.id if active_section != self.sections[0] else None)
            actions.append({
                             'is_active': is_active,
                             'name': action.name,
                             'icon': action.icon,
                             'help': action.help,
                             'route': action.route
                             })
            if is_active:
                active_action = action
        
        # If no action was found to be active, default to first one
        if not active_action:
            active_action = active_section.actions[0]
            actions[0]['is_active'] = True
        
        # Return admin navigation for this location
        return {
                'sections': sections,
                'actions': actions,
                'admin_index': self.get_admin_index(),
                }


site = AdminSite();