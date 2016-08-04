/* jshint ignore:start */
import React from 'react';
import Event from './event';
import Post from './post';

export default function(props) {
  if (props.posts.isLoaded) {
    return <ul className="posts-list ui-ready">
      {props.posts.results.map((post) => {
        return <ListItem key={post.id} post={post} {...props} />;
      })}
    </ul>;
  } else {
    return <ul className="posts-list ui-preview">
      <li>POSTS LIST PREVIEW</li>
    </ul>;
  }
}

export function ListItem(props) {
  if (props.post.is_event) {
    return <Event {...props} />;
  } else {
    return <Post {...props} />;
  }
}