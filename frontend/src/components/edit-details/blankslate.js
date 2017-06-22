/* jshint ignore:start */
import React from 'react';
import PanelMessage from 'misago/components/panel-message';

export default function({ display }) {
  if (!display) return null;

  return (
    <PanelMessage
      helpText={gettext("No profile details are editable at this time.")}
      message={gettext("This option is currently unavailable.")}
    />
  );
}