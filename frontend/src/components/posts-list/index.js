/* jshint ignore:start */
import React from 'react';
import Post from './post';

export default function(props) {
  if (props.posts.isLoaded) {
    return <ul className="posts-list ui-ready">
      {props.posts.results.map((post) => {
        return <Post key={post.id} post={post} {...props} />;
      })}
    </ul>;
  } else {
    return <ul className="posts-list ui-preview">
      <li>POSTS LIST PREVIEW</li>
    </ul>;
  }
}