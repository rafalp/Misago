/* jshint ignore:start */
import React from 'react';

export function FlagHidden(props) {
  if (isVisible(props) && props.post.is_hidden) {
    return (
      <div className="post-status-message post-status-hidden">
        <span className="material-icon">visibility_off</span>
        <p>{gettext("This post is hidden. Only users with permission may see its contents.")}</p>
      </div>
    );
  } else {
    return null
  }
}

export function FlagUnapproved(props) {
  if (isVisible(props) && props.post.is_unapproved) {
    return (
      <div className="post-status-message post-status-unapproved">
        <span className="material-icon">remove_circle_outline</span>
        <p>{gettext("This post is unapproved. Only users with permission to approve posts and its author may see its contents.")}</p>
      </div>
    );
  } else {
    return null
  }
}

export function isVisible(props) {
  return !props.post.is_hidden || props.post.acl_can_see_hidden;
}