/* jshint ignore:start */
import React from 'react';

export default function(props) {
  if (props.posts.isLoaded) {
    return <ul className="posts-list ui-ready">
      <li>POSTS LIST</li>
    </ul>;
  } else {
    return <ul className="posts-list ui-preview">
      <li>POSTS LIST PREVIEW</li>
    </ul>;
  }
}
/* jshint ignore:end */