/* jshint ignore:start */
import React from 'react';
import Icon from './icon';
import Info from './info';
import Message from './message';
import UnreadLabel from './unread-label';
import Waypoint from '../waypoint';

export default function(props) {
  let className = 'event';
  if (props.post.isDeleted) {
    className = 'hide';
  } else if (props.post.is_hidden) {
    className = 'event post-hidden';
  }

  return (
    <li id={'post-' + props.post.id} className={className}>
      <UnreadLabel post={props.post} />
      <div className="media">
        <div className="media-left">
          <Icon {...props} />
        </div>
        <Waypoint className="media-body" post={props.post}>
          <Message {...props} />
          <Info {...props} />
        </Waypoint>
      </div>
    </li>
  );
}