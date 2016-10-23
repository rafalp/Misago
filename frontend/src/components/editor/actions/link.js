// jshint ignore:start
import React from 'react';
import Action from './action';
import isUrl from 'misago/utils/is-url';

export default function(props) {
  return (
    <Action
      execAction={insertLink}
      title={gettext("Insert link")}
      {...props}
    >
      link
    </Action>
  );
}

export function insertLink(selection, replace) {
  let url = '';
  let label = '';

  if (selection.length) {
    if (isUrl(selection)) {
      url = selection;
    } else {
      label = selection;
    }
  }

  url = $.trim(prompt(gettext("Enter link address") + ':', url));
  label = $.trim(prompt(gettext("Enter link label (optional)") + ':', label));

  if (url.length) {
    if (label.length > 0) {
      replace('[' + label + '](' + url + ')');
    } else {
      replace(url);
    }
  }
}