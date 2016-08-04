/* jshint ignore:start */
import React from 'react';

export default function(props) {
  if (isVisible(props.post)) {
    return (
      <div className="panel-footer post-footer">
        <Likes {...props} />
        <Like {...props} />
        <Reply {...props} />
        <Edit {...props} />
      </div>
    );
  } else {
    return null;
  }
}

export function isVisible(post) {
  return (!post.is_hidden || post.acl.can_see_hidden) && (
    post.acl.can_reply ||
    post.acl.can_edit ||
    post.acl.can_see_likes ||
    post.acl.can_like
  );
}

export function Likes(props) {
  if (props.post.acl.can_see_likes) {
    return (
      <button type="button" className="btn btn-likes pull-left" disabled="disabled">
        Likes
      </button>
    );
  } else {
    return null;
  }
}

export function Like(props) {
  if (props.post.acl.can_like) {
    return (
      <button type="button" className="btn btn-like pull-left" disabled="disabled">
        {gettext("Like")}
      </button>
    );
  } else {
    return null;
  }
}

export function Reply(props) {
  if (props.post.acl.can_reply) {
    return (
      <button type="button" className="btn btn-reply pull-right" disabled="disabled">
        {gettext("Reply")}
      </button>
    );
  } else {
    return null;
  }
}

export function Edit(props) {
  if (props.post.acl.can_edit) {
    return (
      <button type="button" className="btn btn-edit pull-right" disabled="disabled">
        {gettext("Edit")}
      </button>
    );
  } else {
    return null;
  }
}