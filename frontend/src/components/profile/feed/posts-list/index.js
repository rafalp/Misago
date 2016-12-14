// jshint ignore:start
import React from 'react';
import Post from './post';
import PostPreview from './post-preview';

export default function(props) {
  if (!props.isReady) {
    return (
      <ul className="posts-list ui-preview">
        <PostPreview />
      </ul>
    );
  }

  return (
    <ul className="posts-list ui-ready">
      {props.posts.map((post) => {
        return (
          <Post key={post.id} post={post} />
        );
      })}
    </ul>
  );
}