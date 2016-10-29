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
    url += props.user.avatar_hash + '/' + size + '/' + props.user.id + '.png';
  } else {
    // just append avatar size to file to produce no-avatar placeholder
    url += size + '.png';
  }

  return url;
}