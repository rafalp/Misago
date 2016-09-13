/* jshint ignore:start */
import React from 'react';
import Dropdown from './dropdown';

export default function(props) {
  if (isVisible(props.post.acl)) {
    return (
      <div className="pull-right dropdown">
        <button
          aria-expanded="true"
          aria-haspopup="true"
          className="btn btn-default btn-icon dropdown-toggle"
          data-toggle="dropdown"
          type="button"
        >
          <span className="material-icon">
            expand_more
          </span>
        </button>
        <Dropdown {...props} />
      </div>
    );
  } else {
    return null;
  }
}

export function isVisible(acl) {
  return (
    acl.can_approve ||
    acl.can_hide ||
    acl.can_protect ||
    acl.can_unhide ||
    acl.can_delete ||
    acl.can_move
  );
}