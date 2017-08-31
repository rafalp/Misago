// jshint ignore:start
import React from 'react';
import Input from './input';

export default function({ children, onChange, query }) {
  return (
    <ul className="dropdown-menu dropdown-search-results" role="menu">
      <li className="form-group">
        <Input
          value={query}
          onChange={onChange}
        />
      </li>
      {children}
    </ul>
  );
}