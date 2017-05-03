/* jshint ignore:start */
import React from 'react';
import Body from './body';
import Header from './header';
import PostSide from './post-side';

export default function({ post, poster }) {
  return (
    <li id={'post-' + post.id} className="post">
      <div className="panel panel-default panel-post">
        <div className="panel-body">
          <PostSide
            post={post}
            poster={poster || post.poster}
          />
          <Header post={post} />
          <Body post={post} />
        </div>
      </div>
    </li>
  );
}