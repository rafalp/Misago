// jshint ignore:start
import React from 'react';
import AttachmentComplete from './complete';
import AttachmentError from './error';
import AttachmentUpload from './upload';
import misago from 'misago';
import escapeHtml from 'misago/utils/escape-html';

export default function(props) {
  if (props.item.id) {
    return (
      <AttachmentComplete {...props} />
    );
  }

  if (props.item.error) {
    return (
      <AttachmentError {...props} />
    );
  }

  return (
    <AttachmentUpload {...props} />
  );
}