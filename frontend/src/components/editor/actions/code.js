// jshint ignore:start
import React from 'react';
import Action from './action';
import isUrl from 'misago/utils/is-url';

export default function(props) {
  return (
    <Action
      execAction={insertCode}
      title={gettext("Insert code")}
      {...props}
    >
      code
    </Action>
  );
}

export function insertCode(selection, replace) {
  const syntax = $.trim(prompt(gettext("Enter name of syntax of your code (optional)") + ':'));
  replace("\n\n```" + syntax + '\n' + selection + "\n```\n\n");
}