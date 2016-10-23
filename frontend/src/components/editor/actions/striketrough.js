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
      striketrough
    </Action>
  );
}

export function makeStriketrough(selection, replace) {
  if (selection.length) {
    replace('~~' + selection + '~~');
  }
}