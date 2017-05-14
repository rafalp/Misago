// jshint ignore:start
import React from 'react';

export default function({ category }) {
  return (
    <div
      className={getClassName(category)}
      title={getTitle(category)}
    >
      <span className="material-icon">
        {getIcon(category)}
      </span>
    </div>
  );
}

export function getClassName(category) {
  if (category.is_read) {
    return 'read-status item-read';
  }

  return 'read-status item-new';
}

export function getTitle(category) {
  if (category.is_closed) {
    if (category.is_read) {
      return gettext("This category has no new posts. (closed)");
    }

    return gettext("This category has new posts. (closed)");
  }

  if (category.is_read) {
    return gettext("This category has no new posts.");
  }

  return gettext("This category has new posts.");
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