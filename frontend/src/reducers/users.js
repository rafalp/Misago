export const UPDATE_AVATAR = 'UPDATE_AVATAR';

export function updateAvatar(user, avatarHash) {
  return {
    type: UPDATE_AVATAR,
    userId: user.id,
    avatarHash
  };
}