import moment from 'moment';

export const APPEND_USERS = 'APPEND_USERS';
export const HYDRATE_USERS = 'HYDRATE_USERS';
export const UPDATE_AVATAR = 'UPDATE_AVATAR';
export const UPDATE_USERNAME = 'UPDATE_USERNAME';

export function append(items) {
  return {
    type: APPEND_USERS,
    items
  };
}

export function hydrate(items) {
  return {
    type: HYDRATE_USERS,
    items
  };
}

export function hydrateStatus(status) {
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
    case APPEND_USERS:
      return state.concat(action.items.map(function(item) {
        return Object.assign({}, item, {
          joined_on: moment(item.joined_on),
          status: hydrateStatus(item.status)
        });
      }));

    case HYDRATE_USERS:
      return action.items.map(function(item) {
        return Object.assign({}, item, {
          joined_on: moment(item.joined_on),
          status: hydrateStatus(item.status)
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