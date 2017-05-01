/* jshint ignore:start */
import React from 'react';
import Avatar from 'misago/components/avatar';

export default function({ post, size }) {
  if (post.poster) {
    return (
      <a href={post.poster.absolute_url}>
        <Avatar size={size || 100} size2x={size || 150} user={post.poster} />
      </a>
    );
  }

  return (
    <Avatar size={size || 100} />
  );
}
