// jshint ignore:start
import React from 'react';
import Main from './main';
import LastThread from './last-thread';
import Stats from './Stats';
import Subcategories from './subcategories';

export default function({ category, isFirst }) {
  let className = 'list-group-item';
  if (isFirst) {
    className += ' list-group-item-first';
  }
  if (category.css_class) {
    className += ' list-group-item-' + category.css_class;
  }

  return (
    <li className={className}>
      <div className="row">
        <Main category={category} />
        <Stats category={category} />
        <LastThread category={category} />
      </div>
      <Subcategories
        category={category}
        isFirst={isFirst}
      />
    </li>
  );
}