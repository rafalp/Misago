/* jshint ignore:start */
import React from 'react';
import Dropdown from './dropdown';

export default function(props) {
  if (!props.user.id || !isVisible(props.thread, props.posts.results)) {
    return null;
  }

  const selection = props.posts.results.filter((post) => {
    return post.isSelected;
  });

  return (
    <div className="dropup">
      <button
        aria-expanded="true"
        aria-haspopup="true"
        className="btn btn-default dropdown-toggle btn-block btn-outline"
        data-toggle="dropdown"
        disabled={!selection.length}
        type="button"
      >
        {gettext("Posts options")}
      </button>
      <Dropdown selection={selection} {...props} />
    </div>
  );
}

export function isVisible(thread, posts) {
  if (thread.acl.can_merge_posts && posts.length > 1) {
    // fast test: show moderation menu if we can merge posts
    return true;
  }

  // slow test: show moderation if any of posts has moderation options
  let visible = false;
  posts.forEach((post) => {
    if (!post.is_event) {
      const showModeration = (
        post.acl.can_approve ||
        post.acl.can_delete ||
        (!post.is_hidden && post.acl.can_hide) ||
        post.acl.can_move ||
        post.acl.can_protect ||
        (post.is_hidden && post.acl.can_unhide) ||
        post.acl.can_unprotect
      );

      if (showModeration) {
        visible = true;
      }
    }
  });
  return visible;
}