// jshint ignore:start
import React from 'react';
import DropdownMenu from './dropdown-menu';

export default function({ message }) {
  return (
    <DropdownMenu>
      <li className="dropdown-search-message">
        {message}
      </li>
    </DropdownMenu>
  );
}