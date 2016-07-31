/* jshint ignore:start */
import React from 'react';
import Event from './event';
import Post from './post';

export default function(props) {
  if (props.post.is_event) {
    return <Event {...props} />;
  } else {
    return <Post {...props} />;
  }
}