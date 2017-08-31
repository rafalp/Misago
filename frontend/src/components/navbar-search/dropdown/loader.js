// jshint ignore:start
import React from 'react';
import Loader from 'misago/components/loader';

export default function({ message }) {
  return (
    <li className="dropdown-search-loader">
      <Loader />
    </li>
  );
}