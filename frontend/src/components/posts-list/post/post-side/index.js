/* jshint ignore:start */
import React from 'react';
import Anonymous from './anonymous';
import Registered from './registered';

export default function({ post }) {
  if (post.poster) {
    return (
      <Registered post={post} />
    );
  }

  return (
    <Anonymous post={post} />
  );
}