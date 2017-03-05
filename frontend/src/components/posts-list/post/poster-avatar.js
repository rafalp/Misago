/* jshint ignore:start */
import React from 'react';
import Avatar from 'misago/components/avatar';

export default function(props) {
  if (props.post.poster) {
    return (
      <a href={props.post.poster.absolute_url}>
        <Avatar size={props.size || 100} size2x={props.size || 150} user={props.post.poster} />
      </a>
    );
  } else {
    return <Avatar size={props.size || 100} />;
  }
}
