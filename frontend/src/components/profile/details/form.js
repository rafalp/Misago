/* jshint ignore:start */
import React from 'react';
import Form from 'misago/components/edit-profile-details';

export default function({ api, display, onCancel, onSuccess }) {
  if (!display) return null;

  return (
    <Form
      api={api}
      onSuccess={onSuccess}
      onCancel={onCancel}
    />
  );
}