// jshint ignore:start
import React from 'react';

export default function({ provider }) {
  return (
    <li className="dropdown-search-header">
      {provider.name}
    </li>
  );
}