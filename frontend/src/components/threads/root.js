import { connect } from 'react-redux';
import Route from 'misago/components/threads/route';
import misago from 'misago/index';

export function getSelect(options) {
  return function(store) {
    return {
      'options': options,
      'selection': store.selection,
      'threads': store.threads,
      'tick': store.tick.tick,
      'user': store.auth.user
    };
  };
}

export function getLists(user) {
  let lists = [
    {
      type: 'all',
      path: '',
      name: gettext("All"),
      longName: gettext("All threads")
    }
  ];

  if (user.id) {
    lists.push({
      type: 'my',
      path: 'my/',
      name: gettext("My"),
      longName: gettext("My threads")
    });
    lists.push({
      type: 'new',
      path: 'new/',
      name: gettext("New"),
      longName: gettext("New threads")
    });
    lists.push({
      type: 'unread',
      path: 'unread/',
      name: gettext("Unread"),
      longName: gettext("Unread threads")
    });
    lists.push({
      type: 'subscribed',
      path: 'subscribed/',
      name: gettext("Subscribed"),
      longName: gettext("Subscribed threads")
    });

    if (user.acl.can_see_unapproved_content_lists) {
      lists.push({
        type: 'unapproved',
        path: 'unapproved/',
        name: gettext("Unapproved"),
        longName: gettext("Unapproved content")
      });
    }
  }

  return lists;
}

export function paths(user, mode) {
  let lists = getLists(user);
  let routes = [];
  let categoriesMap = {};

  misago.get('CATEGORIES').forEach(function(category) {
    lists.forEach(function(list) {
      categoriesMap[category.id] = category;

      routes.push({
        path: category.url.index + list.path,
        component: connect(getSelect(mode))(Route),

        categories: misago.get('CATEGORIES'),
        categoriesMap,
        category,

        lists,
        list
      });
    });
  });

  return routes;
}