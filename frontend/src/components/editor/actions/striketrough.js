// jshint ignore:start
import React from 'react';
import Action from './action';

export default function(props) {
  return (
    <Action
      execAction={makeStriketrough}
      title={gettext("Striketrough selection")}
      {...props}
    >
      <span className="material-icon">
        format_strikethrough
      </span>
    </Action>
  );
}

export function makeStriketrough(selection, replace) {
  if (selection.length) {
    replace('~~' + selection + '~~');
  }
}