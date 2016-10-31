// jshint ignore:start
import React from 'react';
import Action from './action';
import isUrl from 'misago/utils/is-url';

export default function(props) {
  return (
    <Action
      execAction={insertImage}
      title={gettext("Insert image")}
      {...props}
    >
      <span className="material-icon">
        insert_photo
      </span>
    </Action>
  );
}

export function insertImage(selection, replace) {
  let url = '';
  let label = '';

  if (selection.length) {
    if (isUrl(selection)) {
      url = selection;
    } else {
      label = selection;
    }
  }

  url = $.trim(prompt(gettext("Enter link to image") + ':', url));
  label = $.trim(prompt(gettext("Enter image label (optional)") + ':', label));

  if (url.length) {
    if (label.length > 0) {
      replace('![' + label + '](' + url + ')');
    } else {
      replace('!(' + url + ')');
    }
  }
}