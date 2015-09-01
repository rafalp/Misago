import Ember from 'ember';

export function updateObjProps(obj, props) {
  if (props) {
    return Ember.$.extend({}, obj, props);
  } else {
    return Ember.$.extend({}, obj);
  }
}

export function paginatedJSON(results, count, page, per_page, orphans) {
  count = count || 0;
  var pages = 0;

  if (count && per_page) {
    pages = Math.ceil(count / per_page);
  }

  if (orphans && pages > 1 && count - (pages - 1) * per_page <= orphans) {
    pages -= 1;
  }

  var next = null;
  var last = null;
  if (page < pages) {
    last = pages;
    if (page + 1 < pages) {
      next = page + 1;
    }
  }

  var previous = null;
  var first = null;
  if (page > 1) {
    first = 1;
    if (page > 2) {
      previous = page - 1;
    }
  }

  var before = 0;
  if (page > 1) {
    before = (page - 1) * per_page;
  }

  var more = 0;
  if (last) {
    more = count - before - per_page;
  }

  return {
    'results': results || [],

    'count': count,
    'pages': pages,
    'next': next,
    'last': last,
    'previous': previous,
    'first': first,
    'before': before,
    'more': more
  };
}

export function rankJSON(id, props) {
    var mock = {
      'id': id,
      'name': 'Members',
      'slug': 'members',
      'description': '',
      'title': '',
      'css_class': '',
      'is_tab': false
    };

    return updateObjProps(mock, props);
}

export function userJSON(id, props) {
  var mock = {
    'id': id,
    'username': 'MockedUser' + id,
    'slug': 'mockeduser' + id,
    'avatar_hash': 'h4sh',
    'title': null,
    'rank': rankJSON(1),
    'state': {
      'is_offline_hidden': false,
      'is_online_hidden': false,
      'is_offline': true,
      'is_online': false,
      'is_banned': false,
      'last_click': '2015-07-05T16:06:44.010Z',
      'is_hidden': false,
      'banned_until': null
    },
    'signature': null
  };

  return updateObjProps(mock, props);
}
