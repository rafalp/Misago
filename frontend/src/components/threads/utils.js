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

export function isThreadChanged(current, fromDb) {
  return [
    current.title === fromDb.title,
    current.weight === fromDb.weight,
    current.category === fromDb.category,
    current.top_category === fromDb.top_category,
    current.last_post === fromDb.last_post,
    current.last_poster_name === fromDb.last_poster_name
  ].indexOf(false) >= 0;
}

export function diffThreads(current, fromDb) {
  let currentMap = {};
  current.forEach(function(thread) {
    currentMap[thread.id] = thread;
  });

  return fromDb.filter(function(thread) {
    if (currentMap[thread.id]) {
      return isThreadChanged(currentMap[thread.id], thread);
    } else {
      return true;
    }
  });
}

export function getModerationActions(threads) {
  let moderation = {
    allow: false,

    can_pin: 0,
    can_close: 0,
    can_hide: 0,
    can_move: 0
  };

  threads.forEach(function(thread) {
    if (thread.acl.can_pin > moderation.can_pin) {
      moderation.can_pin = thread.acl.can_pin;
    }

    if (thread.acl.can_close > moderation.can_close) {
      moderation.can_close = thread.acl.can_close;
    }

    if (thread.acl.can_hide > moderation.can_hide) {
      moderation.can_hide = thread.acl.can_hide;
    }

    if (thread.acl.can_move > moderation.can_move) {
      moderation.can_move = thread.acl.can_move;
    }

    moderation.allow = (
      moderation.can_pin ||
      moderation.can_close ||
      moderation.can_hide ||
      moderation.can_move
    );
  });

  return moderation;
}