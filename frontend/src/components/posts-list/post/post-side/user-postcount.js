/* jshint ignore:start */
import React from 'react';

export default function({ poster }) {
  const message = ngettext(
    "%(posts)s post",
    "%(posts)s posts",
    poster.posts
  );

  return (
    <span className="user-postcount">
      {interpolate(message, {
        'posts': poster.posts
      }, true)}
    </span>
  );
}