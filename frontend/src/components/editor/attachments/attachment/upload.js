// jshint ignore:start
import React from 'react';
import escapeHtml from 'misago/utils/escape-html';

const STRONG = '<strong>%(name)s</strong>';

export default function(props) {
  const filename = interpolate(STRONG, {
    name: escapeHtml(props.item.filename)
  }, true);

  const message = interpolate(gettext("Uploading %(filename)s... %(progress)s"), {
    filename,
    progress: props.item.progress + '%'
  }, true);

  return (
    <li className="editor-attachment-upload">
      <div className="editor-attachment-progress-bar">
        <div
          className="editor-attachment-progress"
          style={{width: props.item.progress + '%'}}
        />
      </div>
      <p
        className="editor-attachment-upload-message"
        dangerouslySetInnerHTML={{__html: message}}
      />
    </li>
  );
};