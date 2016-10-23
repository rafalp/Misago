// jshint ignore:start
import React from 'react';
import Action from './action';

export default function(props) {
  return (
    <Action
      execAction={makeEmphasis}
      title={gettext("Emphase selection")}
      {...props}
    >
      emphasis
    </Action>
  );
}

export function makeEmphasis(selection, replace) {
  if (selection.length) {
    replace('*' + selection + '*');
  }
}