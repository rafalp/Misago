/* jshint ignore:start */
import React from 'react';

export default function(props) {
  return (
    <button
      className={props.className || 'btn btn-success'}
      onClick={props.onClick}
      type="button"
    >
      {gettext("Reply")}
    </button>
  );
}
