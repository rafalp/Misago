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
        return Object.assign({}, item, {

        });
      });

    default:
      return state;
  }
}