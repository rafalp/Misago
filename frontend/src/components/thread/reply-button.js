/* jshint ignore:start */
import React from 'react';

export default function(props) {
  return (
    <button
      className={props.className || 'btn btn-primary btn-outline'}
      onClick={props.onClick}
      type="button"
    >
      <span className="material-icon">
        chat
      </span>
      {gettext("Reply")}
    </button>
  );
}
