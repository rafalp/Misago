/* jshint ignore:start */
import React from 'react';
import Icon from './icon';
import Info from './info';
import Message from './message';

export default function(props) {
  let className = 'event';
  if (props.post.isDeleted) {
    className = 'hide';
  } else if (props.post.is_hidden && !props.post.acl.can_see_hidden) {
    className = 'event post-hidden';
  }

  return (
    <li id={'post-' + props.post.id} className={className}>
      <div className="post-border">

        <Icon {...props} />
        <div className="post-body">
          <Message {...props} />
          <Info {...props} />
        </div>

      </div>
    </li>
  );
}