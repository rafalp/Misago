/* jshint ignore:start */
import React from 'react';
import misago from 'misago';

export default function(props) {
  return (
    <img
      className={props.className || 'user-avatar'}
      src={getSrc(props)}
      title={gettext("User avatar")}
    />
  );
}

export function getSrc(props) {
  const size = props.size || 100; // jshint ignore:line
  let url = misago.get('MISAGO_PATH') + 'user-avatar/';

  if (props.user && props.user.id) {
    // just avatar hash, size and user id
    return resolveAvatarForSize(props.user.avatars, size).url;
  } else {
    // just append avatar size to file to produce no-avatar placeholder
    return misago.get('MISAGO_PATH') + 'user-avatar/' + size + '.png';
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