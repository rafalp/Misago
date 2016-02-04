import moment from 'moment';

export const DEHYDRATE_RESULT = 'DEHYDRATE_RESULT';
export const UPDATE_AVATAR = 'UPDATE_AVATAR';
export const UPDATE_USERNAME = 'UPDATE_USERNAME';

export function dehydrate(items) {
  return {
    type: DEHYDRATE_RESULT,
    items: items
  };
}

export function updateAvatar(user, avatarHash) {
  return {
    type: UPDATE_AVATAR,
    userId: user.id,
    avatarHash
  };
}

export function updateUsername(user, username, slug) {
  return {
    type: UPDATE_USERNAME,
    userId: user.id,
    username,
    slug
  };
}

export default function user(state=[], action=null) {
  switch (action.type) {
    case DEHYDRATE_RESULT:
      return action.items.map(function(item) {
        let status = item.status || null;
        if (status) {
          status = Object.assign({}, status, {
            last_click: status.last_click ? moment(status.last_click) : null,
            banned_until: status.banned_until ? moment(status.banned_until) : null
          });
        }

        return Object.assign({}, item, {
          status
        });
      });

    default:
      return state;
  }
}