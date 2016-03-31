import { connect } from 'react-redux';
import Route from 'misago/components/threads/route';
import misago from 'misago/index';

export function select(store) {
  return {
    'tick': store.tick.tick,
    'user': store.auth.user,
    'threads': store.threads
  };
}

export function getLists() {
  let lists = [
    {
      type: 'all',
      path: '',
      name: gettext("All"),
      longName: gettext("All threads")
    }
  ];

  if (misago.get('isAuthenticated')) {
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
  }

  return lists;
}

export function paths() {
  let lists = getLists();
  let paths = [];
  let categoriesMap = {};

  misago.get('CATEGORIES').forEach(function(category) {
    lists.forEach(function(list) {
      categoriesMap[category.id] = category;

      paths.push({
        path: category.absolute_url + list.path,
        component: connect(select)(Route),

        categoriesMap,
        category,

        lists,
        list
      });
    });
  });

  return paths;
}