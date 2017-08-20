// jshint ignore:start
import React from 'react';
import DropdownMenu from './dropdown-menu';
import Loader from 'misago/components/loader';

export default function({ message }) {
  return (
    <DropdownMenu>
      <li className="dropdown-search-loader">
        <Loader />
      </li>
    </DropdownMenu>
  );
}