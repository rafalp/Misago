// jshint ignore:start
import React from 'react';

export default function({ children }) {
  return (
    <ul className="dropdown-menu dropdown-search-results" role="menu">
      {children}
    </ul>
  );
}