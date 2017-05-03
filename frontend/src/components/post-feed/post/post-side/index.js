/* jshint ignore:start */
import React from 'react';
import Anonymous from './anonymous';
import Registered from './registered';

export default function({ post, poster }) {
  if (poster.id) {
    return (
      <Registered
        post={post}
        poster={poster}
      />
    );
  }

  return (
    <Anonymous post={post} />
  );
}