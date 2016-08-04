/* jshint ignore:start */
import React from 'react';

const ICON = {
  pinned_globally: 'bookmark',
  pinned_locally: 'bookmark_border',
  unpoinned: 'panorama_fish_eye',

  moved: 'arrow_forward',
  merged: 'call_merge',

  approved: 'done',

  opened: 'lock_open',
  closed: 'lock_outline',

  unhid: 'visibility',
  hid: 'visibility_off'
}

export default function(props) {
  return (
    <div className="post-avatar">
      <span className="material-icon">
        {ICON[props.post.event_type]}
      </span>
    </div>
  );
}