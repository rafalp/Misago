// jshint ignore:start
import React from 'react';
import List from './list';
import Uploader from './uploader';
import misago from 'misago';

export default function(props) {
  if (!misago.get('user').acl.max_attachment_size) {
    return null;
  }

  return (
    <div className="editor-attachments">
      <List {...props} />
      <Uploader {...props} />
    </div>
  );
};
