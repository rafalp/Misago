/* jshint ignore:start */
import React from 'react';
import Icon from './icon';
import Info from './info';
import Message from './message';
import Waypoint from '../waypoint';

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
        <Waypoint className="post-body" post={props.post}>
          <Message {...props} />
          <Info {...props} />
        </Waypoint>

      </div>
    </li>
  );
}