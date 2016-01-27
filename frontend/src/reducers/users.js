export const UPDATE_AVATAR = 'UPDATE_AVATAR';
export const UPDATE_USERNAME = 'UPDATE_USERNAME';

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