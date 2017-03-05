/* jshint ignore:start */
import React from 'react';

export function FlagHidden(props) {
  if (!(isVisible(props.post) && props.post.is_hidden)) {
    return null;
  }

  return (
    <div className="post-status-message post-status-hidden">
      <span className="material-icon">visibility_off</span>
      <p>{gettext("This post is hidden. Only users with permission may see its contents.")}</p>
    </div>
  );
}

export function FlagUnapproved(props) {
  if (!(isVisible(props.post) && props.post.is_unapproved)) {
    return null;
  }

  return (
    <div className="post-status-message post-status-unapproved">
      <span className="material-icon">remove_circle_outline</span>
      <p>{gettext("This post is unapproved. Only users with permission to approve posts and its author may see its contents.")}</p>
    </div>
  );
}

export function FlagProtected(props) {
  if (!(isVisible(props.post) && props.post.is_protected)) {
    return null;
  }

  return (
    <div className="post-status-message post-status-protected visible-xs-block">
      <span className="material-icon">lock_outline</span>
      <p>{gettext("This post is protected. Only moderators may change it.")}</p>
    </div>
  );
}

export function isVisible(post) {
  return !post.is_hidden || post.acl.can_see_hidden;
}