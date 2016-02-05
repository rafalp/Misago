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

export function dehydrateStatus(status) {
  if (status) {
    return Object.assign({}, status, {
      last_click: status.last_click ? moment(status.last_click) : null,
      banned_until: status.banned_until ? moment(status.banned_until) : null
    });
  } else {
    return null;
  }
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
        let status = dehydrateStatus(item.status);

        return Object.assign({}, item, {
          status
        });
      });

    case UPDATE_AVATAR:
      return state.map(function(item) {
        item = Object.assign({}, item);
        if (item.id === action.userId) {
          item.avatar_hash = action.avatarHash;
        }

        return item;
      });

    default:
      return state;
  }
}