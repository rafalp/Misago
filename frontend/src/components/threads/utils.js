import misago from 'misago/index';

export function getPageTitle(route) {
  if (!route.category.special_role) {
    if (route.list.path) {
      return {
        title: route.list.longName,
        parent: route.category.name
      };
    } else {
      return {
        title: route.category.name
      };
    }
  } else if (!misago.get('CATEGORIES_ON_INDEX')) {
    if (route.list.path) {
      return {
        title: route.list.longName
      };
    } else {
      return null;
    }
  } else {
    if (route.list.path) {
      return {
        title: route.list.longName,
        parent: gettext("Threads")
      };
    } else {
      return {
        title: gettext("Threads")
      };
    }
  }
}

export function getTitle(route) {
  if (!route.category.special_role) {
    return route.category.name;
  } else if (!misago.get('CATEGORIES_ON_INDEX')) {
    if (misago.get('SETTINGS').forum_index_title) {
      return misago.get('SETTINGS').forum_index_title;
    } else {
      return misago.get('SETTINGS').forum_name;
    }
  } else {
    return gettext("Threads");
  }
}