/* jshint ignore:start */
import React from 'react';
import misago from 'misago';

export default function(props) {
  const size = props.size || 100;

  return (
    <img
      className={props.className || 'user-avatar'}
      src={getSrc(props.user, size)}
      title={gettext("User avatar")}
      width={size}
      height={size}
    />
  );
}

export function getSrc(user, size) {
  if (user && user.id) {
    // just avatar hash, size and user id
    return resolveAvatarForSize(user.avatars, size).url;
  } else {
    // just append avatar size to file to produce no-avatar placeholder
    return misago.get('BLANK_AVATAR_URL');
  }
}

export function resolveAvatarForSize(avatars, size) {
  let avatar = avatars[0];
  avatars.forEach((av) => {
    if (av.size >= size) {
      avatar = av;
    }
  });
  return avatar;
}