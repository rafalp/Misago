// jshint ignore:start
import React from 'react';

export default function({ value, onChange, onFocus }) {
  return (
    <input
      aria-haspopup="true"
      aria-expanded="false"
      autoComplete="off"
      className="form-control"
      value={value}
      onChange={onChange}
      onFocus={onFocus}
      placeholder={gettext("Search")}
      role="combobox"
      type="text"
    />
  );
}