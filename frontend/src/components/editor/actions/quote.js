// jshint ignore:start
import React from 'react';
import Action from './action';
import isUrl from 'misago/utils/is-url';

export default function(props) {
  return (
    <Action
      execAction={insertQuote}
      title={gettext("Insert quote")}
      {...props}
    >
      <span className="material-icon">
        format_quote
      </span>
    </Action>
  );
}

export function insertQuote(selection, replace) {
  let author = $.trim(prompt(gettext("Enter image label (optional)") + ':', author));
  if (author.length && author[0] !== '@') {
    author = '@' + author;
  }

  if (author) {
    replace('\n\n[quote="' + author + '"]\n' + selection + '\n[/quote]\n\n');
  } else {
    replace('\n\n[quote=]\n' + selection + '\n[/quote]\n\n');
  }
}