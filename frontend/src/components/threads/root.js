import { connect } from 'react-redux';
import Route from 'misago/components/threads/route';
import misago from 'misago/index';

export function select(store) {
  return {
    'tick': store.tick.tick,
    'user': store.auth.user
  };
}

export function getLists() {
  let lists = [
    {
      path: '',
      name: gettext("All"),
      longName: gettext("All threads")
    }
  ];

  if (misago.get('isAuthenticated')) {
    lists.push({
      path: 'my/',
      name: gettext("My"),
      longName: gettext("My threads")
    });
    lists.push({
      path: 'new/',
      name: gettext("New"),
      longName: gettext("New threads")
    });
    lists.push({
      path: 'unread/',
      name: gettext("Unread"),
      longName: gettext("Unread threads")
    });
    lists.push({
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

  misago.get('CATEGORIES').forEach(function(category) {
    lists.forEach(function(list) {
      paths.push({
        path: category.absolute_url + list.path,
        component: connect(select)(Route),
        category: category,

        lists: lists,
        list: list
      });
    });
  });

  return paths;
}