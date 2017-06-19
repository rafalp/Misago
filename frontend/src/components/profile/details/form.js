/* jshint ignore:start */
import React from 'react';
import Form from 'misago/components/edit-profile-details';

export default function({ api, onCancel, dispatch, display }) {
  if (!display) return null;

  return (
    <Form
      api={api}
      dispatch={dispatch}
      onCancel={onCancel}
    />
  );
}