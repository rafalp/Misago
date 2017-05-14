// jshint ignore:start
import React from 'react';

export default function({ category }) {
  let className = 'btn btn-default btn-block btn-sm btn-subcategory';
  if (!category.is_read) {
    className += ' btn-subcategory-new';
  }

  return (
    <div className="col-xs-12 col-sm-4 col-md-3">
      <a
        className={className}
        href={category.absolute_url}
      >
        <span className="material-icon">
          {getIcon(category)}
        </span>
        <span className="icon-text">
          {category.name}
        </span>
      </a>
    </div>
  );
}

export function getIcon(category) {
  if (category.is_closed) {
    if (category.is_read) {
      return 'lock_outline';
    }

    return 'lock';
  }

  if (category.is_read) {
    return 'chat_bubble_outline';
  }

  return 'chat_bubble';
}